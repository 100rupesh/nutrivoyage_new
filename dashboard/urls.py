from django.urls import path
from .views import dashboard  # Import your views

urlpatterns = [
    path('', dashboard, name='homepage'),  # URL for the homepage
    # path('client/', client, name='client'),  # URL for the homepage
]