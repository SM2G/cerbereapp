from django.http import HttpResponse
from .models import Employee

from django.shortcuts import render_to_response

def dashboard(request):
    return render_to_response("dashboard.html",{'all_employees': Employee.objects.all()})
