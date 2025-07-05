from django.db import models
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q, F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.template.defaultfilters import slugify
import datetime
from django.contrib.auth.models import User


class Saison(models.Model):
    # 2024-2025
    start_year = models.IntegerField(validators=[MinValueValidator(2024)], primary_key=True)

    class Meta:
        ordering = ["start_year"]
    # Text repr
    def __str__(self):
        return f"{self.start_year}-{self.start_year-2000+1}"
    # Admin display
    def admin_display(self):
        return f"Saison {self.start_year}-{self.start_year+1}"


class Club(models.Model):
    nom = models.CharField(max_length=20, blank=False, null=False, primary_key=True)
    description = models.CharField(max_length=150, blank=False, null=False, unique=True)
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
        ordering = ["nom"]

    # Text repr
    def __str__(self):
        return f"{self.nom}"
    # Admin display
    def admin_display(self):
        return f"{self.nom} - {self.description}"
    @property
    def affiliations(self) -> str:
        return ", ".join(
            self.federations.all().values_list("nom", flat=True).order_by("nom")
        )
    