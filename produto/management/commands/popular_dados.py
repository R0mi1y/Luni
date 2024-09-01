import os
import requests
from deep_translator import GoogleTranslator
from django.core.management.base import BaseCommand
from faker import Faker
from produto.models import Produto, CategoriaProduto, Tamanho, Estampa
from usuario.models import Usuario
from carrinho.models import Carrinho, ItemCarrinho
from pedido.models import Pedido, ItemPedido
from django.core.files import File
from PIL import Image
from io import BytesIO
from django.conf import settings
from django.db.models import Sum
from urllib.parse import urlparse


fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with data from an external API and fake data"

    def handle(self, *args, **kwargs):
        # Populando Categorias de Produtos
        self.populate_categories()

        # Populando Produtos
        self.populate_products()

        # Populando Usuários
        self.populate_users()

        # Populando Carrinhos e Pedidos
        self.populate_carts_and_orders()

        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))

    def populate_categories(self):
        url = "https://fakestoreapi.com/products/categories"
        response = requests.get(url)
        categories = response.json()
        
        for cat_name in categories:
            CategoriaProduto.objects.get_or_create(nome=cat_name)
    
    def populate_products(self):
        url = "https://fakestoreapi.com/products"
        response = requests.get(url)
        products = response.json()
        translator = GoogleTranslator(source='en', target='pt')

        
        for product_data in products:
            translated_name = translator.translate(product_data['title'])
            product = Produto.objects.create(
                nome=translated_name if translated_name is not None else product_data['title'],
                descricao=product_data['description'],
                preco=product_data['price'],
                quantidade_em_estoque=fake.random_int(min=10, max=100)
            )

            # Baixa a imagem e salva localmente
            image_url = product_data['image']
            image_name = self.download_image(image_url)
            if image_name:
                product.imagem.save(os.path.basename(image_name), File(open(image_name, 'rb')))

            # Adiciona as categorias
            for cat_name in product_data['category'].split(","):
                categoria = CategoriaProduto.objects.get(nome=cat_name)
                product.categorias.add(categoria)
                
            # Adiciona tamanhos e estampas fictícias
            self.add_fake_sizes_and_prints(product)

    def download_image(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            parsed_url = urlparse(url)
            image_filename = os.path.basename(parsed_url.path)
            image_path = os.path.join(settings.MEDIA_ROOT, 'produtos', image_filename)
            
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            img.save(image_path)
            return image_path
        return None

    def add_fake_sizes_and_prints(self, product):
        tamanhos = Tamanho.objects.all()
        estampas = Estampa.objects.all()
        
        if not tamanhos.exists():
            tamanhos = [Tamanho.objects.create(tamanho=size) for size in ['P', 'M', 'G', 'GG']]
        
        if not estampas.exists():
            estampas = [Estampa.objects.create(nome=f'Estampa {i}', descricao=fake.text()) for i in range(5)]

        product.tamanho.set(tamanhos)
        product.estampas.set(estampas)
    
    def populate_users(self):
        url = "https://fakestoreapi.com/users"
        response = requests.get(url)
        users = response.json()
        
        for user_data in users:
            # Verifica se o username já existe
            if not Usuario.objects.filter(username=user_data['username']).exists():
                Usuario.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    telefone=user_data['phone'],
                    endereco=f"{user_data['address']['street']} {user_data['address']['number']}, {user_data['address']['city']}, {user_data['address']['zipcode']}",
                    tipo_cliente='CLIENTE',
                    cpf=fake.unique.random_number(digits=11)
                )

    
    def populate_carts_and_orders(self):
        url = "https://fakestoreapi.com/carts"
        response = requests.get(url)
        carts = response.json()
        
        for cart_data in carts:
            try:
                usuario = Usuario.objects.get(id=cart_data['userId'])
                carrinho = Carrinho.objects.create(usuario=usuario)
                
                for item_data in cart_data['products']:
                    # Use um produto aleatório caso o ID não exista
                    produto = Produto.objects.order_by('?').first()
                    tamanho = Tamanho.objects.order_by('?').first()
                    estampa = Estampa.objects.order_by('?').first()
                    
                    ItemCarrinho.objects.create(
                        carrinho=carrinho,
                        produto=produto,
                        quantidade=item_data['quantity'],
                        tamanho=tamanho,
                        estampa=estampa
                    )
                
                Pedido.objects.create(
                    cliente=usuario,
                    preco_total=carrinho.itens.aggregate(total=Sum('produto__preco'))['total'],
                    status='PROCESSANDO'
                )
            except Usuario.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Usuário com ID {cart_data['userId']} não existe."))

