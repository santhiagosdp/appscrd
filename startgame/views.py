from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import formset_factory
from .models import Jogador, Pelada, Time, Time_jogador
from .forms import JogadorForm, TimeForm, PeladaForm,Time_peladaForm

def index(request):
    jogadores = Jogador.objects.all()
    context = {
        'jogadores':jogadores
    }
    return render(request, 'index.html', context)



def cadastrar_jogador(request):
    jogadores = Jogador.objects.filter(habil=True)

    ## DESABILITAR TODOS JOGADORES
    deletar_todos = request.GET.get('deletar_todos')
    if deletar_todos:
        jogadores = Jogador.objects.all()
        for j in jogadores:
            j.habil = False
            j.save()
        #jogadores.delete()
        return redirect('cadastrar_jogador')
    
    ## DESABILITAR ÚNICO JOGADOR
    deletar_unico = request.GET.get('deletar_unico')
    if deletar_unico:
        jogador = Jogador.objects.get(id = deletar_unico)
        jogador.habil = False
        jogador.save()
        return redirect('cadastrar_jogador')

    if request.method == 'POST':
        form = JogadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_jogador')
    else:
        form = JogadorForm()

    
    context = {
        'jogadores':jogadores,
        'form': form
    }
    return render(request, 'cadastrar_jogador.html', context)



def deletarpelada(request):
    deletar = Pelada.objects.all()
    #print(deletar)
    deletar.delete()

    deletar = Time_jogador.objects.all()
    deletar.delete()

    deletar = Time.objects.all()
    deletar.delete()
    #print('deletados')



def cadastrar_pelada(request):

    if request.method == 'POST':
        #form = PeladaForm(request.POST)
        deletarpelada(request)
        tempo_pelada = request.POST.get('tempo_pelada')
        quantidade_jogadores = request.POST.get('quantidade_jogadores')
        valor_jogador = request.POST.get('valor_jogador')
        local = request.POST.get('local')
        pelada = Pelada.objects.create(
            tempo_pelada=tempo_pelada,
            quantidade_jogadores=quantidade_jogadores,
            valor_jogador=valor_jogador,
            local=local
            )
        pelada.save()
        return redirect('cadastrar_time')
    
    else:
        form = PeladaForm()
    context = {
        'form': form
    }
    return render(request, 'cadastrar_pelada.html', context)



def cadastrar_time(request): #cadastro do time
    jogadores = Jogador.objects.filter(habil=True)
    ## se for cadastrar time
    if request.method == 'POST':
        nome_time = request.POST.get('nome_time')
        cor_time = request.POST.get('cor_time')
        jogadores_selecionados = request.POST.getlist('jogador[]')
        time = Time.objects.create(nome_time = nome_time,cor_time=cor_time)
        time.save()
        for codigo in jogadores_selecionados:
            jogador_selecionado = Jogador.objects.get(id=codigo)
            time_jogador = Time_jogador.objects.create(jogador = jogador_selecionado, time=time)
            time_jogador.save()

        return redirect('cadastrar_time')
    
    else:
        form = TimeForm()

    peladas = Pelada.objects.filter(habil = True)
    pelada = 0
    for p in peladas:
        pelada = p 
    
    time_jogador = Time_jogador.objects.all().order_by('time')
    times = Time.objects.all().order_by('nome_time')

    #JOGADORES DISPONIVEIS
    jogs_indisponiveis = []
    for tj in time_jogador:
        for jogador in jogadores:
            if jogador == tj.jogador:
                jogs_indisponiveis.append(jogador)

    jogs_indisponiveis = time_jogador.values_list('jogador__pk', flat=True)
    jogadores_disponiveis = jogadores.exclude(pk__in=jogs_indisponiveis)

    if pelada != 0:        
        context = {      
            'times' : times,
            'time_jogador': time_jogador,  
            'jogadores': jogadores_disponiveis,
            'quant': pelada.quantidade_jogadores,  #qjuantidade de jogadores por time
            'form': form
        }
        return render(request, 'cadastrar_time.html', context)
    else:
        return redirect('cadastrar_pelada')



def temporizador(request):
    peladas = Pelada.objects.filter(habil = True)
    pelada = 0
    for p in peladas:
        pelada = p 

    context = {
        'pelada':pelada,
        'tempo': int(pelada.tempo_pelada)*60
    }
    return render(request, 'temporizador.html', context)



def distribuir_jogadores(request):
    jogadores = Jogador.objects.filter(is_disponivel=True)
    #if len(jogadores) % 2 != 0:
        #return HttpResponse('Número de jogadores ímpar. Não é possível distribuir equipes.')
    n_jogadores = 5 #len(jogadores) / 2   # quantidde de jogadores por equipe
    time1 = jogadores.order_by('?')[:n_jogadores]
    time2 = jogadores.exclude(pk__in=time1).order_by('?')[:n_jogadores]
    for jogador in time1:
        jogador.is_disponivel = False
        jogador.is_selecionado = True
        jogador.save()
    for jogador in time2:
        jogador.is_disponivel = False
        jogador.is_selecionado = True
        jogador.save()
    return render(request, 'distribuir_jogadores.html', {'time1': time1, 'time2': time2})



def listar_jogadores(request):
    jogadores = Jogador.objects.filter(is_selecionado=True)
    return render(request, 'listar_jogadores.html', {'jogadores': jogadores})
