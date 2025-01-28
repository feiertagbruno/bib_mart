from django.shortcuts import render
from bibm.models import Livro, Anotacao, Historico, Endereco, Autor, Genero, Regiao
from bibm.forms import AnotacaoForm, LivroForm, ClassificacaoForm
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.utils import timezone
import locale
from django.db.models import Q, Max
from django.contrib import messages
from django.db.models import Value
from django.db.models.functions import Concat
from utils.functions import get_ordem_alfabetica_lista, get_queryset_filtro_letra
import random
from django.core.paginator import Paginator
from openpyxl import Workbook
from datetime import datetime
import os
from django.conf import settings
from django.core.serializers import serialize, deserialize

def context_home():
    livros_lendo = Livro.objects.filter(lendo=True,deletado=False)
    livros_planejamento = Livro.objects.filter(planejamento=1,deletado=False)
    mostrar_lendo = False
    mostrar_planejamento = False
    if len(livros_lendo) > 0:
        mostrar_lendo = True
    else:
        if len(livros_planejamento) > 0:
            mostrar_planejamento = True
    context = {
        "livros_lendo": livros_lendo,
        "livros_planejamento": livros_planejamento,
        "mostrar_lendo": mostrar_lendo,
        "mostrar_planejamento": mostrar_planejamento,
    }

    return context

def context_add_um_livro(
        autores=True,
        generos=True,
        enderecos=True,
        regioes=True
    ):
        context = {}
        if autores:
            autores = list(Autor.objects.filter(deletado=False).annotate(
                    nome=Concat("prim_nome", Value(" "), "ult_nome")
                ).values_list("id", "nome")
            )
            context.update({"autores":autores})

        if generos:
            generos = list(Genero.objects.exclude(
                Q(Q(id=1)|Q(deletado=True))
            ).values_list("id","genero"))
            context.update({"generos":generos})

        if enderecos:
            enderecos = list(
                Endereco.objects.filter(deletado=False).annotate(
                    nome=Concat("codigo", Value(" "), "descricao")
                ).values_list("id", "nome")
            )
            context.update({"enderecos":enderecos})

        if regioes:
            regioes = Regiao.objects.exclude(
                Q(Q(id=1)|Q(deletado=True))
            ).values_list("id", "regiao")
            context.update({"regioes":regioes})

        return context

def livros_planejamento():
    livros_plan = Livro.objects.exclude(
        Q(Q(planejamento=None)|Q(deletado=True))
    ).order_by("planejamento")
    ultimo_plan = len(livros_plan)
    ultimo_plan_agregate = Livro.objects.filter(deletado=False).aggregate(
        planejamento=Max("planejamento"))["planejamento"]
    p = 1
    if ultimo_plan != None and ultimo_plan != ultimo_plan_agregate:
        todos_os_planejados = Livro.objects.exclude(
            Q(Q(planejamento=None)|Q(deletado=True))
        ).order_by("planejamento")
        for livro in todos_os_planejados:
            livro.planejamento = None
            livro.save()
        for livro in todos_os_planejados:
            livro.planejamento = p
            livro.save()
            p += 1
        livros_plan = Livro.objects.exclude(
            Q(Q(planejamento=None)|Q(deletado=True))
        ).order_by("planejamento")
    return livros_plan

def acrescentar_plan(livro_id):
    livros_planejamento()
    proximo_planejamento = Livro.objects.filter(deletado=False).aggregate(
        planejamento = Max("planejamento"))["planejamento"]
    if proximo_planejamento == None:
        proximo_planejamento = 1
    else:
        proximo_planejamento += 1
    livro = Livro.objects.get(id = livro_id)
    livro.planejamento = proximo_planejamento
    livro.save()

