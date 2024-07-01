from bibm.forms import LivroForm, AutorForm, RegiaoForm, GeneroForm, EnderecoForm
from bibm.models import Livro, Endereco
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .views_all import context_add_um_livro
from django.core.exceptions import ValidationError
import json

def add_um_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST)
        if form.is_valid():
            livro_salvo = form.save()
            if livro_salvo:
                messages.success(request,"Livro salvo com sucesso.")
        else:
            for er in form.errors.items():
                messages.error(request, f"{er[0].capitalize()} - {er[1][0]}")
            request.session["info_livro"] = request.POST
            return HttpResponseRedirect(reverse("bibm:add_um_livro"))
    
    info_livro = request.session.get("info_livro")
    if info_livro:
        del(request.session["info_livro"])

    autor_salvo = request.session.get("autor_salvo")
    if autor_salvo:
        del(request.session["autor_salvo"])
    
    regiao_salva = request.session.get("regiao_salva")
    if regiao_salva:
        del(request.session["regiao_salva"])

    genero_salvo = request.session.get("genero_salvo")
    if genero_salvo:
        del(request.session["genero_salvo"])
    
    endereco_salvo = request.session.get("endereco_salvo")
    if endereco_salvo:
        del(request.session["endereco_salvo"])
    
    form = LivroForm(initial=info_livro)
    context = context_add_um_livro()

    if form:
        context.update({
            "form":form, 
            "add_um_livro":True,
            "autor_salvo": autor_salvo,
            "regiao_salva": regiao_salva,
            "genero_salvo": genero_salvo,
            "endereco_salvo": endereco_salvo,
        })
        
    return render(request, "bibm/pages/addUmLivro.html", context)

def editar_um_livro(request, livro_id):

    livro = Livro.objects.filter(id=livro_id).first()
    caller = request.GET.get("caller")
    filtro = request.GET.get("filtro")

    form = LivroForm(instance=livro)
    if form.instance.data_compra:
        form.initial["data_compra"] = form.initial["data_compra"].strftime("%Y-%m-%d")
    if form.instance.data_leitura:
        form.initial["data_leitura"] = form.initial["data_leitura"].strftime("%Y-%m-%d")

    context = {
        "form": form,
        "livro_id":livro_id,
        "add_um_livro": True,
        "editar_um_livro":True,
        "caller":caller,
        "filtro":filtro,
    }

    context.update({
        **context_add_um_livro()
    })
    return render(request,"bibm/pages/addUmLivro.html", context)

def editar_um_livro_save(request):
    
    livro_id = request.POST.get("livro_id")
    caller = request.POST.get("caller")
    filtro = request.POST.get("filtro")

    livro = Livro.objects.filter(id=livro_id).first()
    livro_lido = livro.lido

    form = LivroForm(instance=livro, data=request.POST)
    if form.is_valid():
        livro_form = form.save(commit=False)
        if livro_lido and not livro_form.lido:
            livro_form.classificacao = None
            livro_form.data_leitura = None
            livro_form.leria_de_novo = False
        livro_form.save()
        messages.success(request, "Livro alterado com sucesso.")
    else:
        for er in form.errors.items():
            messages.error(request, f"{er[0].capitalize()} - {er[1][0]}")

    if caller == "meus_livros":
        return HttpResponseRedirect(reverse("bibm:meus_livros", kwargs={"filtro": filtro}))
    elif caller == "editar_planejamento":
        return HttpResponseRedirect(reverse("bibm:editar_planejamento", kwargs={"filtro": filtro}))

def deletar_um_livro(request):
    if request.method == "POST":
        filtro = request.POST.get("filtro")
        livro_id = request.POST.get("livro_id")
        if livro_id:
            livro = Livro.objects.filter(id=livro_id).first()
            if livro:
                livro.delete()

        if livro.id == None and livro != None:
            messages.info(request, "Livro deletado com sucesso.")
        else:
            raise ValidationError("Houve um erro durante a deleção.")
    else:
        messages.error(request, "O livro não foi deletado")
    return HttpResponseRedirect(reverse("bibm:meus_livros", kwargs={"filtro":filtro}))

