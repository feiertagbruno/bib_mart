const select_opc = document.querySelector(".autores-opcoes")

const autores = select_opc.options
let lista_autores = []
const autor_input = document.querySelector("#autor-input")
const botao_abrir_select = document.querySelector(".abrir-select")

for (let aut of autores) {
	lista_autores.push(aut["value"])
}

autor_input.addEventListener("input", function(e) {
	const inputValue = this.value.toLowerCase()
	select_opc.innerHTML = ""

	if (inputValue) {
		const filtro = lista_autores.filter(item => item.toLowerCase().includes(inputValue))

		for (let item of filtro) {
			const option = document.createElement("option")
			option.value = item
			option.textContent = item
			select_opc.appendChild(option)
		}

		eventoFocusDoSelect()
		
		select_opc.style.display = filtro.length ? "block" : "none"
		if (filtro.length) {
			select_opc.selectedIndex = 0
		} else {
			select_opc.style.display = "none"
		}
	} else {
		select_opc.style.display = "none"
		for (let item of lista_autores) {
			const option = document.createElement("option")
			option.value = item
			option.textContent = item
			const elemento = select_opc.appendChild(option)
			eventoFocusDoSelect()
		}
	}
})

autor_input.addEventListener("keydown", function(e) {
	if (e.key === "Enter" || e.key === "Tab") {
		if (select_opc.style.display === "block" && autores.length > 0) {
			autor_input.value = select_opc.options[select_opc.selectedIndex].value
			select_opc.style.display = "none"
		}
	}
	if (e.key === "ArrowDown") {
		e.preventDefault()
		if (select_opc.style.display === "block" && autores.length > 0) {
			select_opc.selectedIndex = (select_opc.selectedIndex + 1) % select_opc.options.length
		}
	}
	if (e.key === "ArrowUp") {
		e.preventDefault()
		if (select_opc.style.display === "block" && autores.length > 0) {
			select_opc.selectedIndex = (select_opc.selectedIndex - 1 + select_opc.options.length)
			% select_opc.options.length
		}
	}
})

botao_abrir_select.addEventListener("click", function(e) {
	select_opc.style.display = "block"
	autor_input.focus()
})

autor_input.addEventListener("blur", function(e) {
    setTimeout(() => {
        select_opc.style.display = "none";
    }, 500);
});

function eventoFocusDoSelect() {
	for (let i = 0; i < select_opc.length; i++) {
		select_opc[i].addEventListener("mouseover",function(e) {
			select_opc.selectedIndex = e.target.index
		});
	};
}
eventoFocusDoSelect()

select_opc.addEventListener("click", function(e) {
	if (e.target.tagName === "OPTION") {
		autor_input.value = e.target.value
		select_opc.style.display = "none"
	}
})