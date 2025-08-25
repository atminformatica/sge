from django.db import models

from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    data_inicio = models.DateField()
    historico = models.TextField(blank=True, null=True)
    pessoas = models.ManyToManyField(Pessoa, through='Participacao')

    def __str__(self):
        return self.nome

class Participacao(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    funcao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pessoa.nome} - {self.funcao}"
    

class Brand(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    