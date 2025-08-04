from django.urls import path
from .views import client,client_activity,client_plan,client_progress,client_appointment,update_client,client_message,client_detail_view,client_meal,create_client,client_list # Import your views

urlpatterns = [
    path('', client, name='client'),  # URL for the homepage
    path('create-client/', create_client, name='create_client'),
    path('activity/', client_activity, name='activity'),  # URL for the homepage
    path('plan/', client_plan, name='plan'),  # URL for the homepage
    path('progress/', client_progress, name='progress'),  # URL for the homepage
    path('appointment/', client_appointment, name='appointment'),  # URL for the homepage
    path('message/', client_message, name='message'),  # URL for the homepage
    path('meal/', client_meal, name='meal'),  # URL for the homepage
    path('client_list/', client_list, name='client_list'),  # URL for the homepage
    path('detail/<int:client_id>/', client_detail_view, name='client_detail'),
    path('edit/<int:client_id>/', update_client, name='update_client'),
]