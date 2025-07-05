from django.contrib import admin

from hab.admin import HabiletePersonneInline
from .models import *

class SaisonAdmin(admin.ModelAdmin):
    list_display = ["admin_display",]
admin.site.register(Saison, SaisonAdmin)


class ClubAdmin(admin.ModelAdmin):
    list_display = ["admin_display", "nom", "description", "type_adhesion", "affiliations"]
admin.site.register(Club, ClubAdmin)

