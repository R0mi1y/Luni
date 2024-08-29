from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


@login_required
def listar_estampas(request):
    estampas = Estampa.objects.all()
    return render(request, 'estampa/listar_estampas.html', {'estampas': estampas})


@login_required
def create_estampa(request):
    if request.method == "POST":
        form = EstampaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/estampa/')
        else:
            return render(request, "form.html", {"form" : form, 'titulo' : 'Criar Estampa'})
    else:
        form = EstampaForm()
        return render(request, "form.html", {"form" : form, 'titulo' : 'Criar Estampa'})
    

@login_required
def edit_estampa(request, id):
    estampa = Estampa.objects.get(pk = id)
    print(estampa)

    if request.method == "POST":
        form = EstampaForm(request.POST, request.FILES, instance=estampa)

        if form.is_valid():
            form.save()

            return redirect('/estampa/')
    else:
        form = EstampaForm(instance=estampa)

    return render(request, 'form.html', {'form' : form, 'current_image_url': estampa.imagem.url, 'titulo' : 'Editar Estampa'})


@login_required
def remove_estampa(request, id):
    Estampa.objects.filter(pk = id).first().delete()

    return redirect('listar_estampas')