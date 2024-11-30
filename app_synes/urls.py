from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),  # Ou use 'register/' se preferir
]
