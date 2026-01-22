from django import forms
from .models import Despesa

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['data', 'valor', 'origem', 'numero', 'info', 'categoria', 'subcategoria', 'descricao']
        
        widgets = {
            # Campo de Data: Adicionamos o placeholder "mm/dd/yyyy"
            # Usamos DateInput que é melhor para celulares (abre o calendário)
            'data': forms.DateInput(attrs={'type': 'date'}), 
            
            # Campo Subcategoria
            'subcategoria': forms.Select(attrs={'id': 'id_subcategoria'}),
        }


# NOVA CLASSE ABAIXO
class RelatorioForm(forms.Form):
    data_inicio = forms.DateField(label='Data Início', widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label='Data Fim', widget=forms.DateInput(attrs={'type': 'date'}))
