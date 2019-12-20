from django.urls import path
from .views import RegistrationView

app_name = 'registration'

urlpatterns = [

    path('registration/', RegistrationView.as_view(), name='registration'),
    #path('registration/validation/', RegistrationValidationView.as_view(), name='registration-validation'),

]
