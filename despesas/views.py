from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout # <--- NOVA IMPORTAÇÃO
from django.http import HttpResponse
from .forms import DespesaForm
from .models import Despesa

# --- LÓGICA DO LOGOUT -----
def sair_do_sistema(request):
    logout(request)
    # Força a limpeza completa da sessão no servidor
    if hasattr(request, 'session'):
        request.session.flush()
        request.session.delete()
    
    # Cria a resposta de redirecionamento
    resp = redirect('/login/')
    
    # ORDEM EXPLÍCITA PARA O NAVEGADOR: Apague os cookies!
    # Isso apaga o rastro da sessão no Chrome/Firefox
    resp.delete_cookie('sessionid', path='/', domain=None)
    resp.delete_cookie('csrftoken', path='/', domain=None)
    
    return resp
# --- CADASTRAR ---
@login_required(login_url='/login/')
def cadastrar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            
            # AQUI ESTÁ A MÁGICA: Verifica qual botão foi clicado
            if 'btn_stay' in request.POST:
                # Botão: Salvar e Criar Outra
                return redirect('home')
            elif 'btn_leave' in request.POST:
                # Botão: Salvar e Pesquisar (Ir para Lista)
                return redirect('lista_despesas')
    else:
        form = DespesaForm()
    return render(request, 'despesas/index.html', {'form': form})
# --- LISTAR ---
@login_required(login_url='/login/')
def lista_despesas(request):
    todas_despesas = Despesa.objects.all().order_by('-data')
    return render(request, 'despesas/lista_despesas.html', {'despesas': todas_despesas})

# --- EXCLUIR ---
@login_required(login_url='/login/')
def excluir_despesa(request, id):
    despesa = Despesa.objects.get(id=id)
    despesa.delete()
    return redirect('lista_despesas')

# --- EDITAR ---
@login_required(login_url='/login/')
def editar_despesa(request, id):
    despesa = Despesa.objects.get(id=id)
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('lista_despesas')
    else:
        form = DespesaForm(instance=despesa)
    return render(request, 'despesas/editar_despesa.html', {'form': form})

# --- EXPORTAR TUDO ---
@login_required(login_url='/login/')
def exportar_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Despesas"
    ws.append(["Data", "Valor", "Origem", "Número", "Info", "Categoria", "Subcategoria", "Descrição"])
    for cell in ws[1]: cell.font = Font(bold=True)
    despesas = Despesa.objects.all()
    for item in despesas:
        ws.append([item.data, item.valor, item.origem, item.numero, item.info, item.categoria, item.subcategoria, item.descricao])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=todas_despesas.xlsx'
    wb.save(response)
    return response

# --- RELATÓRIO FILTRADO ---
@login_required(login_url='/login/')
def gerar_relatorio(request):
    if 'data_inicio' in request.GET and 'data_fim' in request.GET:
        form = RelatorioForm(request.GET)
        if form.is_valid():
            inicio = form.cleaned_data['data_inicio']
            fim = form.cleaned_data['data_fim']
            despesas_filtradas = Despesa.objects.filter(data__range=[inicio, fim])
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Relatório Filtrado"
            ws.append(["Data", "Valor", "Origem", "Número", "Info", "Categoria", "Subcategoria", "Descrição"])
            for cell in ws[1]: cell.font = Font(bold=True)
            for item in despesas_filtradas:
                ws.append([item.data, item.valor, item.origem, item.numero, item.info, item.categoria, item.subcategoria, item.descricao])
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=relatorio_filtrado.xlsx'
            wb.save(response)
            return response
    else:
        form = RelatorioForm()
    return render(request, 'despesas/relatorio.html', {'form': form})
