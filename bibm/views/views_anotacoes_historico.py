from django.shortcuts import render
from bibm.models import Livro, Anotacao, Historico

def minhas_anotacoes(request):
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