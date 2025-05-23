from django.urls import path
from .views import client,client_activity,client_plan,client_progress,client_appointment,client_message,client_meal  # Import your views

urlpatterns = [
    path('', client, name='client'),  # URL for the homepage
    path('activity/', client_activity, name='activity'),  # URL for the homepage
    path('plan/', client_plan, name='plan'),  # URL for the homepage
    path('progress/', client_progress, name='progress'),  # URL for the homepage
    path('appointment/', client_appointment, name='appointment'),  # URL for the homepage
    path('message/', client_message, name='message'),  # URL for the homepage
    path('meal/', client_meal, name='meal'),  # URL for the homepage
]