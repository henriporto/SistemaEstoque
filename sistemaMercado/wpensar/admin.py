from django.contrib import admin

from .models import Compra
from .models import Produto
from .models import ProdutoCompra

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display=("name", "author", "created")

class ProdutoCompraInline(admin.TabularInline):
    model = ProdutoCompra
    extra = 2

class CompraAdmin(admin.ModelAdmin):
    inlines = (ProdutoCompraInline,)

admin.site.register(Compra, CompraAdmin)