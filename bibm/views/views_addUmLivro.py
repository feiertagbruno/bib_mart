from bibm.forms import LivroForm, AutorForm, RegiaoForm, GeneroForm, EnderecoForm
from bibm.models import Livro, Endereco, Autor, Regiao, Genero, Historico
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .views_all import context_add_um_livro
from django.core.exceptions import ValidationError
from utils.functions import list_para_string
from bibm.views.views_all import acrescentar_plan

def criar_historico(livro):
    historico = Historico.objects.create(**{
        "livro":livro,
        "data_ini":livro.data_leitura,
        "data_fim":livro.data_leitura,
        "terminou": True,
        "classificacao":livro.classificacao
    })
    return historico

def add_um_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST)
        if form.is_valid():
            livro_salvo = form.save()
            if livro_salvo.id:
                messages.success(request,"Livro salvo com sucesso.")
                if form.cleaned_data.get("acrescentar_no_planejamento"):
                    acrescentar_plan(livro_salvo.id)
                if livro_salvo.lido:
                    criar_historico(livro_salvo)
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
    
    if request.session.get("caller_regiao"):
        del(request.session["caller_regiao"])
    
    relacao_autor_regiao = list_para_string(
        Autor.objects.filter(deletado=False).values_list("id", "regiao__id"),
        "|",
        "-"
    )
    
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
            "relacao_autor_regiao": relacao_autor_regiao,
        })
        
    return render(request, "bibm/pages/addUmLivro.html", context)

def editar_um_livro(request, livro_id):

    livro = Livro.objects.get(id=livro_id)
    caller = request.GET.get("caller")
    filtro = request.GET.get("filtro")
    ordem = request.GET.get("ordem")

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
        "ordem": ordem,
    }

    context.update({
        **context_add_um_livro()
    })
    return render(request,"bibm/pages/addUmLivro.html", context)

def editar_um_livro_save(request):
    
    livro_id = request.POST.get("livro_id")
    caller = request.POST.get("caller")
    filtro = request.POST.get("filtro")
    ordem = request.POST.get("ordem")

    livro = Livro.objects.get(id=livro_id)
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
        return HttpResponseRedirect(reverse("bibm:meus_livros", kwargs={
            "filtro": filtro,
            "ordem": ordem,
        }))
    elif caller == "editar_planejamento":
        return HttpResponseRedirect(reverse("bibm:editar_planejamento", kwargs={
            "filtro": filtro,
            "ordem": ordem,
        }))
    else:
        return HttpResponseRedirect(reverse("bibm:home"))

def deletar_um_livro(request):
    if request.method == "POST":
        filtro = request.POST.get("filtro")
        ordem = request.POST.get("ordem")
        livro_id = request.POST.get("livro_id")
        if livro_id:
            livro = Livro.objects.get(id=livro_id)
            if livro:
                livro.deletado = True
                livro.titulo += "#"
                livro.save()

        if livro.deletado and livro != None:
            messages.info(request, "Livro deletado com sucesso.")
        else:
            raise ValidationError("Houve um erro durante a deleção.")
    else:
        messages.error(request, "O livro não foi deletado")
    return HttpResponseRedirect(reverse("bibm:meus_livros", kwargs={
        "filtro":filtro,
        "ordem": ordem,
    }))

def add_um_autor_livro(request):

    caller_regiao = request.session.get("caller_regiao", None)

    caller = request.GET.get("caller", None)
    if not caller and request.session.get("caller"):
        caller = request.session.get("caller")
        del(request.session["caller"])

    autor_id = request.GET.get("autor_id", None)
    if not autor_id and request.session.get("autor_id"):
        autor_id = request.session.get("autor_id")
        del(request.session["autor_id"])
    if autor_id:
        autor_id = int(autor_id)
    
    filtro = request.GET.get("filtro", None)
    if not filtro and request.session.get("filtro"):
        filtro = request.session.get("filtro")
        del(request.session["filtro"])

    if caller == "autores":
        autor = Autor.objects.get(id= autor_id )

    info_autor = None

    if not caller_regiao and not caller:
        request.session["info_livro"] = request.POST
    elif caller_regiao == "add_um_autor" or caller == "autores_add":
        info_autor = request.session.get("info_autor", None)
        if info_autor:
            del(request.session["info_autor"])
    
    regiao_salva = request.session.get("regiao_salva")
    if regiao_salva:
        del(request.session["regiao_salva"])

    if info_autor:
        form = AutorForm(initial=info_autor)
    elif caller == "autores":
        form = AutorForm(instance=autor)
    else:
        form = AutorForm()

    context = {
        "form":form,
        **context_add_um_livro(autores=False,generos=False,enderecos=False),
        "add_um_autor_livro":True,
        "regiao_salva": regiao_salva,
        "caller": caller,
        "autor_id": autor_id,
        "filtro": filtro,
    }

    return render(request, "bibm/pages/addUmAutor.html", context)

