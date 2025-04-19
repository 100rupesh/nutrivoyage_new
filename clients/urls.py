from django.urls import path
from .views import client  # Import your views

urlpatterns = [
    path('', client, name='client'),  # URL for the homepage
    # path('client/', client, name='client'),  # URL for the homepage
]