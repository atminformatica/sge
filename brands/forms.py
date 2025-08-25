from django import forms
from . import models
from django.forms import inlineformset_factory, modelform_factory
from .models import Projeto, Participacao, Pessoa

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'data_inicio', 'historico']
        widgets = {
                'nome': forms.TextInput(attrs={'class': 'form-control'}),
                'data_inicio': forms.DateInput(attrs={'class': 'form-control'}),
                'historico': forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 4,
                })
        }
        labels = {
                'name': 'Nome',
                'historico': 'Historico',
        }

class ParticipacaoForm(forms.ModelForm):
    nome = forms.CharField(max_length=100, required=True)
    telefone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Participacao
        fields = ['nome', 'telefone', 'funcao']

    def save(self, commit=True, projeto=None):
        nome = self.cleaned_data.get('nome')
        telefone = self.cleaned_data.get('telefone')
        pessoa, _ = Pessoa.objects.get_or_create(nome=nome, telefone=telefone)
        self.instance.pessoa = pessoa
        if projeto:
            self.instance.projeto = projeto
        return super().save(commit=commit)

ParticipacaoFormSet = inlineformset_factory(
    Projeto,
    Participacao,
    form=ParticipacaoForm,
    fields=('nome', 'telefone', 'funcao'),
    extra=1,
    can_delete=True
)

class BrandForm(forms.ModelForm):
    class Meta:
        model = models.Brand
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            })
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
        }