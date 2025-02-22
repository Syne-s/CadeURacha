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

@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'endereco', 'cidade', 'estado', 'pais', 'status']
    search_fields = ['nome', 'endereco', 'cidade', 'estado', 'pais']
    list_filter = ['status', 'cidade', 'estado', 'pais']
    
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        return perms

    class Meta:
        verbose_name = 'Quadra'
        verbose_name_plural = 'Quadras'

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Adicionando pode_cadastrar_quadra no list_display
    list_display = ['username', 'email', 'is_staff', 'is_active', 'pode_cadastrar_quadra', 'is_superuser', 'foto_perfil']
    list_filter = ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions']
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
            user.is_staff = True  # Define como staff
            user.user_permissions.add(permission)
            user.save()  # Salva as alterações
    dar_permissao_quadra.short_description = "Dar permissão para cadastrar quadras"

    def remover_permissao_quadra(self, request, queryset):
        arena_content_type = ContentType.objects.get_for_model(Arena)
        permission = Permission.objects.get(
            codename='can_add_arena',
            content_type=arena_content_type,
        )
        for user in queryset:
            user.is_staff = False  # Remove status de staff
            user.user_permissions.remove(permission)
            user.save()  # Salva as alterações
    remover_permissao_quadra.short_description = "Remover permissão para cadastrar quadras"

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('foto_perfil',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('foto_perfil',)}),
    )

    def has_view_permission(self, request, obj=None):
        # Permite visualização para staff e usuários com permissão de cadastrar quadra
        return request.user.is_staff or request.user.has_perm('app_synes.can_add_arena')

    def has_change_permission(self, request, obj=None):
        # Apenas superuser pode editar
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Apenas superuser pode deletar
        return request.user.is_superuser

    def has_add_permission(self, request):
        # Apenas superuser pode adicionar
        return request.user.is_superuser

    def get_readonly_fields(self, request, obj=None):
        # Se não for superuser, todos os campos são somente leitura
        if not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Se não for superuser, oculta os superusers da listagem
        if not request.user.is_superuser:
            qs = qs.filter(is_superuser=False)
        return qs

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['username', 'email', 'is_staff', 'is_active', 'pode_cadastrar_quadra', 'is_superuser', 'foto_perfil']
        else:
            # Remove is_superuser, email e foto_perfil da listagem para não superusers
            return ['username', 'is_staff', 'is_active', 'pode_cadastrar_quadra']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

admin.site.register(CustomUser, CustomUserAdmin)