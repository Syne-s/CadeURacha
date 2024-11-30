from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('app_synes.urls')),  # Incluindo as URLs do app_synes
]
