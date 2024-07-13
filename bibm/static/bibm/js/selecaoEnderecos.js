const select_opc_end = document.querySelector("#enderecos-opcoes")
const enderecos = select_opc_end.options
let lista_enderecos = []
const endereco_input = document.querySelector("#endereco-input")
const botao_abrir_select_end = document.querySelector("#abrir-select-endereco")
const endereco_id = document.querySelector("#endereco_id_field")
const btn_add_um_endereco_livro = document.querySelector("#add_um_endereco_livro")
const endereco_salvo = document.querySelector("#endereco_salvo")
const mensagem_endereco = document.querySelector("#mensagem-endereco")

document.addEventListener("DOMContentLoaded", function(dom) {
	if (endereco_salvo) {
		if (endereco_salvo.value) {
			endereco_id.value = endereco_salvo.value
		}
	}

	if (endereco_id.value) {
		for (let end of enderecos) {
			if (end.value == endereco_id.value) {
				endereco_input.value = end.text
				break
			}
		}
	}

	for (let aut of enderecos) {
		lista_enderecos.push(aut)
	}
	
	endereco_input.addEventListener("input", function(e) {
		const inputValue = this.value.toLowerCase()
		select_opc_end.innerHTML = ""
	
		if (inputValue) {
			const filtro = lista_enderecos.filter(item => item.text.toLowerCase().includes(inputValue))
	
			for (let item of filtro) {
				const option = document.createElement("option")
				option.value = item.value
				option.textContent = item.text
				select_opc_end.appendChild(option)
			}
	
			eventoFocusDoSelect()
			
			select_opc_end.style.display = filtro.length ? "block" : "none"
			if (filtro.length) {
				select_opc_end.selectedIndex = 0
				mensagem_endereco.textContent = ""
			} else {
				select_opc_end.style.display = "none"
				endereco_id.value = null
				if (endereco_input.value) {
					mensagem_endereco.textContent = "Busca sem resultados."
				} else {
					mensagem_endereco.textContent = ""
				}
			}
		} else {
			select_opc_end.style.display = "none"
			for (let item of lista_enderecos) {
				const option = document.createElement("option")
				option.value = item.value
				option.textContent = item.text
				const elemento = select_opc_end.appendChild(option)
				eventoFocusDoSelect()
			}
		}
	})
	
	endereco_input.addEventListener("keydown", function(e) {
		if (e.key === "Enter" || e.key === "Tab") {
			if (e.key ==="Enter") e.preventDefault()
			if (select_opc_end.style.display === "block" && enderecos.length > 0) {
				endereco_input.value = select_opc_end.options[select_opc_end.selectedIndex].text
				endereco_id.value = select_opc_end.options[select_opc_end.selectedIndex].value
				select_opc_end.style.display = "none"
				btn_add_um_endereco_livro.style.display = "none"
				mensagem_endereco.textContent = ""
			}
		}
		if (e.key === "ArrowDown") {
			e.preventDefault()
			if (select_opc_end.style.display === "block" && enderecos.length > 0) {
				select_opc_end.selectedIndex = (select_opc_end.selectedIndex + 1) % select_opc_end.options.length
			} else if (select_opc_end.style.display === "" || select_opc_end.style.display === "none") {
				select_opc_end.style.display = "block"
			}
		}
		if (e.key === "ArrowUp") {
			e.preventDefault()
			if (select_opc_end.style.display === "block" && enderecos.length > 0) {
				select_opc_end.selectedIndex = (select_opc_end.selectedIndex - 1 + select_opc_end.options.length)
				% select_opc_end.options.length
			}
		}
		if (e.key === "Backspace" || e.key ==="Delete") {
			endereco_id.value = null
		}
	})
	
	botao_abrir_select_end.addEventListener("click", function(e) {
		select_opc_end.style.display = "block"
		endereco_input.focus()
	})
	
	document.addEventListener("click", function(e) {
		if (
			!botao_abrir_select_end.contains(e.target) && 
			!endereco_input.contains(e.target) && 
			!select_opc_end.contains(e.target)
		) {
			setTimeout(() => {
				select_opc_end.style.display = "none";
			}, 300);
		}
	});
	
	function eventoFocusDoSelect() {
		for (let i = 0; i < select_opc_end.length; i++) {
			select_opc_end[i].addEventListener("mouseover",function(e) {
				select_opc_end.selectedIndex = e.target.index
			});
		};
	}
	eventoFocusDoSelect()
	
	select_opc_end.addEventListener("click", function(e) {
		if (e.target.tagName === "OPTION") {
			endereco_input.value = e.target.text
			endereco_id.value = e.target.value
			select_opc_end.style.display = "none"
			btn_add_um_endereco_livro.style.display = "none"
			mensagem_endereco.textContent = ""
		}
	})
		
	select_opc_end.addEventListener('wheel', function(event) {
    const maxScrollTop = this.scrollHeight - this.clientHeight;
    if (
        (event.deltaY > 0 && this.scrollTop >= maxScrollTop) ||
        (event.deltaY < 0 && this.scrollTop <= 0)
    ) {
        event.preventDefault();
    }
	});

	btn_add_um_endereco_livro.addEventListener("click", function(e) {
		form.action = form.action + "adicionarumendereco/"
		form.setAttribute("novalidate", "novalidate")
	})
		
	btn_add_um_endereco_livro.addEventListener("blur", function(e) {
		setTimeout(() => {
				if (
					!elemento_em_foco.contains(endereco_input) && 
					!elemento_em_foco.contains(select_opc_end)
				) {
				btn_add_um_endereco_livro.style.display = "none"
				if (!endereco_id.value) {mensagem_endereco.textContent = "Nenhum endereço selecionado."}
				elemento_em_foco.focus()
			}
		}, 300);
	})

	endereco_input.addEventListener("focus", function(e) {
		if (!document.querySelector("[name='editar_um_livro']")) {
			btn_add_um_endereco_livro.style.display = "block"
		}
	})
	
	endereco_input.addEventListener("blur", function(e) {
		setTimeout(() => {
				if (
					!elemento_em_foco.contains(btn_add_um_endereco_livro) &&
					!elemento_em_foco.contains(select_opc_end)
				) {
				btn_add_um_endereco_livro.style.display = "none"
				if (!endereco_id.value) {mensagem_endereco.textContent = "Nenhum endereço selecionado."}
				elemento_em_foco.focus()
			}
		}, 300);
	})
		
	select_opc_end.addEventListener("blur", function(e) {
		setTimeout(() => {
			if (
				!elemento_em_foco.contains(btn_add_um_endereco_livro) &&
				!elemento_em_foco.contains(endereco_input)
			) {
				btn_add_um_endereco_livro.style.display = "none"
				if (!endereco_id.value) {mensagem_endereco.textContent = "Nenhum endereço selecionado."}
				elemento_em_foco.focus()
			}
		}, 300);
	})

	// document.addEventListener("focusin", function(e) {
	// 	elemento_em_foco = e.target
	// })

})

