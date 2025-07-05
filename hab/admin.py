from django.contrib import admin
from .models import *

class HabiletePersonneInline(admin.TabularInline):
    model = HabiletePersonne
    extra = 1


class SportAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom"]} 
    list_display = [ "admin_display"]
admin.site.register(Sport, SportAdmin)


class TypeHabileteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom"]} 
    list_display = [ "admin_display", "nom",  "admin_nb_domaines"]
    fieldsets = [
        ( "", {"fields": ["nom", "description"], },  ),
        ( "Informatique", 
            {
                "classes": ["collapse"],
                "fields": ["slug", ], 
                "description" : "Informations à usage interne - NE PAS MODIFIER"
            },  
        ),
    ]
admin.site.register(TypeHabilete, TypeHabileteAdmin)


class DomaineHabileteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": [ "nom"]} 
    list_filter = ('type_habilete',)
    list_display = [ "admin_display", "type_habilete",  "nom", "admin_nb_habiletes"]
    fieldsets = [
        ( "", {"fields": ["type_habilete", "nom", "description"], },  ),
        ( "Informatique", 
            {
                "classes": ["collapse"],
                "fields": ["slug", ], 
                "description" : "Informations à usage interne - NE PAS MODIFIER"
            },  
        ),
    ]
admin.site.register(DomaineHabilete, DomaineHabileteAdmin)


class HabileteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom"]} 
    list_filter = ('sport','domaine',)
    list_display = [ "admin_display", "nom", "description",  "sport"]
    fieldsets = [
        ( "", {"fields": ["domaine", "nom", "description"], },  ),
        ( "Informatique", 
            {
                "classes": ["collapse"],
                "fields": ["slug", ], 
                "description" : "Informations à usage interne - NE PAS MODIFIER"
            },  
        ),
    ]
    inlines = [HabiletePersonneInline]
admin.site.register(Habilete, HabileteAdmin)


class SystemeNotationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom","sport"]} 
    list_filter = ('sport',)
    list_display = [ "admin_display", "nom", "sport"]
    fieldsets = [
        ( "", {"fields": ["sport", "nom", "description"], },  ),
        ( "Informatique", 
            {
                "classes": ["collapse"],
                "fields": ["slug", ], 
                "description" : "Informations à usage interne - NE PAS MODIFIER"
            },  
        ),
    ]
admin.site.register(SystemeNotation, SystemeNotationAdmin)


class NiveauSportifAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom","systeme"]} 
    list_filter = ('systeme',)
    list_display = [ "admin_display", "systeme", "nom"]
    fieldsets = [
        ( "", {"fields": ["systeme", "nom", "habiletes"], },  ),
        ( "Informatique", 
            {
                "classes": ["collapse"],
                "fields": ["slug", ], 
                "description" : "Informations à usage interne - NE PAS MODIFIER"
            },  
        ),
    ]
    filter_horizontal = ('habiletes',) 
admin.site.register(NiveauSportif, NiveauSportifAdmin)


class HabiletePersonneAdmin(admin.ModelAdmin):
    list_display = [ "id", "personne", "habilete", "acquisition_habilete"]
admin.site.register(HabiletePersonne, HabiletePersonneAdmin)
