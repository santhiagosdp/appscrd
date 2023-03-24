from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Jogador(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    habil = models.BooleanField(default=True)
    nome = models.CharField(max_length=100)
    posicao = models.IntegerField(default=0)
    is_disponivel = models.BooleanField(default=True)
    is_selecionado = models.BooleanField(default=False)

class Pelada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    habil = models.BooleanField(default=True)
    tempo_pelada = models.IntegerField(default=5)
    quantidade_jogadores = models.IntegerField(default=7)
    #valor_jogador = models.FloatField(default=10)
    #local = models.CharField(default='Society', max_length=50)

class Time(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    habil = models.BooleanField(default=True)
    nome_time = models.CharField(max_length=50)
    cores_choices = (
        ("green", "Verde"),
        ("yellow", "Amarelo"),
        ("blue", "Azul"),
        ("black", "Preto"),
        ("orange", "Laranja"),
        ("red", "Vermelho")
    )
    cor_time = models.CharField(max_length=6, choices=cores_choices, blank=False, null=False)

class Time_jogador(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    habil = models.BooleanField(default=True)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)


class Time_pelada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    habil = models.BooleanField(default=True)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE)
    gols_time = models.IntegerField(default=0)




