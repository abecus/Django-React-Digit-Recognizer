from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.api_overview, name="api-overview"),
    path("recognize/", views.recognize, name="recognize"),
]
