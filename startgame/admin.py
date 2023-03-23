from django.contrib import admin
from .models import Jogador, Pelada, Time, Time_jogador, Time_pelada

admin.site.register(Jogador)
admin.site.register(Pelada)
admin.site.register(Time)
admin.site.register(Time_jogador)
admin.site.register(Time_pelada)