from django.test import TestCase
from bibm.models import Regiao, Genero, Endereco, Autor, Livro
from datetime import datetime as dt
from django.db.models import Max

class BibmBaseDefs(TestCase):

    # FUNÇÕES NECESSÁRIAS PARA OS TESTES

    def make_regiao_dict(self, regiao = None, comentario = None):
        if regiao == None:
            i = 1
            regiao = "Região Padrão"
            while Regiao.objects.filter(regiao = regiao).exists():
                regiao = f"Região Padrão{i}"
                i += 1
        return {
            "regiao": regiao,
            "comentario": comentario,
        }

    def make_genero_dict(self, genero=None, comentario=None):
        if genero == None:
            genero = "Gênero Padrão"
        return {
            "genero":genero,
            "comentario":comentario,
        }

    def make_endereco_dict(self, codigo=None, descricao=None, comentario=None):
        if codigo == None:
            codigo = "TST01"
        if descricao == None:
            descricao = "Descrição Padrão"
        return {
            "codigo": codigo,
            "descricao": descricao,
            "comentario": comentario,
        }
    
    def make_autor_dict(
            self,
            prim_nome = None,
            ult_nome = None,
            nacionalidade = None,
            comentario = None,
            regiao = None,
    ):
        if prim_nome == None:
            prim_nome = "Autor"
        if ult_nome == None:
            ult_nome = "Padrão"
        if nacionalidade == None:
            nacionalidade = "Brasileiro"
        if regiao == None:
            regiao_padrao_id = Autor._meta.get_field("regiao").get_default()
            if Regiao.objects.filter(id=regiao_padrao_id).exists():
                regiao = Regiao.objects.get(id=regiao_padrao_id)
            else:
                regiao = self.criar_regiao_default()

        return {
            "prim_nome":prim_nome,
            "ult_nome":ult_nome,
            "nacionalidade":nacionalidade,
            "comentario":comentario,
            "regiao":regiao,
        }
    
    def criar_regiao_default(self):
        regiao = Regiao(**self.make_regiao_dict())
        regiao.id = 2
        regiao.full_clean()
        regiao.save()
        return regiao
    
    def make_livros_dict(
            self,
            titulo = "Título do Livro",
            editora = "Editora do Livro",
            autor = None,
            genero = None,
            tema = "Tema do Livro",
            lendo = Livro._meta.get_field("lendo").get_default(),
            lido = Livro._meta.get_field("lido").get_default(),
            data_leitura = dt.now(),
            leria_de_novo = Livro._meta.get_field("leria_de_novo").get_default(),
            classificacao = 10,
            endereco = None,
            data_compra = dt.now(),
            regiao = None,
            comentario = None,
            planejamento = None,
            definir_planejamento = False,
    ):
        # TRATAMENTO DE TÍTULO DUPLICADO
        if titulo != "Título Duplicado":
            i = 0
            titulo_alt = titulo
            while len(Livro.objects.filter(titulo = titulo_alt)) > 0:
                i += 1
                titulo_alt = f"{titulo}{i}"
            titulo = titulo_alt

        # TRATAR OS FOREIGNKEYS
        # AUTOR, GENERO, ENDERECO, REGIAO
        if regiao == None:
            livro_regiao_default = Livro._meta.get_field("regiao").default
            if not Regiao.objects.filter(id = livro_regiao_default).exists():
                regiao = Regiao(**self.make_regiao_dict())
                regiao.id = livro_regiao_default
                regiao.full_clean()
                regiao.save()
            else:
                regiao = Regiao.objects.get(id = livro_regiao_default)
        
        if autor == None:
            livro_autor_default = Livro._meta.get_field("autor").default
            if not Autor.objects.filter(id = livro_autor_default).exists():
                autor = Autor(**self.make_autor_dict())
                autor.id = livro_autor_default
                autor.full_clean()
                autor.save()
            else:
                autor = Autor.objects.get(id = livro_autor_default)
        
        if genero == None:
            livro_genero_default = Livro._meta.get_field("genero").default
            if len(Genero.objects.filter(id = livro_genero_default)) == 0:
                genero = Genero(**self.make_genero_dict())
                genero.id = livro_genero_default
                genero.full_clean()
                genero.save()
            else:
                genero = Genero.objects.get(id = livro_genero_default)
        
        if endereco == None:
            endereco = Endereco.objects.create(**self.make_endereco_dict())
        
        if definir_planejamento == True:
            planejamento = Livro.objects.aggregate(planejamento = Max("planejamento"))["planejamento"]
            if planejamento == None:
                planejamento = 1
            else:
                planejamento += 1

        return {
            "titulo": titulo,
            "editora": editora,
            "autor": autor,
            "genero": genero,
            "tema": tema,
            "lendo": lendo,
            "lido": lido,
            "data_leitura": data_leitura,
            "leria_de_novo": leria_de_novo,
            "classificacao": classificacao,
            "endereco": endereco,
            "data_compra": data_compra,
            "regiao": regiao,
            "comentario": comentario,
            "planejamento": planejamento,
        }

    def make_anotacao_dict(
        self,
        livro = None,
        anotacao = "Anotação teste."
    ):
        if livro == None:
            if Livro.objects.first() == None:
                livro = Livro.objects.create(**self.make_livros_dict())
            else:
                livro = Livro.objects.first()
        return {
            "livro":livro,
            "anotacao":anotacao,
        }