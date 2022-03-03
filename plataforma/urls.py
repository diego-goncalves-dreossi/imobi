from django.urls import path
from . import views
# . significa que desse diretório

urlpatterns = [
    path('',views.home, name="home"),
    path('imovel/<str:id>', views.imovel, name="imovel"),
    #URL dinamica, vai ser passado um parametro id que sera o restante da url
    path('agendar_visitas', views.agendar_visitas, name="agendar_visitas"),
    path('agendamentos', views.agendamentos, name="agendamentos"),
    path('cancelar_agendamento/<str:id>', views.cancelar_agendamento, name="cancelar_agendamento")

]
