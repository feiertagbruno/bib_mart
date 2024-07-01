from django.shortcuts import render
from bibm.models import Endereco, Livro
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from bibm.forms import EnderecoForm

def mapa_da_bibli(request):

    search_term = request.GET.get("q","")
    if search_term != "":
        guia = request.session.get("guia",0)
        if guia == 0:
            try:
                enderecos = Endereco.objects.filter(Q(
                    Q(codigo__icontains=search_term) |
                    Q(descricao__icontains=search_term) |
                    Q(
                        codigo = Livro.objects.filter(titulo__icontains = search_term).first().endereco.codigo
                    )
                ))
            except AttributeError:
                enderecos = Endereco.objects.none()

            if enderecos.exists():
                enderecos_list = list(enderecos.values_list("id", flat=True))
                enderecos_string = ""
                
                for end in enderecos_list:
                    if not enderecos_string:
                        enderecos_string = str(end)
                    else:
                        enderecos_string += "|" + str(end)
                request.session["enderecos"] = enderecos_string
                guia += 1
                request.session["guia"] = guia

            if request.session.get("sem_endereco"):
                search_term = "sem endereço"
                del(request.session["sem_endereco"])
                if request.session.get("guia"):
                    del(request.session["guia"])
                if request.session.get("enderecos"):
                    del(request.session["enderecos"])
                
        elif guia == 1:
            enderecos_string = request.session["enderecos"]
            enderecos_list = enderecos_string.split("|")
            try:
                enderecos = Endereco.objects.filter(Q(
                    Q(codigo__icontains=search_term) |
                    Q(descricao__icontains=search_term) |
                    Q(
                        codigo = Livro.objects.filter(titulo__icontains = search_term).first().endereco.codigo
                    )
                ))
            except AttributeError:
                enderecos = Endereco.objects.none()
            if enderecos.exists():
                del(request.session["guia"])
                del(request.session["enderecos"])
            enderecos = enderecos.union(
                Endereco.objects.filter(id__in=enderecos_list)
            )
        
    else:
        enderecos = Endereco.objects.all()
        if request.session.get("guia", None):
            del(request.session["guia"])
        if request.session.get("enderecos", None):
            del(request.session["enderecos"])
        if request.session.get("sem_endereco", None):
            del(request.session["sem_endereco"])
    
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
        # fazer isso para tratar a pesquisa de endereço que não retorna os sem endereço
        if search_term.lower() in "sem endereço" and search_term != "":
            if guia == 0:
                request.session["sem_endereco"] = True

    if not enderecos_dict:
        messages.info(request,"Sua busca retornou sem resultados.")

    context = {
        "enderecos": enderecos_dict,
        "mapa_da_bibli": True,
        "caller": "mapa_da_bibli",
    }

    return render(request, "bibm/pages/mapaDaBibli.html",context)

def enderecar_livro(request):
    if request.method == "POST":
        livro = Livro.objects.filter(id = request.POST.get("livro_id_form")).first()
        endereco_id = request.POST.get("endereco_id_form")
        if endereco_id != "None":
            endereco = Endereco.objects.filter(id = endereco_id).first()
            livro.endereco = endereco
        else:
            livro.endereco = None
        livro.save()
    return HttpResponseRedirect(reverse("bibm:mapa_da_bibli"))

def editar_endereco(request, endereco_id):

    form = EnderecoForm(instance= Endereco.objects.filter(id=endereco_id).first())
    caller = request.GET.get("caller", None)

    context = {
        "form": form,
        "caller": caller,
        "endereco_id": endereco_id,
    }

    return render(request, "bibm/pages/addUmEndereco.html", context)

def deletar_endereco(request):
    if request.method == "POST":
        endereco = Endereco.objects.get(id=request.POST.get("endereco_id"))
        endereco.delete()
        return HttpResponseRedirect(reverse("bibm:mapa_da_bibli"))
    else:
        return Http404