from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


def error_handler(request, exception=None, status_code=None):
    if status_code is None:
        status_code = 500
    context = {
        'status_code': status_code,
        'exception': exception,
    }
    return render(request, 'error.html', context, status=status_code)


handler400 = error_handler
handler403 = error_handler
handler404 = error_handler
handler500 = error_handler


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