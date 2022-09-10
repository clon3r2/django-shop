from django.urls import path
from rest_framework.routers import DefaultRouter

from entrypoints.rest_server.account.views import CustomerLoginView, CustomerRegisterView

router = DefaultRouter()


urlpatterns = [
    path('login/', CustomerLoginView.as_view(), name='customer-login'),
    path('register/', CustomerRegisterView.as_view(), name='customer-login'),

]
