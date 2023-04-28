#######
#prioritario
from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


############### do app ##############################
from django.http import HttpResponseRedirect
from .models import NotaFiscal
from django.http import FileResponse
import mimetypes
from django.shortcuts import get_object_or_404

######################################

@login_required
def notaseasy(request):

    ##### SALVANDO A NOTA #########
    if request.method == 'POST':
        titulo = request.POST['titulo']
        arquivo = request.FILES['arquivo']
        nota_fiscal = NotaFiscal(usuario=request.user, titulo=titulo, arquivo=arquivo)
        nota_fiscal.save()
        return HttpResponseRedirect('/notaseasy')
    
    #### BUSCANDO AS NOTAS SALVAS ##############
    notas = NotaFiscal.objects.filter(habil=True, usuario=request.user)

    context = {
        'titulo' : "Notas Easy",
        'usuario' : request.user,
        'notas': notas
    }
    return render(request, 'notaseasy.html', context)





def abrir_nota_fiscal(request, nota_id):
    nota = get_object_or_404(NotaFiscal, id=nota_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(nota.arquivo))
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mimetypes.guess_type(file_path)[0])
        response['Content-Disposition'] = 'inline; filename="{}"'.format(os.path.basename(file_path))
        return response


def download_nota_fiscal(request, nota_id):
    nota = get_object_or_404(NotaFiscal, id=nota_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(nota.arquivo))
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mimetypes.guess_type(file_path)[0])
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(file_path))
        return response









##################                  ##################
#########             AUTENTICACAO           #########
##################                  ##################


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password"
            return render(request, 'aut/login.html', {'error': error})
    else:
        return render(request, 'aut/login.html')



def logout_view(request):
    logout(request)
    return redirect('home')



def new_user(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('home')
    else:
        form_usuario = UserCreationForm()
    
    context = {
        'titulo' : "Usuário",
        'form_usuario': form_usuario
    }
    return render(request, 'aut/new_user.html', context)


