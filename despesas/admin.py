from django.contrib import admin
from .models import Despesa

# Isso diz ao Django: "Mostre a Despesa no painel admin"
admin.site.register(Despesa)
