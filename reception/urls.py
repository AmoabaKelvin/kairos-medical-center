from django.urls import path 
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('reception/', views.ReceptionHomeView.as_view(), name='reception_home'),
    path('createnew/', views.create_receptionist, name='create_receptionist'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('info/<int:pk>', views.PatientDetailAndEditView.as_view(), name='info'),
    path('search/', views.search_for_patient, name='search_view'),
]