# Página de login
import os
import git
import subprocess
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Repository
from .forms import RepositoryForm
from graphviz import Source
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



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
    return render(request, 'register.html')


# Logout
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('login')  # Redireciona para a página de login


#message
def success_view(request):
    return render(request, 'success.html')

@login_required
def dashboard(request):
    print("/dashboard")
    error = None
    success = None
    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data['repo_url']

            # Verifica se o repositório já foi clonado
            # if Repository.objects.filter(repo_url=repo_url, user=request.user).exists():
            #     print("O repositório já foi clonado.")
            #     error = "O repositório já foi clonado."
            # else:
                # Clona o repositório
            try:
                target_dir = os.path.join('repos', f'{request.user.username}_{repo_url.split("/")[-1]}')
                if os.path.exists(target_dir):
                    error = "O repositório já existe, remova-o ou escolha outro."
                    # Executa o pyreverse
                    print(target_dir)
                    classes_dot_path = run_pyreverse(target_dir)
                    print(classes_dot_path)
                    if classes_dot_path:
                        success = "Diagrama gerado com sucesso!"
                        return redirect('show_diagram', repo_id=repo.id)
                    else:
                        error = "Erro ao gerar arquivo .dot"
                else:
                    git.Repo.clone_from(repo_url, target_dir)
                    repo = Repository(user=request.user, repo_url=repo_url)
                    repo.save()

                    # Executa o pyreverse
                    print(target_dir)
                    classes_dot_path = run_pyreverse(target_dir)
                    print(classes_dot_path)
                    if classes_dot_path:
                        success = "Diagrama gerado com sucesso!"
                        return redirect('show_diagram', repo_id=repo.id)
                    else:
                        error = "Erro ao gerar arquivo .dot"
            except Exception as e:
                error = f"Erro ao clonar repositório: {e}"
        else:
            error = "URL inválida."
    else:
        form = RepositoryForm()

    return render(request, 'show_diagram.html', {'form': form, 'error': error, 'success': success})

# Função para executar pyreverse
def run_pyreverse(source_dir):
    try:
        # Direciona o arquivo .dot para um local dentro do diretório do usuário
        output_dir = os.path.join(source_dir, 'diagrams')
        os.makedirs(output_dir, exist_ok=True)
        dot_path = os.path.join(output_dir, 'classes.dot')

        command = f"pyreverse -o dot -p Diagrams {source_dir}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(command)
        print(result)
        if result.returncode != 0:
            return None

        return dot_path  # Retorna o caminho absoluto do arquivo .dot gerado
    except Exception as e:
        print("Erro ao executar o Pyreverse. Erro: " + e)
        return None

# Função para mostrar o diagrama
@login_required
def show_diagram(request, repo_id):
    try:
        repo = Repository.objects.get(id=repo_id, user=request.user)
        # Aqui você vai gerar o diagrama a partir do arquivo .dot
        dot_path = os.path.join('repos', f'{request.user.username}_{repo.repo_url.split("/")[-1]}', 'diagrams', 'classes.dot')
        
        if not os.path.exists(dot_path):
            return redirect('dashboard')  # Se o arquivo .dot não existir, redireciona para o dashboard

        source = Source.from_file(dot_path)
        response = HttpResponse(content_type="image/png")
        response['Content-Disposition'] = 'inline; filename=diagram.png'
        source.render(response=response, format='png')
        return response
    except Repository.DoesNotExist:
        return redirect('dashboard')