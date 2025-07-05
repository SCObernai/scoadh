from django.contrib import admin

from .models import *


class JaugeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom", "saison"]} 
    list_display = ["id", "saison", "nom", "niveau_min", "niveau_max", "slug"]
admin.site.register(Jauge, JaugeAdmin)

class ActiviteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom", "saison"]} 
    list_display = ["id", "saison", "nom", "club_organisateur", "membership_required", "licences_possibles"]
    fieldsets = [
        ( "", {"fields": ["saison", "club_organisateur", "nom", "date_debut", "date_fin", "multi_date", "url_info"], },  ),
        ( "Conditions de licence ou d'adhésion", 
            {
                "classes": ["collapse"],
                "fields": ["type_lic_req", "membership_required", ], 
            },  
        ),
        (
            "Paniers et jauges", {"classes": ["collapse"],"fields": ["slug", "jauges"], },
        ),
    ]
admin.site.register(Activite, ActiviteAdmin)

class VarianteAdmin(admin.ModelAdmin):
    list_display = [ "id", "activite", "description", "ouverte", "date_debut", "date_fin"]
    fieldsets = [
        ( "", {"fields": ["activite", "description", "ouverte"], },  ),
        ( "Dates de la variante", 
            {
                "classes": ["collapse"],
                "fields": ["date_debut", "date_fin", ], 
                "description" : "VALABLE UNIQUEMENT POUR LES ACTIVITES MULTI DATES"
            },  
        ),
    ]
admin.site.register(VarianteActivite, VarianteAdmin)

class PriceByAgeAdmin(admin.ModelAdmin):
    list_display = [ "id", "variante","min_age", "max_age",  "min_birth", "max_birth", "min_price", "max_price"]
admin.site.register(PriceByAge, PriceByAgeAdmin)


