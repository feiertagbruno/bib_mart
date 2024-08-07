const select_opc = document.querySelector("#autores-opcoes")
const autores = select_opc.options
let lista_autores = []
const autor_input = document.querySelector("#autor-input")
const botao_abrir_select = document.querySelector("#abrir-select-autor")
const autor_id = document.querySelector("#autor_id_field")
const btn_add_um_autor_livro = document.querySelector("#add_um_autor_livro")
const autor_salvo = document.querySelector("#autor_salvo")
const mensagem_autor = document.querySelector("#mensagem-autor")

document.addEventListener("DOMContentLoaded", function(dom) {
	if (autor_salvo) {
		if (autor_salvo.value) {
			autor_id.value = autor_salvo.value
		}
	}
	
	if (autor_id.value) {
		for (let aut of autores) {
			if (aut.value == autor_id.value) {
				autor_input.value = aut.text
				break
			}
		}
	}

	for (let aut of autores) {
		lista_autores.push(aut)
	}
	
	autor_input.addEventListener("input", function(e) {
		const inputValue = this.value.toLowerCase()
		select_opc.innerHTML = ""
	
		if (inputValue) {
			const filtro = lista_autores.filter(item => item.text.toLowerCase().includes(inputValue))
	
			for (let item of filtro) {
				const option = document.createElement("option")
				option.value = item.value
				option.textContent = item.text
				select_opc.appendChild(option)
			}
	
			eventoFocusDoSelect()
			
			select_opc.style.display = filtro.length ? "block" : "none"
			if (filtro.length) {
				select_opc.selectedIndex = 0
				mensagem_autor.textContent = ""
			} else {
				select_opc.style.display = "none"
				autor_id.value = null
				if (autor_input.value) {
					mensagem_autor.textContent = "Busca sem resultados, considere adicionar um novo autor."
				} else {
					mensagem_autor.textContent = ""
				}
			}
		} else {
			select_opc.style.display = "none"
			for (let item of lista_autores) {
				const option = document.createElement("option")
				option.value = item.value
				option.textContent = item.text
				const elemento = select_opc.appendChild(option)
				eventoFocusDoSelect()
			}
		}
	})
	
	autor_input.addEventListener("keydown", function(e) {
		if (e.key === "Enter" || e.key === "Tab") {
			if (e.key ==="Enter") e.preventDefault()
			if (select_opc.style.display === "block" && autores.length > 0) {
				autor_input.value = select_opc.options[select_opc.selectedIndex].text
				autor_id.value = select_opc.options[select_opc.selectedIndex].value
				select_opc.style.display = "none"
				btn_add_um_autor_livro.style.display = "none"
				mensagem_autor.textContent = ""
				preencheRegiao(autor_id.value)
			}
		}
		if (e.key === "ArrowDown") {
			e.preventDefault()
			if (select_opc.style.display === "block" && autores.length > 0) {
				select_opc.selectedIndex = (select_opc.selectedIndex + 1) % select_opc.options.length
			} else if (select_opc.style.display === "" || select_opc.style.display === "none") {
				select_opc.style.display = "block"
			}
		}
		if (e.key === "ArrowUp") {
			e.preventDefault()
			if (select_opc.style.display === "block" && autores.length > 0) {
				select_opc.selectedIndex = (select_opc.selectedIndex - 1 + select_opc.options.length)
				% select_opc.options.length
			}
		}
		if (e.key === "Backspace" || e.key ==="Delete") {
			autor_id.value = null
		}
	})
	
	botao_abrir_select.addEventListener("click", function(e) {
		select_opc.style.display = "block"
		autor_input.focus()
	})
	
	document.addEventListener("click", function(e) {
		if (
			!botao_abrir_select.contains(e.target) && 
			!autor_input.contains(e.target) && 
			!select_opc.contains(e.target)
		) {
			setTimeout(() => {
				select_opc.style.display = "none";
			}, 300);
		}
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
			autor_input.value = e.target.text
			autor_id.value = e.target.value
			select_opc.style.display = "none"
			btn_add_um_autor_livro.style.display = "none"
			mensagem_autor.textContent = ""
			preencheRegiao(autor_id.value)
		}
	})
		
	select_opc.addEventListener('wheel', function(event) {
    const maxScrollTop = this.scrollHeight - this.clientHeight;
    if (
        (event.deltaY > 0 && this.scrollTop >= maxScrollTop) ||
        (event.deltaY < 0 && this.scrollTop <= 0)
    ) {
        event.preventDefault();
    }
	});

	btn_add_um_autor_livro.addEventListener("click", function(e) {
		if (form.action.slice(-18) === "/adicionarumlivro/") {
			form.action = form.action + "adicionarumautor/"
			form.setAttribute("novalidate", "novalidate")
		} 
		// else if (form.action.slice(-15) === "/editarumlivro/") {
		// 	form.action = form.action.slice(0, form.action.length - 15) + "/adicionarumlivro/adicionarumautor/"
		// }
	})

	btn_add_um_autor_livro.addEventListener("blur", function(e) {
		setTimeout(() => {
				if (
					!elemento_em_foco.contains(autor_input) && 
					!elemento_em_foco.contains(select_opc)
			) {
				btn_add_um_autor_livro.style.display = "none"
				if (!autor_id.value) {mensagem_autor.textContent = "Nenhum autor selecionado."}
				elemento_em_foco.focus()
			}
		}, 300);
	})

	autor_input.addEventListener("focus", function(e) {
		if (!document.querySelector("[name='editar_um_livro']")) {
			btn_add_um_autor_livro.style.display = "block"
		}
	})

	autor_input.addEventListener("blur", function(e) {
		setTimeout(() => {
				if (
					!elemento_em_foco.contains(btn_add_um_autor_livro) &&
					!elemento_em_foco.contains(select_opc)
				) {
				btn_add_um_autor_livro.style.display = "none"
				if (!autor_id.value) {mensagem_autor.textContent = "Nenhum autor selecionado."}
				elemento_em_foco.focus()
			}
		}, 300);
	})

	select_opc.addEventListener("blur", function(e) {
		setTimeout(() => {
				if (
					!elemento_em_foco.contains(btn_add_um_autor_livro) &&
					!elemento_em_foco.contains(autor_input)
				) {
				btn_add_um_autor_livro.style.display = "none"
				if (!autor_id.value) {mensagem_autor.textContent = "Nenhum autor selecionado."}
				elemento_em_foco.focus()
			}
		}, 300);
	})

	document.addEventListener("focusin", function(e) {
		elemento_em_foco = e.target
	})

	function preencheRegiao(id_autor) {
		const relacao_autor_regiao = document.querySelector("#relacao_autor_regiao").value.split("|")

		for (let rel of relacao_autor_regiao) {

			const autor_regiao_list = rel.split("-")
			const autor_id_relacao = autor_regiao_list[0]

			if (autor_id_relacao == id_autor) {
				const regiao_id_relacao = autor_regiao_list[1]
				regiao_id.value = regiao_id_relacao

				for (let reg of regioes) {

					if (reg.value == regiao_id.value) {
						regiao_input.value = reg.text
						break
					}
				}
				break
			}
		}
	}
})

