from django.db import models
from django.contrib.auth.models import User


# Create your models here.

PATIENT, DOCTOR, PHARMACIST = range(3)
UserType = (
    (PATIENT, 'PATIENT'),
    (DOCTOR, 'DOCTOR'),
    (PHARMACIST, 'PHARMACIST'),
)

class UserProfiles(models.Model):
    User = models.OneToOneField(User, related_name="Profile", on_delete=models.CASCADE)
    Image = models.ImageField(null=True, blank=True, upload_to = 'images/users')
    Name = models.CharField(max_length=64)
    BirthDate = models.DateField(auto_now_add=False)
    Type = models.IntegerField(
        choices=UserType,
        verbose_name="User type",
        null=False,
        blank=False
    )
    def __str__(self): 
         return self.Name +"("+str(self.Type)+")"

class Visits(models.Model):
    Patient = models.ForeignKey(UserProfiles, related_name='DoctorVisits', on_delete=models.CASCADE)
    Doctor = models.ForeignKey(UserProfiles, related_name = 'PatientVisits', on_delete=models.CASCADE)

class Drug(models.Model):
    Name = models.CharField(max_length=60)
    Structure = models.ImageField(null=True, blank=True)
    Description = models.CharField(max_length=512)
    Uses = models.CharField(max_length = 2048, null=True, blank=True)
    SideEffects = models.CharField(max_length = 2048, null=True, blank=True)
    Mechanism = models.CharField(max_length = 2048, null=True, blank=True)
    IsOral = models.BooleanField(default=True)
    IsInjected = models.BooleanField(default=True)
    IsPatch = models.BooleanField(default=True)
    def __str__(self): 
         return self.Name

class DrugBrands(models.Model):
    Image = models.ImageField(null=True, blank=True, upload_to='images/brands')
    GenericDrug = models.ForeignKey(Drug, related_name = "Brands", on_delete=models.CASCADE)
    Name = models.CharField(max_length=120)
    Manafacturer = models.CharField(max_length=128)
    Price = models.IntegerField(null=True, blank=True)
    def __str__(self): 
         return self.Name

TABLET_IR, TABLET_SR, SYRUP, SUPPOSITORY, IV, PATCH = range(6)
FormType = (
    (TABLET_IR, 'TABLET_IR'),
    (TABLET_SR, 'TABLET_SR'),
    (SYRUP, 'SYRUP'),
    (SUPPOSITORY, 'SUPPOSITORY'),
    (IV, 'IV'),
    (PATCH, 'PATCH'),

)

class AvailabeForms(models.Model):
    Name = models.CharField(max_length = 64, null=True, blank=True)
    Brand = models.ForeignKey(DrugBrands, related_name="Forms", on_delete=models.CASCADE)
    Form = models.IntegerField(
        choices=FormType,
        verbose_name="FormType",
        null=False,
        blank=False
    )
    Dosage = models.IntegerField(null=False, blank=False)
    Price = models.IntegerField(null=True, blank=True)
    Unit = models.CharField(max_length = 100)
    Quantity = models.IntegerField(null=True, blank=True)
    def __str__(self): 
         return self.Name +"("+self.Brand.Name+")"

class AvailabeTests(models.Model):
    Name = models.CharField(max_length=20)
    ReferenceAverage = models.IntegerField()
    ReferenceLow = models.IntegerField()
    ReferenceHigh = models.IntegerField()

class Hospital(models.Model):
    Name = models.CharField(max_length=64)
    Location = models.CharField(max_length=512)
    Lat = models.FloatField()
    Lon = models.FloatField()
    Website = models.URLField(null=True, blank=True)

class HospitalDoctors(models.Model):
    Doctor = models.ForeignKey(UserProfiles, related_name="Hospitals", on_delete=models.CASCADE)
    Hospital = models.ForeignKey(Hospital, related_name="Doctors", on_delete=models.CASCADE)
    Description = models.CharField(max_length=64)
    CurrentlyActive = models.BooleanField(default=False)
    Price = models.IntegerField(default=100)
    AllowVirtual = models.BooleanField(default=True)
    SlotLength = models.IntegerField(default=10)
    SatStart = models.TimeField(auto_now_add=False, null=True, blank=True)
    SatEnd = models.TimeField(auto_now_add=False, null=True, blank=True)
    SunStart = models.TimeField(auto_now_add=False, null=True, blank=True)
    SunEnd = models.TimeField(auto_now_add=False, null=True, blank=True)
    MonStart = models.TimeField(auto_now_add=False, null=True, blank=True)
    MonEnd = models.TimeField(auto_now_add=False, null=True, blank=True)
    TueStart = models.TimeField(auto_now_add=False, null=True, blank=True)
    TueEnd = models.TimeField(auto_now_add=False, null=True, blank=True)
    WedStart = models.TimeField(auto_now_add=False, null=True, blank=True)
    WedEnd = models.TimeField(auto_now_add=False, null=True, blank=True)
    ThuStart = models.TimeField(auto_now_add=False, null=True, blank=True)
    ThuEnd = models.TimeField(auto_now_add=False, null=True, blank=True)
    FriStart = models.TimeField(auto_now_add=False, null=True, blank=True)
    FriEnd = models.TimeField(auto_now_add=False, null=True, blank=True)

WDAY, MDAY, ALT= range(3)
VisitTiimeType = (
    (WDAY, 'TABLET_IR'),
    (MDAY, 'TABLET_SR'),
    (ALT, 'SYRUP'),
)

