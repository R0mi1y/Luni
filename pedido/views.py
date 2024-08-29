from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
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