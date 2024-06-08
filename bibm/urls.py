from django.contrib import admin
from django.urls import path
from . import views

app_name = "bibm"

urlpatterns = [
	path("", views.home, name="home"),
    path("anotacao/<livro_id>/", views.add_anotacao, name="add_anotacao"),
    path("anotacao/<livro_id>/editar/<anotacao_id>/", views.edit_anotacao, name="edit_anotacao"),
    path("anotacao/<livro_id>/excluir/<anotacao_id>", views.delete_anotacao, name="delete_anotacao"),
    path("meuslivros/<filtro>/", views.meus_livros, name="meus_livros"),
    path("meuslivros/pegarestelivro/", views.pegar_este_livro, name="pegar_este_livro"),
    path("meuslivros/devolver/<livro_id>/", views.devolver, name="devolver"),
    path("meuslivros/devolver_sim/", views.devolver_sim, name="devolver_sim"),
    path("meuslivros/devolver_sim_classificacao/<livro_id>/", views.devolver_sim_classificacao, name="devolver_sim_classificacao"),
    path("meuslivros/devolver_nao/", views.devolver_nao, name="devolver_nao"),
    path("editarplanejamento/<filtro>/", views.editar_planejamento, name="editar_planejamento"),
    path("subirplan/<livro_id>/", views.subir_plan, name="subir_plan"),
    path("descerplan/<livro_id>/", views.descer_plan, name="descer_plan"),
	path("pulareste/", views.pular_este, name="pular_este"),
	path("removerdoplanejamento/", views.remover_do_planejamento, name="remover_do_planejamento"),
	path("mapadabibli/", views.mapa_da_bibli, name="mapa_da_bibli"),
	path("adicionarumlivro/", views.add_um_livro, name="add_um_livro"),
	path("adicionarumlivro/autor/", views.add_livro_autor, name="add_livro_autor"),
	path("acrescentarnoplanejamento/", views.acrescentar_no_planejamento, name="acrescentar_no_planejamento"),
	path("acrescentarnoplanejamentomeuslivros/", views.acrescentar_no_planejamento_meus_livros, name="acrescentar_no_planejamento_meus_livros"),
	path("testes/", views.chamar_html_teste, name="testes"),
]