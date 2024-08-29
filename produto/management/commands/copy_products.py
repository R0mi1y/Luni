from django.core.management.base import BaseCommand
from produto.models import Produto

class Command(BaseCommand):
    help = 'Cria cópias de todos os produtos'

    def handle(self, *args, **kwargs):
        produtos = Produto.objects.all()
        for produto in produtos:
            # Cria uma nova instância do produto
            novo_produto = Produto(
                nome=produto.nome + " (cópia)",
                descricao=produto.descricao,
                preco=produto.preco,
                quantidade_em_estoque=produto.quantidade_em_estoque,
                imagem=produto.imagem,
            )
            novo_produto.save()
            
            # Adiciona as relações ManyToMany
            novo_produto.categorias.set(produto.categorias.all())
            novo_produto.tamanho.set(produto.tamanho.all())
            novo_produto.estampas.set(produto.estampas.all())

        self.stdout.write(self.style.SUCCESS('Todos os produtos foram copiados com sucesso.'))
