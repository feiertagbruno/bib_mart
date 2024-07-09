from django.shortcuts import render
from bibm.models import Autor, Livro, Anotacao, Regiao
from django.db.models.functions import Concat
from django.db.models import Value
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
        autores = Autor.objects.annotate(nome=Concat("ult_nome", Value(", "), "prim_nome")).order_by("nome")
        filtro_letra = filtro[9:]
        filtro = "sobrenome"
    elif filtro[:12] == "primeironome":
        autores = Autor.objects.annotate(nome=Concat("prim_nome", Value(" "), "ult_nome")).order_by("nome")
        filtro_letra = filtro[12:]
        filtro = "primeironome"
    elif filtro[:6] == "regiao":
        autores = {}
        for regiao in Regiao.objects.filter(id__in = Autor.objects.values("regiao__id").distinct()).order_by("regiao"):
            autores[regiao.regiao] = Autor.objects.filter(regiao__id = regiao.id).annotate(
                nome=Concat("ult_nome", Value(", "), "prim_nome")
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
    if caller == "buscar_livros" or autor_id_livro:
        livros = Livro.objects.filter(autor__id= autor_id_livro).values_list("titulo", flat=True).order_by("titulo")

    context = {
        "autores": autores,
        "filtro": filtro,
        "ordem_lista": ordem_lista,
        "caller":"autores",
        "ordem_alfabetica_lista": ordem_alfabetica_lista,
        "filtro_letra": filtro_letra,
        "livros": livros,
        "autor_id_livro": autor_id_livro,
    }

    request = zerar_session(request)

    return render(request, "bibm/pages/autores.html", context)

def deletar_autor(request):

    if request.method != "POST":
        return Http404
    
    filtro = request.POST.get("filtro")
    autor = Autor.objects.get(id = request.POST.get("autor_id"))
    autor.delete()

    if not autor.id:
        messages.info(request, "Autor excluído com sucesso. "\
                      "Os livros deste autor foram realocados para 'Autor desconhecido'.")

    return HttpResponseRedirect(reverse("bibm:autores", kwargs={"filtro":filtro}))