from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="service_list"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("account/", views.account_page, name="account"),
    path("services/<slug:slug>/reviews/create/", views.create_service_review, name="create_service_review"),
]