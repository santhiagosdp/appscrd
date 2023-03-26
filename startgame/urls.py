from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.cadastrar_jogador, name='cadastrar_jogador'),
    path('cadastrar_jogador/', views.cadastrar_jogador, name='cadastrar_jogador'),
    path('cadastrar_time/', views.cadastrar_time, name='cadastrar_time'),
    path('cadastrar_pelada/', views.cadastrar_pelada, name='cadastrar_pelada'),
    #path('temporizador/', views.temporizador, name='temporizador'),

    
    path('accounts/login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('new_user', views.new_user, name='new_user'),


    path('listar_jogadores/', views.listar_jogadores, name='listar_jogadores'),
]