def zerar_session(request):
    if request.session.get("info_livro"):
        del(request.session["info_livro"])
    if request.session.get("autor_salvo"):
        del(request.session["autor_salvo"])
    if request.session.get("regiao_salva"):
        del(request.session["regiao_salva"])
    if request.session.get("genero_salvo"):
        del(request.session["genero_salvo"])
    if request.session.get("endereco_salvo"):
        del(request.session["endereco_salvo"])
    if request.session.get("caller"):
        del(request.session["caller"])
    if request.session.get("guia"):
        del(request.session["guia"])
    if request.session.get("enderecos"):
        del(request.session["enderecos"])
    if request.session.get("sem_endereco"):
        del(request.session["sem_endereco"])
    if request.session.get("funcao_enderecar"):
        del(request.session["funcao_enderecar"])
    if request.session.get("caller_regiao"):
        del(request.session["caller_regiao"])
    if request.session.get("filtro"):
        del(request.session["filtro"])
    if request.session.get("autor_id"):
        del(request.session["autor_id"])
    if request.session.get("caller"):
        del(request.session["caller"])
    if request.session.get("info_autor"):
        del(request.session["info_autor"])
    if request.session.get("regiao_id"):
        del(request.session["regiao_id"])
    if request.session.get("genero_id"):
        del(request.session["genero_id"])
    if request.session.get("meus_livros_excel"):
        del(request.session["meus_livros_excel"])
    return request

def get_pagination_range(current_page, num_pages):
    range_size = 20
    mid_num = int(range_size/2)

    if num_pages <= range_size:
        return [i for i in range(1,num_pages+1)]

    first_num = current_page - mid_num + 2
    last_num = current_page + mid_num + 1 + (range_size % 2)

    if first_num < 1:
        last_num += 1-first_num
        first_num = 1
    
    if last_num > num_pages:
        first_num -= (last_num - num_pages)
        last_num = num_pages

    if last_num > num_pages: last_num = num_pages
    pagination_range = []

    for i in range(first_num,last_num + 1):
        pagination_range.append(i)

    return pagination_range


def get_pagination(current_page,pagination_obj):
    paginator = Paginator(pagination_obj, 15)
    page_obj = paginator.get_page(current_page)
    first_step_pagination_range = get_pagination_range(current_page,paginator.num_pages)
    
    primeira = True if first_step_pagination_range[0] != 1 else False
    ultima = True if first_step_pagination_range[len(first_step_pagination_range)-1] != paginator.num_pages else False

    pagination_range = []
    for i in first_step_pagination_range:
        pagination_range.append([i, i, paginator.get_page(i)[0].titulo])

    if primeira: pagination_range.insert(0,["primeira", 1,""])
    if ultima: pagination_range.append(["última", paginator.num_pages,""])

    return (page_obj, pagination_range)



def gerar_livros_excel(livros):
    wb = Workbook()
    ws = wb.active
    ws.title = "Meus Livros"
    ws.append([
        "Título", "Editora","Autor", 
        "Nacionalidade Autor", "Região Autor", "Comentário Sobre o Autor",
        "Gênero","Tema","Lendo?", 
        "Lido?","Data da Leitura","Leria Novamente?",
        "Classificação","Endereço", "Descrição do Endereço",
        "Data da Compra", 
        "Região","Comentário","No Planejamento?", "Categoria" 
    ])
    
    for livro in livros:
        ws.append([
            livro.titulo,
            livro.editora,
            livro.autor.prim_nome + " " + livro.autor.ult_nome,
            livro.autor.nacionalidade,
            livro.autor.regiao.regiao,
            livro.autor.comentario,
            livro.genero.genero,
            livro.tema,
            livro.lendo,
            livro.lido,
            datetime.strftime(livro.data_leitura,"%d/%m/%Y") if livro.data_leitura else None,
            livro.leria_de_novo,
            livro.classificacao,
            livro.endereco.codigo if livro.endereco else None,
            livro.endereco.descricao if livro.endereco else None,
            datetime.strftime(livro.data_compra,"%d/%m/%Y") if livro.data_compra else None,
            livro.regiao.regiao,
            livro.comentario,
            livro.planejamento,
            livro.categoria
        ])
    caminho_arquivo = os.path.join(settings.MEDIA_ROOT,"meus_livros.xlsx")
    wb.save(caminho_arquivo)
    return caminho_arquivo

# Create your views here.


def home(request):
    request = zerar_session(request)
    context = context_home()
    return render(request, "bibm/pages/meumeu.html", context)


