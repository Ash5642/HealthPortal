from rest_framework import serializers
from .. import models
from . import DrugSerializer
from django.core import exceptions
from datetime import datetime, timezone,timedelta

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hospital
        fields = '__all__'

class TimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HospitalDoctorTiming
        fields = '__all__'
class DoctorHospitalSerializer(serializers.ModelSerializer):
    Hospital = HospitalSerializer(many = False)
    Timings = TimingSerializer(many=True)

    class Meta:
        model = models.HospitalDoctors
        fields = '__all__'
class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorMeta
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    Drug = DrugSerializer.AvailableFormsSerializer(many = False)
    class Meta:
        model = models.Prescription
        fields = '__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    Hospitals = DoctorHospitalSerializer(many = True)
    MetaInfo = MetaSerializer(many = False)
    class Meta:
        model = models.UserProfiles
        fields = '__all__'

class DoctorHospitalSerializerFull(serializers.ModelSerializer):
    Hospital = HospitalSerializer(many = False)
    Timings = TimingSerializer(many=True)
    Doctor = DoctorProfileSerializer(many = False)
    class Meta:
        model = models.HospitalDoctors
        fields = '__all__'
    
class AppointmentSerializer(serializers.ModelSerializer):
    Prescriptions = PrescriptionSerializer(many = True)
    Timing = TimingSerializer(many=False)
    Doctor = DoctorHospitalSerializerFull(many=False)
    class Meta:
        model = models.Appointment
        fields = '__all__'