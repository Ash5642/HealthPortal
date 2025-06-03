from rest_framework import serializers
from .. import models
from . import DrugSerializer, UserSerializers, DoctorSerializers
from django.core import exceptions
from datetime import datetime, timezone,timedelta

class PrescriptionSerializer(serializers.ModelSerializer):
    Drug = DrugSerializer.AvailableFormsSerializer(many = False)
    class Meta:
        model = models.Prescription
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    Patient = UserSerializers.UserSerializer(many = False)
    Prescriptions = PrescriptionSerializer(many=True)
    Timing = DoctorSerializers.TimingSerializer(many = False)
    class Meta:
        model = models.Appointment
        fields = '__all__'
        
