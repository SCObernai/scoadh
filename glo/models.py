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
    start_year = models.IntegerField(validators=[MinValueValidator(2024)], unique=True)

    class Meta:
        ordering = ["start_year"]

    # Text repr
    def __str__(self):
        return f"Saison {self.start_year}-{self.start_year+1}"

