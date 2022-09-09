from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from entrypoints.rest_server.account.views import CustomerLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomerLoginView.as_view(), name='customer-login')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

