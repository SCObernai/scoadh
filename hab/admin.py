from django.contrib import admin
from .models import *

class HabiletePersonneInline(admin.TabularInline):
    model = HabiletePersonne
    extra = 1

class SportAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom"]} 
    list_display = [ "id", "nom", "slug"]

class HabileteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom"]} 
    list_display = [ "id", "nom", "description", "criteres_reussite", "sport"]
    inlines = [HabiletePersonneInline]

class SystemeNotationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom","sport"]} 
    list_display = [ "id", "nom", "sport"]

class NiveauSportifAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["nom","systeme"]} 
    list_display = [ "id", "nom", "systeme"]
    filter_horizontal = ('habiletes',) 

class HabiletePersonneAdmin(admin.ModelAdmin):
    list_display = [ "id", "personne", "habilete", "acquisition_habilete"]



admin.site.register(TypeHabilete)
admin.site.register(DomaineHabilete)
admin.site.register(Sport, SportAdmin)
admin.site.register(Habilete, HabileteAdmin)
admin.site.register(HabiletePersonne, HabiletePersonneAdmin)
admin.site.register(SystemeNotation, SystemeNotationAdmin)
admin.site.register(NiveauSportif, NiveauSportifAdmin)