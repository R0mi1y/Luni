from django.urls import path
from . import views

urlpatterns = [
    path('add-carrinho/<int:id>/', views.adicionar_ao_carrinho, name='add_carrinho'),
    path('<int:id>/', views.detalhes_produto, name='detalhes_produto'),
    path('rm-carrinho/<int:id>/', views.remover_do_carrinho, name='rm_carrinho'),
    path('listar/produtos/', views.listar_produtos, name='listar_produtos'),
    path('listar/tipos/', views.listar_tipos_produtos, name='listar_tipo_produtos'),
    path('pesquisa/', views.pesquisar_produtos, name='pesquisar_produto'),
    path('create/', views.create_produto, name='create_produto'),
    path('update/<int:id>/', views.edit_produto, name='edit_produto'),
    path('delete/<int:id>/', views.remove_produto, name='delete_produto'),
    path('tipo/create/', views.create_tipo_produto, name='create_tipo_produto'),
    path('tipo/update/<int:id>/', views.edit_tipo_produto, name='edit_tipo_produto'),
    path('tipo/delete/<int:id>/', views.remove_tipo_produto, name='delete_tipo_produto'),
]