from .test_base import BibmBaseDefs
from django.urls import reverse
from ..models import Livro, Historico, Anotacao, Regiao, Endereco, Autor, Genero
# from parameterized import parameterized
from ..views import livros_planejamento

class BibmViewsTests(BibmBaseDefs):
	def test_home_view_menu(self):
		url = reverse("bibm:home")
		self.assertEqual(url, "/")
		response = self.client.get(url)
		self.assertIn("Meus Livros", response.content.decode("utf-8"))
	
	def test_home_view_exibicao_tela_inicial(self):
		"""Mostra tela inicial de acordo com o momento, se tiver em posse de um livro,
		aparece 'Você está lendo'. Sem livro em posse e com livro no planejamento
		aparece 'Sua próxima leitura é:'. Se não possui posse nem livro no planejamento
		aparece 'Ainda não há planejamento'."""
		url = reverse("bibm:home")
		html = self.client.get(url).content.decode("utf-8")
		self.assertIn("Ainda não há planejamento", html)

		livro = Livro.objects.create(**self.make_livros_dict(planejamento=1))
		html = self.client.get(url).content.decode("utf-8")
		self.assertIn("Sua próxima leitura é:", html)

		livro.lendo = True
		livro.save()
		html = self.client.get(url).content.decode("utf-8")
		self.assertIn("Você está lendo:", html)

	def test_view_pegar_este_livro(self):
		livro = Livro.objects.create(**self.make_livros_dict(definir_planejamento=True))
		self.assertEqual(livro.planejamento, 1)

		livros_planejamento()

		url = reverse("bibm:pegar_este_livro", kwargs={"livro_id":livro.planejamento})
		self.assertEqual(url, "/meuslivros/pegarestelivro/1/")

		Livro.objects.create(**self.make_livros_dict(planejamento=3))
		Livro.objects.create(**self.make_livros_dict(planejamento=4))
		self.client.post(url)

		self.assertEqual(len(Livro.objects.filter(planejamento=1)), 1)
		self.assertEqual(len(Livro.objects.filter(planejamento=2)), 1)
		self.assertEqual(str(Historico.objects.get(id=1)), "1 - Título do Livro")
	
	def test_views_add_anotacao(self):
		livro = Livro.objects.create(**self.make_livros_dict())
		url = reverse("bibm:add_anotacao", kwargs={"livro_id":livro.id})
		form = self.client.get(url).context["form_anotacao"].fields
		form["livro"] = livro.id + 1
		form["anotacao"] = "Anotação Teste"
		self.client.post(url,data = form)
		self.assertEqual(len(Anotacao.objects.all()),0)
		form["livro"] = livro.id
		self.client.post(url,data = form)
		self.assertEqual(len(Anotacao.objects.all()),1)

	
	def test_views_edit_anotacao(self):
		anotacao = Anotacao.objects.create(**self.make_anotacao_dict())
		url = reverse("bibm:edit_anotacao", kwargs={"livro_id":anotacao.livro.id,"anotacao_id":anotacao.id})
		form = self.client.get(url).context.get("form_anotacao")
		form.fields["livro"] = anotacao.livro.id + 1
		form.fields["anotacao"] = form.instance.anotacao + " editado."
		self.client.post(url,data=form.fields)
		self.assertEqual(Anotacao.objects.first().anotacao,"Anotação teste.")
		form.fields["livro"] = anotacao.livro.id
		self.client.post(url,data=form.fields)
		self.assertEqual(Anotacao.objects.first().anotacao,"Anotação teste. editado.")
	
	def test_views_delete_anotacao(self):
		anotacao = Anotacao.objects.create(**self.make_anotacao_dict())
		livro_id = anotacao.livro.id
		url_anotacao = reverse("bibm:add_anotacao", kwargs={"livro_id": livro_id})
		content = self.client.get(url_anotacao).content.decode("utf-8")
		self.assertIn("Anotação teste.", content)
		url_delete = reverse("bibm:delete_anotacao", kwargs={"livro_id":livro_id,"anotacao_id":anotacao.id})
		self.client.get(url_delete)
		self.assertFalse(Anotacao.objects.all().exists())
	
	def test_views_devolver_sim_e_classificacao_e_leriadenovo_true(self):
		livro = Livro.objects.create(**self.make_livros_dict())
		url_pegar_livro = reverse("bibm:pegar_este_livro", kwargs={"livro_id":livro.id})
		self.client.get(url_pegar_livro)
		self.assertTrue(Historico.objects.all().exists())

		url_devolver = reverse("bibm:devolver", kwargs={"livro_id":livro.id})
		content = self.client.get(url_devolver).content.decode("utf-8")
		self.assertIn("Sim",content)
		self.assertIn("Não",content)

		url_devolver = reverse("bibm:devolver_sim_classificacao", kwargs={"livro_id":livro.id})
		content = self.client.get(url_devolver).content.decode("utf-8")
		response = self.client.get(url_devolver)
		self.assertIn("Classificação",content)
		self.assertIn("Leria de novo",content)

		url_devolver = reverse("bibm:devolver_sim", kwargs={"livro_id":livro.id})
		form = response.context.get("form_classificacao").fields
		form["classificacao"] = 10
		form["leria_de_novo"] = "on"
		response = self.client.post(url_devolver,data=form)
		self.assertFalse(Livro.objects.filter(lendo = True).exists())
		self.assertTrue(Livro.objects.filter(classificacao=10).exists())
		self.assertGreater(len(Historico.objects.exclude(data_fim=None)), 0)
	
	def test_views_devolver_validacao_historico_duplicado_e_leriadenovo_false(self):
		livro = Livro.objects.create(**self.make_livros_dict())
		url_pegar_livro = reverse("bibm:pegar_este_livro", kwargs={"livro_id":livro.id})
		self.client.get(url_pegar_livro)
		duplicar_historico = Historico.objects.first()
		duplicar_historico.id = None
		duplicar_historico.save()
		self.assertEqual(len(Historico.objects.all()),2)
		
		url_devolver = reverse("bibm:devolver_sim_classificacao", kwargs={"livro_id":livro.id})
		response = self.client.get(url_devolver)
		form = response.context.get("form_classificacao").fields
		form["classificacao"] = 8
		form["leria_de_novo"] = "off"
		url_devolver = reverse("bibm:devolver_sim", kwargs={"livro_id":livro.id})
		self.client.post(url_devolver,data=form)

		self.assertEqual(len(Historico.objects.all()),1)
		self.assertEqual(Livro.objects.first().leria_de_novo, False)

		url_planejamento = reverse("bibm:editar_planejamento")
		content = self.client.get(url_planejamento).content.decode("utf-8")
		self.assertIn("Você não possui nenhum livro não lido.", content)

	def test_views_devolver_nao(self):
		livro = Livro.objects.create(**self.make_livros_dict())
		url_pegar_livro = reverse("bibm:pegar_este_livro", kwargs={"livro_id":livro.id})
		self.client.get(url_pegar_livro)

		duplicar_historico = Historico.objects.first()
		duplicar_historico.id = None
		duplicar_historico.save()
		self.assertEqual(len(Historico.objects.all()),2)

		url_devolver_nao = reverse("bibm:devolver_nao", kwargs={"livro_id":livro.id})
		content = self.client.get(url_devolver_nao, follow=True).content.decode("utf-8")
		
		self.assertIn("Ainda não há planejamento", content)
		self.assertTrue(Livro.objects.filter(lido=False).exists())
		self.assertEqual(len(Historico.objects.all()),1)
	
	def test_views_editar_planejamento_com_search_term(self):
		Livro.objects.create(**self.make_livros_dict(titulo="Buscar este Título Aqui"))
		Livro.objects.create(**self.make_livros_dict(titulo="Não Buscar este Outro"))
		url_editar_planejamento = reverse("bibm:editar_planejamento")
		url = f"{url_editar_planejamento}?q=Aqui"
		content = self.client.get(url).content.decode("utf-8")
		self.assertIn("Buscar este Título Aqui", content)
		self.assertNotIn("Não Buscar", content)
	
	def test_editar_planejamento_subir_plan_e_descer_plan_view(self):
		livro1 = Livro.objects.create(**self.make_livros_dict(definir_planejamento=True))
		livro2 = Livro.objects.create(**self.make_livros_dict(
				regiao=livro1.regiao,
				autor=livro1.autor,
				genero=livro1.genero,
				endereco=livro1.endereco,
				definir_planejamento=True,
			))
		Livro.objects.create(**self.make_livros_dict(
				regiao=livro1.regiao,
				autor=livro1.autor,
				genero=livro1.genero,
				endereco=livro1.endereco,
				definir_planejamento=True,
			))
		url = reverse("bibm:editar_planejamento")
		content = self.client.get(url).content.decode("utf-8")
		self.assertIn("1 - Título do Livro", content)
		self.assertIn("2 - Título do Livro1", content)
		self.assertIn("3 - Título do Livro2", content)

		url_subir = reverse("bibm:subir_plan", kwargs={"livro_id":livro2.id})
		content = self.client.get(url_subir,follow=True).content.decode("utf-8")
		self.assertIn("1 - Título do Livro1", content)
		self.assertIn("2 - Título do Livro", content)
		self.assertIn("3 - Título do Livro2", content)

		url_subir = reverse("bibm:descer_plan", kwargs={"livro_id":livro1.id})
		content = self.client.get(url_subir,follow=True).content.decode("utf-8")
		self.assertIn("1 - Título do Livro1", content)
		self.assertIn("2 - Título do Livro2", content)
		self.assertIn("3 - Título do Livro", content)

		url_subir = reverse("bibm:subir_plan", kwargs={"livro_id":livro2.id})
		content = self.client.get(url_subir,follow=True).content.decode("utf-8")
		self.assertIn("1 - Título do Livro1", content)
		self.assertIn("2 - Título do Livro2", content)
		self.assertIn("3 - Título do Livro", content)

		url_subir = reverse("bibm:descer_plan", kwargs={"livro_id":livro1.id})
		content = self.client.get(url_subir,follow=True).content.decode("utf-8")
		self.assertIn("1 - Título do Livro1", content)
		self.assertIn("2 - Título do Livro2", content)
		self.assertIn("3 - Título do Livro", content)

	def test_pular_este(self):
		regiao = Regiao.objects.create(**self.make_regiao_dict())
		autor = Autor.objects.create(**self.make_autor_dict(regiao = regiao))
		endereco = Endereco.objects.create(**self.make_endereco_dict())
		genero = Genero.objects.create(**self.make_genero_dict())
		dict_para_livro = {
			"autor": autor,
			"regiao": regiao,
			"endereco": endereco,
			"genero": genero,
			"definir_planejamento": True,
		}

		livro = Livro.objects.create(**self.make_livros_dict(**dict_para_livro))
		url_pular_este = reverse("bibm:pular_este", kwargs={"livro_id":livro.id})
		content = self.client.get(url_pular_este,follow=True).content.decode("utf-8")
		self.assertIn("Mãezinha", content)

		for _ in range(2):
			Livro.objects.create(**self.make_livros_dict(**dict_para_livro))
		url_editar_planejamento = reverse("bibm:editar_planejamento")
		content = self.client.get(url_editar_planejamento).content.decode("utf-8")
		self.assertIn("1 - Título do Livro", content)
		self.assertIn("2 - Título do Livro1", content)
		self.assertIn("3 - Título do Livro2", content)

		self.client.get(url_pular_este)
		content = self.client.get(url_editar_planejamento).content.decode("utf-8")
		self.assertIn("1 - Título do Livro1", content)
		self.assertIn("2 - Título do Livro2", content)
		self.assertIn("3 - Título do Livro", content)

	def test_remover_do_planejamento(self):
		livro = Livro.objects.create(**self.make_livros_dict(definir_planejamento=True))
		self.assertTrue(Livro.objects.exclude(planejamento=None).exists())
		url = reverse("bibm:remover_do_planejamento", kwargs={"livro_id":livro.id})
		self.client.get(url)
		self.assertTrue(Livro.objects.filter(planejamento=None).exists())
	