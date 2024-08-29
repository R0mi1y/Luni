from django.urls import path
from . import views

urlpatterns = [
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('<int:id>/mudar_tipo/', views.mudar_tipo, name='mudar_tipo'),
    path('perfil/<int:id>/', views.perfil, name='perfil_usuario'),
    path('perfil/', views.perfil, name='perfil_usuario'),
    path('create/', views.create_usuario, name='create_usuario'),
    path('update/<int:id>/', views.edit_usuario, name='edit_usuario'),
    path('delete/<int:id>/', views.remove_usuario, name='delete_usuario'),
    path('receber_suporte_corporativo/', views.receber_suporte_corporativo, name='receber_suporte_corporativo'),
]