const box_se_lido = document.querySelector("#box-se-lido")
const checkBox_lido = document.querySelector("#checkbox-lido")
const btn_adicionar = document.querySelector("#btn_adicionar")
const titulo_input = document.querySelector("#id_titulo")
const tema_input = document.querySelector("#id_tema")
const data_compra_input = document.querySelector("#data_compra")
let elemento_em_foco = null
const data_leitura_field = document.querySelector("#data_leitura_field")
const data_compra_field = document.querySelector("#data_compra_field")

document.addEventListener("DOMContentLoaded", function(e) {

	checkBox_lido.addEventListener("click",function(e){
		if (e.target.checked) {
			box_se_lido.style.display = "flex";
		} else if (!e.target.checked) {
			box_se_lido.style.display = "none";
		}
	})

	btn_adicionar.addEventListener("click", function(e) {

		form.removeAttribute("novalidate")

		let data_agora = new Date()
		data_agora = `${data_agora.getFullYear()}-`+
			`${(data_agora.getMonth()+1).toString().padStart(2,"0")}-`+
			`${data_agora.getDate().toString().padStart(2,"0")}`

		// VALIDAÇÕES ANTES DE SALVAR
		if (
			checkBox_lido.checked &&
			!data_leitura_field.value
		) {
			if (!confirm("O livro foi marcado como lido, mas a data de leitura não foi preenchida," +
				" a data de hoje será considerada. Tudo bem?")) {
					e.preventDefault()
					data_leitura_field.focus()
					return
				} else {
					data_leitura_field.value = data_agora
				}
		}
		if (data_leitura_field.value > data_agora && data_leitura_field.value) {
			if (!confirm("A data de leitura é maior do que a data de hoje. Deseja salvar assim mesmo?")) {
				e.preventDefault()
				data_leitura_field.focus()
				return
			}
		}
		if (data_compra_field.value > data_agora && data_compra_field.value) {
			if (!confirm("A data de compra é maior do que a data de hoje. Deseja salvar assim mesmo?")) {
				e.preventDefault()
				data_compra_field.focus()
				return
			}
		}
		if (
			data_compra_field.value > data_leitura_field.value &&
			data_compra_field.value && data_leitura_field.value
		) {
			if (!confirm("A data de compra está maior do que a data de leitura, deseja salvar assim mesmo?")) {
				e.preventDefault()
				data_compra_field.focus()
				return
			}
		}
		if (!data_compra_field.value) {
			data_compra_field.value = data_agora
		}
		// VALIDAÇÕES ANTES DE SALVAR -- FIM
	})

	btn_adicionar.addEventListener("keydown", function(e) {
		if (e.key === "Enter") {
			btn_adicionar.click()
		}
	})

	btn_add_um_autor_livro.addEventListener("keydown", function(e) {
		if (e.key === "Enter") {
			btn_add_um_autor_livro.click()
		}
	})

	btn_add_uma_regiao_livro.addEventListener("keydown", function(e) {
		if (e.key === "Enter") {
			btn_add_uma_regiao_livro.click()
		}
	})

	btn_add_um_genero_livro.addEventListener("keydown", function(e) {
		if (e.key === "Enter") {
			btn_add_um_genero_livro.click()
		}
	})

	btn_add_um_endereco_livro.addEventListener("keydown", function(e) {
		if (e.key === "Enter") {
			btn_add_um_endereco_livro.click()
		}
	})

	document.addEventListener("keydown", function(e) {
		if (e.key === "Enter") {
			e.preventDefault()
		}
	})

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

})