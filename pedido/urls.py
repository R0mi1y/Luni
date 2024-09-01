from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.pedido, name='pedido'),
    path('listar_pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('listar_pedidos/<int:id>/', views.listar_pedidos, name='listar_pedidos'),
    path('create/', views.create_pedido, name='create_pedido'),
    path('update/<int:id>/', views.edit_pedido, name='edit_pedido'),
    path('delete/<int:id>/', views.remove_pedido, name='delete_pedido'),
]