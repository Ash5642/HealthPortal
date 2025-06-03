from django.shortcuts import render
import re
# Create your views here.
def MainPage(request):
    return render(request, 'mainpage.html')
def DoctorPage(request):
    return render(request, 'DoctorPage.html')