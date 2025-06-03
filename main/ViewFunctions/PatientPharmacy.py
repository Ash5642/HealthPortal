from .. import models
from ..serializers import DrugSerializer, PharmacySerializer

from django.core import exceptions

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

@api_view(['GET'])
def FindDrugBrand(request):
    Name = request.GET['BrandName']
    print(Name)
    try:
        Drug = models.DrugBrands.objects.get(Name = Name)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'not_found'
        })
    SerializedData = DrugSerializer.DrugBrandSerializer(Drug, many=False)
    return Response({
        'status':True,
        'data':SerializedData.data
    })


@api_view(['GET'])
def FindGenericDrug(request):
    Name = request.GET['GenericName']
    print(Name)
    try:
        Drug = models.Drug.objects.get(Name = Name)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'not_found'
        })
    SerializedData = DrugSerializer.GenericDrugSerializer(Drug, many=False)
    return Response({
        'status':True,
        'data':SerializedData.data
    })

@api_view(['GET'])
def FindDrugForm(request):
    FormID = request.GET['FormID']
    print(FormID)
    try:
        DrugForm = models.AvailabeForms.objects.get(id = FormID)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'not_found'
        })
    SerializedData = DrugSerializer.AvailableFormsSerializer(DrugForm, many=False)
    return Response({
        'status':True,
        'data':SerializedData.data
    })

@api_view(['GET'])
def GetPharmacyInformation(request):
    PharmacyId = request.GET['PharmacyId']
    print(PharmacyId)
    try:
        Pharmacy = models.Pharmacy.objects.get(id = PharmacyId)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'not_found'
        })
    SerializedData = PharmacySerializer.PharmacySerializer(Pharmacy, many=False)
    return Response({
        'status':True,
        'data':SerializedData.data
    })

@api_view(['GET'])
def GetPharmacyStock(request):
    PharmacyId = request.GET['PharmacyId']
    print(PharmacyId)
    try:
        Pharmacy = models.Pharmacy.objects.get(id = PharmacyId)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'not_found'
        })
    InventoryIds = models.PharmacyInventory.objects.filter(Pharmacy = Pharmacy).values_list('Drug_id', flat=True)
    DrugsInventory = models.AvailabeForms.objects.filter(id__in = InventoryIds).order_by("Brand")
    SerializedData = DrugSerializer.AvailableFormsSerializer(DrugsInventory, many=True)
    return Response({
        'status':True,
        'data':SerializedData.data
    })

@api_view(['GET'])
def SearchDrugFormLocations(request):
    FormID = request.GET['FormID']
    UserLat = float(request.GET['PosLat'])
    UserLon = float(request.GET['PosLon'])
    Range = int(request.GET['Range']) * 1000
    print(FormID)
    try:
        DrugForm = models.AvailabeForms.objects.get(id = FormID)
    except exceptions.ObjectDoesNotExist:
        return Response({
            'status':False,
            'detail':'not_found'
        })
    NearbyPharmiciesSquare = models.Pharmacy.objects.filter(Lat__gte = UserLat-Range/111, Lat__lte = UserLat+Range/111, Lon__gte = UserLon-Range/111, Lon__lte = UserLon+Range/111).values_list('id', flat=True)
    InventoryFilter = models.PharmacyInventory.objects.filter(Drug = DrugForm, Pharmacy__in = NearbyPharmiciesSquare)
    SerializedData = PharmacySerializer.PharmacyStockSerializer(InventoryFilter, many=True)
    Alternatives = models.AvailabeForms.objects.filter(Brand__GenericDrug__id = DrugForm.Brand.GenericDrug.id, Dosage = DrugForm.Dosage, Form = DrugForm.Form).exclude(id = FormID).values_list('id', flat=True)
    print(Alternatives)
    AlternativeInventoryFilter = models.PharmacyInventory.objects.filter(Drug__in = Alternatives, Pharmacy__in = NearbyPharmiciesSquare)
    AlternateSerializedData = PharmacySerializer.PharmacyStockSerializer(AlternativeInventoryFilter, many=True)
    return Response({
        'status':True,
        'data':SerializedData.data,
        'alternatives':AlternateSerializedData.data
    })


@api_view(['GET'])
def SearchDrug(request):
    SearchTerm = request.GET['query']

    BrandNamesMatch = models.DrugBrands.objects.filter(Name__icontains = SearchTerm).values_list("GenericDrug", flat=True)
    Drugs = models.Drug.objects.filter(
        Q(Name__icontains = SearchTerm)|
        Q(id__in = BrandNamesMatch)
    )
    Pharmacies = models.Pharmacy.objects.filter(Name__icontains = SearchTerm)
    SerializedData = DrugSerializer.GenericDrugSerializer(Drugs, many=True)
    SerializedPharmacyData = PharmacySerializer.PharmacySerializer(Pharmacies, many = True)
    return Response({
        'status':True,
        'data':SerializedData.data,
        'pharmacies':SerializedPharmacyData.data
    })

@api_view(['GET'])
def SearchDrugForm(request):
    SearchTerm = request.GET['query']

    FormMatch = models.AvailabeForms.objects.filter(Name__icontains = SearchTerm)
    SerializedData = DrugSerializer.AvailableFormsSerializer(FormMatch, many=True)
    return Response({
        'status':True,
        'data':SerializedData.data,
    })