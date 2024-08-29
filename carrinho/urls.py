from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.carrinho, name='carrinho'),
    path('', views.carrinho, name='carrinho'),
    path('atualizar_carrinho/', views.atualizar_carrinho, name='atualizar_carrinho'),
    path('confirmar_compra/', views.confirmar_compra, name='confirmar_compra'),
]