def add_um_autor_livro_save(request):
    if request.method == "POST":
        
        caller = request.POST.get("caller", None)

        if caller == "autores":
            filtro = request.POST.get("filtro", None)
            autor_id = request.POST.get("autor_id", None)
            if autor_id: request.session["autor_id"] = autor_id
            autor = Autor.objects.get(id=autor_id)
            form = AutorForm(instance=autor, data=request.POST)
            if form.is_valid():
                form_save = form.save()
                messages.success(request, "Edição de autor salva com sucesso.")
            return HttpResponseRedirect(reverse("bibm:autores", kwargs={"filtro":filtro}))
        elif caller == "autores_add":
            filtro = request.POST.get("filtro", None)
            form = AutorForm(data=request.POST)
            if form.is_valid():
                form_save = form.save()
                if form_save.id:
                    messages.success(request, "Autor salvo.")
            else:
                for er in form.errors.items():
                    messages.error(request, f"{er[0].capitalize()} - {er[1][0]}")
            return HttpResponseRedirect(reverse("bibm:autores", kwargs={"filtro":filtro}))
        else:
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

        caller_regiao = request.POST.get("caller_regiao")
        request.session["caller_regiao"] = caller_regiao
        caller = request.POST.get("caller")
        autor_id = request.POST.get("autor_id")
        filtro = request.POST.get("filtro")

        if caller_regiao == "add_um_livro":
            request.session["info_livro"] = request.POST
        elif caller_regiao == "add_um_autor":
            request.session["info_autor"] = request.POST
        
        form = RegiaoForm()

        context = {
            "form":form,
            "add_uma_regiao_livro":True,
            "caller": caller,
            "autor_id": autor_id,
            "filtro": filtro,
        }

        return render(request, "bibm/pages/addUmaRegiao.html", context)
    elif request.GET.get("caller") == "regioes_editar":
        caller = request.GET.get("caller")
        regiao_id = request.GET.get("regiao_id")
        regiao = Regiao.objects.get(id = regiao_id)
        form = RegiaoForm(instance=regiao)

        context = {
            "add_uma_regiao_livro": True,
            "caller": caller,
            "form": form,
            "regiao_id": regiao_id,
        }
        return render(request, "bibm/pages/addUmaRegiao.html", context)
    elif request.GET.get("caller") == "regioes_add":
        caller = request.GET.get("caller")
        form = RegiaoForm()
        context = {
            "add_uma_regiao_livro": True,
            "caller": caller,
            "form": form,
        }
        return render(request, "bibm/pages/addUmaRegiao.html", context)
    else:
        return Http404

def add_uma_regiao_livro_save(request):
    if request.method == "POST":
        
        caller_regiao = request.session.get("caller_regiao", None)
        caller = request.POST.get("caller")

        if caller == "regioes_editar":
            regiao_id = request.POST.get("regiao_id")
            if regiao_id:
                request.session["regiao_id"] = regiao_id
            regiao = Regiao.objects.get(id=regiao_id)
            form = RegiaoForm(instance=regiao, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Edição de região salva com sucesso.")
            return HttpResponseRedirect(reverse("bibm:regioes"))
        elif caller == "regioes_add":
            form = RegiaoForm(data=request.POST)
            if form.is_valid():
                form_salvo = form.save()
                if form_salvo.id:
                    messages.success(request, "Região salva.")
                    request.session["regiao_id"] = form_salvo.id
                else:
                    messages.error(request,"A região não foi salva")
                return HttpResponseRedirect(reverse("bibm:regioes"))
            else:
                for er in form.errors.items():
                    messages.error(request, f"{er[0].capitalize()} - {er[1][0]}")
                return HttpResponseRedirect(f"{reverse('bibm:add_uma_regiao_livro')}?caller=regioes_add")
        else:
            if caller:
                request.session["caller"] = caller
                request.session["autor_id"] = request.POST.get("autor_id")
                request.session["filtro"] = request.POST.get("filtro")

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
            "add_um_genero_livro": True,
        }

        return render(request, "bibm/pages/addUmGenero.html", context)
    elif request.GET.get("caller") == "generos_editar":
        caller = "generos_editar"
        genero_id = request.GET.get("genero_id")
        genero = Genero.objects.get(id = genero_id)
        form = GeneroForm(instance=genero)

        context = {
            "add_um_genero_livro": True,
            "caller": caller,
            "form": form,
            "genero_id": genero_id,
        }
        return render(request, "bibm/pages/addUmGenero.html", context)
    elif request.GET.get("caller") == "generos_add":
        caller = request.GET.get("caller")
        form = GeneroForm()
        context = {
            "add_um_genero_livro": True,
            "caller": caller,
            "form": form,
        }
        return render(request, "bibm/pages/addUmGenero.html", context)
    else:
        return Http404

def add_um_genero_livro_save(request):
    if request.method == "POST":
        
        caller = request.POST.get("caller")

        if caller == "generos_editar":
            genero_id = request.POST.get("genero_id")
            if genero_id:
                request.session["genero_id"] = genero_id
            genero = Genero.objects.get(id=genero_id)
            form = GeneroForm(instance=genero, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Edição de gênero salva com sucesso.")
            return HttpResponseRedirect(reverse("bibm:generos"))
        elif caller == "generos_add":
            form = GeneroForm(data=request.POST)
            if form.is_valid():
                form_salvo = form.save()
                if form_salvo.id:
                    messages.success(request, "Gênero salva.")
                    request.session["genero_id"] = form_salvo.id
                else:
                    messages.error(request,"O gênero não foi salvo")
                return HttpResponseRedirect(reverse("bibm:generos"))
            else:
                for er in form.errors.items():
                    messages.error(request, f"{er[0].capitalize()} - {er[1][0]}")
                return HttpResponseRedirect(f"{reverse('bibm:add_um_genero_livro')}?caller=generos_add")
        else:
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
            "add_um_endereco_livro":True,
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
