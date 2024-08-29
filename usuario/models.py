from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum

class Usuario(AbstractUser):
    TIPOS_CLIENTE_DICT = {
        'CLIENTE': 'Cliente', 
        'CORPORATIVO': 'Corporativo', 
        'ADMINISTRADOR': 'Administrador',
    }
    
    TIPOS_CLIENTE = [
        ('CLIENTE', 'Cliente'),
        ('CORPORATIVO', 'Corporativo'),
        ('ADMINISTRADOR', 'Administrador'),
    ]
    
    imagem = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    tipo_cliente = models.CharField(max_length=20, choices=TIPOS_CLIENTE, default='CLIENTE')
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.username}"
    
    def get_size_items(self):
        """Retorna o total de itens no carrinho do usuário."""
        carrinho = self.carrinho.first()  # Assume que um usuário tem um único carrinho
        if carrinho:
            return carrinho.itens.aggregate(total_items=Sum('quantidade'))['total_items'] or 0
        return 0
