from django.contrib import admin
from .models import Jogo

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data', 'horario', 'max_jogadores', 'arena']
    search_fields = ['titulo', 'descricao']
    list_filter = ['data', 'arena']
