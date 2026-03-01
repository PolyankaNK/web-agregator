from django.shortcuts import render, get_object_or_404
from core.models import ServiceCenter
from .models import ServiceCenter

def home(request):
    return render(request, 'core/home.html')

def service_list(request):
    query = request.GET.get('q')
    services = ServiceCenter.objects.all()
    if query:
        services = services.filter(name__icontains=query)
    context = {
        "services": services
    }
    return render(request, "core/service_list.html", context)

def service_detail(request, pk):
    service = get_object_or_404(ServiceCenter, pk=pk)
    return render(request, 'core/service_detail.html', {'service': service})