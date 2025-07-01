from django.contrib import admin

from .models import *

class ActiviteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom", "saison"]} 
    list_display = ["nom", "saison", "club_organisateur", "membership_required", "licences_possibles"]

class VarianteAdmin(admin.ModelAdmin):
    list_display = [ "description", "activite", "ouverte"]

class PriceByAgeAdmin(admin.ModelAdmin):
    list_display = [ "id", "variante","min_age", "max_age",  "min_birth", "max_birth", "min_price", "max_price"]

admin.site.register(Activite, ActiviteAdmin)
admin.site.register(VarianteActivite, VarianteAdmin)
admin.site.register(PriceByAge, PriceByAgeAdmin)