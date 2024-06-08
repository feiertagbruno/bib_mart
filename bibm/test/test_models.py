from bibm.models import Regiao, Genero, Endereco, Autor, Anotacao, Livro
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from datetime import datetime as dt
from .test_base import BibmBaseDefs
from bibm.forms import AnotacaoForm

class BibmModelsTest(BibmBaseDefs):

    # TESTES REGIAO

    def test_model_regiao(self):
        regiao = Regiao(**self.make_regiao_dict())
        regiao.full_clean()
        regiao.save()
        self.assertEqual(Regiao.objects.first().regiao, "Região Padrão")

    def test_model_regiao_max_length_correct(self):
        regiao = Regiao(**self.make_regiao_dict(regiao=("a" * 65)))
        regiao.full_clean()
        regiao.save()
        self.assertEqual(Regiao.objects.first().regiao, ("a" * 65))
    
    def test_model_regiao_max_length_error(self):
        regiao = Regiao(**self.make_regiao_dict(regiao=("a" * 66)))
        with self.assertRaises(ValidationError):
            regiao.full_clean()

    def test_model_regiao_string(self):
        regiao = Regiao.objects.create(**self.make_regiao_dict())
        self.assertEqual(str(regiao), "1 - Região Padrão")

    def test_model_regiao_unique(self):
        Regiao.objects.create(**self.make_regiao_dict(regiao = "Região Duplicada"))
        with self.assertRaises(IntegrityError):
            Regiao.objects.create(**self.make_regiao_dict(regiao = "Região Duplicada"))

    # TESTES GÊNERO

    def test_model_genero(self):
        Genero.objects.create(**self.make_genero_dict())
        self.assertEqual(Genero.objects.first().genero, "Gênero Padrão")

    def test_model_genero_max_length(self):
        genero = Genero()
        genero.genero = "a" * 65
        genero.full_clean()
        genero.save()
        self.assertEqual(Genero.objects.first().genero, "a" * 65)
        genero.genero = "a" * 66
        with self.assertRaises(ValidationError):
            genero.full_clean()
    
    def test_model_genero_string(self):
        Genero.objects.create(**self.make_genero_dict())
        self.assertEqual(str(Genero.objects.first()), "1 - Gênero Padrão")
    
    def test_model_genero_unique_field_genero(self):
        Genero.objects.create(**self.make_genero_dict(genero="Gênero Duplicado"))
        with self.assertRaises(IntegrityError):
            Genero.objects.create(**self.make_genero_dict(genero="Gênero Duplicado"))

    # TESTES ENDERECO

    def test_model_enereco_validacao_codigo_e_max_length(self):
        """A validação do código é: Três letras maiúsculas seguidas de dois números, necessariamente."""
        endereco = Endereco(**self.make_endereco_dict(codigo="AAa01"))
        with self.assertRaises(ValidationError):
            endereco.full_clean()
        endereco = Endereco(**self.make_endereco_dict(codigo="AA101"))
        with self.assertRaises(ValidationError):
            endereco.full_clean()
        endereco = Endereco(**self.make_endereco_dict(codigo="AAAA1"))
        with self.assertRaises(ValidationError):
            endereco.full_clean()
        endereco = Endereco(**self.make_endereco_dict(codigo="AA001"))
        with self.assertRaises(ValidationError):
            endereco.full_clean()
        endereco = Endereco(**self.make_endereco_dict(codigo="AA01"))
        with self.assertRaises(ValidationError):
            endereco.full_clean()
        endereco = Endereco(**self.make_endereco_dict(codigo="AAA001"))
        with self.assertRaises(ValidationError):
            endereco.full_clean()
        endereco = Endereco(**self.make_endereco_dict(codigo="ZZA0B"))
        with self.assertRaises(ValidationError):
            endereco.full_clean()
        endereco = Endereco.objects.create(**self.make_endereco_dict())
        self.assertEqual(Endereco.objects.first().codigo, "TST01")
    
    def test_model_endereco_descricao_max_length(self):
        endereco = Endereco(**self.make_endereco_dict(descricao=("a" * 300)))
        endereco.full_clean()
        endereco.save()
        self.assertEqual(Endereco.objects.first().descricao, ("a" * 300))
        endereco.descricao = "a" * 301
        with self.assertRaises(ValidationError):
            endereco.full_clean()
        
    def test_model_endereco_descricao_null(self):
        Endereco.objects.create(**self.make_endereco_dict(descricao=""))
        self.assertEqual(Endereco.objects.first().descricao, "")
    
    def test_model_endereco_string(self):
        Endereco.objects.create(**self.make_endereco_dict())
        self.assertEqual(str(Endereco.objects.first()), "1 - TST01")
    
    # TESTES AUTOR

    def test_model_autor_max_lengths_dos_nomes_e_string_representation(self):
        """Teste da string representation está na última asserção"""

        # CRIANDO A REGIÃO DEFAULT
        self.criar_regiao_default()

        #CRIANDO O PRIMEIRO AUTOR DENTRO DO LIMITE DO MAX_LENGTH
        autor = Autor(**self.make_autor_dict(prim_nome="a"*65, ult_nome="b"*65))
        autor.full_clean()
        autor.save()

        autor_salvo = Autor.objects.first()

        self.assertEqual(autor_salvo.prim_nome, "a" * 65)
        self.assertEqual(autor_salvo.ult_nome, "b" * 65)

        # ALTERAR PRIM E ULT NOME PARA 66 CARACT PARA CAIR NO VALIDATION ERROR
        autor.prim_nome = "a" * 66
        with self.assertRaises(ValidationError):
            autor.full_clean()
        autor.prim_nome = "a" * 65
        autor.ult_nome = "b" * 66
        with self.assertRaises(ValidationError):
            autor.full_clean()

        # TENTAR SALVAR ZERADO PARA CAIR NO VALIDATION ERROR
        autor.ult_nome = ""
        with self.assertRaises(ValidationError):
            autor.full_clean()
        autor.ult_nome = "Padrão"
        autor.prim_nome = ""
        with self.assertRaises(ValidationError):
            autor.full_clean()
        autor.prim_nome = "Autor"

        autor.full_clean()
        autor.save()
        autor_salvo = Autor.objects.first()
        self.assertEqual(str(autor_salvo), "1 - Autor Padrão")
    
    def test_model_autor_deixa_salvar_nacionalidade_em_branco(self):

        # CRIANDO A REGIÃO DEFAULT
        self.criar_regiao_default()

        autor = Autor(**self.make_autor_dict(nacionalidade=""))
        autor.full_clean()
        autor.save()

        self.assertEqual(Autor.objects.first().nacionalidade, "")
    
    def test_model_autor_apagando_regiao_para_testar_set_default(self):

        # CRIANDO A REGIÃO DEFAULT
        self.criar_regiao_default()

        # CRIANDO MAIS UMA REGIÃO
        nova_regiao = Regiao.objects.create(**self.make_regiao_dict(regiao="Nova Região"))

        autor = Autor(**self.make_autor_dict())
        autor.regiao = nova_regiao
        autor.full_clean()
        autor.save()

        nova_regiao.delete()
        autor_default_regiao_id = Autor._meta.get_field("regiao").default

        self.assertEqual(
            Autor.objects.first().regiao.pk, 
            autor_default_regiao_id
        )
    
    def test_model_anotacao_criando_nova_anotacao(self):
        nova_anotacao = Anotacao(
            livro = Livro.objects.create(**self.make_livros_dict()),
            anotacao = "Nova anotação teste"
        )
        nova_anotacao.full_clean()
        nova_anotacao.save()
        self.assertEqual(Anotacao.objects.first().anotacao, "Nova anotação teste")
    