def add_anotacao(request, livro_id):

    livro = Livro.objects.get(id=livro_id)
    todas_anotacoes_livro = Anotacao.objects.filter(livro=livro,deletado=False).order_by("-id")

    # jogada com locale e timezone feita porque o 'abril' criado pelo timezone ficou com letra minuscula
    # fiz isso para ficar com a data igualzinha à data do django
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
    data_inclusao = timezone.localdate(timezone.now())
    data_inclusao = data_inclusao.strftime(
        f"%d de {data_inclusao.strftime('%B').capitalize()} de %Y"
    )

    if request.method != "POST":
        form_anotacao = AnotacaoForm(initial={"livro": livro})
    else:
        form_anotacao = AnotacaoForm(data=request.POST)
        if form_anotacao.is_valid():
            anotacao = form_anotacao.save(commit=False)
            anotacao.full_clean()
            anotacao.save()
            return HttpResponseRedirect(
                reverse("bibm:add_anotacao", kwargs={"livro_id": livro.id})
            )
    context = {
        "edicao": False,
        "livro_id": livro_id,
        "form_anotacao": form_anotacao,
        "titulo": livro.titulo,
        "data_inclusao": data_inclusao,
        "todas_anotacoes_livro": todas_anotacoes_livro,
    }
    return render(request, "bibm/pages/adicionarAnotacao.html", context)


def edit_anotacao(request, livro_id, anotacao_id):
    livro = Livro.objects.get(id=livro_id)
    anotacao = Anotacao.objects.get(id=anotacao_id)
    data_inclusao = anotacao.data_inclusao
    todas_anotacoes_livro = Anotacao.objects.filter(livro=livro_id,deletado=False).order_by("-id")

    if request.method != "POST":
        form_anotacao = AnotacaoForm(instance=anotacao)
    else:
        form_anotacao = AnotacaoForm(instance=anotacao, data=request.POST)
        if form_anotacao.is_valid():
            anotacao.save()
            return HttpResponseRedirect(
                reverse("bibm:add_anotacao", kwargs={"livro_id": livro.id})
            )

    context = {
        "edicao": True,
        "livro_id": livro_id,
        "anotacao_id": anotacao_id,
        "form_anotacao": form_anotacao,
        "titulo": livro.titulo,
        "data_inclusao": data_inclusao,
        "todas_anotacoes_livro": todas_anotacoes_livro,
    }

    return render(request, "bibm/pages/adicionarAnotacao.html", context)


def delete_anotacao(request, livro_id, anotacao_id):
    anotacao_para_excluir = Anotacao.objects.get(id=anotacao_id)
    anotacao_para_excluir.deletado = True
    anotacao_para_excluir.save()
    if anotacao_para_excluir.deletado == True:
        messages.info(request, "Anotação deletada.")
    else:
        messages.error(request, "Por alguma razão a anotação não foi deletada.")
    return HttpResponseRedirect(
        reverse("bibm:add_anotacao", kwargs={"livro_id": livro_id})
    )