class HospitalDoctorTiming(models.Model):
    HospitalDoctor = models.ForeignKey(HospitalDoctors, related_name = 'Timings', on_delete = models.CASCADE)
    StartTime = models.TimeField(auto_now_add = False, null=False, blank=False)
    EndTime = models.TimeField(auto_now_add = False, null=False, blank=False)
    WeekDayCode = models.IntegerField(default = 0)
    Form = models.IntegerField(
        choices=VisitTiimeType,
        verbose_name="VisitTimeType",
        null=False,
        blank=False
    )

class DoctorMeta(models.Model):
    Doctor = models.OneToOneField(UserProfiles, null=False, blank=False, related_name = 'MetaInfo', on_delete = models.CASCADE)
    Speciality = models.CharField(max_length = 128, blank=True, null=True)
    Quals = models.CharField(max_length=128, blank=True, null=True)
    Rating = models.IntegerField(null=True, blank=True)
    Ratings = models.IntegerField(null=True, blank=True)
    Experience = models.IntegerField(default = 0)

class TestCenters(models.Model):
    Name = models.CharField(max_length=128)
    Location = models.CharField(max_length=512)
    Lat = models.FloatField()
    Lon = models.FloatField()
    Website = models.URLField(null=True, blank=True)
    AssociatedHospital = models.OneToOneField(Hospital, related_name = "TestCenter", null=True, blank=True, on_delete=models.CASCADE)

class TestCenterTests(models.Model):
    TestCenter = models.ForeignKey(TestCenters, related_name="Tests", on_delete=models.CASCADE)
    Test = models.ForeignKey(AvailabeTests, related_name="TestCenters", on_delete=models.CASCADE)
    Pricing = models.IntegerField(null=True, blank=True)
    Description = models.CharField(max_length=256)

class Devices(models.Model):
    Name = models.CharField(max_length=64)
    User = models.ForeignKey(UserProfiles, null=False, blank=False, related_name="Devices", on_delete = models.CASCADE)
    Added = models.DateTimeField(auto_now_add=True)
    UserHasGivenPermission = models.BooleanField(default=False)

class DevicePermissions(models.Model):
    Test = models.ForeignKey(AvailabeTests, related_name = "DevicesAuthorized", on_delete = models.CASCADE)
    Device = models.ForeignKey(Devices, related_name="Permissions", on_delete=models.CASCADE)
    Granted = models.BooleanField(default=False)


PENDING, COMPLETE = range(2)
TestStatuses = (
    (PENDING, 'PENDING'),
    (COMPLETE, 'COMPLETE'),
)

class TestResult(models.Model):
    Patient = models.ForeignKey(UserProfiles, related_name="TestResults",on_delete=models.CASCADE)
    Test = models.ForeignKey(AvailabeTests, related_name="Tests", on_delete=models.CASCADE)
    Value = models.IntegerField(null = True, blank=True)
    Time = models.DateTimeField(null = False, blank=False)
    Status = models.IntegerField(
        choices=TestStatuses,
        verbose_name="TestStatus",
        null=False,
        blank=False,
        default=PENDING
    )
    TestCenter = models.ForeignKey(TestCenters, null=True, blank=True, related_name='Results', on_delete = models.CASCADE)
    Device = models.ForeignKey(Devices, null=True, blank=True, related_name='Results', on_delete = models.CASCADE)

class Appointment(models.Model):
    Doctor = models.ForeignKey(HospitalDoctors, on_delete=models.CASCADE)
    Timing = models.ForeignKey(HospitalDoctorTiming, related_name = 'Appointments', on_delete = models.CASCADE)
    Patient = models.ForeignKey(UserProfiles , on_delete = models.CASCADE)
    Day = models.IntegerField(blank=True, null=True)
    DocHasConfirmed = models.BooleanField(default=False)

class Prescription(models.Model):
    Doctor = models.ForeignKey(Appointment, related_name="Prescriptions", on_delete=models.CASCADE)
    Drug = models.ForeignKey(AvailabeForms, related_name = "Prescriptions", on_delete=models.CASCADE)
    AllowSubstitutiions = models.BooleanField(default=True)
    Lenght = models.IntegerField()
    Quantity = models.IntegerField()
    Instructions = models.CharField(max_length=2048)

class RecommendTest(models.Model):
    Appointment = models.ForeignKey(Appointment, related_name="RecommmededTests", on_delete=models.CASCADE)
    Test = models.ForeignKey(AvailabeTests, related_name="RecommendedBy", on_delete = models.CASCADE)
    AutoForwardResults = models.BooleanField(default = True)

class Pharmacy(models.Model):
    Pharmacist = models.OneToOneField(UserProfiles, null=True, blank=True, related_name = 'Pharmacy', on_delete = models.CASCADE)
    Name = models.CharField(max_length=256, null=True, blank=True)
    Location = models.CharField(max_length=512)
    Image = models.ImageField(null=True, blank=True, upload_to='images/pharmacies')
    Lat = models.FloatField()
    Lon = models.FloatField()
    Website = models.URLField(null=True, blank=True)
    Address = models.CharField(max_length = 2048, null=True, blank=True)
    def __str__(self): 
         return self.Name

class PharmacyInventory(models.Model):
    Drug = models.ForeignKey(AvailabeForms, null=False, blank=True, on_delete = models.CASCADE)
    Price = models.IntegerField(null=True, blank=True)
    Pharmacy = models.ForeignKey(Pharmacy, null=False, blank=False, on_delete = models.CASCADE)
    Quantity = models.IntegerField(blank=True, null=True)