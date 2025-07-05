from django.db import models

# Create your models here.
class Paiement(models.Model):
    valide = models.BooleanField(default=False)


    class Meta:
        pass

    # Text repr
    def __str__(self):
        return f"TODO PAIEMENT"
