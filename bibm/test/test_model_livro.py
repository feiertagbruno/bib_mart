from bibm.models import Livro
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from datetime import datetime as dt
from .test_base import BibmBaseDefs

    # TESTES DOS LIVROS

class BibmModelLivroTest(BibmBaseDefs):

    def test_model_livro_salvar_primeiro_livro(self):
        livro_dict = self.make_livros_dict()
        livro = Livro.objects.create(**livro_dict)
        self.assertEqual(Livro.objects.first(), livro)
    
    def test_model_livro_titulo_max_length(self):
        # TESTE TAMANHO IGUAL MAX_LENGTH (DEVE PASSAR)
        dict_livro = self.make_livros_dict()
        livro = Livro(**dict_livro)
        livro.titulo = "a" * 300
        livro.full_clean()
        livro.save()
        self.assertEqual(Livro.objects.first().titulo, "a" * 300)
        # TESTE TAMANHO MAIOR QUE O MAX_LENGTH
        livro.titulo = "a" * 301
        with self.assertRaises(ValidationError):
            livro.full_clean()
        livro.titulo = dict_livro["titulo"]

    def test_model_livro_titulo_unique(self):
        dict_livro = self.make_livros_dict(titulo="Título Duplicado")
        Livro.objects.create(**dict_livro)
        with self.assertRaises(IntegrityError):
            Livro.objects.create(**self.make_livros_dict(titulo="Título Duplicado"))
    
    def test_model_livro_editora_max_length(self):
        livro = Livro(**self.make_livros_dict(editora="a"*300))
        livro.full_clean()
        livro.save()
        self.assertEqual(Livro.objects.first(), livro)

        livro.editora = "a"*301
        with self.assertRaises(ValidationError):
            livro.full_clean()
        
    def test_model_livro_titulo_vazio_raises_error(self):
        livro = Livro(**self.make_livros_dict(titulo=""))
        with self.assertRaises(ValidationError):
            livro.full_clean()
    
    def test_model_livro_tema_max_length(self):
        livro = Livro(**self.make_livros_dict())
        livro.tema = "a" * 600
        livro.full_clean()
        livro.save()
        self.assertEqual(Livro.objects.first(), livro)

        livro.tema = "a" * 601
        with self.assertRaises(ValidationError):
            livro.full_clean()
    
    def test_model_livro_lido_default_false(self):
        Livro.objects.create(**self.make_livros_dict())
        self.assertEqual(Livro.objects.first().lido, False)
    
    def test_model_livro_leria_de_novo_default_false(self):
        Livro.objects.create(**self.make_livros_dict())
        self.assertEqual(Livro.objects.first().leria_de_novo, False)

    def test_model_livro_string_representation(self):
        Livro.objects.create(**self.make_livros_dict())
        self.assertEqual(Livro.objects.first().__str__(),"1 - Título do Livro")
    
    def test_model_livro_planejamento_nao_permite_duplicacao(self):
        for i in range(2):
            livro = Livro(**self.make_livros_dict(titulo=f"Título-{i}"))
            livro.full_clean()
            livro.save()
        self.assertEqual(len(Livro.objects.all()),2)

        livro = Livro.objects.get(id=1)
        livro.planejamento = 1
        livro.full_clean()
        livro.save()
        livro = Livro.objects.get(id=2)
        with self.assertRaises(ValidationError):
            livro.planejamento = 1
            livro.full_clean()