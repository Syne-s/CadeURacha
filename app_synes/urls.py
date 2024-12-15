from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),
    path('map/', views.map, name='map'),      
]
