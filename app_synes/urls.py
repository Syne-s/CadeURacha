from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import cadastrar_jogo, criar_reserva, listar_jogos, listar_reservas

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
    path('reservar/', criar_reserva, name='criar_reserva'),
    path('reservas/', listar_reservas, name='listar_reservas'),
    path('reservas/editar/<int:id>/', views.editar_reserva, name='editar_reserva'),  # Adicionada
    path('reservas/excluir/<int:id>/', views.excluir_reserva, name='excluir_reserva'),  # Adicionada
    path('jogos/', listar_jogos, name='listar_jogos'),
    path('jogos/editar/<int:id>/', views.editar_jogo, name='editar_jogo'),  # Adicionada
    path('jogos/excluir/<int:id>/', views.excluir_jogo, name='excluir_jogo'),  # Adicionada
    path('listar_todos_jogos/', views.listar_todos_jogos, name='listar_todos_jogos'),  # Adicionada
    path('listar_todas_reservas/', views.listar_todas_reservas, name='listar_todas_reservas'),  # Adicionada
    path('search/', views.search, name='search'),
]
