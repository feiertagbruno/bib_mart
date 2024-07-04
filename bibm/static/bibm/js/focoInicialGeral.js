const prim_nome_autor = document.querySelector("#prim_nome_autor")
const genero_input_id = document.querySelector("#genero_input_id")
const regiao_input_id = document.querySelector("#regiao_input_id")
const endereco_input_id = document.querySelector("#endereco_input_id")

document.addEventListener("DOMContentLoaded", function(e) {

	if (prim_nome_autor) {
		prim_nome_autor.focus()
	}

	if (genero_input_id) {
		genero_input_id.focus()
	}

	if (regiao_input_id) {
		regiao_input_id.focus()
	}

	if (endereco_input_id) {
		endereco_input_id.focus()
	}

})