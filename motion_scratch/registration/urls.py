from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from app.registration.views import RegistrationView, RegistrationValidationView, TokenUserObtainView, PasswordResetView, \
    PasswordResetValidationView

app_name = 'registration'

urlpatterns = [

    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registration/validation/', RegistrationValidationView.as_view(), name='registration-validation'),

]
