const box_se_lido = document.querySelector("#box-se-lido")
const checkBox_lido = document.querySelector("#checkbox-lido")
const btn_adicionar = document.querySelector("#btn_adicionar")
const form = document.querySelector(".autor-box-form")
const titulo_input = document.querySelector("#id_titulo")
const tema_input = document.querySelector("#id_tema")
const data_compra_input = document.querySelector("#data_compra")
let elemento_em_foco = null;

document.addEventListener("DOMContentLoaded", function(e) {
	if (checkBox_lido.checked) {
		box_se_lido.style.display = "flex"
	}

	if (autor_salvo) {
		titulo_input.focus()
	} else if (regiao_salva) {
		genero_input.focus()
	} else if (genero_salvo) {
		tema_input.focus()
	} else if (endereco_salvo) {
		data_compra_input.focus()
	} else {
		autor_input.focus()
	}

	checkBox_lido.addEventListener("click",function(e){
		if (e.target.checked) {
			box_se_lido.style.display = "flex";
		} else if (!e.target.checked) {
			box_se_lido.style.display = "none";
		}
	})

	btn_adicionar.addEventListener("click", function(e) {
		form.removeAttribute("novalidate")
	})

})