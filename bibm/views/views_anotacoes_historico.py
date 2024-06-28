from django.shortcuts import render
from bibm.models import Livro, Anotacao, Historico
from django.db.models import Q

def minhas_anotacoes(request, filtro):

    termo_busca = request.GET.get("q", "").strip()
    ordem_alfabetica_lista = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p",
                              "q","r","s","t","u","v","w","x","y","z","0-9..."]
    filtros = {
        "todos": "Todos", 
        "naolidos": "Não lidos", 
        "lidos": "Lidos", 
        "lidoeleriadenovo": "Lido e Leria de novo"
    }
    if termo_busca == "":
        if filtro[:5] == "todos":
            meus_livros = Livro.objects.all().order_by("titulo")
            filtro_letra = filtro[5:]
            filtro = "todos"
        if filtro[:8] == "naolidos":
            meus_livros = Livro.objects.filter(lido=False).order_by("titulo")
            filtro_letra = filtro[8:]
            filtro = "naolidos"
        elif filtro[:5] == "lidos":
            meus_livros = Livro.objects.filter(lido=True).order_by("titulo")
            filtro_letra = filtro[5:]
            filtro = "lidos"
        elif filtro[:16] == "lidoeleriadenovo":
            meus_livros = Livro.objects.filter(lido=True, leria_de_novo=True).order_by("titulo")
            filtro_letra = filtro[16:]
            filtro = "lidoeleriadenovo"

        if len(filtro_letra) == 1:
            if filtro_letra.lower() == "a":
                meus_livros = meus_livros.filter(titulo__regex=r"^[AaÁáÀàÂâÃãÄäÅå]")
            elif filtro_letra.lower() == "e":
                meus_livros = meus_livros.filter(titulo__regex=r"^[EeÈèÉéÊêËë]")
            elif filtro_letra.lower() == "i":
                meus_livros = meus_livros.filter(titulo__regex=r"^[IiÌìÍíÎîÏï]")
            elif filtro_letra.lower() == "o":
                meus_livros = meus_livros.filter(titulo__regex=r"^[OoÒòÓóÔôÕõÖö]")
            elif filtro_letra.lower() == "u":
                meus_livros = meus_livros.filter(titulo__regex=r"^[UuÙùÚúÛûÜü]")
            elif filtro_letra.lower() == "c":
                meus_livros = meus_livros.filter(titulo__regex=r"^[cCçÇ]")
            else:
                meus_livros = meus_livros.filter(titulo__istartswith=filtro_letra)
        elif filtro_letra == "0-9...":
            meus_livros = meus_livros.filter(titulo__regex=r"^[^A-Za-zÀ-ÿ]")
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
        filtro = ""

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