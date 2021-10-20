from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.urls import reverse

class Produto(models.Model):
    name = models.CharField(max_length=255, help_text='Digite o nome do produto.', unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Compra(models.Model):
    name = models.CharField(max_length=255, help_text='Digite o nome identificador da compra.', unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    produtos = ManyToManyField(Produto, through='ProdutoCompra', blank=True)
    valorTotal = models.FloatField()
    slug = models.SlugField(max_length=255, unique=True)
    def __str__(self):
        return self.name

    #Retorna a URL da compra
    def get_absolute_url(self):
        return reverse("wpensar:detail", kwargs={"slug": self.slug})
    
    #Orderna as compras da mais nova para a mais antiga
    class Meta:
        ordering = ("-created",) 
    
    #Calculo do preco medio de cada compra.
    def precomedio(self): 
        quantprodutos=0
        for a in ProdutoCompra.objects.filter(compra_id=self.id):
            quantprodutos += a.quantidade
        if(quantprodutos<=0):
            return 0
        return self.valorTotal / quantprodutos

    #Retorna a quantidade de cada produto na compra
    def quant(self):
        def aux(ID):
            for b in ProdutoCompra.objects.filter(compra_id=self.id).filter(produto_id=ID):
                return str(b.quantidade)
        frase = ""
        for a in self.produtos.all():
            frase += "Quantidade de " + a.name + "s: " + aux(a.id) + " un.<br>"
        return frase

# Classe auxiliar onde é guardado a quantidade de produtos por compra.
class ProdutoCompra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    quantidade = models.IntegerField(null=True,blank=True)
