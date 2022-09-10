from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter

from entrypoints.rest_server.account.views import CustomerLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include("entrypoints.rest_server.account.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

