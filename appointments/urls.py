from django.urls import path
from .views import create_appointment,appointment_list,appointment_detail_view,create_diet_plan,download_diet_pdf


urlpatterns = [
    path('create/', create_appointment, name='create_appointment'),
    path('', appointment_list, name='appointment_list'),
    path('detail/<int:appointment_id>/', appointment_detail_view, name='appointment_detail'),
    path('<int:appointment_id>/diet-plan/create/<int:diet_no>', create_diet_plan, name='create_diet_plan'),
    path('<int:appointment_id>/download-pdf/', download_diet_pdf, name='download_diet_pdf'),

]