def add_um_autor_livro(request):
    request.session["info_livro"] = request.POST
    
    regiao_salva = request.session.get("regiao_salva")
    if regiao_salva:
        del(request.session["regiao_salva"])

    form = AutorForm()

    context = {
        "form":form,
        **context_add_um_livro(autores=False,generos=False,enderecos=False),
        "add_um_autor_livro":True,
        "regiao_salva": regiao_salva,
    }

    return render(request, "bibm/pages/addUmAutor.html", context)

def add_um_autor_livro_save(request):
    if request.method == "POST":
        
        caller = request.POST.get("caller", None)
        form = AutorForm(data = request.POST)

        if form.is_valid():
            autor_salvo = form.save()
            request.session["autor_salvo"] = autor_salvo.id
            request.session["regiao_salva"] = autor_salvo.regiao.id
            messages.success(request,"Autor salvo.")
        else:
            for er in form.errors.items():
                messages.error(request, f"{er[0].capitalize()} - {er[1][0]}")
        
        return HttpResponseRedirect(reverse("bibm:add_um_livro"))
    else:
        return Http404
    
def add_uma_regiao_livro(request):
    if request.method == "POST":

        request.session["info_livro"] = request.POST
        request.session["caller_regiao"] = request.POST.get("caller_regiao")
        
        form = RegiaoForm()

        context = {
            "form":form,
        }

        return render(request, "bibm/pages/addUmaRegiao.html", context)
    else:
        return Http404

def add_uma_regiao_livro_save(request):
    if request.method == "POST":
        
        caller_regiao = request.session.get("caller_regiao", None)
        if caller_regiao:
            del(request.session["caller_regiao"])

        form = RegiaoForm(data = request.POST)

        if form.is_valid():
            regiao_salva = form.save()
            request.session["regiao_salva"] = regiao_salva.id
            messages.success(request,"Região salva.")
        else:
            for er in form.errors.items():
                messages.error(request, f"{er[0].capitalize()} - {er[1][0]}")

        
        if caller_regiao == "add_um_autor":
            return HttpResponseRedirect(reverse("bibm:add_um_autor_livro"))
        else:
            return HttpResponseRedirect(reverse("bibm:add_um_livro"))
    else:
        return Http404
    
def add_um_genero_livro(request):
    if request.method == "POST":
        request.session["info_livro"] = request.POST
        
        form = GeneroForm()

        context = {
            "form":form,
        }

        return render(request, "bibm/pages/addUmGenero.html", context)
    else:
        return Http404

def add_um_genero_livro_save(request):
    if request.method == "POST":
        
        form = GeneroForm(data = request.POST)

        if form.is_valid():
            genero_salvo = form.save()
            request.session["genero_salvo"] = genero_salvo.id
            messages.success(request,"Gênero salvo.")
        else:
            for er in form.errors.items():
                messages.error(request, f"{er[0].capitalize()} - {er[1][0]}")
        
        return HttpResponseRedirect(reverse("bibm:add_um_livro"))
    else:
        return Http404
    
def add_um_endereco_livro(request):
    if request.method == "POST":
        request.session["info_livro"] = request.POST
        caller = request.POST.get("caller", None)
        
        form = EnderecoForm()

        context = {
            "form":form,
            "caller":caller,
        }

        return render(request, "bibm/pages/addUmEndereco.html", context)
    else:
        return Http404

def add_um_endereco_livro_save(request):
    if request.method == "POST":
        
        caller= request.POST.get("caller", None)
        endereco_id = request.POST.get("endereco_id")
        if endereco_id:
            form = EnderecoForm(
                instance = Endereco.objects.get(id=endereco_id),
                data = request.POST
            )
        else:
            form = EnderecoForm(data = request.POST)

        if form.is_valid():
            endereco_salvo = form.save()
            request.session["endereco_salvo"] = endereco_salvo.id
            messages.success(request,"Endereço salvo.")
        else:
            for er in form.errors.items():
                messages.error(request, f"{er[0].capitalize()} - {er[1][0]}")
        
        if caller == "mapa_da_bibli":
            return HttpResponseRedirect(reverse("bibm:mapa_da_bibli"))
        else:
            return HttpResponseRedirect(reverse("bibm:add_um_livro"))
    else:
        return Http404
