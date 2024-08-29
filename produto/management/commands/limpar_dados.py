from django.core.management.base import BaseCommand
from produto.models import Produto, Estampa
from pedido.models import Pedido, ItemPedido
from django.db import transaction

class Command(BaseCommand):
    help = 'Limpa o banco de dados exceto os usuários'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Limpar Produtos
            Produto.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Produtos excluídos com sucesso'))

            # Limpar Estampas
            Estampa.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Estampas excluídas com sucesso'))

            # Limpar Pedidos e ItensPedido
            ItemPedido.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Itens de pedido excluídos com sucesso'))
            Pedido.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Pedidos excluídos com sucesso'))