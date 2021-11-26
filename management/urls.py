from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="management"),
    path("summary/", views.days_summary, name="summary"),
    path('workers/', views.get_current_workers, name='show_workers'),
]
