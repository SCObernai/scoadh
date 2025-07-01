from django.contrib import admin

# Register your models here.
from .models import *
from hab.admin import HabiletePersonneInline

class ClubAdmin(admin.ModelAdmin):
    list_display = ["alias", "nom", "affiliations"]
admin.site.register(Club, ClubAdmin)



class PersonAdmin(admin.ModelAdmin):
    inlines = [HabiletePersonneInline]
    fieldsets = [
        ( "État civil", {"fields": ["nom_naissance", "prenoms_naissance", "date_naissance"], },  ),
        ( "Nom & prénoms d'usage / nom marital", 
            {
                "classes": ["collapse"],
                "fields": ["nom_usage", "prenoms_usage", ], 
            },  
        ),
        (
            "Contact", {"classes": ["collapse"],"fields": ["email", "tgram", "whatsapp", "discord"], },
        ),
        (
            "Familles", {"classes": ["collapse"],"fields": ["familles"], },
        ),
    ]
admin.site.register(Personne, PersonAdmin)

admin.site.register(Famille)


