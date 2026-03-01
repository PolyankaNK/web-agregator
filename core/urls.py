from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="service_list"),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
]