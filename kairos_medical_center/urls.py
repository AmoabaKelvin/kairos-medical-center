from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("reception.urls"), name="reception"),
    path('accounts/', include('accounts.urls')),
    path('services/', include('services.urls')),
    path('management/', include('management.urls'))
]
