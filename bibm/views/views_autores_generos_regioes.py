from django.shortcuts import render

def autores(request):
  return render(request, "bibm/pages/autores.html")