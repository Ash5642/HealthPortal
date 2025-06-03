from rest_framework import serializers
from .. import models
from django.core import exceptions
from datetime import datetime, timezone,timedelta

class MiniDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Drug
        fields = '__all__'

class MiniAvailableFormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AvailabeForms
        fields = '__all__'


class DrugBrandSerializer(serializers.ModelSerializer):
    GenericDrug = MiniDrugSerializer(many=False)
    Forms = MiniAvailableFormsSerializer(many = True)
    class Meta:
        model = models.DrugBrands
        fields =  ['GenericDrug', 'Name', 'Manafacturer', 'Forms', 'Image']


class GenericDrugSerializer(serializers.ModelSerializer):
    Brands = DrugBrandSerializer(many=True)
    class Meta:
        model = models.Drug
        fields =  ['Name', 'Structure', 'Brands', 'Description', 'Uses', 'Mechanism', 'SideEffects']

class AvailableFormsSerializer(serializers.ModelSerializer):
    Brand = DrugBrandSerializer(many = False)
    class Meta:
        model = models.AvailabeForms
        fields = ['Dosage', 'Unit', 'Price', 'Brand', 'Name', 'Quantity', 'id']

class DosageFormSerializer(serializers.ModelSerializer):
    GenericName = DrugBrandSerializer(many = False)
    class Meta:
        model = models.AvailabeForms
        fields = ['Dosage', 'Unit']
    