def meus_livros(request, filtro, ordem):
    termo_busca = request.GET.get("q", "").strip()
    classe_btn = "btn-azul"
    ordem_alfabetica_lista = get_ordem_alfabetica_lista()

    filtros = {
        "todos": "Todos", 
        "naolidos": "Não lidos", 
        "lidos": "Lidos", 
        "lidoeleriadenovo": "Lido e Leria de novo",
        "ficcao": "Ficção",
        "naoficcao": "Não-Ficção",
    }

    ordens = {
        "adicao": "Ordem de adição",
        "alfabetica": "Ordem alfabética",
    }
    
    if termo_busca == "":
        if filtro[:5] == "todos":
            meus_livros = Livro.objects.filter(deletado=False)
            filtro_letra = filtro[5:]
            filtro = "todos"
        if filtro[:8] == "naolidos":
            meus_livros = Livro.objects.filter(lido=False,deletado=False)
            filtro_letra = filtro[8:]
            filtro = "naolidos"
        elif filtro[:5] == "lidos":
            meus_livros = Livro.objects.filter(lido=True,deletado=False)
            filtro_letra = filtro[5:]
            filtro = "lidos"
        elif filtro[:16] == "lidoeleriadenovo":
            meus_livros = Livro.objects.filter(lido=True, leria_de_novo=True,deletado=False)
            filtro_letra = filtro[16:]
            filtro = "lidoeleriadenovo"
        elif filtro[:6] == "ficcao":
            meus_livros = Livro.objects.filter(categoria="F",deletado=False)
            filtro_letra = filtro[6:]
            filtro = "ficcao"
        elif filtro[:9] == "naoficcao":
            meus_livros = Livro.objects.filter(categoria="NF",deletado=False)
            filtro_letra = filtro[9:]
            filtro = "naoficcao"

        if filtro_letra:
            if len(filtro_letra) == 1 or filtro_letra == "0-9...":
                meus_livros = get_queryset_filtro_letra(filtro_letra, meus_livros, "titulo")

    else:
        meus_livros = Livro.objects.filter(Q(Q(
        Q(titulo__icontains = termo_busca) |
        Q(editora__icontains = termo_busca) |
        Q(autor__prim_nome__icontains = termo_busca) |
        Q(genero__genero__icontains = termo_busca) |
        Q(tema__icontains = termo_busca) |
        Q(endereco__codigo__icontains = termo_busca) |
        Q(regiao__regiao__icontains = termo_busca)
        ),Q(deletado=False))).order_by("titulo")
        filtro_letra = ""

    if ordem == "adicao":
        meus_livros = meus_livros.order_by("-id")
    if ordem == "alfabetica":
        meus_livros = meus_livros.order_by("titulo")

    request.session["meus_livros_excel"] = serialize("json",meus_livros)

    quantos_livros = meus_livros.filter(
        Q(Q(endereco__presencial = True) |
          Q(endereco = None))
    ).count()

    

    try:
        current_page = int(request.GET.get("page",1))
    except:
        current_page = 1

    meus_livros, pagination_range = get_pagination(current_page,meus_livros)

    context = {
        "meus_livros": meus_livros,
        "caller": "meus_livros",
        "filtro": filtro,
        "filtros": filtros,
        "classe_btn": classe_btn,
        "ordem_alfabetica_lista": ordem_alfabetica_lista,
        "filtro_letra": filtro_letra,
        "ordem": ordem,
        "ordens": ordens,
        "quantos_livros": quantos_livros,
        "pagination_range": pagination_range,
        "current_page": current_page,
    }

    return render(request, "bibm/pages/meusLivros.html", context)


def pegar_este_livro(request):

    if request.method =="POST":
        livro_id = request.POST.get("livro_id")
        livro = Livro.objects.get(id=livro_id)
        livro.planejamento = None
        livro.lendo = True
        livro.leria_de_novo = False
        livro.save()

        livros_planejamento()

        historico = Historico(livro=livro, data_ini=timezone.localtime(timezone.now()))
        historico.save()

        caller = request.POST.get("caller")
        filtro = request.POST.get("filtro")
        ordem = request.POST.get("ordem")
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

    return HttpResponseRedirect(reverse("bibm:home"))


def devolver(request, livro_id):
    context = context_home()
    context["devolvendo"] = True
    context["livro_id"] = int(livro_id)
    return render(request, "bibm/pages/meumeu.html", context)

def devolver_sim_classificacao(request, livro_id):
    context = context_home()
    context["devolvendo"] = True
    context["classificacao"] = True
    context["form_classificacao"] = ClassificacaoForm()
    context["livro_id"] = int(livro_id)
    return render(request, "bibm/pages/meumeu.html", context)


