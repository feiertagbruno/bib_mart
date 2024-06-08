from django.contrib import admin
from .models import *

# Register your models here.
class RegiaoAdmin(admin.ModelAdmin):
    ...

class GeneroAdmin(admin.ModelAdmin):
    ...

class EnderecoAdmin(admin.ModelAdmin):
    ...

class AutorAdmin(admin.ModelAdmin):
    ...

class LivroAdmin(admin.ModelAdmin):
    ...

class HistoricoAdmin(admin.ModelAdmin):
    ...

class AnotacaoAdmin(admin.ModelAdmin):
    ...

admin.site.register(Regiao, RegiaoAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Livro, LivroAdmin)
admin.site.register(Historico, HistoricoAdmin)
admin.site.register(Anotacao, AnotacaoAdmin)