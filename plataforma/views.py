from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
#Importar imoveis do banco de dados
from .models import Imovei, Cidade, Visitas
# Create your views here.

# Todas view com @login_required só podem ser acessados se estiverem logados
# e caso não estiverem são redirecionados para o login 
@login_required(login_url="/auth/login")
def home(request):
    # Pro filtro
    preco_minimo = request.GET.get('preco_minimo')
    preco_maximo = request.GET.get('preco_maximo')
    cidade = request.GET.get('cidade')
    tipo = request.GET.getlist('tipo') # É uma lista, pois podemos clicar + de 1
    cidades = Cidade.objects.all()
    #
    # Se qualquer filtro foi feito / Ler imóveis do banco de dados 
   
    if preco_minimo or preco_maximo or cidade or tipo:
        
        if not preco_minimo:
            preco_minimo = 0.0
        if not preco_maximo:
            preco_maximo = 999999999.0
        if not tipo:
            tipo = ['A', 'C']
        
        
        imoveis = Imovei.objects.filter(valor__gte=preco_minimo)\
        .filter(valor__lte=preco_maximo)\
        .filter(tipo_imovel__in=tipo).filter(cidade=cidade)
        # Onde o valor do imovel seja maior que o preço minimo, menor que o preço máximo
    else:
        imoveis = Imovei.objects.all()
    
    return render(request, 'home.html', {'imoveis': imoveis, 'cidades': cidades})
    
    
    # imoveis e cidades são carregado junto pra página

    
def imovel(request, id):
    imovel = get_object_or_404(Imovei, id=id)
    # Retorna um objeto se há um com tal id ou erro 404 avisando que página não existe 
    sugestoes = Imovei.objects.filter(cidade=imovel.cidade).exclude(id=id)[:2]
    # Essa é pra mostrar sugestões de outros imoveis, se exclui o que está sendo vizualizado no momento. o [:2] é para exibir só 2
    return render(request,'imovel.html',{'imovel':imovel, 'sugestoes':sugestoes})

def agendar_visitas(request):
    usuario = request.user
    dia = request.POST.get('dia')
    horario = request.POST.get('horario')
    id_imovel = request.POST.get('id_imovel')

    visitas = Visitas(
        imovel_id = id_imovel,
        usuario = usuario,
        dia = dia,
        horario = horario
    )

    # Efetivar no banco de dados
    visitas.save()

    return redirect('/agendamentos')


def agendamentos(request):
    visitas = Visitas.objects.filter(usuario=request.user)
    # Visitas que o usuário logado fez
    return render(request, "agendamentos.html", {'visitas': visitas})

def cancelar_agendamento(request, id):
    visitas = get_object_or_404(Visitas, id=id)
    visitas.status = "C"
    visitas.save()
    return redirect('/agendamentos')