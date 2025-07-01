from .models import *
from rest_framework import serializers
from glo.serializers import *


__all__ = (
   'NestedPriceByAgeSerializer', 
   'NestedVarianteSerializer',
   'JsonActiviteSerializer',
)

class NestedPriceByAgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PriceByAge
        fields = ['id', 'min_birth', 'max_birth', 'min_price', 'max_price']

class NestedVarianteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VarianteActivite
        fields = ['id', 'description', 'pass_allowed', 'ouverte', 'pricebyage_set']
    pricebyage_set=NestedPriceByAgeSerializer(many=True)
    
class JsonActiviteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activite
        fields = ['id', 'saison', 'nom', 'slug', 'membership_required', 'variantes']
    saison=NestedSaisonSerializer()
    variantes=NestedVarianteSerializer(many=True)


