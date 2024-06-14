const select_opc_reg = document.querySelector("#regioes-opcoes")
const regioes = select_opc_reg.options
let lista_regioes = []
const regiao_input = document.querySelector("#regiao-input")
const botao_abrir_select_reg = document.querySelector("#abrir-select-regiao")
const regiao_id = document.querySelector("#regiao_id_field")

for (let reg of regioes) {
	lista_regioes.push(reg)
}

regiao_input.addEventListener("input", function(e) {
	const inputValue = this.value.toLowerCase()
	select_opc_reg.innerHTML = ""

	if (inputValue) {
		const filtro = lista_regioes.filter(item => item.text.toLowerCase().includes(inputValue))

		for (let item of filtro) {
			const option = document.createElement("option")
			option.value = item.value
			option.textContent = item.text
			select_opc_reg.appendChild(option)
		}

		eventoFocusDoSelect()
		
		select_opc_reg.style.display = filtro.length ? "block" : "none"
		if (filtro.length) {
			select_opc_reg.selectedIndex = 0
		} else {
			select_opc_reg.style.display = "none"
		}
	} else {
		select_opc_reg.style.display = "none"
		for (let item of lista_regioes) {
			const option = document.createElement("option")
			option.value = item.value
			option.textContent = item.text
			const elemento = select_opc_reg.appendChild(option)
			eventoFocusDoSelect()
		}
	}
})

regiao_input.addEventListener("keydown", function(e) {
	if (e.key === "Enter" || e.key === "Tab") {
		if (e.key ==="Enter") e.preventDefault()
		if (select_opc_reg.style.display === "block" && regioes.length > 0) {
			regiao_input.value = select_opc_reg.options[select_opc_reg.selectedIndex].text
			regiao_id.value = select_opc_reg.options[select_opc_reg.selectedIndex].value
			select_opc_reg.style.display = "none"
		}
	}
	if (e.key === "ArrowDown") {
		e.preventDefault()
		if (select_opc_reg.style.display === "block" && regioes.length > 0) {
			select_opc_reg.selectedIndex = (select_opc_reg.selectedIndex + 1) % select_opc_reg.options.length
		}
	}
	if (e.key === "ArrowUp") {
		e.preventDefault()
		if (select_opc_reg.style.display === "block" && regioes.length > 0) {
			select_opc_reg.selectedIndex = (select_opc_reg.selectedIndex - 1 + select_opc_reg.options.length)
			% select_opc_reg.options.length
		}
	}
	if (e.key === "Backspace") {
		regiao_id.value = null
	}
})

botao_abrir_select_reg.addEventListener("click", function(e) {
	select_opc_reg.style.display = "block"
	regiao_input.focus()
})

document.addEventListener("click", function(e) {
	if (
		!botao_abrir_select_reg.contains(e.target) && 
		!regiao_input.contains(e.target) && 
		!select_opc_reg.contains(e.target)
	) {
		setTimeout(() => {
			select_opc_reg.style.display = "none";
		}, 300);
	}
});

function eventoFocusDoSelect() {
	for (let i = 0; i < select_opc_reg.length; i++) {
		select_opc_reg[i].addEventListener("mouseover",function(e) {
			select_opc_reg.selectedIndex = e.target.index
		});
	};
}
eventoFocusDoSelect()

select_opc_reg.addEventListener("click", function(e) {
	if (e.target.tagName === "OPTION") {
		regiao_input.value = e.target.text
		regiao_id.value = e.target.value
		select_opc_reg.style.display = "none"
	}
})