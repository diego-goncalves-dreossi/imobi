from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
# Importa das aplicações já criadas do django o banco de dados usuário
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
# Mensagens 

# Create your views here.

# render é uma função que permite a renderização de páginas html
def cadastro(request):
    # Quando acessamos pelo navegador/ pela url
    if request.method == "GET":
        if request.user.is_authenticated:
            # Casos em que já estou logado, impede que voltemos as páginas
            # de login e cadastro
            return redirect('/')

        return render(request,'cadastro.html')

    # Quando enviamos dados pela url atraves de formulário     
    elif request.method == "POST":
        print(request.POST)
        username = request.POST.get('username')
        email =  request.POST.get('email')
        senha =  request.POST.get('senha')

        # Aqui verificamos se algo foi escrito nos inputs
        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR,'Preencha todos os campos')
            return redirect('/auth/cadastro')
        
        user = User.objects.filter(username=username)
        # Pegua os objetos da tabalea usuario pelo filtro do username

        if user.exists():
            messages.add_message(request, constants.ERROR,'Usuário já existe')
            return redirect('/auth/cadastro')
        # Se usuario cadastrado redirecione para a página cadastro

        try:
            user = User.objects.create_user(username=username, email = email, password=senha )
            # cria instancia de usuario
            user.save()
            messages.add_message(request, constants.SUCCESS,'Usuário cadastrado com sucesso!')
            # salva no bd
            return redirect('/auth/login')

        except:
            messages.add_message(request, constants.ERROR,'Erro interno do sistema')
            return redirect('/auth/login')

        
          

def logar(request):
    # Quando acessamos pelo navegador/ pela url
    if request.method == "GET":
        if request.user.is_authenticated:
            # Casos em que já estou logado, impede que voltemos as páginas
            # de login e cadastro
            return redirect('/')
        return render(request,'logar.html')
    # Quando enviamos dados pela url atraves de formulário     
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=senha)
        # Verifica se usuário se existe no sistema

        if not usuario:
            messages.add_message(request, constants.ERROR,'Usuário ou senha inválidos')
            return redirect('/auth/login')
        else:
            auth.login(request, usuario)
            # Cria uma sessão
            return redirect('/') # Página inicial

        return HttpResponse(f"{username}, {senha}")    

def sair(request):
    auth.logout(request)
    return redirect('/auth/login')