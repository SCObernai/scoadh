from django.db import models
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q, F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.template.defaultfilters import slugify
import datetime
from django.contrib.auth.models import User
from glo.models import Saison
from adh.models import Club


class Federation(models.Model):
    alias = models.CharField(max_length=20, blank=False, null=False, unique=True)
    nom = models.CharField(max_length=150, blank=False, null=False, unique=True)
    # TODO url

    class Meta:
        verbose_name = "Fédération"
        verbose_name_plural = "Fédérations"
        ordering = ["alias"]

    # Text repr
    def __str__(self):
        return f"{self.alias}"


class TypeLicence(models.Model):
    alias = models.CharField(max_length=20, blank=False, null=False, unique=True)
    nom = models.CharField(max_length=150, blank=False, null=False, unique=True)
    federation = models.ForeignKey(
        Federation,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="types_licences",
    )
    # TODO : url

    class Meta:
        ordering = ["alias"]
        verbose_name = "Type de licence"
        verbose_name_plural = "Types de licence"

    # Text repr
    def __str__(self):
        return f"{self.federation.alias} : {self.alias}"

    @property
    def full_name(self) -> str:
        return f"{self.federation.alias} {self.alias}"


class NiveauAssurance(models.Model):
    alias = models.CharField(max_length=20, blank=False, null=False)
    nom = models.CharField(max_length=150, blank=False, null=False)
    type_licence = models.ForeignKey(
        TypeLicence,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="niveaux_assurances",
    )
    # TODO : url

    class Meta:
        ordering = ["alias"]
        verbose_name = "Niveau d'assurance"
        verbose_name_plural = "Niveaux d'assurance"
        constraints = [
            UniqueConstraint(fields=["alias", "type_licence"], name="niveau_assurance_uc"),
        ]
    # Text repr
    def __str__(self):
        return f"{self.type_licence} : {self.alias}"

    @property
    def full_name(self) -> str:
        return f"{self.type_licence} {self.alias}"


class IdentiteFederale(models.Model):
    personne = models.ForeignKey(
        "adh.Personne", on_delete=models.PROTECT, null=False, blank=False, related_name="+"
    )
    federation = models.ForeignKey(
        Federation,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="identites_federales",
    )
    numero_licence = models.CharField(max_length=20, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Identités fédérales"
        constraints = [
            UniqueConstraint(
                fields=["personne", "federation"], name="idf_personne_fede_unique"
            ),
            UniqueConstraint(
                fields=["numero_licence", "federation"], name="idf_numlic_fede_unique"
            ),
        ]

    # Text repr
    def __str__(self):
        return f"{self.federation.alias} #{self.numero_licence} : {self.personne}"


class LicenceSaison(models.Model):
    identite_federale = models.ForeignKey(
        IdentiteFederale,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="licences_saisons",
    )
    saison = models.ForeignKey(
        Saison,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="licences_saisons",
    )
    niveau_assurance = models.ForeignKey(
        NiveauAssurance,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="licences_saisons",
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="licences_saisons",
    )
    validateur = models.CharField(max_length=150, blank=False, null=False)
    date_validation = models.DateTimeField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "Licences saison"
        constraints = [
            UniqueConstraint(
                fields=["identite_federale", "saison"],
                name="idf_saison_unique",
            ),
        ]

    def clean(self):
        # # Vérif que la personne correspond à l'identité fédérale
        # if self.personne != self.identite_federale.personne:
        #     raise ValidationError(
        #         f"La personne ({self.personne}) ne correspond pas à la personne de l'identité fédérale ({self.identite_federale.personne}) !"
        #     )
        # # Vérif que la fédération correspond à l'identité fédérale
        # if self.federation != self.identite_federale.federation:
        #     raise ValidationError(
        #         f"La fédération ({self.federation}) ne correspond pas à la fédération de l'identité fédérale ({self.identite_federale.federation}) !"
        #     )
        # # Vérif que la licence annuelle matérialisée ici pour une fédé est d'un type délivré par la fédération en question
        # if self.federation != self.type_licence.federation:
        #     raise ValidationError(
        #         f"Les licences <{self.type_licence}> ne sont pas délivrées par la fédération {self.federation} !"
        #     )
        # # Vérif que le club qui délivre la licence est bien affilié à la fédération correspondante
        # if self.federation not in self.club.federations.all():
        #     raise ValidationError(
        #         f"Le club {self.club} n'est pas affilié à la fédération {self.federation} !"
        #     )

        if self.identite_federale.federation != self.niveau_assurance.type_licence.federation:
            raise ValidationError(f"TODO !")
        if self.niveau_assurance.type_licence.federation not in self.club.federations.all():
            raise ValidationError(f"TODO")

    # Text repr
    def __str__(self):
        return f"Licence {self.niveau_assurance.type_licence.alias} ({self.niveau_assurance.alias}) {self.niveau_assurance.type_licence.federation.alias} #{self.identite_federale.numero_licence} "

    @property
    def numero_licence(self) -> str:
        return self.identite_federale.numero_licence
