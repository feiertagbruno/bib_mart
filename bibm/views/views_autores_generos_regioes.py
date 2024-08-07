from django.shortcuts import render
from bibm.models import Autor, Livro, Regiao, Genero
from django.db.models.functions import Concat
from django.db.models import Value, Q
from utils.functions import get_ordem_alfabetica_lista, get_queryset_filtro_letra
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from bibm.views.views_all import zerar_session

def autores(request, filtro):

    ordem_lista = [
        ("sobrenome", "Sobrenome"),
        ("primeironome", "Primeiro nome"),
        ("regiao", "Região"),
    ]

    ordem_alfabetica_lista = get_ordem_alfabetica_lista()

    if filtro[:9] == "sobrenome":
        autores = Autor.objects.filter(deletado=False).annotate(
            nome=Concat("ult_nome", Value(", "), "prim_nome")
            ).order_by("nome")
        filtro_letra = filtro[9:]
        filtro = "sobrenome"
    elif filtro[:12] == "primeironome":
        autores = Autor.objects.filter(deletado=False).annotate(
            nome=Concat("prim_nome", Value(" "), "ult_nome")
            ).order_by("nome")
        filtro_letra = filtro[12:]
        filtro = "primeironome"
    elif filtro[:6] == "regiao":
        autores = {}
        for regiao in Regiao.objects.filter(
            id__in = Autor.objects.filter(deletado=False).values("regiao__id").distinct(),
            deletado=False
        ).order_by("regiao"):
            autores[regiao.regiao] = Autor.objects.filter(regiao__id=regiao.id,deletado=False).annotate(
                nome=Concat("prim_nome", Value(" "), "ult_nome")
                ).order_by("nome")
        filtro_letra = filtro[6:]
        filtro = "regiao"

    if len(filtro_letra) == 1 or filtro_letra == "0-9...":
        autores = get_queryset_filtro_letra(filtro_letra, autores, "nome")
    
    caller = request.GET.get("caller")
    livros = None
    autor_id_livro = request.GET.get("autor_id")
    if request.session.get("autor_id"):
        if not autor_id_livro:
            autor_id_livro = request.session.get("autor_id")
        del(request.session["autor_id"])
    
    if autor_id_livro is not None: autor_id_livro = int(autor_id_livro)
    
    quantos_livros = 0
    
    if caller == "buscar_livros" or autor_id_livro:
        livros = Livro.objects.filter(
            autor__id= autor_id_livro,deletado=False
        ).values_list("titulo", "endereco__codigo").order_by("titulo")

        quantos_livros = livros.filter(
            Q(Q(endereco__presencial = True) |
            Q(endereco = None))
        ).count()

        # quantos_livros = livros.count()

    context = {
        "autores": autores,
        "filtro": filtro,
        "ordem_lista": ordem_lista,
        "caller":"autores",
        "ordem_alfabetica_lista": ordem_alfabetica_lista,
        "filtro_letra": filtro_letra,
        "livros": livros,
        "autor_id_livro": autor_id_livro,
        "quantos_livros": quantos_livros,
    }

    request = zerar_session(request)

    return render(request, "bibm/pages/autores.html", context)

def deletar_autor(request):

    if request.method != "POST":
        return Http404
    
    autor_default = Autor.objects.get(id=Livro._meta.get_field("autor").default)
    
    filtro = request.POST.get("filtro")
    autor = Autor.objects.get(id = request.POST.get("autor_id"))
    autor.deletado = True
    autor.ult_nome += "#"
    autor.save()

    if autor.deletado:
        messages.info(request, "Autor excluído com sucesso.")
        livros = Livro.objects.filter(autor=autor)
        for livro in livros:
            livro.autor = autor_default
            livro.save()

    return HttpResponseRedirect(reverse("bibm:autores", kwargs={"filtro":filtro}))

def regioes(request):

    regioes = Regiao.objects.filter(deletado=False).order_by("regiao")

    regiao_id_livro = request.GET.get("regiao_id")
    if not regiao_id_livro:
        regiao_id_livro = request.session.get("regiao_id")
        if regiao_id_livro:
            del(request.session["regiao_id"])
    if regiao_id_livro: regiao_id_livro = int(regiao_id_livro)
    
    regiao_livros = None
    quantos_livros = 0

    if regiao_id_livro:
        regiao_livros = Livro.objects.filter(regiao__id=regiao_id_livro,deletado=False).order_by("titulo")

        quantos_livros = regiao_livros.filter(
            Q(Q(endereco__presencial = True) |
            Q(endereco = None))
        ).count()

        # quantos_livros = regiao_livros.count()

    context = {
        "caller": "regioes",
        "regioes": regioes,
        "regiao_id_livro": regiao_id_livro,
        "regiao_livros": regiao_livros,
        "quantos_livros": quantos_livros,
    }

    return render(request, "bibm/pages/regioes.html", context)

def regioes_deletar(request):
    
    if request.method != "POST":
        return Http404
    
    regiao_default_livro = Regiao.objects.get(id=Livro._meta.get_field("regiao").default)
    regiao_default_autor = Regiao.objects.get(id=Autor._meta.get_field("regiao").default)
    
    regiao = Regiao.objects.get(id=request.POST.get("regiao_id"))
    regiao.deletado = True
    regiao.regiao += "#"
    regiao.save()

    if regiao.deletado:
        messages.info(request, "Região excluída.")

        livros = Livro.objects.filter(regiao=regiao)
        for livro in livros:
            livro.regiao = regiao_default_livro
            livro.save()
        
        autores = Autor.objects.filter(regiao=regiao)
        for autor in autores:
            autor.regiao = regiao_default_autor
            autor.save()

    return HttpResponseRedirect(reverse("bibm:regioes"))

def generos(request):

    generos = Genero.objects.filter(deletado=False).order_by("genero")

    genero_id_livro = request.GET.get("genero_id")
    if not genero_id_livro:
        genero_id_livro = request.session.get("genero_id")
        if genero_id_livro:
            del(request.session["genero_id"])
    if genero_id_livro: genero_id_livro = int(genero_id_livro)
    
    genero_livros = None
    quantos_livros = 0

    if genero_id_livro:
        genero_livros = Livro.objects.filter(genero__id=genero_id_livro,deletado=False).order_by("titulo")
        quantos_livros = genero_livros.filter(
            Q(Q(endereco__presencial = True) |
            Q(endereco = None))
        ).count()
        # quantos_livros = genero_livros.count()
    

    context = {
        "caller": "generos",
        "generos": generos,
        "genero_id_livro": genero_id_livro,
        "genero_livros": genero_livros,
        "quantos_livros": quantos_livros,
    }

    return render(request, "bibm/pages/generos.html", context)

def generos_deletar(request):
    
    if request.method != "POST":
        return Http404
    
    genero_default = Genero.objects.get(id=Livro._meta.get_field("genero").default)
    
    genero = Genero.objects.get(id=request.POST.get("genero_id"))
    genero.deletado = True
    genero.genero += "#"
    genero.save()

    if genero.deletado:
        messages.info(request, "Gênero excluído.")
        livros = Livro.objects.filter(genero=genero)
        for livro in livros:
            livro.genero = genero_default
            livro.save()

    return HttpResponseRedirect(reverse("bibm:generos"))