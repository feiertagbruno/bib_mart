from django.shortcuts import render
from bibm.models import Endereco, Livro
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

def mapa_da_bibli(request):

    search_term = request.GET.get("q","")
    if search_term != "":
        enderecos = Endereco.objects.filter(Q(
            Q(codigo__icontains=search_term) |
            Q(descricao__icontains=search_term)
        ))
    else:
        enderecos = Endereco.objects.all()
    
    enderecos_dict = {}
    if enderecos.exists():
        for endereco in enderecos:
            livro_lista = []
            livros_endereco = Livro.objects.filter(endereco__codigo = endereco.codigo)
            for livro in livros_endereco:
                livro_lista.append((livro.id, livro.titulo))
            enderecos_dict[endereco.codigo] = ((endereco.id, endereco.descricao),livro_lista)

    if search_term == "" or search_term.lower() in "sem endereço":
        livro_lista = []
        livros_endereco = Livro.objects.filter(endereco = None)
        for livro in livros_endereco:
            livro_lista.append((livro.id, livro.titulo))
        enderecos_dict["Sem endereço"] = ((None ,None),livro_lista)

    if not enderecos_dict:
        messages.info(request,"Sua busca retornou sem resultados.")

    context = {
        "enderecos": enderecos_dict,
        "mapa_da_bibli": True,
    }

    return render(request, "bibm/pages/mapaDaBibli.html",context)

def enderecar_livro(request):
    if request.method == "POST":
        livro = Livro.objects.filter(id = request.POST.get("livro_id_form")).first()
        endereco = Endereco.objects.filter(id = request.POST.get("endereco_id_form")).first()
        livro.endereco = endereco
        livro.save()
    return HttpResponseRedirect(reverse("bibm:mapa_da_bibli"))