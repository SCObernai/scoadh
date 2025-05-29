from .models import *
from rest_framework import serializers



class NestedSaisonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Saison
        fields = ['id', 'start_year']

class NestedPeriodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Periode
        fields = ['id', 'saison', 'label', 'visible', 'slug']
    saison=NestedSaisonSerializer()

class NestedPriceByAgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PriceByAge
        fields = ['id', 'min_birth', 'max_birth', 'min_price', 'max_price']

class NestedVarianteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Variante
        fields = ['id', 'description', 'pass_allowed', 'ouverte', 'pricebyage_set']
    pricebyage_set=NestedPriceByAgeSerializer(many=True)
    
class JsonActiviteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activite
        fields = ['id', 'periode', 'nom', 'ski_licence_required', 'membership_required', 'variante_set']
    periode=NestedPeriodeSerializer()
    variante_set=NestedVarianteSerializer(many=True)


