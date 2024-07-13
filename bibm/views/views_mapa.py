from django.shortcuts import render
from bibm.models import Endereco, Livro
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from bibm.forms import EnderecoForm
import re

def mapa_da_bibli(request):

    search_term = request.GET.get("q","")
    if search_term != "":
        guia = request.session.get("guia",0)
        if guia == 0:
            
            if request.session.get("enderecos"):
                del(request.session["enderecos"])

            codigo_endereco_livro = Livro.objects.filter(titulo__icontains=search_term,deletado=False).first()

            if codigo_endereco_livro:
                try:
                    codigo_endereco_livro = codigo_endereco_livro.endereco.codigo
                except AttributeError:
                    codigo_endereco_livro = ""
            else:
                codigo_endereco_livro = ""

            try:
                enderecos = Endereco.objects.filter(Q(
                    Q(
                        Q(codigo__icontains=search_term) |
                        Q(descricao__icontains=search_term) |
                        Q(codigo = codigo_endereco_livro)
                    ), Q(deletado=False)
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
                
        elif guia == 1:
            enderecos_string = request.session["enderecos"]
            enderecos_list = enderecos_string.split("|")

            codigo_endereco_livro = Livro.objects.filter(titulo__icontains=search_term,deletado=False).first()
            
            if codigo_endereco_livro:
                try:
                    codigo_endereco_livro = codigo_endereco_livro.endereco.codigo
                except AttributeError:
                    codigo_endereco_livro = ""
            else:
                codigo_endereco_livro = ""
            
            try:
                enderecos = Endereco.objects.filter(Q(
                    Q(
                        Q(codigo__icontains=search_term) |
                        Q(descricao__icontains=search_term) |
                        Q(codigo = codigo_endereco_livro)
                    ), Q(deletado=False)
                ))
            except AttributeError:
                enderecos = Endereco.objects.none()

            if enderecos.exists():
                del(request.session["guia"])

            enderecos = enderecos.union(
                Endereco.objects.filter(id__in=enderecos_list,deletado=False)
            )

            if enderecos.exists():
                enderecos_list = list(enderecos.values_list("id", flat=True))
                enderecos_string = ""
                
                for end in enderecos_list:
                    if not enderecos_string:
                        enderecos_string = str(end)
                    else:
                        enderecos_string += "|" + str(end)

                request.session["enderecos"] = enderecos_string

    elif request.session.get("funcao_enderecar") and request.session.get("enderecos") != "|se":

        enderecos_string = request.session["enderecos"]
        l = len(enderecos_string) - 3
        
        if enderecos_string.count("|se") == 0:
            search_term = "escapa_sem_endereco"
            enderecos_string = enderecos_string.replace("|se", "")
            enderecos_list = enderecos_string.split("|")
        else:
            enderecos_list = enderecos_string[:l].split("|")

        enderecos = Endereco.objects.filter(id__in=enderecos_list,deletado=False)
        del(request.session["funcao_enderecar"])

    else:
        enderecos = Endereco.objects.filter(deletado=False).order_by("codigo")
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
            livros_endereco = Livro.objects.filter(endereco__codigo = endereco.codigo,deletado=False)
            for livro in livros_endereco:
                livro_lista.append((livro.id, livro.titulo))
            enderecos_dict[endereco.codigo] = ((endereco.id, endereco.descricao),livro_lista)

    if search_term == "" or search_term.lower() in "sem endereço":

        livro_lista = []
        livros_endereco = Livro.objects.filter(endereco = None,deletado=False)

        for livro in livros_endereco:
            livro_lista.append((livro.id, livro.titulo))

        enderecos_dict["Sem endereço"] = ((None ,None),livro_lista)

        # fazer isso para tratar a pesquisa de endereço que não retorna os sem endereço
        if search_term.lower() in "sem endereço" and search_term != "":
            if guia == 0:
                request.session["sem_endereco"] = True

        if request.session.get("enderecos"):
            if request.session["enderecos"][(len(request.session["enderecos"])-3):] != "|se":
                request.session["enderecos"] = request.session["enderecos"] + "|se"
        else:
            request.session["enderecos"] = "|se"

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
            endereco = Endereco.objects.filter(id = endereco_id,deletado=False).first()
            livro.endereco = endereco
        else:
            livro.endereco = None
        livro.save()

    request.session["funcao_enderecar"] = True
    if request.session.get("guia"):
        del(request.session["guia"])

    return HttpResponseRedirect(reverse("bibm:mapa_da_bibli"))

def editar_endereco(request, endereco_id):

    form = EnderecoForm(instance= Endereco.objects.filter(id=endereco_id,deletado=False).first())
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
        endereco.deletado = True
        endereco.save()

        if endereco.deletado:
            messages.info(request, "Endereço excluído.")

            livros = Livro.objects.filter(endereco=endereco)
            for livro in livros:
                livro.endereco = None
                livro.save()

        return HttpResponseRedirect(reverse("bibm:mapa_da_bibli"))
    else:
        return Http404