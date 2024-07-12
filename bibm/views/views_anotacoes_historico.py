from django.shortcuts import render
from bibm.models import Livro, Anotacao, Historico
from django.db.models import Q, Max, F, Value
from utils.functions import get_queryset_filtro_letra, is_integer
from datetime import datetime as dt
from dateparser import parse
from django.db.models.functions import Coalesce
from datetime import datetime

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
                ultima_anotacao_data = Max(Coalesce(F("anotacao__id"),Value(-1))),
            ).order_by("-ultima_anotacao_data")
            filtro_letra = filtro[5:]
            filtro = "todos"
        if filtro[:8] == "naolidos":
            meus_livros = Livro.objects.filter(lido=False).annotate(
                ultima_anotacao_data = Max(Coalesce(F("anotacao__id"),Value(-1))),
            ).order_by("-ultima_anotacao_data")
            filtro_letra = filtro[8:]
            filtro = "naolidos"
        elif filtro[:5] == "lidos":
            meus_livros = Livro.objects.filter(Q(Q(lido=True)|Q(lendo=True))).annotate(
                ultima_anotacao_data = Max(Coalesce(F("anotacao__id"),Value(-1))),
            ).order_by("-ultima_anotacao_data")
            filtro_letra = filtro[5:]
            filtro = "lidos"
        elif filtro[:16] == "lidoeleriadenovo":
            meus_livros = Livro.objects.filter(lido=True, leria_de_novo=True).annotate(
                ultima_anotacao_data = Max(Coalesce(F("anotacao__id"),Value(-1))),
            ).order_by("-ultima_anotacao_data")
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
        anot = Anotacao.objects.filter(livro__id=livro.id).order_by("-id")
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
    historico_id_livro = request.GET.get("historico_id")
    if is_integer(historico_id_livro):
        historico_id_livro = int(historico_id_livro)
    
    if search_term:
        historicos = Historico.objects.filter(livro__titulo__icontains=search_term).order_by("-data_fim")
    else:
        historicos = Historico.objects.all().order_by("-data_fim")

    anotacoes = None

    if historico_id_livro:
        livro_id = request.GET.get("livro_id")
        if is_integer(livro_id):
            livro_id = int(livro_id)
        data_ini = request.GET.get("data_ini")
        if data_ini:
            data_ini = parse(data_ini)
        data_fim = request.GET.get("data_fim")
        if data_fim == "None" or not data_fim:
            data_fim = datetime.now()
        else:
            data_fim = parse(data_fim)

        anotacoes = Anotacao.objects.filter(Q(
            Q(livro = livro_id),
            Q(data_inclusao__gte = data_ini) |
            Q(data_inclusao__lte = data_fim)
        )).order_by("-id")

    context = {
        "historicos": historicos,
        "historico_id_livro": historico_id_livro,
        "anotacoes": anotacoes,
        "search_term": search_term,
        "caller": "historico"
    }

    return render(request, "bibm/pages/historico.html", context)

def historico_de_compra(request, filtro, ordem):

    filtros = {
        "todos": "Todos", 
        "naolidos": "Não lidos", 
        "lidos": "Lidos", 
        "lidoeleriadenovo": "Lido e Leria de novo"
    }

    ordens = {
        "descrescente": "Descrescente",
        "crescente": "Crescente",
    }

    if filtro == "todos":
        historico = Livro.objects.all()
    elif filtro == "naolidos":
        historico = Livro.objects.filter(lido=False)
    elif filtro == "lidos":
        historico = Livro.objects.filter(lido=True)
    elif filtro == "lidoeleriadenovo":
        historico = Livro.objects.filter(lido=True,leria_de_novo=True)
    
    if ordem == "crescente":
        historico = historico.order_by("data_compra")
    elif ordem == "descrescente":
        historico = historico.order_by("-data_compra")

    context = {
        "filtros": filtros,
        "filtro": filtro,
        "classe_btn": "btn-verde",
        "caller": "historico_de_compra",
        "ordens": ordens,
        "ordem": ordem,
        "historico": historico,
    }

    return render(request, "bibm/pages/historicoDeCompra.html", context)