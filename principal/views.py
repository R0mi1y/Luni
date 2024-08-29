from email.headerregistry import Group
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from produto.forms import CategoriaProdutoForm
from produto.models import CategoriaProduto

def about(request):
    return render(request, 'about.html')


def home(request):
    if request.user.is_superuser and not request.user.groups.filter(name='Administradores').exists():
        request.user.tipo_cliente = "ADMINISTRADOR"
        grupo, _ = Group.objects.get_or_create(name='Administradores')
        request.user.groups.add(grupo)
        
    return render(request, 'principal/home.html')


@login_required
def settings(request):
    return render(request, 'principal/settings.html', {})