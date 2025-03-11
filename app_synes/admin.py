from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Jogo, CustomUser, Arena
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data', 'horario', 'arena', 'display_imagem']
    search_fields = ['titulo', 'descricao']
    list_filter = ['data', 'arena']

    # Add verbose names for the model
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        return perms
    
    class Meta:
        verbose_name = 'Racha'
        verbose_name_plural = 'Rachas'

    def display_imagem(self, obj):
        if obj.imagem:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="50" height="50" style="object-fit: cover;" /><br>Ver imagem</a>', obj.imagem.url, obj.imagem.url)
        return "Sem imagem"
    
    display_imagem.short_description = "Imagem do Racha"

@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'endereco', 'cidade', 'estado', 'pais', 'status', 'display_foto']
    search_fields = ['nome', 'endereco', 'cidade', 'estado', 'pais']
    list_filter = ['status', 'cidade', 'estado', 'pais']
    
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        return perms

    class Meta:
        verbose_name = 'Quadra'
        verbose_name_plural = 'Quadras'

    def display_foto(self, obj):
        if obj.foto_url:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="50" height="50" style="object-fit: cover;" /><br>Ver imagem</a>', obj.foto_url, obj.foto_url)
        elif obj.foto_quadra:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="50" height="50" style="object-fit: cover;" /><br>Ver imagem</a>', obj.foto_quadra.url, obj.foto_quadra.url)
        return "Sem imagem"
    
    display_foto.short_description = "Foto da Quadra"

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Adicionando pode_cadastrar_quadra no list_display
    list_display = ['username', 'email', 'is_staff', 'is_active', 'pode_cadastrar_quadra', 'is_superuser', 'foto_perfil', 'display_foto_perfil']
    list_filter = ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions']
    actions = ['dar_permissao_quadra', 'remover_permissao_quadra']
    
    # Método que verifica a permissão
    def pode_cadastrar_quadra(self, obj):
        return obj.is_superuser or obj.has_perm('app_synes.can_add_arena')
    pode_cadastrar_quadra.short_description = 'Pode cadastrar quadra'
    pode_cadastrar_quadra.boolean = True  # Isso fará aparecer como ícone de check

    def dar_permissao_quadra(self, request, queryset):
        arena_content_type = ContentType.objects.get_for_model(Arena)
        permission = Permission.objects.get(
            codename='can_add_arena',
            content_type=arena_content_type,
        )
        for user in queryset:
            if not user.is_superuser:  # não altera superusers
                user.is_staff = True
                user.user_permissions.add(permission)
                user.save()
    dar_permissao_quadra.short_description = "Dar permissão para cadastrar quadras"

    def remover_permissao_quadra(self, request, queryset):
        arena_content_type = ContentType.objects.get_for_model(Arena)
        permission = Permission.objects.get(
            codename='can_add_arena',
            content_type=arena_content_type,
        )
        for user in queryset:
            if not user.is_superuser:  # não altera superusers
                user.is_staff = False
                user.user_permissions.remove(permission)
                user.save()
    remover_permissao_quadra.short_description = "Remover permissão para cadastrar quadras"

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('foto_perfil', 'foto_url', 'levar_bola')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('foto_perfil', 'foto_url')}),
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
            return ['username', 'email', 'is_staff', 'is_active', 'pode_cadastrar_quadra', 'is_superuser', 'foto_perfil', 'display_foto_perfil']
        else:
            # Remove is_superuser, email e foto_perfil da listagem para não superusers
            return ['username', 'is_staff', 'is_active', 'pode_cadastrar_quadra']

    def get_list_display_links(self, request, list_display):
        # Se não for superuser, retorna None para remover todos os links
        if not request.user.is_superuser:
            return None
        # Se for superuser, mantém o comportamento padrão
        return super().get_list_display_links(request, list_display)

    def display_foto_perfil(self, obj):
        if obj.foto_url:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" /><br>Ver imagem</a>', obj.foto_url, obj.foto_url)
        elif obj.foto_perfil:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" /><br>Ver imagem</a>', obj.foto_perfil.url, obj.foto_perfil.url)
        return "Sem imagem"
    
    display_foto_perfil.short_description = "Foto de Perfil"

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

admin.site.register(CustomUser, CustomUserAdmin)