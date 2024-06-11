const select_opc_gen = document.querySelector("#generos-opcoes")
const generos = select_opc_gen.options
let lista_generos = []
const genero_input = document.querySelector("#genero-input")
const botao_abrir_select_gen = document.querySelector("#abrir-select-genero")
const genero_id = document.querySelector("#genero_id")

for (let gen of generos) {
	lista_generos.push(gen)
}

genero_input.addEventListener("input", function(e) {
	const inputValue = this.value.toLowerCase()
	select_opc_gen.innerHTML = ""

	if (inputValue) {
		const filtro = lista_generos.filter(item => item.text.toLowerCase().includes(inputValue))

		for (let item of filtro) {
			const option = document.createElement("option")
			option.value = item.value
			option.textContent = item.text
			select_opc_gen.appendChild(option)
		}

		eventoFocusDoSelect()
		
		select_opc_gen.style.display = filtro.length ? "block" : "none"
		if (filtro.length) {
			select_opc_gen.selectedIndex = 0
		} else {
			select_opc_gen.style.display = "none"
		}
	} else {
		select_opc_gen.style.display = "none"
		for (let item of lista_generos) {
			const option = document.createElement("option")
			option.value = item.value
			option.textContent = item.text
			const elemento = select_opc_gen.appendChild(option)
			eventoFocusDoSelect()
		}
	}
})

genero_input.addEventListener("keydown", function(e) {
	if (e.key === "Enter" || e.key === "Tab") {
		if (e.key ==="Enter") e.preventDefault()
		if (select_opc_gen.style.display === "block" && generos.length > 0) {
			genero_input.value = select_opc_gen.options[select_opc_gen.selectedIndex].text
			genero_id.value = select_opc_gen.options[select_opc_gen.selectedIndex].value
			select_opc_gen.style.display = "none"
		}
	}
	if (e.key === "ArrowDown") {
		e.preventDefault()
		if (select_opc_gen.style.display === "block" && generos.length > 0) {
			select_opc_gen.selectedIndex = (select_opc_gen.selectedIndex + 1) % select_opc_gen.options.length
		}
	}
	if (e.key === "ArrowUp") {
		e.preventDefault()
		if (select_opc_gen.style.display === "block" && generos.length > 0) {
			select_opc_gen.selectedIndex = (select_opc_gen.selectedIndex - 1 + select_opc_gen.options.length)
			% select_opc_gen.options.length
		}
	}
	if (e.key === "Backspace") {
		genero_id.value = null
	}
})

botao_abrir_select_gen.addEventListener("click", function(e) {
	select_opc_gen.style.display = "block"
	genero_input.focus()
})

document.addEventListener("click", function(e) {
	if (
		!botao_abrir_select_gen.contains(e.target) && 
		!genero_input.contains(e.target) && 
		!select_opc_gen.contains(e.target)
	) {
		setTimeout(() => {
			select_opc_gen.style.display = "none";
		}, 300);
	}
});

function eventoFocusDoSelect() {
	for (let i = 0; i < select_opc_gen.length; i++) {
		select_opc_gen[i].addEventListener("mouseover",function(e) {
			select_opc_gen.selectedIndex = e.target.index
		});
	};
}
eventoFocusDoSelect()

select_opc_gen.addEventListener("click", function(e) {
	if (e.target.tagName === "OPTION") {
		genero_input.value = e.target.text
		genero_id.value = e.target.value
		select_opc_gen.style.display = "none"
	}
})