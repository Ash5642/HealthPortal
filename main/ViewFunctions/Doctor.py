from .. import models
from ..serializers import DrugSerializer, PharmacySerializer, DoctorSerializers, ProviderSerializers

from django.core import exceptions

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

@api_view(['GET'])
def GetUpcomingPatients(request):
    try:
        CurrentUser = request.auth.user
        CurrentUserProfile = models.UserProfiles.objects.get(User = CurrentUser, Type = models.DOCTOR)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'no_auth'
        })
    Practices = models.HospitalDoctors.objects.filter(Doctor = CurrentUserProfile).values_list('id')
    Upcoming = models.Appointment.objects.filter(Doctor__Doctor = CurrentUserProfile)
    SerializedData = ProviderSerializers.PatientSerializer(Upcoming, many=True)
    return Response({
        'status':True,
        'data':SerializedData.data
    })

@api_view(['POST', 'GET'])
def ManageAppointment(request):
    AppointmentId = request.GET['AppointmentId']
    try:
        CurrentUser = request.auth.user
        CurrentUserProfile = models.UserProfiles.objects.get(User = CurrentUser, Type = models.DOCTOR)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'no_auth'
        })
    try:
        Appointment = models.Appointment.objects.get(id = AppointmentId)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'not_found'
        })
    if request.method == 'POST':
        Appointment.DocHasConfirmed = True
        Appointment.save()
        for Prescription in request.data.get('Prescriptions'):
            Drug = models.AvailabeForms.objects.get(id = Prescription["Drug"])
            models.Prescription.objects.create(Doctor = Appointment, Instructions = Prescription["Instructions"], Drug = Drug, Quantity = Prescription["Quantity"], Lenght = Prescription["Lenght"])
        return Response({
            'status':True
        })
    else:
        SerializedData = ProviderSerializers.PatientSerializer(Appointment, many=False)
        return Response({
            'status':True,
            'data':SerializedData.data
        })