def devolver_sim(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        livro = Livro.objects.get(id=livro_id)
        classificacao = request.POST.get("classificacao")
        leria_de_novo = request.POST.get("leria_de_novo")

        historico = Historico.objects.filter(
            livro=livro, data_fim=None, deletado=False
        ).order_by("-id").first()
        if historico != None:
            historico.data_fim = timezone.localtime(timezone.now())
            historico.terminou = True
            historico.classificacao = classificacao
            historico.save()

        historico = Historico.objects.filter(
            livro=livro, data_fim=None, deletado=False
        ).order_by("-id")
        if len(historico) > 0:
            for hist in historico:
                hist.delete()

        if classificacao != "":
            livro.classificacao = int(classificacao)
        if leria_de_novo == "on":
            livro.leria_de_novo = True
        else:
            livro.leria_de_novo = False
        livro.lido = True
        livro.lendo = False
        livro.data_leitura = timezone.localtime(timezone.now())
        livro.save()
    return HttpResponseRedirect(reverse("bibm:home"))


def devolver_nao(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        livro = Livro.objects.get(id=livro_id)

        historico = Historico.objects.filter(
            livro=livro, data_fim=None, deletado=False
        ).order_by("-id").first()
        historico.data_fim = timezone.localtime(timezone.now())
        historico.save()

        historico = Historico.objects.filter(
            livro=livro, data_fim=None, deletado=False
        ).order_by("-id")
        if len(historico) > 0:
            for hist in historico:
                hist.delete()

        livro.lendo = False
        livro.save()
    return HttpResponseRedirect(reverse("bibm:home"))


def editar_planejamento(request, filtro, ordem):

    termo_busca = request.GET.get("q", "").strip()

    filtros = {
        "naolidos": "Não lidos", 
        "todos": "Todos", 
        "lidos": "Lidos", 
        "lidoeleriadenovo": "Lido e Leria de novo",
        "ficcao": "Ficção",
        "naoficcao": "Não-Ficção",
    }

    ordens = {
        "adicao": "Ordem de adição",
        "alfabetica": "Ordem alfabética",
    }
    
    ordem_alfabetica_lista = get_ordem_alfabetica_lista()
    classe_btn = "btn-vermelho"

    livros_plan = livros_planejamento()
    ultimo_plan = Livro.objects.filter(deletado=False).aggregate(
        planejamento=Max("planejamento"))["planejamento"]

    if termo_busca == "":
        if filtro[:5] == "todos":
            meus_livros = Livro.objects.filter(deletado=False)
            filtro_letra = filtro[5:]
            filtro = "todos"
        if filtro[:8] == "naolidos":
            meus_livros = Livro.objects.filter(lido=False,deletado=False)
            filtro_letra = filtro[8:]
            filtro = "naolidos"
        elif filtro[:5] == "lidos":
            meus_livros = Livro.objects.filter(lido=True,deletado=False)
            filtro_letra = filtro[5:]
            filtro = "lidos"
        elif filtro[:16] == "lidoeleriadenovo":
            meus_livros = Livro.objects.filter(lido=True, leria_de_novo=True, deletado=False)
            filtro_letra = filtro[16:]
            filtro = "lidoeleriadenovo"
        elif filtro[:6] == "ficcao":
            meus_livros = Livro.objects.filter(categoria="F",deletado=False)
            filtro_letra = filtro[6:]
            filtro = "ficcao"
        elif filtro[:9] == "naoficcao":
            meus_livros = Livro.objects.filter(categoria="NF",deletado=False)
            filtro_letra = filtro[9:]
            filtro = "naoficcao"

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
            ),
            Q(deletado=False)
        ))
        filtro_letra = ""

    if ordem == "adicao":
        meus_livros = meus_livros.order_by("-id")
    if ordem == "alfabetica":
        meus_livros = meus_livros.order_by("titulo")

    try:
        current_page = int(request.GET.get("page",1))
    except:
        current_page = 1

    meus_livros, pagination_range = get_pagination(current_page,meus_livros)

    context = {
        "livros_plan": livros_plan,
        "ultimo_plan": ultimo_plan,
        "meus_livros": meus_livros,
        "termo_pesquisado": termo_busca,
        "filtro": filtro,
        "filtros": filtros,
        "caller":"editar_planejamento",
        "classe_btn": classe_btn,
        "ordem_alfabetica_lista": ordem_alfabetica_lista,
        "filtro_letra": filtro_letra,
        "ordem": ordem,
        "ordens": ordens,
        "pagination_range":pagination_range,
        "current_page": current_page,
    }
    return render(request, "bibm/pages/editarPlanejamento.html", context)


