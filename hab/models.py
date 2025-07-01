from django.db import models

# Create your models here.
from django.db import models
from django.db.models import UniqueConstraint
from django.template.defaultfilters import slugify



class Sport(models.Model):
    nom = models.CharField(max_length=20, blank=False, null=False, unique=True)
    slug = models.SlugField(unique=True)
    class Meta:
        ordering = ["nom"]
    # Text repr
    def __str__(self):
        return f"{self.nom}"


class TypeHabilete(models.Model):
    nom = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(unique=True)
    class Meta:
        ordering = ["nom"]
        verbose_name = "Type d'habileté"
        verbose_name_plural = "Types d'habiletés"
    # Text repr
    def __str__(self):
        return f"{self.nom}"


class DomaineHabilete(models.Model):
    nom = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    type_habilite = models.ForeignKey(TypeHabilete, on_delete=models.PROTECT, 
        blank=False, null=False, related_name="domaines_habiletes")
    class Meta:
        verbose_name = "Domaine d'habileté"
        verbose_name_plural = "Domaines d'habiletés"
        ordering = ["nom"]
    # Text repr
    def __str__(self):
        return f"{self.nom}"


class Habilete(models.Model):
    nom = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    criteres_reussite = models.TextField(max_length=500, blank=True, null=True)
    mise_en_place = models.TextField(max_length=500, blank=True, null=True)
    domaine = models.ForeignKey(DomaineHabilete, on_delete=models.PROTECT, 
        blank=False, null=False, related_name="habiletes")
    sport = models.ForeignKey(Sport,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="habiletes",
    )

    class Meta:
        verbose_name = "Habileté"
        verbose_name_plural = "Habiletés"
        ordering = ["nom"]
        constraints = [
            UniqueConstraint(fields=["nom", "sport"], name="habilete_de_sport"),
        ]
    # Text repr
    def __str__(self):
        return f"{self.sport}:{self.nom}"

class SystemeNotation(models.Model) :
    nom = models.CharField(max_length=20, blank=False, null=False)
    slug=models.SlugField(unique=True)
    sport=models.ForeignKey(Sport,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="systemes_notation",
    )

    class Meta:
        ordering = ["nom"]
        verbose_name = "Système de notation"
        verbose_name_plural = "Systèmes de notation"
        constraints = [
            UniqueConstraint(fields=["nom", "sport"], name="notation_de_sport"),
        ]
    # Text repr
    def __str__(self):
        return f"{self.sport}:{self.nom}"


class NiveauSportif(models.Model) :
    nom = models.CharField(max_length=40, blank=False, null=False)
    slug=models.SlugField(unique=True)
    systeme=models.ForeignKey(SystemeNotation,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="niveaux_sportifs",
    )
    habiletes = models.ManyToManyField(Habilete, related_name="niveaux_sportifs")

    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Niveaux sportifs"
        constraints = [
            UniqueConstraint(fields=["nom", "systeme"], name="niveau_dans_systeme"),
        ]
    # Text repr
    def __str__(self):
        return f"{self.systeme}:{self.nom}"

    # TODO : verrouiler pour que l'habilete soit dans le même sport que le systeme de notation


class HabiletePersonne(models.Model):
    personne = models.ForeignKey("adh.Personne", on_delete=models.PROTECT, blank=False, null=False, related_name="habiletes_personne")
    habilete = models.ForeignKey(Habilete, on_delete=models.PROTECT, blank=False, null=False, related_name="habiletes_personne")
    ACQUIS = "A"
    ENCOURS = "E"
    NONACQUIS = "N"
    INCONNU = "I"
    ACQUISITION_HABILETE_CHOICES = [
        (ACQUIS, "Acquis"),
        (ENCOURS, "En cours"),
        (NONACQUIS, "Non acquis"),
        (INCONNU, "Inconnu"),
    ]
    acquisition_habilete = models.CharField(
        max_length=1,
        choices=ACQUISITION_HABILETE_CHOICES,
        default=INCONNU,
    )
    class Meta:
        ordering = ["personne", "habilete", "acquisition_habilete"]
        verbose_name = "Habileté de personne"
        verbose_name_plural = "Habiletés des personnes"
        constraints = [
            UniqueConstraint(
                fields=["personne", "habilete"],
                name="habilete_personne",
            ),
        ]
    
    # Text repr
    def __str__(self):
        return f"{self.personne} <<-->> {self.habilete} ---->>  {dict(HabiletePersonne.ACQUISITION_HABILETE_CHOICES).get(self.acquisition_habilete)}"