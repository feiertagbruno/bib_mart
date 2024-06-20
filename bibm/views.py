from django.shortcuts import render
from .models import Livro, Anotacao, Historico, Endereco, Autor, Genero, Regiao
from .forms import AnotacaoForm, LivroForm, ClassificacaoForm, AutorForm, RegiaoForm, GeneroForm, EnderecoForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
import locale
from django.db.models import Q
from django.db.models import Max
from django.contrib import messages
from django.db.models import Value
from django.db.models.functions import Concat


def context_home():
    livros_lendo = Livro.objects.filter(lendo=True)
    livros_planejamento = Livro.objects.filter(planejamento=1)
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
            autores = list(Autor.objects.annotate(
                    nome=Concat("prim_nome", Value(" "), "ult_nome")
                ).values_list("id", "nome")
            )
            context.update({"autores":autores})

        if generos:
            generos = list(Genero.objects.all().values_list("id","genero"))
            context.update({"generos":generos})

        if enderecos:
            enderecos = list(
                Endereco.objects.annotate(
                    nome=Concat("codigo", Value(" "), "descricao")
                ).values_list("id", "nome")
            )
            context.update({"enderecos":enderecos})

        if regioes:
            regioes = Regiao.objects.all().values_list("id", "regiao")
            context.update({"regioes":regioes})

        return context

def livros_planejamento():
    livros_plan = Livro.objects.exclude(planejamento=None).order_by("planejamento")
    ultimo_plan = len(livros_plan)
    ultimo_plan_agregate = Livro.objects.aggregate(planejamento=Max("planejamento"))["planejamento"]
    p = 1
    if ultimo_plan != None and ultimo_plan != ultimo_plan_agregate:
        todos_os_planejados = Livro.objects.exclude(planejamento=None).order_by("planejamento")
        for livro in todos_os_planejados:
            livro.planejamento = None
            livro.save()
        for livro in todos_os_planejados:
            livro.planejamento = p
            livro.save()
            p += 1
        livros_plan = Livro.objects.exclude(planejamento=None).order_by("planejamento")
    return livros_plan

def acrescentar_plan(livro_id):
    livros_planejamento()
    proximo_planejamento = Livro.objects.aggregate(planejamento = Max("planejamento"))["planejamento"]
    if proximo_planejamento == None:
        proximo_planejamento = 1
    else:
        proximo_planejamento += 1
    livro = Livro.objects.get(id = livro_id)
    livro.planejamento = proximo_planejamento
    livro.save()

def zerar_session(request):
    info_livro = request.session.get("info_livro")
    if info_livro:
        del(request.session["info_livro"])
    return request

# Create your views here.


def home(request):
    request = zerar_session(request)
    context = context_home()
    return render(request, "bibm/pages/meumeu.html", context)


def add_anotacao(request, livro_id):

    livro = Livro.objects.get(id=livro_id)
    todas_anotacoes_livro = Anotacao.objects.filter(livro=livro).order_by("-id")

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
    todas_anotacoes_livro = Anotacao.objects.filter(livro=livro_id).order_by("-id")

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
    anotacao_para_excluir.delete()
    return HttpResponseRedirect(
        reverse("bibm:add_anotacao", kwargs={"livro_id": livro_id})
    )


