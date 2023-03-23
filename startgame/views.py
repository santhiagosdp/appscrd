from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import formset_factory
from .models import Jogador, Pelada, Time, Time_jogador
from .forms import JogadorForm, TimeForm, PeladaForm, Time_peladaForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    jogadores = Jogador.objects.filter(habil=True, usuario=request.user)

    context = {
        'titulo' : "Inicio",
        'usuario' : request.user,
        'jogadores' : jogadores
    }
    return render(request, 'index.html', context)


@login_required
def cadastrar_jogador(request):
    jogadores = Jogador.objects.filter(usuario=request.user, habil=True)

    ## DESABILITAR TODOS JOGADORES
    deletar_todos = request.GET.get('deletar_todos')
    if deletar_todos:
        jogadores = Jogador.objects.filter(habil=True, usuario=request.user)
        for j in jogadores:
            j.habil = False
            j.save()
        #jogadores.delete()
        return redirect('cadastrar_jogador')
    
    ## DESABILITAR ÚNICO JOGADOR
    deletar_unico = request.GET.get('deletar_unico')
    if deletar_unico:
        jogador = Jogador.objects.get(id = deletar_unico, usuario=request.user)
        jogador.habil = False
        jogador.save()
        return redirect('cadastrar_jogador')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        posicao = request.POST.get('posicao')
        jogador = Jogador.objects.create(
            usuario=request.user,
            nome = nome,
            posicao = posicao,
        )
        return redirect('cadastrar_jogador')
    else:
        form = JogadorForm()

    context = {
        'titulo' : "Jogador",
        'usuario' : request.user,
        'jogadores':jogadores,
        'form': form
    }
    return render(request, 'cadastrar_jogador.html', context)


@login_required
def deletarpelada(request):
    deletar = Pelada.objects.filter(usuario=request.user)
    #print(deletar)
    deletar.delete()

    deletar = Time_jogador.objects.filter(usuario=request.user)
    deletar.delete()

    deletar = Time.objects.filter(usuario=request.user)
    deletar.delete()
    #print('deletados')


@login_required
def cadastrar_pelada(request):

    if request.method == 'POST':
        #form = PeladaForm(request.POST)
        deletarpelada(request)
        tempo_pelada = request.POST.get('tempo_pelada')
        quantidade_jogadores = request.POST.get('quantidade_jogadores')
        valor_jogador = request.POST.get('valor_jogador')
        local = request.POST.get('local')
        pelada = Pelada.objects.create(
            usuario = request.user,
            tempo_pelada=tempo_pelada,
            quantidade_jogadores=quantidade_jogadores,
            valor_jogador=valor_jogador,
            local=local
            )
        pelada.save()
        return redirect('cadastrar_time')
    
    context = {
        'titulo' : "Pelada",        
        'usuario' : request.user
    }
    return render(request, 'cadastrar_pelada.html', context)


@login_required
def cadastrar_time(request): #cadastro do time
    jogadores = Jogador.objects.filter(habil=True, usuario = request.user)
    ## se for cadastrar time
    if request.method == 'POST':
        nome_time = request.POST.get('nome_time')
        cor_time = request.POST.get('cor_time')
        jogadores_selecionados = request.POST.getlist('jogador[]')
        time = Time.objects.create(
            usuario = request.user,
            nome_time = nome_time,
            cor_time=cor_time)
        time.save()
        for codigo in jogadores_selecionados:
            jogador_selecionado = Jogador.objects.get(id=codigo, usuario = request.user)
            time_jogador = Time_jogador.objects.create(
                usuario = request.user,
                jogador = jogador_selecionado,
                time=time)
            time_jogador.save()

        return redirect('cadastrar_time')
     
    time_jogador = Time_jogador.objects.filter(habil = True, usuario = request.user).order_by('time')
    times = Time.objects.filter(habil = True, usuario = request.user).order_by('nome_time')

    #JOGADORES DISPONIVEIS
    jogs_indisponiveis = []
    for tj in time_jogador:
        for jogador in jogadores:
            if jogador == tj.jogador:
                jogs_indisponiveis.append(jogador)

    jogs_indisponiveis = time_jogador.values_list('jogador__pk', flat=True)
    jogadores_disponiveis = jogadores.exclude(pk__in=jogs_indisponiveis)

    peladas = Pelada.objects.filter(habil = True, usuario = request.user)
    pelada = 0
    for p in peladas:
        pelada = p

    if pelada != 0:        
        context = {     
            'titulo' : "Time",
            'usuario' : request.user, 
            'times' : times,
            'time_jogador': time_jogador,  
            'jogadores': jogadores_disponiveis,
            'quant': pelada.quantidade_jogadores,  #qjuantidade de jogadores por time
        }
        return render(request, 'cadastrar_time.html', context)
    else:
        return redirect('cadastrar_pelada')


@login_required
def temporizador(request):
    peladas = Pelada.objects.filter(habil = True, usuario = request.user)
    pelada = 0
    for p in peladas:
        pelada = p 
        
    if pelada != 0:  
        context = {
            'titulo' : "Temporizador",
            'usuario' : request.user,
            'pelada':pelada,
            'tempo': int(pelada.tempo_pelada)*60
        }
        return render(request, 'temporizador.html', context)
    else:
        return redirect('cadastrar_pelada')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = "Invalid username or password"
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('login')



def new_user(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('index')
    else:
        form_usuario = UserCreationForm()
    
    context = {
        'titulo' : "Usuário",
        'form_usuario': form_usuario
    }
    return render(request, 'new_user.html', context)






@login_required
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

    context = {
        'usuario' : request.user,
        'time1': time1,
         'time2': time2
            }
    
    return render(request, 'distribuir_jogadores.html', context)


@login_required
def listar_jogadores(request):
    jogadores = Jogador.objects.filter(is_selecionado=True)
    context = {
        'usuario' : request.user,
        'jogadores': jogadores
    }
    return render(request, 'listar_jogadores.html', context)

