from django.contrib import admin
from . import models


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)

class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'historico',)
    search_fields = ('nome',)

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone',)
    search_fields = ('nome',)

class ParticipacaoAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'projeto',)
    search_fields = ('pessoa',)


admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Projeto, ProjetoAdmin)
admin.site.register(models.Pessoa, PessoaAdmin)
admin.site.register(models.Participacao, ParticipacaoAdmin)