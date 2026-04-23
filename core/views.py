from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceCenter, Favorite, ServiceReview, KYIV_DISTRICT_CHOICES
from .forms import ServiceReviewForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ServiceReviewCreateSerializer, FavoriteSerializer, ServiceCenterListSerializer, ServiceCenterMapSerializer
from django.db.models import Count, Avg, F, FloatField, ExpressionWrapper, Q


def home(request):
    service_count = ServiceCenter.objects.count()
    review_count = ServiceReview.objects.count()

    average_rating_data = ServiceReview.objects.annotate(
        total_rating=ExpressionWrapper(
            (F("service_rating") + F("price_rating") + F("quality_rating")) / 3.0,
            output_field=FloatField()
        )
    ).aggregate(avg_rating=Avg("total_rating"))

    average_rating = average_rating_data["avg_rating"] or 0

    context = {
        "service_count": service_count,
        "review_count": review_count,
        "average_rating": round(average_rating, 1),
    }

    return render(request, "core/home.html", context)

def service_list(request):
    query = request.GET.get("q", "")
    district = request.GET.get("district", "")

    services = ServiceCenter.objects.all()

    if query:
        services = services.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(description__icontains=query)
        )

    if district:
        services = services.filter(district=district)

    context = {
        "services": services,
        "query": query,
        "selected_district": district,
        "district_choices": KYIV_DISTRICT_CHOICES,
    }

    return render(request, "core/service_list.html", context)


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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, slug):
    service = get_object_or_404(ServiceCenter, slug=slug)

    favorite = Favorite.objects.filter(
        user=request.user,
        service_center=service
    ).first()

    if favorite:
        favorite.delete()
        return Response({
            "status": "removed",
            "message": "Сервіс видалено з обраного."
        }, status=status.HTTP_200_OK)

    Favorite.objects.create(
        user=request.user,
        service_center=service
    )

    return Response({
        "status": "added",
        "message": "Сервіс додано в обране."
    }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def favorite_services(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("service_center")
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def service_centers_json(request):
    services = ServiceCenter.objects.all()
    serializer = ServiceCenterListSerializer(services, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def favorites_page(request):
    return render(request, "core/favorites.html")

@api_view(["GET"])
def service_centers_map_json(request):
    services = ServiceCenter.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    serializer = ServiceCenterMapSerializer(services, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)