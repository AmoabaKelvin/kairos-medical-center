from django.urls import path

from . import views

urlpatterns = [
    path("", views.ReceptionHomeView.as_view(), name="reception_home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("info/<int:pk>", views.PatientDetailAndEditView.as_view(), name="info"),
]
