from .models import *
from rest_framework import serializers



class NestedSportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'slug', 'nom']

class NestedTypeHabileteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeHabilete
        fields = ['id', 'slug', 'nom']

class NestedDomaineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DomaineHabilete
        fields = ['id', 'slug', 'nom', 'description', 'type_habilite']
    type_habilite=NestedTypeHabileteSerializer()

class NestedSystemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SystemeNotation
        fields = ['id', 'slug', 'nom', 'sport',]
    sport=NestedSportSerializer()

class NestedNiveauSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NiveauSportif
        fields = ['id', 'slug', 'nom', 'systeme']
    systeme=NestedSystemeSerializer()
    
class JsonHabileteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Habilete
        fields = ['id', 'slug', 'nom', 'description', 'criteres_reussite', 'mise_en_place', "domaine", "sport", "niveaux_sportifs"]
    domaine=NestedDomaineSerializer()
    sport=NestedSportSerializer()
    niveaux_sportifs=NestedNiveauSerializer(many=True)


