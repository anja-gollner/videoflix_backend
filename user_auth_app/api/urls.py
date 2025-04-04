from django.urls import path
from .views import RegistrationView, LoginView, ActivationView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uid>/<token>/', ActivationView.as_view(), name='activate'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password/<str:uid>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
 