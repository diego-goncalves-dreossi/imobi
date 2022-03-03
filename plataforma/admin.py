from django.contrib import admin
from .models import DiasVisita,Cidade,Imagem,Horario,Visitas, Imovei
# Register your models here.

admin.site.register(DiasVisita)
admin.site.register(Cidade)
admin.site.register(Imagem)
admin.site.register(Horario)
admin.site.register(Visitas)

@admin.register(Imovei)
class ImoveiAdmin(admin.ModelAdmin):
    list_display = ('rua','valor','quartos','tamanho','cidade','tipo')
    list_editable = ('valor','tipo') # Permite edição sem ter que entrar no objeto
    list_filter = ('cidade','tipo') # Cria filtro

# Bloco que permite maior personalização na página Admin    
