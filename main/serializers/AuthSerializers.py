from rest_framework import serializers
from .. import models
from . import DrugSerializer, UserSerializers, DoctorSerializers
from django.core import exceptions
from datetime import datetime, timezone,timedelta

class UserProfiileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfiles
        fields = ['Name', 'Image', 'BirthDate']
class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pharmacy
        fields = ['Image', 'Location', 'Lat', 'Lon', 'Name', 'Address']