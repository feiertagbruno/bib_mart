const box_se_lido = document.querySelector("#box-se-lido")
const checkBox_lido = document.querySelector("#checkbox-lido")
const btn_adicionar = document.querySelector("#btn_adicionar")
const form = document.querySelector(".autor-box-form")
let elemento_em_foco = null;

document.addEventListener("DOMContentLoaded", function(e) {
	if (checkBox_lido.checked) {
		box_se_lido.style.display = "flex"
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