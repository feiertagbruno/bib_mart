from django.shortcuts import render
from bibm.models import Livro, Anotacao, Historico
from django.db.models import Q, Max
from utils.functions import get_queryset_filtro_letra

def minhas_anotacoes(request, filtro):

    termo_busca = request.GET.get("q", "").strip()
    ordem_alfabetica_lista = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p",
                              "q","r","s","t","u","v","w","x","y","z","0-9..."]
    filtros = {
        "lidos": "Lidos", 
        "todos": "Todos", 
        "naolidos": "Não lidos", 
        "lidoeleriadenovo": "Lido e Leria de novo"
    }
    if termo_busca == "":
        if filtro[:5] == "todos":
            meus_livros = Livro.objects.all().annotate(
                ultima_anotacao=Max("anotacao__data_inclusao")
            ).order_by("-ultima_anotacao")
            filtro_letra = filtro[5:]
            filtro = "todos"
        if filtro[:8] == "naolidos":
            meus_livros = Livro.objects.filter(lido=False).annotate(
                ultima_anotacao=Max("anotacao__data_inclusao")
            ).order_by("-ultima_anotacao")
            filtro_letra = filtro[8:]
            filtro = "naolidos"
        elif filtro[:5] == "lidos":
            meus_livros = Livro.objects.filter(Q(Q(lido=True)|Q(lendo=True))).annotate(
                ultima_anotacao=Max("anotacao__data_inclusao")
            ).order_by("-ultima_anotacao")
            filtro_letra = filtro[5:]
            filtro = "lidos"
        elif filtro[:16] == "lidoeleriadenovo":
            meus_livros = Livro.objects.filter(lido=True, leria_de_novo=True).annotate(
                ultima_anotacao=Max("anotacao__data_inclusao")
            ).order_by("-ultima_anotacao")
            filtro_letra = filtro[16:]
            filtro = "lidoeleriadenovo"

        if len(filtro_letra) == 1 or filtro_letra == "0-9...":
            meus_livros = get_queryset_filtro_letra(filtro_letra, meus_livros, "titulo")
    else:
        meus_livros = Livro.objects.filter(Q(
            Q(
                Q(titulo__icontains = termo_busca) |
                Q(editora__icontains = termo_busca) |
                Q(autor__prim_nome__icontains = termo_busca) |
                Q(autor__ult_nome__icontains = termo_busca) |
                Q(genero__genero__icontains = termo_busca) |
                Q(tema__icontains = termo_busca) |
                Q(endereco__codigo__icontains = termo_busca) |
                Q(regiao__regiao__icontains = termo_busca)
            )
        ))
        filtro = filtro_letra = ""

    anotacoes = []
    for livro in meus_livros:
        anot = Anotacao.objects.filter(livro__id=livro.id)
        anotacoes.append((livro, anot))

    context = {
        "filtro": filtro,
        "caller": "minhas_anotacoes",
        "filtros": filtros,
        "ordem_alfabetica_lista": ordem_alfabetica_lista,
        "classe_btn":"btn-azul",
        "anotacoes_livros": anotacoes,
        "filtro_letra": filtro_letra,
    }

    return render(request, "bibm/pages/minhasAnotacoes.html", context)

def historico(request):

    search_term = request.GET.get("q","").strip()
    
    if search_term:
        historicos = Historico.objects.filter(livro__titulo__icontains=search_term)
    else:
        historicos = Historico.objects.all().order_by("-id")

    context = {
        "historicos": historicos
    }

    return render(request, "bibm/pages/historico.html", context)

def historico_de_compra(request, filtro):

    filtros = {
        "todos": "Todos", 
        "naolidos": "Não lidos", 
        "lidos": "Lidos", 
        "lidoeleriadenovo": "Lido e Leria de novo"
    }

    context = {
        "filtros": filtros,
    }

    return render(request, "bibm/pages/historicoDeCompra.html", context)