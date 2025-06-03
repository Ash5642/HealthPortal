from rest_framework import serializers
from .. import models
from django.core import exceptions
from datetime import datetime, timezone,timedelta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfiles
        fields = ['Name', 'BirthDate', 'Name', 'Image']