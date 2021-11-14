from django.urls import path 
from . import views

urlpatterns = [
    path('', views.add_patient, name='reception_home'),
    path('createnew/', views.create_receptionist, name='create_receptionist'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editinfo/<int:pk>', views.EditPatientInfoView.as_view(), name='edit_info')
]