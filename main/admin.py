from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Drug)
admin.site.register(models.DrugBrands)
admin.site.register(models.AvailabeForms)
admin.site.register(models.Pharmacy)
admin.site.register(models.PharmacyInventory)
admin.site.register(models.UserProfiles)
admin.site.register(models.Hospital)
admin.site.register(models.HospitalDoctors)
admin.site.register(models.DoctorMeta)
admin.site.register(models.HospitalDoctorTiming)
admin.site.register(models.Appointment)
admin.site.register(models.Prescription)

