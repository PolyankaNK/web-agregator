from django.shortcuts import render
from core.models import ServiceCenter

def home(request):
    return render(request, 'core/home.html')

def service_list(request):
    services = ServiceCenter.objects.all()
    context = {
        "services": services
    }
    return render(request, "core/service_list.html", context)