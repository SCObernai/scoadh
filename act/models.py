from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q, F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.template.defaultfilters import slugify
import datetime
from django.contrib.auth.models import User

from lic.models import *

class Activite(models.Model):
    saison = models.ForeignKey(Saison, on_delete=models.PROTECT)
    nom = models.CharField(max_length=200, null=False, blank=False)
    type_lic_req = models.ManyToManyField(to=TypeLicence, related_name="activites")
    # TODO organisateur
    club_organisateur = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="activites",
    )
    membership_required = models.BooleanField(default=False)
    slug = models.SlugField(verbose_name="ID Panier")
    date_debut = models.DateField(
        default=datetime.date.today,
        blank=True,
        null=True,
        verbose_name="Début de l'activité ",
    )
    date_fin = models.DateField(
        default=datetime.date.today,
        blank=True,
        null=True,
        verbose_name="Date de fin de l'activité ",
    )

    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        constraints = [
            UniqueConstraint(fields=["saison", "nom"], name="unique_activite"),
            CheckConstraint(
                check=Q(
                    Q(date_debut__isnull=True)
                    | Q(date_fin__isnull=True)
                    | Q(date_fin__gte=F("date_debut"))
                ),
                name="check_dates_activites_deb_fin",
            ),
        ]

    # Text repr
    def __str__(self):
        return f"{self.saison} - {self.nom}"

    @property
    def licences_possibles(self) -> str:
        tl: TypeLicence
        ret: list[str] = list()
        for tl in self.type_lic_req.all():
            ret.append(tl.full_name)
        ret.sort()
        return ", ".join(ret)


class VarianteActivite(models.Model):
    activite = models.ForeignKey(Activite, on_delete=models.PROTECT, related_name="variantes")
    description = models.CharField(max_length=200, blank=True)
    pass_allowed = models.BooleanField(default=False)
    ouverte = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Variante d'activité"
        verbose_name_plural = "Variantes d'activités"
        constraints = [
            UniqueConstraint(
                fields=["activite", "description"], name="unique_variante"
            ),
        ]

    # Text repr
    def __str__(self):
        if self.description is None or self.description.strip() == "":
            return f"{self.activite}"
        return f"{self.activite} - {self.description.strip()}"


class PriceByAge(models.Model):
    variante = models.ForeignKey(VarianteActivite, on_delete=models.PROTECT)

    min_age = models.IntegerField(
        validators=[MinValueValidator(0)], blank=True, null=True
    )
    max_age = models.IntegerField(
        validators=[MinValueValidator(0)], blank=True, null=True
    )

    min_price = models.IntegerField(
        validators=[MinValueValidator(0)], blank=True, null=True
    )
    max_price = models.IntegerField(
        validators=[MinValueValidator(0)], blank=True, null=True
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(
                    Q(max_price__isnull=True)
                    | Q(min_price__isnull=True)
                    | Q(max_price__gte=F("min_price"))
                ),
                name="check_price",
            ),
            CheckConstraint(
                check=Q(
                    Q(max_age__isnull=True)
                    | Q(min_age__isnull=True)
                    | Q(max_age__gte=F("min_age"))
                ),
                name="check_age",
            ),
        ]

    @property
    def max_birth(self):
        if self.variante.activite.date_debut is None:
            return None
        if self.variante.activite.date_fin is None:
            return None
        if self.min_age is None: 
            return None
        duree_sejour=self.variante.activite.date_fin-self.variante.activite.date_debut
        deb_sej_age=PriceByAge.sub_years(self.variante.activite.date_debut, self.min_age)
        one_day:datetime.timedelta=datetime.timedelta(days=1)
        ret=deb_sej_age - one_day
        return ret

    @property
    def min_birth(self):
        if self.variante.activite.date_debut is None:
            return None
        if self.variante.activite.date_fin is None:
            return None
        if self.max_age is None: 
            return None
        deb_sej_age=PriceByAge.sub_years(self.variante.activite.date_debut, self.max_age+1)
        one_day:datetime.timedelta=datetime.timedelta(days=1)
        ret=deb_sej_age 
        return ret

    @staticmethod
    def sub_years(start_date, years):
        try:
            return start_date.replace(year=start_date.year - years)
        except ValueError:
            # 👇️ preserve calendar day (if Feb 29th doesn't exist
            # set to March 1st)
            return start_date + (
                datetime.date(start_date.year - years, 1, 1) - datetime.date(start_date.year, 1, 1)
            )

    def get_price_range_txt(self) -> str:
        if self.min_price is None and self.max_price is None:
            return " prix inconnu "
        elif self.min_price is None:
            return f"<={self.max_price}€"
        elif self.max_price is None:
            return f">={self.min_price}€"
        elif self.min_price == self.max_price:
            return f"{self.min_price}€"
        return f"{self.min_price}~{self.max_price}€"

    def get_age_range_txt(self) -> str:
        if self.min_age is not None and self.max_age is not None:
            if self.min_age == self.max_age:
                return f'{self.min_age} ans'
            return f'entre {self.min_age} et {self.max_age} ans'
        elif self.max_age is not None:
            return f'{self.max_age} maximum'
        elif self.min_age is not None:
            return f'{self.min_age} minimum'
        else:
            return " sans contrainte d'age "
        
    def get_birth_range_txt(self) -> str:
        if self.min_birth is not None and self.max_birth is not None:
            if self.min_birth == self.max_birth:
                return f'{self.min_birth.strftime("%d/%m/%Y")}'
            return f'né(e) entre le {self.min_birth.strftime("%d/%m/%Y")} et le {self.max_birth.strftime("%d/%m/%Y")}'
        elif self.max_birth is not None:
            return f'né(e) avant le {self.max_birth.strftime("%d/%m/%Y")}'
        elif self.min_birth is not None:
            return f'né(e) après le {self.min_birth.strftime("%d/%m/%Y")}'
        else:
            return " sans contrainte d'age "

    # Text repr
    def __str__(self):
        return f"Activité : {self.variante} / {self.get_birth_range_txt()} / Tarif : {self.get_price_range_txt()}"
