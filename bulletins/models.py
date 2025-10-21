from django.db import models

class Boletim(models.Model):    
    data_hora_inicio = models.DateTimeField(blank=True, null=True)
    data_hora_termino = models.DateTimeField(blank=True, null=True)
    numero_bi = models.CharField(max_length=30)
    numero_bo = models.CharField(blank=True, null=True, max_length=30)
    classificacao = models.CharField(blank=True, null=True, max_length=100)
    destinatario = models.CharField(blank=True, null=True, max_length=255)
    historico = models.TextField(blank=True, null=True)
    relatornome = models.CharField(blank=True, null=True, max_length=255)
    relatordocumento = models.CharField(blank=True, null=True, max_length=50)
    destinatario = models.CharField(blank=True, null=True, max_length=255)
    autoridadenome = models.CharField(blank=True, null=True, max_length=255)
    autoridadedocumento = models.CharField(blank=True, null=True, max_length=50)
    endereco_dofato = models.CharField(blank=True, null=True, max_length=255)
    numero_dofato = models.CharField(blank=True, null=True, max_length=20)
    bairro_dofato = models.CharField(blank=True, null=True, max_length=100)
    orgao = models.CharField(blank=True, null=True, max_length=100)
    secao = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BO {self.numero_bo} - BI {self.numero_bi}"


class Envolvido(models.Model):
    nome = models.CharField(max_length=255)
    naturalidade = models.CharField(blank=True, null=True, max_length=100)
    datanascimento = models.DateField(blank=True, null=True)
    endereco = models.CharField(blank=True, null=True, max_length=255)
    numero = models.CharField(blank=True, null=True, max_length=20)
    bairro = models.CharField(blank=True, null=True, max_length=100)
    cidade = models.CharField(blank=True, null=True, max_length=100)
    uf = models.CharField(blank=True, null=True, max_length=2)
    cep = models.CharField(blank=True, null=True, max_length=10)
    telefone = models.CharField(blank=True, null=True, max_length=20)
    estadocivil = models.CharField(blank=True, null=True, max_length=50)
    cpf = models.CharField(blank=True, null=True, max_length=14)
    identidade = models.CharField(blank=True, null=True, max_length=20)
    profissao = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(blank=True, null=True, )
    escolaridade = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.nome


class BoletimEnvolvimento(models.Model):
    TIPOS_ENVOLVIMENTO = [
        ('SOLICITANTE', 'Solicitante'),
        ('VITIMA', 'Vítima'),
        ('AUTOR', 'Autor'),
        ('TESTEMUNHA', 'Testemunha'),
        ('SOLICITANTE_VITIMA', 'Solicitante/Vítima'),
        ('SOLICITANTE_AUTOR', 'Solicitante/Autor'),
        ('SOLICITANTE_TESTEMUNHA', 'Solicitante/Testemunha'),
    ]

    boletim = models.ForeignKey(Boletim, on_delete=models.CASCADE)
    envolvido = models.ForeignKey(Envolvido, on_delete=models.CASCADE)
    tipo_envolvimento = models.CharField(max_length=30, choices=TIPOS_ENVOLVIMENTO)

    def __str__(self):
        return f"{self.envolvido.nome} ({self.get_tipo_envolvimento_display()})"