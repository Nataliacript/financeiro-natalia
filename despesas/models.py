from django.db import models

# --- LISTAS DE OPÇÕES ---

CATEGORIAS = [
    ('alimentacao', 'Alimentação'),
    ('lazer', 'Lazer'),
    ('transporte', 'Transporte'),
]

ORIGENS = [
    ('mercado', 'Mercado'),
    ('feira', 'Feira'),
    ('outro', 'Outro'),
]

# Definimos todas as subcategorias possíveis aqui.
# A filtragem ("café" mostra pão, "almoço" mostra arroz) será feita na tela (HTML/JS).
# Para garantir que não escrevem besteira, definimos uma lista geral aqui.
SUBCATEGORIAS = [
    # Alimentação - Café
    ('cafe_pao', 'Café - Pão'),
    ('cafe_manteiga', 'Café - Manteiga'),
    ('cafe_ovo', 'Café - Ovo'),
    
    # Alimentação - Almoço
    ('almoco_arroz', 'Almoço - Arroz'),
    ('almoco_feijao', 'Almoço - Feijão'),
    ('almoco_carne', 'Almoço - Carne'),

    # Lazer
    ('lazer_cinema', 'Cinema'),
    ('lazer_jogo', 'Jogos'),
]

# -------------------------------------

class Despesa(models.Model):
    data = models.DateField(verbose_name="Data da Despesa")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor (R$)")
    
    origem = models.CharField(max_length=100, choices=ORIGENS, verbose_name="Origem")
    numero = models.CharField(max_length=50, blank=True, verbose_name="Número")
    info = models.TextField(blank=True, verbose_name="Info Extras")
    
    # Categoria é fixo (Dropdown)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS, verbose_name="Categoria")
    
    # Subcategoria: REMOVEMOS o 'choices' aqui.
    # Isso permite qualquer valor válido ser salvo.
    subcategoria = models.CharField(max_length=100, verbose_name="Subcategoria")
    
    descricao = models.TextField(blank=True, verbose_name="Descrição")

    def __str__(self):
        return f"{self.data} - R$ {self.valor}"
