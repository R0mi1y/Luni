from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


@login_required
def listar_pedidos(request, id=None):
    if id:
        if not request.user.is_superuser and id != request.user.pk:
            redirect('listar_pedidos', request.user.pk)
            
        user = get_object_or_404(Usuario, pk=id)
        pedidos = Pedido.objects.filter(cliente=user)
        
    elif request.user.is_superuser:
        pedidos = Pedido.objects.all()
        
    else:
        redirect('listar_pedidos', request.user.pk)
        
    return render(request, 'pedido/listar_pedidos.html', {'pedidos': pedidos})


@login_required
def create_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/pedido/')
        else:
            return render(request, "form.html", {"form" : form, 'titulo' : 'Criar pedido'})
    else:
        form = PedidoForm()
        return render(request, "form.html", {"form" : form, 'titulo' : 'Criar pedido'})
    

@login_required
def edit_pedido(request, id):
    pedido = Pedido.objects.get(pk = id)
    print(pedido)

    if request.method == "POST":
        form = PedidoForm(request.POST, instance=pedido)

        if form.is_valid():
            form.save()

            return redirect('/pedido/')
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'form.html', {'form' : form, 'titulo': 'Editar pedido'})


@login_required
def remove_pedido(request, id):
    Pedido.objects.filter(pk = id).first().delete()

    return redirect('listar_pedidos')