def subir_plan(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        filtro = request.POST.get("filtro")
        ordem = request.POST.get("ordem")

        livro = Livro.objects.get(id=livro_id)
        if livro.planejamento > 1:
            livro_acima = Livro.objects.filter(planejamento=livro.planejamento - 1).first()
            livro_acima.planejamento = None
            livro_acima.save()

            livro.planejamento -= 1
            livro.save()

            livro_acima.planejamento = livro.planejamento + 1
            livro_acima.save()

    return HttpResponseRedirect(reverse("bibm:editar_planejamento", kwargs={
        "filtro":filtro,
        "ordem": ordem,
    }))


def descer_plan(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        filtro = request.POST.get("filtro")
        ordem = request.POST.get("ordem")

        livro = Livro.objects.get(id=livro_id)
        maior_planejamento = Livro.objects.filter(deletado=False).aggregate(
            planejamento=Max("planejamento"))["planejamento"]

        if livro.planejamento < maior_planejamento:
            livro_abaixo = Livro.objects.filter(planejamento=livro.planejamento + 1).first()
            livro_abaixo.planejamento = None
            livro_abaixo.save()

            livro.planejamento += 1
            livro.save()

            livro_abaixo.planejamento = livro.planejamento - 1
            livro_abaixo.save()

    return HttpResponseRedirect(reverse("bibm:editar_planejamento", kwargs={
        "filtro":filtro,
        "ordem": ordem,
    }))

def pular_este(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        livro = Livro.objects.get(id=livro_id)
        ultimo_plan = Livro.objects.filter(deletado=False).aggregate(
            planejamento=Max("planejamento"))["planejamento"]
        if livro.planejamento != ultimo_plan:
            livros_plan_maiores = Livro.objects.filter(
                planejamento__gt = livro.planejamento, deletado=False
            ).order_by("planejamento")
            if len(livros_plan_maiores) > 0:
                livro.planejamento = None
                livro.save()
                for livro_plan in livros_plan_maiores:
                    livro_plan.planejamento -= 1
                    livro_plan.save()
                livro.planejamento = ultimo_plan
                livro.save()
        else:
            messages.info(request,"Mãezinha, não vai dar pra pular este livro porque só tem ele no planejamento.")
            messages.info(request,"A função Pular Este, torna este livro o último do planejamento, como só tem ele, nada vai acontecer.")
            messages.info(request,"Você tem duas opções, ou acrescenta mais livros no planejamento, ou entra em Meus Livros e pega um direto por lá.")


    return HttpResponseRedirect(
        reverse("bibm:home")
    )

def remover_do_planejamento(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        filtro = request.POST.get("filtro")
        ordem = request.POST.get("ordem")
        livro = Livro.objects.get(id=livro_id)
        livro.planejamento = None
        livro.save()

        livros_planejamento()

    return HttpResponseRedirect(
        reverse("bibm:editar_planejamento", kwargs={
            "filtro":filtro,
            "ordem":ordem,
            })
    )

def acrescentar_no_planejamento(request):
    filtro = request.POST.get("filtro")
    ordem = request.POST.get("ordem")
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        acrescentar_plan(livro_id)
    return HttpResponseRedirect(reverse("bibm:editar_planejamento", kwargs={
        "filtro":filtro,
        "ordem": ordem,
    }))

def acrescentar_no_planejamento_meus_livros(request):
    livro_id = request.POST.get("livro_id")
    filtro = request.POST.get("filtro")
    ordem = request.POST.get("ordem")
    acrescentar_plan(livro_id)
    return HttpResponseRedirect(reverse("bibm:meus_livros", kwargs={
        "filtro":filtro,
        "ordem": ordem,
    }))

def chamar_html_teste(request):
    if request.method == "GET":
        form = LivroForm()
        context = {
            "form":form
        }
    elif request.method == "POST":
        POST = request.POST
        form = LivroForm(POST)
        if form.is_valid():
            livro = form.save(commit=False)
            ...
    return render(request,"bibm/testes.html", context)

def sortear_um_livro(request):
    lista_ids = list(Livro.objects.filter(
        Q(Q(lido=False)|Q(leria_de_novo=True)),
        Q(deletado=False)
    ).values_list("id", flat=True))

    if lista_ids:
        livro_aleatorio = random.choice(lista_ids)
        acrescentar_plan(livro_aleatorio)
    else:
        messages.info(request, "Não há livros para sortear.")
    
    return HttpResponseRedirect(reverse("bibm:home"))

def exportar_livros_excel(request):

    meus_livros_json = request.session.get("meus_livros_excel")

    meus_livros = [obj.object for obj in deserialize("json",meus_livros_json)]

    if not meus_livros:
        return HttpResponseRedirect(reverse("bibm:home"))

    caminho_arquivo = gerar_livros_excel(meus_livros)
    return FileResponse(open(caminho_arquivo,"rb"), as_attachment=True, filename="meus_livros.xlsx")