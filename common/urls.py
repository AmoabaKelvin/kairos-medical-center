from django.urls import path
from . import views

urlpatterns = [
    path("search/patient/", views.search_for_patient, name="search_view"),
    path("mail/", views.mail, name="send_mail"),
    path("update/mail/", views.edit_email_defaults, name="update_email"),
]
