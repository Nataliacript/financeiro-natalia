from django.urls import path
from . import views

urlpatterns = [

    path('', views.cadastrar_despesa, name='home'),
    # Rota manual de logout
    path('logout/', views.sair_do_sistema, name='logout'),

    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),

    path('relatorios/', views.gerar_relatorio, name='relatorios'), # NOVA ROTA

 # --- NOVAS ROTAS ---
    path('minhas-despesas/', views.lista_despesas, name='lista_despesas'),
    path('excluir/<int:id>/', views.excluir_despesa, name='excluir_despesa'),
    path('editar/<int:id>/', views.editar_despesa, name='editar_despesa'),

]
