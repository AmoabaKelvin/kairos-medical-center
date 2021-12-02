from django.contrib import admin
from django.urls import path, include
from common.views import homepage
from django.conf.urls import static
from django.conf import settings

urlpatterns = [
    path('', homepage, name='homepage'),
    path("admin/", admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("reception/", include("reception.urls"), name="reception"),
    path('accounts/', include('accounts.urls')),
    path('services/', include('services.urls')),
    path('management/', include('management.urls')),
    path('common/', include('common.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
