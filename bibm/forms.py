from django import forms
from bibm.models import Anotacao, Livro, Endereco, Regiao, Autor, Genero
from utils.functions import is_integer
from django.core.exceptions import ValidationError

class AnotacaoForm(forms.ModelForm):
    
    class Meta:
        model = Anotacao
        fields = [
            "livro",
            "anotacao",
        ]
        widgets = {
            "anotacao": forms.Textarea(
                attrs={
                    "class": "caixa-texto-comentario anotacao-field"
                }
            )
        }

class LivroForm(forms.ModelForm):
    autor = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"autor_id_field"
            }
        ),
        required=True,
        error_messages={
            "required": "Nenhum autor válido foi selecionado."
        }
    )
    genero = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"genero_id_field"
            }
        ),
        required=False
        # error_messages={
        #     "required": "Nenhum gênero válido foi selecionado."
        # }
    )
    endereco = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"endereco_id_field"
            }
        ),
        required=False
        # error_messages={
        #     "required": "Nenhum endereço válido foi selecionado."
        # }
    )
    regiao = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"regiao_id_field"
            }
        ),
        required=False
        # error_messages={
        #     "required": "Nenhuma região válida foi selecionada."
        # }
    )
    acrescentar_no_planejamento = forms.BooleanField(
        required=False
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
            "categoria",
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
                    "autocomplete": "on",
                }
            ),
            "tema":forms.TextInput(
                attrs={
                    "class":"autor-input",
                    "placeholder":"Digite o tema.",
                    "autocomplete": "on",
                }
            ),
            "data_compra":forms.DateInput(
                attrs={
                    "type":"date",
                    "class":"data-input",
                    "id": "data_compra_field",
                }
            ),
            "data_leitura":forms.DateInput(
                attrs={
                    "type":"date",
                    "class":"data-input",
                    "id": "data_leitura_field",
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
            "categoria": forms.Select(
                attrs={
                    "class":"categoria-field",
                }
            )
        }

    def clean(self):
        cleaned_fields = super().clean()
        if is_integer(self.data["autor"]):
            cleaned_fields["autor"] = Autor.objects.filter(id=self.data["autor"]).first()
        if is_integer(self.data["regiao"]):
            cleaned_fields["regiao"] = Regiao.objects.filter(id=self.data["regiao"]).first()
        else:
            cleaned_fields["regiao"] = Regiao.objects.get(id=Livro._meta.get_field("regiao").default)
        if is_integer(self.data["genero"]):
            cleaned_fields["genero"] = Genero.objects.filter(id=self.data["genero"]).first()
        else:
            cleaned_fields["genero"] = Genero.objects.get(id=Livro._meta.get_field("genero").default)
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
        label="Classificação",
        required=False
        )
    leria_de_novo = forms.BooleanField(
        label="Leria de novo?",
        initial=False,
        widget=forms.CheckboxInput(attrs={
                "class": "btn-leria-de-novo"
            }
        ),
        required=False
    )

class AutorForm(forms.ModelForm):

    regiao = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                "id":"regiao_id_field"
            }
        ),
        required=False
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
                    "id": "prim_nome_autor",
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
        if is_integer(self.data["regiao"]):
            cleaned_fields["regiao"] = Regiao.objects.filter(id=self.data["regiao"]).first()
        else:
            cleaned_fields["regiao"] = Regiao.objects.get(id=Autor._meta.get_field("regiao").default)

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
                    "id": "regiao_input_id",
                },
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
        error_messages = {
            "regiao": {
                "unique": "Esta região já existe. A região não foi adicionada."
            }
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
                    "id":"genero_input_id",
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

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            "codigo",
            "descricao",
            "presencial",
        ]
        widgets = {
            "codigo": forms.TextInput(
                attrs={
                    "placeholder": "O código deve ter 3 letras e 2 números. Ex.: ABC12",
                    "class": "autor-input",
                    "autocomplete":"off",
                    "id": "endereco_input_id",
                }
            ),
            "descricao": forms.TextInput(
                attrs={
                    "placeholder": "Digite aqui uma descrição para o código. Campo não obrigatório.",
                    "class": "autor-input",
                    "autocomplete":"off",
                }
            ),
            "presencial": forms.CheckboxInput(
                attrs={
                    "id": "presencial_id"
                }
            )
        }

    def clean(self):
        cleaned_fields = super().clean()
        cleaned_fields["codigo"] = cleaned_fields["codigo"].upper()
