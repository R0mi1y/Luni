from django.core.management.base import BaseCommand
from produto.models import Produto, Estampa
from usuario.models import Usuario
from pedido.models import Pedido, ItemPedido
from decimal import Decimal
import random
from faker import Faker
import requests
from PIL import Image
import os

fake = Faker()

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados fictícios'

    def handle(self, *args, **options):
        # Criar estampas com imagens fictícias
        estampas = []
        for _ in range(10):
            nome = fake.word()
            descricao = fake.sentence()
            imagem_url = fake.image_url()  # URL da imagem fictícia
            imagem_path = f'./media/estampas/{nome}.jpg'
            self._download_and_resize_image(imagem_url, imagem_path)
            estampas.append(Estampa(nome=nome, descricao=descricao, imagem=imagem_path.replace('/media', '')))
        Estampa.objects.bulk_create(estampas)
        self.stdout.write(self.style.SUCCESS('Estampas criadas com sucesso'))

        # Criar produtos com imagens fictícias
        produtos = []
        categorias = ['CAMISA', 'CAMISETA', 'CALCA', 'SAIA', 'JAQUETA', 'ACESSORIO', 'VESTIDO', 'OUTRO']
        for _ in range(20):
            nome = fake.word()
            descricao = fake.sentence()
            tipo = random.choice(categorias)
            preco = Decimal(random.uniform(10.0, 200.0)).quantize(Decimal('0.01'))
            tamanho = random.choice(['P', 'M', 'G', 'GG', '42'])
            quantidade_em_estoque = random.randint(1, 100)
            imagem_url = fake.image_url()  # URL da imagem fictícia
            imagem_path = f'./media/produtos/{nome}.jpg'
            self._download_and_resize_image(imagem_url, imagem_path)
            produto = Produto(
                nome=nome,
                descricao=descricao,
                tipo=tipo,
                preco=preco,
                tamanho=tamanho,
                quantidade_em_estoque=quantidade_em_estoque,
                imagem=imagem_path.replace('/media', '')
            )
            produto.save()
            produto.estampas.set(Estampa.objects.all())
            produtos.append(produto)
        self.stdout.write(self.style.SUCCESS('Produtos criados com sucesso'))

        # Criar usuários com dados fictícios
        usuarios = []
        for _ in range(5):
            usuario = Usuario(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                telefone=fake.phone_number(),
                endereco=fake.address(),
                tipo_cliente=random.choice(['INDIVIDUAL', 'CORPORATIVO', 'ADMINISTRADOR']),
                cpf=fake.ssn()
            )
            usuario.save()
            usuarios.append(usuario)
        self.stdout.write(self.style.SUCCESS('Usuários criados com sucesso'))

        # Criar pedidos com dados fictícios
        for usuario in usuarios:
            for _ in range(2):
                pedido = Pedido(cliente=usuario, preco_total=Decimal(random.uniform(30.0, 150.0)).quantize(Decimal('0.01')), status=random.choice(['PROCESSANDO', 'ENVIADO', 'ENTREGUE']))
                pedido.save()
                for _ in range(random.randint(1, 3)):
                    produto = random.choice(produtos)
                    ItemPedido.objects.create(
                        pedido=pedido,
                        produto=produto,
                        quantidade=random.randint(1, 5),
                        preco=produto.preco
                    )
        self.stdout.write(self.style.SUCCESS('Pedidos criados com sucesso'))

    def _download_and_resize_image(self, url, path, target_size=(800, 800)):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
            
            # Redimensionar a imagem para manter a proporção
            with Image.open(path) as img:
                img = img.convert('RGB')  # Converte a imagem para o modo RGB
                img.thumbnail(target_size, Image.Resampling.LANCZOS)  # Mantém a proporção da imagem
                img.save(path, format='JPEG')  # Salva como JPEG

