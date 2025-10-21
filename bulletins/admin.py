from django.contrib import admin
from .models import Boletim, Envolvido, BoletimEnvolvimento

class BoletimEnvolvimentoInline(admin.TabularInline):
    model = BoletimEnvolvimento
    extra = 2  # Começa com dois formulários
    autocomplete_fields = ['envolvido']
    show_change_link = True
    can_delete = True

@admin.register(Boletim)
class BoletimAdmin(admin.ModelAdmin):
    list_display = ['numero_bi', 'numero_bo', 'data_hora_inicio', 'classificacao', 'orgao']
    search_fields = ['numero_bo', 'numero_bi', 'classificacao', 'destinatario']
    list_filter = ['classificacao', 'orgao', 'secao']
    inlines = [BoletimEnvolvimentoInline]

@admin.register(Envolvido)
class EnvolvidoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'cidade', 'uf', 'profissao']
    search_fields = ['nome', 'cpf', 'identidade', 'email']
    list_filter = ['cidade', 'uf', 'estadocivil', 'escolaridade']

@admin.register(BoletimEnvolvimento)
class BoletimEnvolvimentoAdmin(admin.ModelAdmin):
    list_display = ['boletim', 'envolvido', 'tipo_envolvimento']
    list_filter = ['tipo_envolvimento']
    autocomplete_fields = ['boletim', 'envolvido']