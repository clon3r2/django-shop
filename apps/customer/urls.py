from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserLogoutView, UserPasswordResetView, UserPasswordResetDoneView, \
    UserPasswordResetConfirmView, UserPasswordResetCompleteView, PanelView, UserAddressView, UserProfileView, \
    UserProfileEditView, UserProfileImageEditView, UserAddressCreateView, UserAddressDeleteView

app_name = 'customer'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('reset/', UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('panel/', PanelView.as_view(), name='panel'),
    path('address/<pk>', UserAddressView.as_view(), name='address-edit'),
    path('address/', UserAddressCreateView.as_view(), name='address-create'),
    path('address-delete/<pk>', UserAddressDeleteView.as_view(), name='address-delete'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/<pk>', UserProfileEditView.as_view(), name='profile-edit'),
    path('profile-image/<pk>', UserProfileImageEditView.as_view(), name='profile-image-edit'),

]
