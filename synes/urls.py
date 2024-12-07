from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),               # Admin
    path('', include('app_synes.urls')),           # Inclui as rotas do app
]
