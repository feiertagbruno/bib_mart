from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Anotacao, Livro

class AnotacaoForm(forms.ModelForm):
    
    class Meta:
        model = Anotacao
        fields = [
            "livro",
            "anotacao",
        ]

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            "titulo",
            "editora",
            "autor",
            "genero",
            "tema",
            "lido",
            "data_leitura",
            "leria_de_novo",
            "classificacao",
            "endereco",
            "data_compra",
            "regiao",
            "comentario",
        ]

class ClassificacaoForm(forms.Form):
    classificacao = forms.ChoiceField(
        choices=[
            (0,"0"),
            (1,"1"),
            (2,"2"),
            (3,"3"),
            (4,"4"),
            (5,"5"),
            (6,"6"),
            (7,"7"),
            (8,"8"),
            (9,"9"),
            (10,"10"),
        ],
        label="Classificação"
        )
    leria_de_novo = forms.BooleanField(
        label="Leria de novo?",
        initial=False,
        widget=forms.CheckboxInput(attrs={
                "class": "btn-leria-de-novo"
            }
        )
    )