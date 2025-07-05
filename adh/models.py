from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q, F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.template.defaultfilters import slugify
import datetime
from django.contrib.auth.models import User


from glo.models import Club
from hab.models import Habilete, HabiletePersonne
from pan.models import Paiement

class Famille(models.Model):
    alias = models.CharField(max_length=150, blank=False, null=False, unique=True)
    bosses = models.CharField(max_length=500, blank=False, null=False)

    # Text repr
    def __str__(self):
        return f"Famille {self.alias}"
    
    # TODO : fonction d'ajout de boss / supression de boss / check de boss



class TypeMembre(models.Model):
    club = models.ForeignKey(to=Club, on_delete=models.PROTECT, null=False, blank=False)
    nom = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=False)
    
    class Meta:
        verbose_name = "Type de membre"
        verbose_name_plural = "Types de membres"
        constraints = [
            UniqueConstraint(fields=["club", "nom"], name="unique_typemembre_club"),
        ]

    # Text repr
    def __str__(self):
        return f"{self.club}:{self.nom}"
    

class Adhesion(models.Model):
    personne = models.ForeignKey(to="Personne", on_delete=models.PROTECT, null=False, blank=False)
    club = models.ForeignKey(to=Club, on_delete=models.PROTECT, null=False, blank=False)
    date_adhesion = models.DateField(null=False, blank=False)
    paiement = models.ForeignKey(to=Paiement, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "Adhésion au club"
        verbose_name_plural = "Adhésions aux club"


    # Text repr
    def __str__(self):
        return f"Adhesion de {self.personne} à {self.club} en date du {self.date_adhesion} -> {self.paiement}"
    

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

