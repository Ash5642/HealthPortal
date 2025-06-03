from .. import models
from ..serializers import DrugSerializer, PharmacySerializer, DoctorSerializers

from django.core import exceptions

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

@api_view(['GET'])
def GetDoctorPractices(request):
    DoctorId = request.GET['DoctorId']
    try:
        Doctor = models.UserProfiles.objects.get(Type = models.DOCTOR, id = DoctorId)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'not_found'
        })
    SerializedData = DoctorSerializers.DoctorProfileSerializer(Doctor, many=False)
    return Response({
        'status':True,
        'data':SerializedData.data
    })
@api_view(['GET'])
def FilterDoctors(request):
    Range = float(request.GET['Range'])
    Type = request.GET['Type']
    Price = request.GET['Price']
    UserLat = float(request.GET['PosLat'])
    UserLon = float(request.GET['PosLon'])
    HospitalsInRange = models.Hospital.objects.filter(Lat__gte = UserLat-Range/111, Lat__lte = UserLat+Range/111, Lon__gte = UserLon-Range/111, Lon__lte = UserLon+Range/111).values_list('id', flat=True)  
    VisitsInRange = models.HospitalDoctors.objects.filter(Hospital__in = HospitalsInRange, Price__lte = Price).values_list('Doctor_id', flat=True)
    DoctorsInRange = models.UserProfiles.objects.filter(Type = models.DOCTOR, id__in = VisitsInRange, MetaInfo__Speciality = Type)
    SerializedData = DoctorSerializers.DoctorProfileSerializer(DoctorsInRange, many=True)
    return Response({
        'status':True,
        'data':SerializedData.data
    })
@api_view(['POST', 'GET'])
def GetAppointment(request):
    VisitId = request.GET['VisitId']
    Time = request.GET['Time']
    try:
        CurrentUser = request.auth.user
        CurrentUserProfile = models.UserProfiles.objects.get(User = CurrentUser)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'no_auth'
        })
    try:
        Visit = models.HospitalDoctors.objects.get(id = VisitId)
        Timing = models.HospitalDoctorTiming.objects.get(id = Time)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'not_found'
        })
    if request.method == 'POST':
        try:
            Appointment = models.Appointment.objects.get(Doctor = Visit, Timing = Timing, Patient = CurrentUserProfile, DocHasConfirmed = False)
            return Response({
                'status':False,
                'detail':'already_exists'
            })
        except exceptions.ObjectDoesNotExist:
            pass
        Appointment = models.Appointment.objects.create(Doctor = Visit, Timing = Timing, Patient = CurrentUserProfile)
        return Response({
                'status':True,
            })
            
    if request.method == 'GET':
        try:
            Appointment = models.Appointment.objects.get(Doctor = Visit, Timing = Timing, Patient = CurrentUserProfile)
        except exceptions.ObjectDoesNotExist:
            return Response({
                'status':False,
                'detail':'no_appointment'
            })
        SerializedData = DoctorSerializers.AppointmentSerializer(Appointment, many=False)
        return Response({
            'status':True,
            'data':SerializedData.data
        })

@api_view(['GET'])
def ListPatientAppointments(request):
    try:
        CurrentUser = request.auth.user
        CurrentUserProfile = models.UserProfiles.objects.get(User = CurrentUser)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'no_auth'
        })
    Appointments = models.Appointment.objects.filter(Patient = CurrentUserProfile)
    SerializedData = DoctorSerializers.AppointmentSerializer(Appointments, many=True)
    return Response({
        'status':True,
        'data':SerializedData.data
    })