from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Jogo, CustomUser, Arena
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

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
    # Adicionando pode_cadastrar_quadra no list_display
    list_display = ['username', 'email', 'is_staff', 'is_active', 'pode_cadastrar_quadra', 'foto_perfil']
    list_filter = ['is_staff', 'is_active', 'groups', 'user_permissions']
    actions = ['dar_permissao_quadra', 'remover_permissao_quadra']
    
    # Método que verifica a permissão
    def pode_cadastrar_quadra(self, obj):
        return obj.has_perm('app_synes.can_add_arena')
    pode_cadastrar_quadra.short_description = 'Pode cadastrar quadra'
    pode_cadastrar_quadra.boolean = True  # Isso fará aparecer como ícone de check

    def dar_permissao_quadra(self, request, queryset):
        arena_content_type = ContentType.objects.get_for_model(Arena)
        permission = Permission.objects.get(
            codename='can_add_arena',
            content_type=arena_content_type,
        )
        for user in queryset:
            user.user_permissions.add(permission)
    dar_permissao_quadra.short_description = "Dar permissão para cadastrar quadras"

    def remover_permissao_quadra(self, request, queryset):
        arena_content_type = ContentType.objects.get_for_model(Arena)
        permission = Permission.objects.get(
            codename='can_add_arena',
            content_type=arena_content_type,
        )
        for user in queryset:
            user.user_permissions.remove(permission)
    remover_permissao_quadra.short_description = "Remover permissão para cadastrar quadras"

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