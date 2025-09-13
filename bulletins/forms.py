from django import forms
from django.forms import inlineformset_factory
from .models import Boletim, BoletimEnvolvimento, Envolvido

class BoletimForm(forms.ModelForm):
    class Meta:
        model = Boletim
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'id':
                field.widget.attrs['class'] = 'form-control'

class EnvolvidoForm(forms.ModelForm):
    class Meta:
        model = Envolvido
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'id':
                field.widget.attrs['class'] = 'form-control'


class BoletimEnvolvimentoForm(forms.ModelForm):
    envolvido_nome = forms.CharField(label='Nome', max_length=255)
    envolvido_naturalidade = forms.CharField(label='Naturalidade', max_length=100)
    envolvido_datanascimento = forms.DateField(label='Data de Nascimento', required=False )
    envolvido_endereco = forms.CharField(label='Endereço', max_length=255)
    # Adicione aqui todos os campos que você quer do Envolvido

    class Meta:
        model = BoletimEnvolvimento
        fields = ['tipo_envolvimento']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'id':
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        envolvido_data = {
            'nome': self.cleaned_data['envolvido_nome'],
            'naturalidade' : self.cleaned_data['envolvido_naturalidade'],
            'datanascimento' : self.cleaned_data['envolvido_datanascimento'],
            'endereco': self.cleaned_data['envolvido_endereco'],
            # Adicione os outros campos aqui
        }
        envolvido = Envolvido.objects.create(**envolvido_data)
        self.instance.envolvido = envolvido
        return super().save(commit=commit)
