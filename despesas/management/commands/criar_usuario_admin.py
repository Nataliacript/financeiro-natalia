from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria ou redefine a senha do superusuário baseado nas Environment Variables'

    def handle(self, *args, **kwargs):
        # Lê as variáveis de ambiente do Render
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

        if User.objects.filter(username=username).exists():
            # O usuário já existe: ATUALIZA A SENHA
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.WARNING(f'Usuário {username} encontrado. Senha atualizada!'))
        else:
            # O usuário não existe: CRIA ELE
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f'Usuário {username} criado com sucesso!'))
