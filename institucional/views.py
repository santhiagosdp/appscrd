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



######################################

@login_required
def home(request):

    context = {
        'titulo' : "Home",
        'usuario' : request.user
    }
    return render(request, 'home.html', context)




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


