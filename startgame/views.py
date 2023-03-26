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
        listaj = Jogador.objects.filter(usuario = request.user, habil = True).order_by('posicao')
        posicao = 1
        for jog in listaj:
            posicao = jog.posicao+1

        jogador = Jogador.objects.create(
            usuario=request.user,
            nome = nome.upper(),
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
    deletar.delete()

    deletar = Time_jogador.objects.filter(usuario=request.user)
    deletar.delete()

    deletar = Time.objects.filter(usuario=request.user)
    deletar.delete()

    restaurar = Jogador.objects.filter(usuario=request.user, habil=True).order_by('id')
    aux = 1
    for jog in restaurar:
        jog.posicao = aux
        jog.save()
        aux = aux+1



@login_required
def cadastrar_pelada(request):

    if request.method == 'POST':
        #form = PeladaForm(request.POST)
        deletarpelada(request)
        tempo_pelada = request.POST.get('tempo_pelada')
        quantidade_jogadores = request.POST.get('quantidade_jogadores')
        #valor_jogador = request.POST.get('valor_jogador')
        #local = request.POST.get('local')
        pelada = Pelada.objects.create(
            usuario = request.user,
            tempo_pelada=tempo_pelada,
            quantidade_jogadores=quantidade_jogadores,
            #valor_jogador=valor_jogador,
            #local=local.upper()
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
    '''players = Jogador.objects.filter(usuario=request.user, habil=True).order_by('posicao')
    for jog in players:
        jog.nome = "chegada: "+str(jog.posicao)
        jog.save()'''
    
    peladas = Pelada.objects.filter(habil = True, usuario = request.user)
    pelada = 0
    for p in peladas:
        pelada = p

    if pelada != 0:
        ##montar times do zero
        n = pelada.quantidade_jogadores
        players = Jogador.objects.filter(usuario=request.user, habil=True).order_by('posicao')

        # seleciona os jogadores para o time azul
        time_azul = players.values_list('id', flat=True)[:n]
        azul = list(Jogador.objects.filter(id__in=time_azul))

        # seleciona os jogadores para o time vermelho
        time_vermelho = players.exclude(id__in=Jogador.objects.filter(id__in=time_azul)).values_list('id', flat=True)[:n]
        vermelho = list(Jogador.objects.filter(id__in=time_vermelho))

        proximos = []
        for jogador in  players:
            if jogador not in azul and jogador not in vermelho:
                #jogador.status = "proximos"
                proximos.append(jogador)
        
        #nesse momento tenho 4 listas
        # players = tem todos jogadores
        # vermelho = jogadores do time vermelho
        # azul = jogadores do time azul
        # proximos = jogadores restantes pros proximos jogos

###### Após jogo, vai vir o GET com o perdedor e vou fazer as trocas
        get_perdedor = request.GET.get('perdedor')
        if get_perdedor:
            if get_perdedor == "azul":
                perdedor = azul
                vencedor = vermelho
            if get_perdedor == "vermelho":
                perdedor = vermelho
                vencedor = azul

            # pegando posicao do ultimo na lista de proximo
            aux = 0
            for jogador in proximos:
                aux = jogador.posicao
            #acrescentando cada perdedor por ordem ao final da lista de proximo 
            for perd in perdedor:
                perd.posicao = aux+1
                proximos.append(perd)
                aux = aux+1

            # se azul perdeu, o vencedor (vermelho) tem que ser o segundo a criar times, criando primeiro o time dos proximos (azul)
            if get_perdedor == "azul":
                #qtd_jgs_time = len(perdedor)
                aux = 1
                for jogador in proximos:
                    if aux > pelada.quantidade_jogadores and aux < pelada.quantidade_jogadores*2: # qtd_jgs_time:
                        for jog in vencedor:
                            jog.posicao = aux
                            jog.save()
                            aux = aux+1
                    jogador.posicao = aux
                    jogador.save()
                    aux = aux+1
                return redirect('cadastrar_time')

            else: # se vermelho perder, faz isso normal e cria o azul vencedor primeiro
                #atualizo as listas no banco de dados pra gerar novos times
                aux = 1
                for jogador in vencedor:
                    jogador.posicao = aux
                    jogador.save()
                    aux = aux+1
                for jogador in proximos:
                    jogador.posicao = aux
                    jogador.save()
                    aux = aux+1
                #Redireciona de volta pra mostrar o novo time
                return redirect('cadastrar_time')

        context = {     
            'proximos' : proximos,
            'titulo' : "Time",
            'time_vermelho' : vermelho,
            'time_azul' : azul,
            'usuario' : request.user, 
            'pelada': pelada,  #quantidade de jogadores por time
        }
        return render(request, 'cadastrar_time.html', context)
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








## SEM UTILIZACAO

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

