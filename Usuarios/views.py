from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as do_logout

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                return redirect('/')

    return render(request, "usuario/login.html", {'form': form})

def registro(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                do_login(request, user)
                return redirect('/')
    return render(request, "usuario/registro.html", {'form': form})

def logout(request):
    do_logout(request)
    return redirect('/')

def inicio(request):
    return render(request, 'core/index.html')

def contacto(request):
    if request.method == "POST":
        return render(request, 'extra/gracias.html')
    return render(request, "extra/contacto.html")

def acerca(request):
    return render(request, 'extra/acerca.html')

def privacidad(request):
    return render(request, 'extra/privacidad.html')

def terminos(request):
    return render(request, 'extra/terminos.html')
