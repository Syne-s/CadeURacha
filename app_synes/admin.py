from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Jogo, CustomUser

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data', 'horario', 'max_jogadores', 'arena']
    search_fields = ['titulo', 'descricao']
    list_filter = ['data', 'arena']

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active', 'foto_perfil']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('foto_perfil',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('foto_perfil',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)