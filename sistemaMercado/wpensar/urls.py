from django.urls import path
from . import views

app_name = "wpensar"
urlpatterns = [
    path("", views.view_index, name="index"),
    path("listar-compras/", views.CompraListView.as_view(), name="list"),
    path("listar-compras/<slug:slug>/", views.CompraDetailView.as_view(), name="detail"),
    path("nova_compra/", views.nova_compra, name="nova_compra"),
    path("adicionar_produtos/", views.adicionar_produtos, name="adicionar_produtos"),
    path("processa_formulario/", views.processa_formulario, name="processa_formulario"),
    path("processa_formulario_compra/", views.processa_formulario_compra, name="processa_formulario_compra"),
    ]


