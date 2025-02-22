from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Jogo, CustomUser

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data', 'horario', 'arena']
    search_fields = ['titulo', 'descricao']
    list_filter = ['data', 'arena']

    # Add verbose names for the model
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        return perms
    
    class Meta:
        verbose_name = 'Racha'
        verbose_name_plural = 'Rachas'

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active', 'foto_perfil']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('foto_perfil',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('foto_perfil',)}),
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

admin.site.register(CustomUser, CustomUserAdmin)