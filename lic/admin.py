from django.contrib import admin
from .models import *





class LicenceSaisonAdmin(admin.ModelAdmin):
    list_display = ["id", "identite_federale", "numero_licence", "saison", "niveau_assurance", "club", "date_validation"]

class TypeLicenceAdmin(admin.ModelAdmin):
    list_display = ["alias", "nom", "federation"]


admin.site.register(Federation)

admin.site.register(TypeLicence, TypeLicenceAdmin)
admin.site.register(LicenceSaison, LicenceSaisonAdmin)
admin.site.register(IdentiteFederale)