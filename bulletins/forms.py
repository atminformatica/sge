from django import forms
from django.forms import inlineformset_factory
from .models import Boletim, BoletimEnvolvimento, Envolvido
from django.core.exceptions import ObjectDoesNotExist

from datetime import date

class BoletimForm(forms.ModelForm):
    data_hora_inicio = forms.DateTimeField(
        label='Data e Hora início',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'max':"2100-12-31 00:00"},
        ),
        required=False
    )

    data_hora_termino = forms.DateTimeField(
        label='Data e Hora término',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'max':"2100-12-31 00:00"},
        ),
        required=False
    )

    class Meta:
        model = Boletim
        fields = '__all__'
        widgets = {
            # Define o campo 'created_at' como readonly
            'created_at': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'id':
                field.widget.attrs['class'] = 'form-control form-control-sm'

    def clean_data_hora_inicio(self):
        data_hora_inicio = self.cleaned_data.get('data_hora_inicio')
        if data_hora_inicio is not None:
            data_inicio = data_hora_inicio.date()
            today = date.today()
            min_date = date(2025, 1, 1)

            if data_inicio:
                if data_inicio > today:
                    raise forms.ValidationError('A data de início não pode ser futura.')
                if data_inicio < min_date:
                    raise forms.ValidationError('A data de início não pode ser anterior a 01/01/2025.')
            
        else:
            pass

        return data_hora_inicio
    
    def clean_data_hora_termino(self):
        data_hora_termino = self.cleaned_data.get('data_hora_termino')
        if data_hora_termino is not None:
            data_termino = data_hora_termino.date()
            today = date.today()
            min_date = date(2025, 1, 1)

            if data_termino:
                if data_termino > today:
                    raise forms.ValidationError('A data de término não pode ser futura.')
                if data_termino < min_date:
                    raise forms.ValidationError('A data de término não pode ser anterior a 01/01/2025.')
        else:
            pass       

        return data_hora_termino
    

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
    envolvido_naturalidade = forms.CharField(label='Naturalidade', max_length=100, required=False)
    envolvido_datanascimento = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date','max':"2100-12-31"},
            format='%Y-%m-%d', # Formato para exibição inicial e widget            
        ),
        input_formats=['%Y-%m-%d'], # Formatos aceitos na entrada do usuário
        required=False,
    )
    envolvido_endereco = forms.CharField(label='Endereço', max_length=255, required=False)
    envolvido_numero = forms.CharField(label='Numero',max_length=20, required=False)
    envolvido_bairro = forms.CharField(label='Bairro',max_length=100, required=False)
    envolvido_cidade = forms.CharField(label='Cidade',max_length=100, required=False)
    envolvido_uf = forms.CharField(label='UF',max_length=2, required=False)
    envolvido_cep = forms.CharField(label='CEP',max_length=10, required=False)
    envolvido_telefone = forms.CharField(label='Telefone',max_length=20, required=False)
    envolvido_estadocivil = forms.CharField(label='Estado Civil',max_length=50, required=False)
    envolvido_cpf = forms.CharField(label='CPF',max_length=14, required=False)
    envolvido_identidade = forms.CharField(label='RG',max_length=20, required=False)
    envolvido_profissao = forms.CharField(label='Profissão',max_length=100, required=False)
    envolvido_email = forms.EmailField(label='Email', required=False)
    envolvido_escolaridade = forms.CharField(label='Escolaridade',max_length=100, required=False)
    
    class Meta:
        model = BoletimEnvolvimento
        fields = ['tipo_envolvimento']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'id':
                field.widget.attrs['class'] = 'form-control form-control-sm'
        
        # Se uma instância do BoletimEnvolvimento for fornecida, preencha os campos do Envolvido
        if self.instance:
            try:
                envolvido = self.instance.envolvido
                self.initial['envolvido_nome'] = envolvido.nome
                self.initial['envolvido_naturalidade'] = envolvido.naturalidade
                self.initial['envolvido_datanascimento'] = envolvido.datanascimento
                self.initial['envolvido_endereco'] = envolvido.endereco
                self.initial['envolvido_numero'] = envolvido.numero
                self.initial['envolvido_bairro'] = envolvido.bairro
                self.initial['envolvido_cidade'] = envolvido.cidade
                self.initial['envolvido_uf'] = envolvido.uf
                self.initial['envolvido_cep'] = envolvido.cep
                self.initial['envolvido_telefone'] = envolvido.telefone
                self.initial['envolvido_estadocivil'] = envolvido.estadocivil
                self.initial['envolvido_cpf'] = envolvido.cpf
                self.initial['envolvido_identidade'] = envolvido.identidade
                self.initial['envolvido_profissao'] = envolvido.profissao
                self.initial['envolvido_email'] = envolvido.email
                self.initial['envolvido_escolaridade'] = envolvido.escolaridade
            except ObjectDoesNotExist:
                # Ocorre quando um BoletimEnvolvimento não tem um Envolvido relacionado.
                # Apenas ignore a exceção, os campos extras ficarão em branco.
                pass

    def clean_envolvido_datanascimento(self):
        data_nascimento = self.cleaned_data.get('envolvido_datanascimento')
        today = date.today()
        min_date = date(1900, 1, 1)

        if data_nascimento:
            if data_nascimento > today:
                raise forms.ValidationError('A data de nascimento não pode ser futura.')
            if data_nascimento < min_date:
                raise forms.ValidationError('A data de nascimento não pode ser anterior a 01/01/1900.')
        
        return data_nascimento
    
    def save2(self, commit=True):
        # Apenas salva o BoletimEnvolvimento; 
        # O objeto `envolvido` já foi atribuído na view
        return super().save(commit=commit)

    def save(self, commit=True):
        envolvido_data = {
            'nome': self.cleaned_data['envolvido_nome'],
            'naturalidade' : self.cleaned_data['envolvido_naturalidade'],
            'datanascimento' : self.cleaned_data['envolvido_datanascimento'],
            'endereco': self.cleaned_data['envolvido_endereco'],
            # Adicione os outros campos aqui
            'numero': self.cleaned_data['envolvido_numero'],
            'bairro': self.cleaned_data['envolvido_bairro'],
            'cidade': self.cleaned_data['envolvido_cidade'],
            'uf': self.cleaned_data['envolvido_uf'],
            'cep': self.cleaned_data['envolvido_cep'],
            'telefone': self.cleaned_data['envolvido_telefone'],
            'estadocivil': self.cleaned_data['envolvido_estadocivil'],
            'cpf': self.cleaned_data['envolvido_cpf'],
            'identidade': self.cleaned_data['envolvido_identidade'],
            'profissao': self.cleaned_data['envolvido_profissao'],
            'email': self.cleaned_data['envolvido_email'],
            'escolaridade': self.cleaned_data['envolvido_escolaridade'],
        }
        # envolvido = Envolvido.objects.create(**envolvido_data)
        envolvido = getattr(self.instance, 'envolvido', None)
        print(">>> Salvando BoletimEnvolvimentoForm")
        print(">>> ID da instância:", self.instance.pk)
        print(">>> Envolvido existente:", getattr(self.instance, 'envolvido', None))

        if envolvido and envolvido.pk:
            print(">>> Atualizando Envolvido existente")
            for field, value in envolvido_data.items():
                print(f" - {field}: {getattr(envolvido, field)} -> {value}")
                setattr(envolvido, field, value)

            if commit:
                envolvido.save()
                print(">>> Envolvido salvo:", envolvido.pk)
        else:
            # Cria novo se não houver
            envolvido = Envolvido.objects.create(**envolvido_data)

            
            self.instance.envolvido = envolvido
            instance = super().save(commit=commit)
            return instance  # <-- ESSENCIAL

BoletimEnvolvimentoFormSet = inlineformset_factory(
    Boletim,
    BoletimEnvolvimento,
    form=BoletimEnvolvimentoForm,
    extra=1,  # número de forms vazios adicionais
    can_delete=True
)
