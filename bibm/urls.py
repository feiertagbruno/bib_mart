from django.contrib import admin
from django.urls import path
from . import views

app_name = "bibm"

urlpatterns = [
	path("", views.home, name="home"),
    path("anotacao/<livro_id>/", views.add_anotacao, name="add_anotacao"),
    path("anotacao/<livro_id>/editar/<anotacao_id>/", views.edit_anotacao, name="edit_anotacao"),
    path("anotacao/<livro_id>/excluir/<anotacao_id>", views.delete_anotacao, name="delete_anotacao"),
    path("meuslivros/pegarestelivro/", views.pegar_este_livro, name="pegar_este_livro"),
    path("meuslivros/devolver/<livro_id>/", views.devolver, name="devolver"),
    path("meuslivros/devolver_sim/", views.devolver_sim, name="devolver_sim"),
    path("meuslivros/devolver_sim_classificacao/<livro_id>/", views.devolver_sim_classificacao, name="devolver_sim_classificacao"),
    path("meuslivros/devolver_nao/", views.devolver_nao, name="devolver_nao"),
    path("meuslivros/<filtro>/", views.meus_livros, name="meus_livros"),
    path("editarplanejamento/<filtro>/", views.editar_planejamento, name="editar_planejamento"),
    path("subirplan/", views.subir_plan, name="subir_plan"),
    path("descerplan/", views.descer_plan, name="descer_plan"),
	path("pulareste/", views.pular_este, name="pular_este"),
	path("removerdoplanejamento/", views.remover_do_planejamento, name="remover_do_planejamento"),
	path("mapadabibli/", views.mapa_da_bibli, name="mapa_da_bibli"),
	path("adicionarumlivro/", views.add_um_livro, name="add_um_livro"),
    path("adicionarumlivro/adicionarumautor/", views.add_um_autor_livro, name="add_um_autor_livro"),
    path("adicionarumlivro/adicionarumautor/save/", views.add_um_autor_livro_save, name="add_um_autor_livro_save"),
    path("adicionarumlivro/adicionarumaregiao/", views.add_uma_regiao_livro, name="add_uma_regiao_livro"),
    path("adicionarumlivro/adicionarumaregiao/save/", views.add_uma_regiao_livro_save, name="add_uma_regiao_livro_save"),
    path("adicionarumlivro/adicionarumgenero/", views.add_um_genero_livro, name="add_um_genero_livro"),
    path("adicionarumlivro/adicionarumgenero/save/", views.add_um_genero_livro_save, name="add_um_genero_livro_save"),
    path("adicionarumlivro/adicionarumendereco/", views.add_um_endereco_livro, name="add_um_endereco_livro"),
    path("adicionarumlivro/adicionarumendereco/save/", views.add_um_endereco_livro_save, name="add_um_endereco_livro_save"),
    path("editarumlivro/<livro_id>/", views.editar_um_livro, name="editar_um_livro"),
    path("editarumlivro/", views.editar_um_livro_save, name="editar_um_livro_save"),
    path("deletarumlivro/", views.deletar_um_livro, name="deletar_um_livro"),
	path("acrescentarnoplanejamento/", views.acrescentar_no_planejamento, name="acrescentar_no_planejamento"),
	path("acrescentarnoplanejamentomeuslivros/", views.acrescentar_no_planejamento_meus_livros, name="acrescentar_no_planejamento_meus_livros"),
	path("testes/", views.chamar_html_teste, name="testes"),
]