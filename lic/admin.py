from django.contrib import admin
from .models import *



class FederationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom"]} 
    list_display = ["admin_display", "nom", "description"]
    fieldsets = [
        ( "", {"fields": ["nom", "description", "url"], },  ),
        ( "Informatique", 
            {
                "classes": ["collapse"],
                "fields": ["slug", ], 
                "description" : "Informations à usage interne - NE PAS MODIFIER"
            },  
        ),
    ]    
admin.site.register(Federation, FederationAdmin)


class TypeLicenceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom"]} 
    list_filter = ('federation',)
    list_display = ["admin_display", "federation", "nom", "description"]
    fieldsets = [
        ( "", {"fields": ["federation", "nom", "description", "url"], },  ),
        ( "Informatique", 
            {
                "classes": ["collapse"],
                "fields": ["slug", ], 
                "description" : "Informations à usage interne - NE PAS MODIFIER"
            },  
        ),
    ]    
admin.site.register(TypeLicence, TypeLicenceAdmin)


class NiveauAssuranceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom"]} 
    list_filter = ('type_licence',)
    list_display = ["admin_display", "type_licence", "nom", "description"]
    fieldsets = [
        ( "", {"fields": ["type_licence", "nom", "description", "url"], },  ),
        ( "Informatique", 
            {
                "classes": ["collapse"],
                "fields": ["slug", ], 
                "description" : "Informations à usage interne - NE PAS MODIFIER"
            },  
        ),
    ]   
admin.site.register(NiveauAssurance, NiveauAssuranceAdmin)


class IdentiteFederaleAdmin(admin.ModelAdmin):
    list_filter = ('federation',)
    list_display = ["admin_display", "federation", "numero_licence", "personne"]
    fieldsets = [
        ( "", {"fields": ["federation", "numero_licence", "personne"], },  ),
    ]   
admin.site.register(IdentiteFederale, IdentiteFederaleAdmin)

class LicenceSaisonAdmin(admin.ModelAdmin):
    list_display = ["id", "identite_federale", "numero_licence", "saison", "niveau_assurance", "club", "date_validation"]





admin.site.register(LicenceSaison, LicenceSaisonAdmin)
