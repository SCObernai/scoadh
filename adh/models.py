from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q, F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.template.defaultfilters import slugify
import datetime
from django.contrib.auth.models import User

from hab.models import Habilete, HabiletePersonne


class Famille(models.Model):
    alias = models.CharField(max_length=150, blank=False, null=False, unique=True)
    bosses = models.CharField(max_length=500, blank=False, null=False)

    # Text repr
    def __str__(self):
        return f"Famille {self.alias}"
    
    # TODO : fonction d'ajout de boss / supression de boss / check de boss


class Club(models.Model):
    alias = models.CharField(max_length=20, blank=False, null=False, unique=True)
    nom = models.CharField(max_length=150, blank=False, null=False, unique=True)
    federations = models.ManyToManyField("lic.Federation")
    FAMILLE = "F"
    INDIVIDUELLE = "I"
    TYPE_ADHESION_CHOICES = [
        (FAMILLE, "Famille"),
        (INDIVIDUELLE, "Individuelle"),
    ]
    type_adhesion = models.CharField(
        max_length=1,
        choices=TYPE_ADHESION_CHOICES,
        default=FAMILLE,
    )
    # TODO : url, validité de l'adhésion

    class Meta:
        ordering = ["alias"]

    # Text repr
    def __str__(self):
        return f"{self.alias}"

    @property
    def affiliations(self) -> str:
        return ", ".join(
            self.federations.all().values_list("alias", flat=True).order_by("alias")
        )
    


class Personne(models.Model):
    nom_naissance = models.CharField(max_length=150, blank=False, null=False, verbose_name="Nom de naissance")
    nom_usage = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nom d'usage")
    prenoms_naissance = models.CharField(max_length=250, blank=False, null=False, verbose_name="Prénoms de naissance")
    prenoms_usage = models.CharField(max_length=250, blank=True, null=True, verbose_name="Prénoms d'usage")
    date_naissance = models.DateField(blank=False, null=False, verbose_name="Date de naissance")
    email=models.EmailField(max_length=150, blank=True, null=True, unique=True)
    tgram=models.CharField(max_length=150, blank=True, null=True, unique=True)
    whatsapp=models.CharField(max_length=150, blank=True, null=True, unique=True)
    discord =models.CharField(max_length=150, blank=True, null=True, unique=True)
    familles = models.ManyToManyField(Famille)
    habiletes = models.ManyToManyField(Habilete, through=HabiletePersonne)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["nom_naissance", "prenoms_naissance", "date_naissance"],
                name="etat_civil_unique",
            ),
        ]

    @property
    def nom(self):
        if self.nom_usage is not None and self.nom_usage.strip() != "":
            return self.nom_usage
        return self.nom_naissance

    @property
    def prenoms(self):
        if self.prenoms_usage is not None and self.prenoms_usage.strip() != "":
            return self.prenoms_usage
        return self.prenoms_naissance

    # Text repr
    def __str__(self):
        return f"{self.nom} {self.prenoms} / Né(e) le {self.date_naissance} "

