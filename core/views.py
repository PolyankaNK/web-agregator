from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceCenter
from .forms import ServiceReviewForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ServiceReviewCreateSerializer

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

from django.shortcuts import render, get_object_or_404
from .models import ServiceCenter


def home(request):
    query = request.GET.get("q", "")
    
    services = ServiceCenter.objects.all()

    if query:
        services = services.filter(name__icontains=query)

    return render(request, "core/home.html", {
        "services": services,
        "query": query
    })


def service_list(request):
    query = request.GET.get("q", "")
    services = ServiceCenter.objects.all()

    if query:
        services = services.filter(name__icontains=query)

    return render(request, "core/service_list.html", {
        "services": services,
        "query": query
    })


def service_detail(request, slug):
    service = get_object_or_404(ServiceCenter, slug=slug)
    images = service.images.all()
    offers = service.offers.filter(is_active=True)
    reviews = service.reviews.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        review_form = ServiceReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.service_center = service
            review.user = request.user
            review.save()
            return redirect("service_detail", slug=service.slug)
    else:
        review_form = ServiceReviewForm()

    return render(request, "core/service_detail.html", {
        "service": service,
        "images": images,
        "offers": offers,
        "reviews": reviews,
        "review_form": review_form,
    })

def login_page(request):
    return render(request,"accounts/login.html")

def register_page(request):
    return render(request,"accounts/register.html")

def account_page(request):
    return render(request,"accounts/account.html")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_service_review(request, slug):
    service = get_object_or_404(ServiceCenter, slug=slug)

    serializer = ServiceReviewCreateSerializer(data=request.data)
    if serializer.is_valid():
        review = serializer.save(
            service_center=service,
            user=request.user
        )

        return Response({
            "message": "Відгук успішно додано.",
            "review_id": review.id
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)