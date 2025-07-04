from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroForm
from django.contrib import messages

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'users/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # redirige a next si viene, o a home
            next_url = request.POST.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Credenciales incorrectas.")
    return render(request, 'users/login.html')

def logout_usuario(request):
    logout(request)
    return redirect('login')
