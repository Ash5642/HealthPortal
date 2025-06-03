from django.urls import path
from .ViewFunctions import PatientPharmacy, PatientDoctor, Doctor, Auth
urlpatterns = [    
    path("pharmacy/drug/bybrand", PatientPharmacy.FindDrugBrand),
    path("pharmacy/drug/generic", PatientPharmacy.FindGenericDrug),
    path("pharmacy/drug/searchform", PatientPharmacy.SearchDrugFormLocations),
    path("pharmacy/drug/byform", PatientPharmacy.FindDrugForm),
    path("pharmacy/drug/search", PatientPharmacy.SearchDrug),
    path("pharmacy/drug/searchformname", PatientPharmacy.SearchDrugForm),
    path("pharmacy/view", PatientPharmacy.GetPharmacyInformation),
    path("pharmacy/view/stock", PatientPharmacy.GetPharmacyStock),

    path("doctor/view", PatientDoctor.GetDoctorPractices),
    path("doctor/filter", PatientDoctor.FilterDoctors),
    path("doctor/appointment", PatientDoctor.GetAppointment),
    path("doctor/listappointments", PatientDoctor.ListPatientAppointments),

    path("provider/upcoming", Doctor.GetUpcomingPatients),
    path("provider/appointments", Doctor.ManageAppointment),

    path('auth/register/regular', Auth.NormalRegistratiiion),
    path('auth/login/regular', Auth.NormalLogIn),

    path('auth/register/doctor', Auth.DoctorRegistration),
    path('auth/register/pharmacy', Auth.RegisterPharmacy),
]

