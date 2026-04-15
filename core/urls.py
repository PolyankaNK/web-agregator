from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="service_list"),
    path("services/json/", views.service_centers_json, name="service_centers_json"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("account/", views.account_page, name="account"),
    path("services/<slug:slug>/reviews/create/", views.create_service_review, name="create_service_review"),
    path("services/<slug:slug>/favorite/toggle/", views.toggle_favorite, name="toggle_favorite"),
    path("favorites/", views.favorites_page, name="favorites_page"),
    path("api/favorites/", views.favorite_services, name="favorite_services"),
]