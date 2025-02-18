from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import cadastrar_racha, listar_jogos

urlpatterns = [
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('logar/', views.login_view, name='logar'),
    path('logout/', views.logout_view, name='logout'),
    path('detalhes_quadra/', views.teste, name='detalhes_quadra'),
    path('detalhes_quadra/<int:id>/', views.detalhes_quadra, name='detalhes_quadra'),
    path('test_jogo/', views.test_jogo, name='detalhes_jogo'),
    path('detalhes_racha/<int:id>/', views.detalhes_jogo, name='detalhes_jogo'),
    path('todos/', views.todos, name='todos'),
    path('', views.index, name='index'),
    path('mapa/', views.mapa_view, name='mapa'),
    path('cadastrar_quadra/', views.cadastrar_quadra, name='cadastrar_quadra'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('confirmar_exclusao_usuario/', views.confirmar_exclusao_usuario, name='confirmar_exclusao_usuario'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('cadastrar_racha/', cadastrar_racha, name='cadastrar_racha'),  # Adicionada
    path('listar_jogos/', listar_jogos, name='listar_jogos'),
    path('jogos/editar/<int:id>/', views.editar_jogo, name='editar_jogo'),  # Adicionada
    path('jogos/excluir/<int:id>/', views.excluir_jogo, name='excluir_jogo'),  # Adicionada
    path('listar_todos_jogos/', views.listar_todos_jogos, name='listar_todos_jogos'),
    path('search/', views.search, name='search'),
    path('confirmar-presenca/<int:id>/', views.confirmar_presenca, name='confirmar_presenca'),
    path('excluir-presenca/<int:id>/', views.excluir_presenca, name='excluir_presenca'),
    path('jogo/<int:jogo_id>/levar_bola/', views.levar_bola, name='levar_bola'),
    path('check_username/', views.check_username, name='check_username'),
    path('update_username/', views.update_username, name='update_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('toggle_presenca/', views.toggle_presenca, name='toggle_presenca'),
    path('toggle_levar_bola/', views.toggle_levar_bola, name='toggle_levar_bola'),
    path('buscar/', views.buscar, name='buscar'),
]
