from django.db.models import query_utils
from django.http.response import HttpResponseRedirect
from .models import Compra, Produto, ProdutoCompra
from django.views.generic import DetailView, ListView
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib import messages

#Usado para garantir que a integridade da url
import re

# ListView sera usado para listar o historico de compras. Já o DetailView para detalhar cada uma delas.
class CompraListView(ListView):
    model = Compra
class CompraDetailView(DetailView):
    model = Compra

# Pagina inicial
def view_index(request):
    return render(request, "wpensar/index.html")

# Processamento do formulario que adiciona novos produtos
def processa_formulario(request):
    nome = request.POST.get('name')
    #Se o produto tem até 20 caracteres
    if(len(nome)<20):
        produto = Produto(name=nome)
        try:
            produto.save()
        except IntegrityError:
            messages.info(request, 'Produto já existente.')
            return HttpResponseRedirect('/adicionar_produtos/')
        messages.info(request, 'Produto adicionado com sucesso!')
        return HttpResponseRedirect('/adicionar_produtos/')
    else:
        messages.info(request, 'Produto invalido.')
        return HttpResponseRedirect('/adicionar_produtos/')

# Pagina: Adicionar novos produtos
def adicionar_produtos(request):
    return render(request, "wpensar/adicionar_produtos.html")

# Pagina: Nova compra
def nova_compra(request):
    # Enviando dados dos produtos
    query_results = Produto.objects.all()
    context = {'query_results' : query_results}
    return render(request, "wpensar/nova_compra.html", context)

# Processamento do formulario que adiciona novas compras
def processa_formulario_compra(request):
    nome = request.POST.get('name')
    valorTotal = request.POST.get('valorTotal')
    #Garante que so tenha numeros
    valorTotal = re.sub('[^0-9,]', "", valorTotal).replace(",", ".")
    #Confere se o nome da compra tem até 20 caracteres e se o nome eo valorTotal sao nulos.
    if(len(nome)<20 and valorTotal!="" and nome!=""):
        compra = Compra(name=nome, valorTotal=valorTotal, slug="compra_"+re.sub('[^A-Za-z0-9]', '', str(nome)))
        #Confere a unicidade do nome da compra
        try:
            compra.save()
        except IntegrityError:
            messages.info(request, 'Identificacao de compra indisponivel.')
            return HttpResponseRedirect('/nova_compra/')
        aux=1
        #A cada produto:
        for a in Produto.objects.all():
            #Garante integridade das quantidades dos produtos enviadas no formulario
            quanti = request.POST.get('produto_'+str(aux))
            quanti = re.sub('[^0-9,]', "", quanti).replace(",", ".")
            if(quanti==""):
                quanti="0"
            #Salva na BS as quantidades dos Produtos da compra em questao, a partir dos ProdutosCompra
            produtocompra = ProdutoCompra(produto=Produto.objects.filter(id=a.id).first(), compra=Compra.objects.filter(name=nome).first(), quantidade=quanti)
            aux+=1
            produtocompra.save()
        messages.info(request, 'Compra adicionada com sucesso!')
        return HttpResponseRedirect('/nova_compra/')
    else:
        messages.info(request, 'Compra invalida.')
        return HttpResponseRedirect('/nova_compra/')