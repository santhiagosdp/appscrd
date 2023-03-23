from django import forms
from .models import Jogador, Time, Time_jogador, Pelada, Time_pelada

class JogadorForm(forms.ModelForm):
    class Meta:
        model = Jogador
        fields = ['nome', 'posicao', 'usuario']


class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['nome_time', 'cor_time']

class Time_jogadorForm(forms.ModelForm):
    class Meta:
        model = Time_jogador
        fields = ['jogador', 'time']


class PeladaForm(forms.ModelForm):
    class Meta:
        model = Pelada
        fields = ['tempo_pelada', 'quantidade_jogadores', 'valor_jogador','local']


class Time_peladaForm(forms.ModelForm):
    class Meta:
        model = Time_pelada
        fields = ['time', 'pelada', 'gols_time']