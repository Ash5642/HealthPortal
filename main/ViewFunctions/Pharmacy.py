from .. import models
from ..serializers import DrugSerializer, PharmacySerializer, DoctorSerializers, ProviderSerializers

from django.core import exceptions

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q


