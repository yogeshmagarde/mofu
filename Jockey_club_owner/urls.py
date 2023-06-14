from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", views.Jockey_club_owners, name="Jockey_club_owner"),
    path("Register/", Register.as_view(), name="Register"),
    path("getallaudiojockey/<jockey_owner_id>/", AudioJockeyList.as_view(), name="getallaudiojockey"),
]
