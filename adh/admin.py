from django.contrib import admin

# Register your models here.
from .models import *
from hab.admin import HabiletePersonneInline


admin.site.register(Famille)

admin.site.register(TypeMembre)
admin.site.register(Adhesion)


class PersonAdmin(admin.ModelAdmin):
    inlines = [HabiletePersonneInline]
    fieldsets = [
        ( "État civil", {"fields": ["nom_naissance", "prenoms_naissance", "date_naissance"], },  ),
        ( "Nom marital ou d'usage - prénom(s) d'usage", 
            {
                "classes": ["collapse"],
                "fields": ["nom_usage", "prenoms_usage", ], 
            },  
        ),
        (
            "Informations de contact", {"classes": ["collapse"],"fields": ["email", "tgram", "whatsapp", "discord"], },
        ),
        (
            "Appartenance aux familles", {"classes": ["collapse"],"fields": ["familles"], },
        ),
    ]
admin.site.register(Personne, PersonAdmin)
