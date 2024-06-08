from django.db import models
from django.core.exceptions import ValidationError
import re

def validacao_endereco(regiao):
    pattern = "^[A-Z]{3}\d{2}$"
    if not re.match(pattern=pattern, string=regiao):
        raise ValidationError("Este campo deve conter duas letras, seguidas de dois números, exemplo: 'XXX99'.")

# Create your models here.
class Regiao(models.Model):
    regiao = models.CharField(max_length=65, unique=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "regiões"

    def __str__(self):
        return str(self.id) + " - " + str(self.regiao)
    

class Genero(models.Model):
    genero = models.CharField(max_length=65, unique=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "gênero"

    def __str__(self):
        return str(self.id) + " - " + str(self.genero)

class Endereco(models.Model):
    # código, nivel, descrição, gênero, tema
    codigo = models.CharField(max_length=5, validators=[validacao_endereco])
    descricao = models.CharField(max_length=300, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Endereço"

    def __str__(self):
        return str(self.id) + " - " + str(self.codigo)

class Autor(models.Model):
    prim_nome = models.CharField(max_length=65)
    ult_nome = models.CharField(max_length=65)
    nacionalidade = models.CharField(max_length=65, blank=True, null=True, default="")
    regiao = models.ForeignKey(Regiao, on_delete=models.SET_DEFAULT, default=2)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "autores"
    
    def __str__(self):
        return str(self.id) + " - " + str(self.prim_nome) + " " + str(self.ult_nome)

class Livro(models.Model):
    titulo = models.CharField(max_length=300, unique=True)
    editora = models.CharField(max_length=300, blank=True, null=True)
    autor = models.ForeignKey(Autor, on_delete=models.SET_DEFAULT, default=1)
    genero = models.ForeignKey(Genero, on_delete=models.SET_DEFAULT, default=1)
    tema = models.CharField(max_length=600, blank=True, null=True)
    lendo = models.BooleanField(default=False)
    lido = models.BooleanField(default=False)
    data_leitura = models.DateField(blank=True, null=True)
    leria_de_novo = models.BooleanField(default=False)
    notas = [(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5"),(6,"6"),(7,"7"),(8,"8"),(9,"9"),(10,"10")]
    classificacao = models.IntegerField(choices=notas, blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, blank=True, null=True)
    data_compra = models.DateField()
    regiao = models.ForeignKey(Regiao, on_delete=models.SET_DEFAULT, default=2)
    comentario = models.TextField(blank=True, null=True)
    planejamento = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.titulo)
    
class Historico(models.Model):
    # Livro, Data Inicio, Data Fim, Terminou
    livro = models.ForeignKey(Livro, on_delete=models.DO_NOTHING)
    data_ini = models.DateTimeField()
    data_fim = models.DateTimeField(blank=True,null=True)
    terminou = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + " - " + str(self.livro.titulo)

class Anotacao(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.DO_NOTHING)
    data_inclusao = models.DateTimeField(auto_now_add=True)
    anotacao = models.TextField()
    def __str__(self):
        return str(self.id) + " - " + str(f"{self.anotacao[:20]}")
