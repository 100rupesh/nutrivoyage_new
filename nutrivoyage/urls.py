from django.contrib import admin
from django.urls import path, include  # include is used to include app URLs
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),  # Include the app's URL configuration
    path('accounts/', include('accounts.urls')),
    path('clients/', include('clients.urls')),
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
]