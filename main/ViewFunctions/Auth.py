from .. import models
from ..serializers import DrugSerializer, PharmacySerializer, DoctorSerializers, ProviderSerializers, AuthSerializers

from django.core import exceptions
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def NormalRegistratiiion(request):
    UserName = request.data.get('UserName')
    Password = make_password(request.data.get('Password'))
    try:
        models.User.objects.get(username = UserName)
        return Response({
            'status':False,
            'detail':'exists'
        })
    except exceptions.ObjectDoesNotExist:
        pass
    NewUser = models.User.objects.create(username = UserName, password=Password)
    UserProfileSerialized = AuthSerializers.UserProfiileSerializer(data=request.data, many=False)
    if UserProfileSerialized.is_valid():
        UserProfileSerialized.save(Type = models.PATIENT, User = NewUser)
    else:
        return Response({
            'status':False,
            'detail':'invalid'
        })
    try:
        Key =  Token.objects.get(user = NewUser).key
    except exceptions.ObjectDoesNotExist:
        Key =  Token.objects.create(user = NewUser).key 
    return Response({
            'status':True,
            'Key':Key
        })
    

@api_view(['POST'])
def NormalLogIn(request):
    UserName = request.data.get('UserName')
    Password = request.data.get('Password')
    try:
        User = models.User.objects.get(username = UserName)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'does_not_exist'
        })
    if User.check_password(Password):
        try:
            Key =  Token.objects.get(user = User).key
        except exceptions.ObjectDoesNotExist:
            Key =  Token.objects.create(user = User).key 
        return Response({
                'status':True,
                'Key':Key
            })

@api_view(['POST'])
def DoctorRegistration(request):
    UserName = request.data.get('UserName')
    Password = make_password(request.data.get('Password'))
    Speciality = request.data.get('Speciality')
    Quals = request.data.get('Quals')
    try:
        models.User.objects.get(username = UserName)
        return Response({
            'status':False,
            'detail':'exists'
        })
    except exceptions.ObjectDoesNotExist:
        pass
    NewUser = models.User.objects.create(username = UserName, password=Password)
    UserProfileSerialized = AuthSerializers.UserProfiileSerializer(data=request.data, many=False)
    if UserProfileSerialized.is_valid():
        UserProfileSerialized.save(Type = models.DOCTOR, User = NewUser)
    else:
        return Response({
            'status':False,
            'detail':'invalid'
        })
    NewUserProfile = models.UserProfiles.objects.get(User = NewUser)
    models.DoctorMeta.objects.create(
        Doctor = NewUserProfile,
        Speciality = Speciality,
        Quals = Quals
    )
    try:
        Key =  Token.objects.get(user = NewUser).key
    except exceptions.ObjectDoesNotExist:
        Key =  Token.objects.create(user = NewUser).key 
    return Response({
            'status':True,
            'Key':Key
        })


@api_view(['POST'])
def RegisterPharmacy(request):
    UserName = request.data.get('UserName')
    Password = make_password(request.data.get('Password'))
    PharmacyName = request.data.get('PharmacyName')
    try:
        models.User.objects.get(username = UserName)
        return Response({
            'status':False,
            'detail':'exists'
        })
    except exceptions.ObjectDoesNotExist:
        pass
    NewUser = models.User.objects.create(username = UserName, password=Password)
    UserProfileSerialized = AuthSerializers.UserProfiileSerializer(data=request.data, many=False)
    if UserProfileSerialized.is_valid():
        UserProfileSerialized.save(Type = models.DOCTOR, User = NewUser)
    else:
        return Response({
            'status':False,
            'detail':'invalid'
        })
    NewUserProfile = models.UserProfiles.objects.get(User = NewUser)
    PharmacySerialized = AuthSerializers.PharmacySerializer(data=request.data, many=False)
    print(request.data)
    if PharmacySerialized.is_valid():
        PharmacySerialized.save(Pharmacist = NewUserProfile)
    else:
        return Response({
            'status':False,
            'detail':'invalissd'
        })
    try:
        Key =  Token.objects.get(user = NewUser).key
    except exceptions.ObjectDoesNotExist:
        Key =  Token.objects.create(user = NewUser).key 
    return Response({
            'status':True,
            'Key':Key
        })