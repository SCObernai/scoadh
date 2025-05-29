from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Saison)
admin.site.register(Periode)
admin.site.register(Activite)
admin.site.register(Variante)
admin.site.register(PriceByAge)