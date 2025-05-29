from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q, F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
import datetime

class Saison(models.Model):
    # 2024-2025 
    start_year=models.IntegerField(validators=[MinValueValidator(2025)], unique=True)
    class Meta:
        ordering = ['start_year']
    # Text repr
    def __str__(self):
        return f"Saison {self.start_year}-{self.start_year+1}"
    
class Periode(models.Model):
    # hiver 2024-2025 / été 2024
    saison=models.ForeignKey(Saison, on_delete=models.PROTECT)
    label=models.CharField(max_length=20)
    visible=models.BooleanField(default=False)
    slug = models.SlugField(null=False, default=F('label'))   
    class Meta:
        constraints = [
            UniqueConstraint(fields=['saison', 'label'], name='periode_de_saison'),
        ]
    # Text repr
    def __str__(self):
        return f"{self.label} ({"visible" if self.visible else "invisible"})"

class Activite(models.Model):
    periode=models.ForeignKey(Periode, on_delete=models.PROTECT)
    nom=models.CharField(max_length=200, null=False, blank=False)
    ski_licence_required=models.BooleanField(default=False)
    membership_required=models.BooleanField(default=False)
    slug = models.SlugField(null=False, default=F('nom'))   
    class Meta:
        constraints = [
            UniqueConstraint(fields=['periode', 'nom'], name='unique_activite'),
        ]
    # Text repr
    def __str__(self):
        return f"{self.periode} - {self.nom}"

class Variante(models.Model):
    activite=models.ForeignKey(Activite, on_delete=models.PROTECT)
    description=models.CharField(max_length=200, blank=True)
    pass_allowed=models.BooleanField(default=False)
    ouverte=models.BooleanField(default=False)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['activite', 'description'], name='unique_variante'),
        ]
    # Text repr
    def __str__(self):
        if self.description is None or self.description.strip()=="":
            return f"{self.activite}"
        return f"{self.activite} - {self.description.strip()}"

class PriceByAge(models.Model):
    variante=models.ForeignKey(Variante, on_delete=models.PROTECT)
    min_birth=models.DateField(default=datetime.date.today, blank=True, null=True)
    max_birth=models.DateField(default=datetime.date.today, blank=True, null=True)
    min_price=models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    max_price=models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(Q(max_price__isnull=True)|Q(min_price__isnull=True)|Q(max_price__gte=F('min_price'))), 
                name = 'check_price',
            ),
             CheckConstraint(
                check = Q(Q(max_birth__isnull=True)|Q(min_birth__isnull=True)|Q(max_birth__gte=F('min_birth'))), 
                name = 'check_birth',
            ),
        ]
    def get_price_range_txt(self)->str:
        if self.min_price is None and self.max_price is None : 
            return " prix inconnu "
        elif self.min_price is None:
            return f'<={self.max_price}€'
        elif self.max_price is None:
            return f'>={self.min_price}€'
        elif self.min_price==self.max_price:
            return f'{self.min_price}€'
        return f'{self.min_price}~{self.max_price}€'
    def get_birth_range_txt(self)->str:
        if self.min_birth is None and self.max_birth is None : 
            return " sans contrainte d'age "
        elif self.min_birth is None:
            return f'né(e) avant le {self.max_birth.strftime("%d/%m/%Y")}'
        elif self.max_birth is None:
            return f'né(e) après le {self.min_birth.strftime("%d/%m/%Y")}'
        elif self.min_birth==self.max_birth:
            return f'{self.min_birth.strftime("%d/%m/%Y")}'
        return f'né(e) entre le {self.min_birth.strftime("%d/%m/%Y")} et le {self.max_birth.strftime("%d/%m/%Y")}'
    # Text repr
    def __str__(self):
        return f"Activité : {self.variante} / {self.get_birth_range_txt()} / Tarif : {self.get_price_range_txt()}"