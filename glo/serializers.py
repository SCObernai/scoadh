from .models import *
from rest_framework import serializers

__all__ = (
   'NestedSaisonSerializer',
)

class NestedSaisonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Saison
        fields = ['id', 'start_year']





