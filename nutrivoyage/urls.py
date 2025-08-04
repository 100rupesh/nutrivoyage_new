from django.contrib import admin
from django.urls import path, include  # include is used to include app URLs
from django.contrib.auth import views as auth_views
from accounts.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),  # Include the app's URL configuration
    path('accounts/', include('accounts.urls')),
    path('client/', include('clients.urls')),
    path('appointment/', include('appointments.urls')),
    path('', login_view, name='login'),
]