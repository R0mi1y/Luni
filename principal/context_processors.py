from produto.models import CategoriaProduto

def variaveis_globais(request):
    return {
        'nome_site': 'Luni',
        'categorias': CategoriaProduto.objects.all(),
    }