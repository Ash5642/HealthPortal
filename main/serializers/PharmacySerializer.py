from rest_framework import serializers
from .. import models
from . import DrugSerializer
from django.core import exceptions
from datetime import datetime, timezone,timedelta

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pharmacy
        fields = '__all__'

class PharmacyStockSerializer(serializers.ModelSerializer):
    Pharmacy = PharmacySerializer(many = False)
    Drug = DrugSerializer.AvailableFormsSerializer(many = False)
    class Meta:
        model = models.PharmacyInventory
        fields = '__all__'