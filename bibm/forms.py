from django import forms
from bibm.models import Anotacao, Livro, Endereco, Regiao, Autor, Genero
from utils.functions import is_integer

class AnotacaoForm(forms.ModelForm):
    
    class Meta:
        model = Anotacao
        fields = [
            "livro",
            "anotacao",
        ]

class LivroForm(forms.ModelForm):
    autor = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"autor_id_field"
            }
        )
    )
    genero = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"genero_id_field"
            }
        )
    )
    endereco = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"endereco_id_field"
            }
        )
    )
    regiao = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"regiao_id_field"
            }
        )
    )
    class Meta:
        model = Livro
        fields = [
            "titulo",
            "editora",
            "tema",
            "lido",
            "data_leitura",
            "leria_de_novo",
            "classificacao",
            "endereco",
            "data_compra",
            "regiao",
            "comentario",
            "autor",
            "genero",
            "planejamento",
        ]
        widgets = {
            "titulo":forms.TextInput(
                attrs={
                    "class":"autor-input",
                    "placeholder": "Digite aqui o título do livro.",
                    "autocomplete": "off",
                }
            ),
            "editora":forms.TextInput(
                attrs={
                    "class":"autor-input",
                    "placeholder":"Digite aqui a editora.",
                    "autocomplete": "off",
                }
            ),
            "tema":forms.TextInput(
                attrs={
                    "class":"autor-input",
                    "placeholder":"Digite o tema.",
                    "autocomplete": "off",
                }
            ),
            "data_compra":forms.DateInput(
                attrs={
                    "type":"date",
                    "class":"data-input",
                }
            ),
            "data_leitura":forms.DateInput(
                attrs={
                    "type":"date",
                    "class":"data-input",
                }
            ),
            "lido":forms.CheckboxInput(
                attrs={
                    "id":"checkbox-lido"
                }
            ),
            "planejamento":forms.HiddenInput(
                attrs={
                    "id":"planejamento_id_field"
                }
            ),
            "id":forms.HiddenInput(
                attrs={
                    "id":"form_id_field"
                }
            ),
        }

    def clean(self):
        cleaned_fields = super().clean()
        if is_integer(self.data["autor"]):
            cleaned_fields["autor"] = Autor.objects.filter(id=self.data["autor"]).first()
        if is_integer(self.data["regiao"]):
            cleaned_fields["regiao"] = Regiao.objects.filter(id=self.data["regiao"]).first()
        if is_integer(self.data["genero"]):
            cleaned_fields["genero"] = Genero.objects.filter(id=self.data["genero"]).first()
        if is_integer(self.data["endereco"]):
            cleaned_fields["endereco"] = Endereco.objects.filter(id=self.data["endereco"]).first()

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

class AutorForm(forms.ModelForm):

    regiao = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"regiao_id_field"
            }
        )
    )
    
    class Meta:
        model = Autor
        fields = [
            "prim_nome",
            "ult_nome",
            "nacionalidade",
            "regiao",
            "comentario",
        ]
        widgets = {
            "prim_nome":forms.TextInput(
                attrs={
                    "class":"autor-input",
                    "placeholder": "Digite aqui a primeira parte do nome.",
                    "autocomplete": "off",
                }
            ),
            "ult_nome":forms.TextInput(
                attrs={
                    "class":"autor-input",
                    "placeholder": "Digite aqui o sobrenome.",
                    "autocomplete": "off",
                }
            ),
            "nacionalidade":forms.TextInput(
                attrs={
                    "class":"autor-input",
                    "placeholder": "Digite aqui a nacionalidade deste autor.",
                    "autocomplete": "off",
                }
            ),
            "comentario":forms.Textarea(
                attrs={
                    "class":"caixa-texto-comentario",
                    "id":"comentario_autor",
                    "placeholder": "Digite aqui seu comentário sobre este autor. Campo não obrigatório.",
                    "autocomplete": "off",
                }
            ),
        }

    def clean(self):
        cleaned_fields = super().clean()
        cleaned_fields["regiao"] = Regiao.objects.filter(id=self.data["regiao"]).first()

class RegiaoForm(forms.ModelForm):
    class Meta:
        model = Regiao
        fields = ["regiao", "comentario"]
        widgets = {
            "regiao": forms.TextInput(
                attrs={
                    "placeholder": "Digite aqui a região a ser adicionada.",
                    "class": "autor-input",
                    "autocomplete":"off",
                }
            ),
            "comentario":forms.Textarea(
                attrs={
                    "class":"caixa-texto-comentario",
                    "id":"comentario_regiao",
                    "placeholder": "Digite aqui seu comentário sobre esta região. Campo não obrigatório.",
                    "autocomplete": "off",
                }
            ),
        }

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = [
            "genero",
            "comentario"
        ]
        widgets = {
            "genero": forms.TextInput(
                attrs={
                    "placeholder": "Digite aqui o gênero a ser adicionado.",
                    "class": "autor-input",
                    "autocomplete":"off",
                }
            ),
            "comentario":forms.Textarea(
                attrs={
                    "class":"caixa-texto-comentario",
                    "id":"comentario_genero",
                    "placeholder": "Digite aqui seu comentário sobre este gênero. Campo não obrigatório.",
                    "autocomplete": "off",
                }
            ),
        }
