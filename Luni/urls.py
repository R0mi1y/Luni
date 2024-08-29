from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("principal.urls"), name="index"),
    path("user/", include("usuario.urls"), name='usuario'),
    path("produto/", include("produto.urls"), name='produto'),
    path("estampa/", include("estampa.urls"), name='estampa'),
    path("carrinho/", include("carrinho.urls"), name='carrinho'),
    path("pedido/", include("pedido.urls"), name='pedido'),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)