def meus_livros(request, filtro):
    termo_busca = request.GET.get("q", "").strip()
    classe_btn = "btn-azul"
    filtros = {
        "todos": "Todos", 
        "naolidos": "Não lidos", 
        "lidos": "Lidos", 
        "lidoeleriadenovo": "Lido e Leria de novo"
    }
    if termo_busca == "":
        if filtro == "todos":
            meus_livros = Livro.objects.all().order_by("titulo")
        if filtro == "naolidos":
            meus_livros = Livro.objects.filter(lido=False)
        elif filtro == "lidos":
            meus_livros = Livro.objects.filter(lido=True)
        elif filtro == "lidoeleriadenovo":
            meus_livros = Livro.objects.filter(lido=True, leria_de_novo=True)
    else:
        meus_livros = Livro.objects.filter(Q(
        Q(titulo__icontains = termo_busca) |
        Q(editora__icontains = termo_busca) |
        Q(autor__prim_nome__icontains = termo_busca) |
        Q(genero__genero__icontains = termo_busca) |
        Q(tema__icontains = termo_busca) |
        Q(endereco__codigo__icontains = termo_busca) |
        Q(regiao__regiao__icontains = termo_busca)
        )).order_by("titulo")

    context = {
        "meus_livros": meus_livros,
        "caller": "meus_livros",
        "filtro": filtro,
        "filtros": filtros,
        "classe_btn": classe_btn,
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

        historico = Historico.objects.filter(Q(livro=livro), Q(data_fim=None)).order_by("-id").first()
        if historico != None:
            historico.data_fim = timezone.localtime(timezone.now())
            historico.terminou = True
            historico.save()

        historico = Historico.objects.filter(Q(livro=livro), Q(data_fim=None)).order_by("-id")
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

        historico = Historico.objects.filter(Q(livro=livro), Q(data_fim=None)).order_by("-id").first()
        historico.data_fim = timezone.localtime(timezone.now())
        historico.save()

        historico = Historico.objects.filter(Q(livro=livro), Q(data_fim=None)).order_by("-id")
        if len(historico) > 0:
            for hist in historico:
                hist.delete()

        livro.lendo = False
        livro.save()
    return HttpResponseRedirect(reverse("bibm:home"))


def editar_planejamento(request, filtro):

    termo_busca = request.GET.get("q", "").strip()
    filtros = {
        "naolidos": "Não lidos", 
        "todos": "Todos", 
        "lidos": "Lidos", 
        "lidoeleriadenovo": "Lido e Leria de novo"
    }
    classe_btn = "btn-vermelho"

    livros_plan = livros_planejamento()
    ultimo_plan = Livro.objects.aggregate(planejamento=Max("planejamento"))["planejamento"]

    if termo_busca == "":
        if filtro == "naolidos":
            meus_livros = Livro.objects.filter(lido=False, planejamento=None)
        elif filtro == "todos":
            meus_livros = Livro.objects.filter(planejamento=None)
        elif filtro == "lidos":
            meus_livros = Livro.objects.filter(lido=True, planejamento=None)
        elif filtro == "lidoeleriadenovo":
            meus_livros = Livro.objects.filter(lido=True, leria_de_novo=True, planejamento=None)

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

    context = {
        "livros_plan": livros_plan,
        "ultimo_plan": ultimo_plan,
        "meus_livros": meus_livros,
        "termo_pesquisado": termo_busca,
        "filtro": filtro,
        "filtros": filtros,
        "caller":"editar_planejamento",
        "classe_btn": classe_btn,
    }
    return render(request, "bibm/pages/editarPlanejamento.html", context)


def subir_plan(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        filtro = request.POST.get("filtro")

        livro = Livro.objects.get(id=livro_id)
        if livro.planejamento > 1:
            livro_acima = Livro.objects.filter(planejamento=livro.planejamento - 1).first()
            livro_acima.planejamento = None
            livro_acima.save()

            livro.planejamento -= 1
            livro.save()

            livro_acima.planejamento = livro.planejamento + 1
            livro_acima.save()

    return HttpResponseRedirect(reverse("bibm:editar_planejamento", kwargs={"filtro":filtro}))


def descer_plan(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        filtro = request.POST.get("filtro")

        livro = Livro.objects.get(id=livro_id)
        maior_planejamento = Livro.objects.aggregate(planejamento=Max("planejamento"))["planejamento"]

        if livro.planejamento < maior_planejamento:
            livro_abaixo = Livro.objects.filter(planejamento=livro.planejamento + 1).first()
            livro_abaixo.planejamento = None
            livro_abaixo.save()

            livro.planejamento += 1
            livro.save()

            livro_abaixo.planejamento = livro.planejamento - 1
            livro_abaixo.save()

    return HttpResponseRedirect(reverse("bibm:editar_planejamento", kwargs={"filtro":filtro}))

def pular_este(request):
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        livro = Livro.objects.get(id=livro_id)
        ultimo_plan = Livro.objects.aggregate(planejamento=Max("planejamento"))["planejamento"]
        if livro.planejamento != ultimo_plan:
            livros_plan_maiores = Livro.objects.filter(planejamento__gt = livro.planejamento).order_by("planejamento")
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
        livro = Livro.objects.get(id=livro_id)
        livro.planejamento = None
        livro.save()

        livros_planejamento()

    return HttpResponseRedirect(
        reverse("bibm:editar_planejamento", kwargs={"filtro":filtro})
    )

def mapa_da_bibli(request):

    search_term = request.GET.get("q","")
    if search_term != "":
        enderecos = Endereco.objects.filter(Q(
            Q(codigo__icontains=search_term) |
            Q(descricao__icontains=search_term)
        ))
    else:
        enderecos = Endereco.objects.all()
    
    context = {"enderecos":{}}
    if len(enderecos) > 0:
        for endereco in enderecos:
            livro_lista = []
            livros_endereco = Livro.objects.filter(endereco__codigo = endereco.codigo)
            for livro in livros_endereco:
                livro_lista.append(livro.titulo)
            context["enderecos"][endereco.codigo] = (endereco.descricao,livro_lista)

    if search_term == "" or search_term.lower() in "sem endereço":
        livro_lista = []
        livros_endereco = Livro.objects.filter(endereco = None)
        for livro in livros_endereco:
            livro_lista.append(livro.titulo)
        context["enderecos"]["Sem endereço"] = (None,livro_lista)

    if not context["enderecos"]:
        messages.info(request,"Sua busca retornou sem resultados.")
        context = {"enderecos":{}}

    return render(request, "bibm/mapaDaBibli.html",context)

def add_um_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Livro salvo com sucesso.")
        else:
            for er in form.errors.items():
                messages.error(request, er)
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
    }

    context.update({
        **context_add_um_livro()
    })
    return render(request,"bibm/pages/addUmLivro.html", context)

def editar_um_livro_save(request):
    
    livro_id = request.POST.get("livro_id")

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
    
    return HttpResponseRedirect(reverse("bibm:home"))

def deletar_um_livro(request):
    ...

def add_um_autor_livro(request):
    if request.method == "POST":
        request.session["info_livro"] = request.POST
        
        form = AutorForm()

        context = {
            "form":form,
            **context_add_um_livro(autores=False,generos=False,enderecos=False),
            "add_um_autor_livro":True,
        }

        return render(request, "bibm/pages/addUmAutor.html", context)
    else:
        return Http404

def add_um_autor_livro_save(request):
    if request.method == "POST":
        
        form = AutorForm(data = request.POST)

        if form.is_valid():
            autor_salvo = form.save()
            request.session["autor_salvo"] = autor_salvo.id
            request.session["regiao_salva"] = autor_salvo.regiao.id
            messages.success(request,"Autor salvo.")
        
        return HttpResponseRedirect(reverse("bibm:add_um_livro"))
    else:
        return Http404
    
def add_uma_regiao_livro(request):
    if request.method == "POST":
        request.session["info_livro"] = request.POST
        
        form = RegiaoForm()

        context = {
            "form":form,
        }

        return render(request, "bibm/pages/addUmaRegiao.html", context)
    else:
        return Http404

def add_uma_regiao_livro_save(request):
    if request.method == "POST":
        
        form = RegiaoForm(data = request.POST)

        if form.is_valid():
            regiao_salva = form.save()
            request.session["regiao_salva"] = regiao_salva.id
            messages.success(request,"Região salva.")
        
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
        
        return HttpResponseRedirect(reverse("bibm:add_um_livro"))
    else:
        return Http404
    
def add_um_endereco_livro(request):
    if request.method == "POST":
        request.session["info_livro"] = request.POST
        
        form = EnderecoForm()

        context = {
            "form":form,
        }

        return render(request, "bibm/pages/addUmEndereco.html", context)
    else:
        return Http404

def add_um_endereco_livro_save(request):
    if request.method == "POST":
        
        form = EnderecoForm(data = request.POST)

        if form.is_valid():
            endereco_salvo = form.save()
            request.session["endereco_salvo"] = endereco_salvo.id
            messages.success(request,"Endereço salvo.")
        
        return HttpResponseRedirect(reverse("bibm:add_um_livro"))
    else:
        return Http404

def acrescentar_no_planejamento(request):
    filtro = request.POST.get("filtro")
    if request.method == "POST":
        livro_id = request.POST.get("livro_id")
        acrescentar_plan(livro_id)
    return HttpResponseRedirect(reverse("bibm:editar_planejamento", kwargs={"filtro":filtro}))

def acrescentar_no_planejamento_meus_livros(request):
    livro_id = request.POST.get("livro_id")
    filtro = request.POST.get("filtro")
    acrescentar_plan(livro_id)
    return HttpResponseRedirect(reverse("bibm:meus_livros", kwargs={"filtro":filtro}))

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