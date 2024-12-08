# Página de login
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('success')  # Redireciona para a página de sucesso
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'login/login.html')

# Página de cadastro
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Usuário cadastrado com sucesso! Faça login para continuar.')
            return redirect('login')  # Redireciona para a página de login
    return render(request, 'login/register.html')


# Logout
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('login')  # Redireciona para a página de login


#message
def success_view(request):
    return render(request, 'login/success.html')

