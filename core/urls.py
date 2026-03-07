from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="service_list"),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("account/", views.account_page, name="account"),
]