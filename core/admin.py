from django.contrib import admin
from .models import ServiceCenter, ServiceCategory, ServiceCenterImage, ServiceOffer, Favorite, ServiceReview, ServiceCenterSubmission


class ServiceCenterImageInline(admin.TabularInline):
    model = ServiceCenterImage
    extra = 1


class ServiceOfferInline(admin.TabularInline):
    model = ServiceOffer
    extra = 1


@admin.register(ServiceCenter)
class ServiceCenterAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "address", "phone", "working_hours", "created_at")
    search_fields = ("name", "city", "address", "phone")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceCenterImageInline, ServiceOfferInline]


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ServiceCenterImage)
class ServiceCenterImageAdmin(admin.ModelAdmin):
    list_display = ("service_center", "created_at")
    list_filter = ("created_at",)
    search_fields = ("service_center__name",)


@admin.register(ServiceOffer)
class ServiceOfferAdmin(admin.ModelAdmin):
    list_display = ("service_center", "title", "category", "price_from", "price_to", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("service_center__name", "title", "description")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "service_center", "created_at")
    search_fields = ("user__username", "service_center__name")

@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "service_center", "service_rating", "price_rating", "quality_rating", "created_at")
    list_filter = ("service_rating", "price_rating", "quality_rating", "created_at")
    search_fields = ("user__username", "service_center__name", "comment")

@admin.register(ServiceCenterSubmission)
class ServiceCenterSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "city", "district", "created_at")
    search_fields = ("name", "address", "user__username")
    list_filter = ("city", "district", "created_at")