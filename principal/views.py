from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from produto.forms import CategoriaProdutoForm
from produto.models import CategoriaProduto, Produto, Tamanho

def about(request):
    return render(request, 'about.html')


def home(request):
    
    
    produtos = Produto.objects.all()
    
    # Filtros
    pesquisa = request.GET.get('pesquisa', '').strip()
    categoria_id = request.GET.get('categoria')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    tamanho_id = request.GET.get('tamanho')
    sort = request.GET.get('sort', '')
    
    if sort == 'preco_asc':
        produtos = produtos.order_by('preco')
    elif sort == 'preco_desc':
        produtos = produtos.order_by('-preco')
        
    if pesquisa:
        produtos = produtos.filter(Q(nome__icontains=pesquisa) | Q(descricao__icontains=pesquisa))
        
    if categoria_id:
        produtos = produtos.filter(categorias__id=categoria_id)
    
    if preco_min:
        produtos = produtos.filter(preco__gte=preco_min)
    
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)
    
    if tamanho_id:
        produtos = produtos.filter(tamanho__id=tamanho_id)
    
    # Paginação
    paginator = Paginator(produtos, 12)  # Mostra 10 produtos por página
    page = request.GET.get('page')
    
    try:
        produtos_pagina = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exiba a primeira página.
        produtos_pagina = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo (por exemplo, 9999), exiba a última página de resultados.
        produtos_pagina = paginator.page(paginator.num_pages)
    
    categorias = CategoriaProduto.objects.all()
    tamanhos = Tamanho.objects.all()
    
    context = {
        'produtos': produtos_pagina,
        'categorias': categorias,
        'tamanhos': tamanhos,
        'pesquisa': pesquisa,
        'preco_min': preco_min,
        'preco_max': preco_max,
        'categoria_id': categoria_id,
        'tamanho_id': tamanho_id,
        'sort': sort,
    }
    
    if request.user.is_superuser and not request.user.groups.filter(name='Administradores').exists():
        request.user.tipo_cliente = "ADMINISTRADOR"
        grupo, _ = Group.objects.get_or_create(name='Administradores')
        request.user.groups.add(grupo)
        
    return render(request, 'principal/home.html', context)


@login_required
def settings(request):
    return render(request, 'principal/settings.html', {})