from django.urls import path
from .views import client,client_activity,client_plan,client_progress,client_appointment,update_client,client_message,client_detail_view,client_meal,create_client,client_list,health_graph,get_graph_data,dietician_dashboard,weekly_report,client_view_graph # Import your views

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
    path('graph/', health_graph, name='health_graph'),
    path('get-graph-data/', get_graph_data, name='get_graph_data'),
    path('dietician/dashboard/', dietician_dashboard, name='dietician_dashboard'),
    path('client/<int:user_id>/', client_view_graph, name='client_view_graph'),
    path('dietician/weekly-report/<int:user_id>/', weekly_report, name='weekly_report'),


]