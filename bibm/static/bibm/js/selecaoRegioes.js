const select_opc_reg = document.querySelector("#regioes-opcoes");
const regioes = select_opc_reg.options;
let lista_regioes = [];
const regiao_input = document.querySelector("#regiao-input");
const botao_abrir_select_reg = document.querySelector("#abrir-select-regiao");
const regiao_id = document.querySelector("#regiao_id_field");
const btn_add_uma_regiao_livro = document.querySelector("#add_uma_regiao_livro")
const regiao_salva = document.querySelector("#regiao_salva")
const mensagem_regiao = document.querySelector("#mensagem-regiao")
const form = document.querySelector(".autor-box-form")
const caller_regiao = document.querySelector("#caller_regiao")

document.addEventListener("DOMContentLoaded", function(dom) {
	if (regiao_salva) {
		if (regiao_salva.value) {
			regiao_id.value = regiao_salva.value
		}
	}

	if (regiao_id.value) {
		for (let reg of regioes) {
			if (reg.value == regiao_id.value) {
				regiao_input.value = reg.text
				break
			}
		}
	}

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
				mensagem_regiao.textContent = ""
			} else {
				select_opc_reg.style.display = "none"
				regiao_id.value = null
				if (regiao_input.value) {
					mensagem_regiao.textContent = "Busca sem resultados. Considere adicionar uma nova região."
				} else {
					mensagem_regiao.textContent = ""
				}
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
				btn_add_uma_regiao_livro.style.display = "none"
				mensagem_regiao.textContent = ""
			}
		}
		if (e.key === "ArrowDown") {
			e.preventDefault()
			if (select_opc_reg.style.display === "block" && regioes.length > 0) {
				select_opc_reg.selectedIndex = (select_opc_reg.selectedIndex + 1) % select_opc_reg.options.length
			} else if (select_opc_reg.style.display === "" || select_opc_reg.style.display === "none") {
				select_opc_reg.style.display = "block"
			}
		}
		if (e.key === "ArrowUp") {
			e.preventDefault()
			if (select_opc_reg.style.display === "block" && regioes.length > 0) {
				select_opc_reg.selectedIndex = (select_opc_reg.selectedIndex - 1 + select_opc_reg.options.length)
				% select_opc_reg.options.length
			}
		}
		if (e.key === "Backspace" || e.key ==="Delete") {
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
			btn_add_uma_regiao_livro.style.display = "none"
			mensagem_regiao.textContent = ""
		}
	})
		
	select_opc_reg.addEventListener('wheel', function(event) {
    const maxScrollTop = this.scrollHeight - this.clientHeight;
    if (
        (event.deltaY > 0 && this.scrollTop >= maxScrollTop) ||
        (event.deltaY < 0 && this.scrollTop <= 0)
    ) {
        event.preventDefault();
    }
	});

	if (btn_add_uma_regiao_livro) {
		btn_add_uma_regiao_livro.addEventListener("click", function(e) {
			if (form.action.slice(-18) === "/adicionarumlivro/") {
				caller_regiao.value = "add_um_livro"
				form.action = form.action + "adicionarumaregiao/"
			} else if (form.action.slice(-23) === "/adicionarumautor/save/") {
				caller_regiao.value = "add_um_autor"
				form.action = form.action.substring(0, form.action.length - 22) + "adicionarumaregiao/"
			}
			form.setAttribute("novalidate", "novalidate")
		})
	}

	if (btn_add_uma_regiao_livro) {
		btn_add_uma_regiao_livro.addEventListener("blur", function(e) {
			setTimeout(() => {
				if (
					!elemento_em_foco.contains(regiao_input) &&
					!elemento_em_foco.contains(select_opc_reg)
				) {
					btn_add_uma_regiao_livro.style.display = "none"
					if (!regiao_id.value) {mensagem_regiao.textContent = "Nenhuma região selecionada."}
					elemento_em_foco.focus()
				}
			},300);
		})
	}

	if (btn_add_uma_regiao_livro) {
		regiao_input.addEventListener("focus", function(e) {
			btn_add_uma_regiao_livro.style.display = "block"
		})
	}

	if (btn_add_uma_regiao_livro) {
		regiao_input.addEventListener("blur", function(e) {
			setTimeout(() => {
				if (
					!elemento_em_foco.contains(btn_add_uma_regiao_livro) &&
					!elemento_em_foco.contains(select_opc_reg)
				) {
					btn_add_uma_regiao_livro.style.display = "none"
					if (!regiao_id.value) {mensagem_regiao.textContent = "Nenhuma região selecionada."}
					elemento_em_foco.focus()
				}
			}, 300);
		})
	}
				
	if (btn_add_uma_regiao_livro) {
		select_opc_reg.addEventListener("blur", function(e) {
			setTimeout(() => {
				if (
					!elemento_em_foco.contains(btn_add_uma_regiao_livro) &&
					!elemento_em_foco.contains(regiao_input)
				) {
					btn_add_uma_regiao_livro.style.display = "none"
					if (!regiao_id.value) {mensagem_regiao.textContent = "Nenhuma região selecionada."}
					elemento_em_foco.focus()
				}
			}, 300);
		})
	}

	document.addEventListener("focusin", function(e) {
		elemento_em_foco = e.target
	})
	
})

