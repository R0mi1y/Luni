from django.urls import path
from . import views

urlpatterns = [
    path('listar_estampas/', views.listar_estampas, name='listar_estampas'),
    path('create/', views.create_estampa, name='create_estampa'),
    path('update/<int:id>/', views.edit_estampa, name='edit_estampa'),
    path('delete/<int:id>/', views.remove_estampa, name='delete_estampa'),
]