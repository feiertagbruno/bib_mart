const boxSeLido = document.querySelector("#box-se-lido")
const checkBoxLido = document.querySelector("#checkbox-lido")

checkBoxLido.addEventListener("click",function(e){
	if (e.target.checked) {
		boxSeLido.style.display = "flex";
	} else if (!e.target.checked) {
		boxSeLido.style.display = "none";
	}
})