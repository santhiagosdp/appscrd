from django.contrib import admin
from .models import Jogador, AuxiliarDesfazer, Pelada, Time, Time_jogador, Time_pelada, Feedback

# ModelAdmin para Jogador
class JogadorAdmin(admin.ModelAdmin):
    list_display = ('usuario','habil', 'nome', 'posicao')
admin.site.register(Jogador, JogadorAdmin)


class AuxiliarDesfazerAdmin(admin.ModelAdmin):
    list_display = ('usuario','habil', 'nome', 'posicao')
admin.site.register(AuxiliarDesfazer, AuxiliarDesfazerAdmin)

class PeladaAdmin(admin.ModelAdmin):
    list_display = ('usuario','habil', 'tempo_pelada', 'quantidade_jogadores', 'corTime01', 'corTime02')
admin.site.register(Pelada, PeladaAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('usuario','habil', 'nome', 'telefone', 'mensagem')
admin.site.register(Feedback, FeedbackAdmin)



admin.site.register(Time)
admin.site.register(Time_jogador)
admin.site.register(Time_pelada)


