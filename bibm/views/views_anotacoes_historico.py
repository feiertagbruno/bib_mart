from django.shortcuts import render
from bibm.models import Livro, Anotacao, Historico

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
      if filtro == "todos":
          meus_livros = Livro.objects.all().order_by("titulo")
      if filtro == "naolidos":
          meus_livros = Livro.objects.filter(lido=False)
      elif filtro == "lidos":
          meus_livros = Livro.objects.filter(lido=True)
      elif filtro == "lidoeleriadenovo":
          meus_livros = Livro.objects.filter(lido=True, leria_de_novo=True)
      elif len(filtro) == 1:
          if filtro.lower() == "a":
              meus_livros = Livro.objects.filter(titulo__regex=r"^[AaÁáÀàÂâÃãÄäÅå]")
          elif filtro.lower() == "e":
              meus_livros = Livro.objects.filter(titulo__regex=r"^[EeÈèÉéÊêËë]")
          elif filtro.lower() == "i":
              meus_livros = Livro.objects.filter(titulo__regex=r"^[IiÌìÍíÎîÏï]")
          elif filtro.lower() == "o":
              meus_livros = Livro.objects.filter(titulo__regex=r"^[OoÒòÓóÔôÕõÖö]")
          elif filtro.lower() == "u":
              meus_livros = Livro.objects.filter(titulo__regex=r"^[UuÙùÚúÛûÜü]")
          elif filtro.lower() == "c":
              meus_livros = Livro.objects.filter(titulo__regex=r"^[cCçÇ]")
          else:
              meus_livros = Livro.objects.filter(titulo__istartswith=filtro)
      elif filtro == "0-9...":
          meus_livros = Livro.objects.filter(titulo__regex=r"^[^A-Za-zÀ-ÿ]")
  else:
      ...

  anotacoes = {}
  livros = Livro.objects.all().order_by("-data_leitura","-id")
  for livro in livros:
    anotacoes.update({})

  context = {
    "filtro": filtro,
  }

  return render(request, "bibm/pages/minhasAnotacoes.html")

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