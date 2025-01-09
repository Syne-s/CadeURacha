from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import cadastrar_jogo

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    path('map/', views.map_view, name='map'),
    path('cadastrar_arena/', views.cadastrar_arena, name='cadastrar_arena'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('confirm_delete_account/', views.confirm_delete_account, name='confirm_delete_account'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('cadastrar_jogo/', cadastrar_jogo, name='cadastrar_jogo'),
]
