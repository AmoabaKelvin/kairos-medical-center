from django.urls import path

from .views import SendMailForm, mail
urlpatterns = [
    # path('mail/', SendMailForm.as_view(), name='send_mail'),
    path('mail/', mail, name='send_mail'),
]