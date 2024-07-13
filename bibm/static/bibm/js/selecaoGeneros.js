const select_opc_gen = document.querySelector("#generos-opcoes")
const generos = select_opc_gen.options
let lista_generos = []
const genero_input = document.querySelector("#genero-input")
const botao_abrir_select_gen = document.querySelector("#abrir-select-genero")
const genero_id = document.querySelector("#genero_id_field")
const btn_add_um_genero_livro = document.querySelector("#add_um_genero_livro")
const genero_salvo = document.querySelector("#genero_salvo")
const mensagem_genero = document.querySelector("#mensagem-genero")

document.addEventListener("DOMContentLoaded", function(dom) {
	if (genero_salvo) {
		if (genero_salvo.value) {
			genero_id.value = genero_salvo.value
		}
	}

	if (genero_id.value) {
		for (let gen of generos) {
			if (gen.value == genero_id.value) {
				genero_input.value = gen.text
				break
			}
		}
	}

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
				mensagem_genero.textContent = ""
			} else {
				select_opc_gen.style.display = "none"
				genero_id.value = null
				if (genero_input.value) {
					mensagem_genero.textContent = "Busca sem resultados."
				} else {
					mensagem_genero.textContent = ""
				}
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
				btn_add_um_genero_livro.style.display = "none"
				mensagem_genero.textContent = ""
			}
		}
		if (e.key === "ArrowDown") {
			e.preventDefault()
			if (select_opc_gen.style.display === "block" && generos.length > 0) {
				select_opc_gen.selectedIndex = (select_opc_gen.selectedIndex + 1) % select_opc_gen.options.length
			} else if (select_opc_gen.style.display === "" || select_opc_gen.style.display === "none") {
				select_opc_gen.style.display = "block"
			}
		}
		if (e.key === "ArrowUp") {
			e.preventDefault()
			if (select_opc_gen.style.display === "block" && generos.length > 0) {
				select_opc_gen.selectedIndex = (select_opc_gen.selectedIndex - 1 + select_opc_gen.options.length)
				% select_opc_gen.options.length
			}
		}
		if (e.key === "Backspace" || e.key ==="Delete") {
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
			btn_add_um_genero_livro.style.display = "none"
			mensagem_genero.textContent = ""
		}
	})
		
	select_opc_gen.addEventListener('wheel', function(event) {
    const maxScrollTop = this.scrollHeight - this.clientHeight;
    if (
        (event.deltaY > 0 && this.scrollTop >= maxScrollTop) ||
        (event.deltaY < 0 && this.scrollTop <= 0)
    ) {
        event.preventDefault();
    }
	});
		
	btn_add_um_genero_livro.addEventListener("click", function(e) {
		form.action = form.action + "adicionarumgenero/"
		form.setAttribute("novalidate", "novalidate")
	})
		
	btn_add_um_genero_livro.addEventListener("blur", function(e) {
		setTimeout(() => {
			if (
				!elemento_em_foco.contains(genero_input) &&
				!elemento_em_foco.contains(select_opc_gen)
			) {
				btn_add_um_genero_livro.style.display = "none"
				if (!genero_id.value) {mensagem_genero.textContent = "Nenhum gênero selecionado."}
				elemento_em_foco.focus()
			}
		}, 300);
	})

	genero_input.addEventListener("focus", function(e) {
		if (!document.querySelector("[name='editar_um_livro']")) {
			btn_add_um_genero_livro.style.display = "block"
		}
	})
	
	genero_input.addEventListener("blur", function(e) {
		setTimeout(() => {
			if (
				!elemento_em_foco.contains(btn_add_um_genero_livro) &&
				!elemento_em_foco.contains(select_opc_gen)
			) {
				btn_add_um_genero_livro.style.display = "none"
				if (!genero_id.value) {mensagem_genero.textContent = "Nenhum gênero selecionado."}
				elemento_em_foco.focus()
			}
		}, 300);
	})
	
select_opc_gen.addEventListener("blur", function(e) {
	setTimeout(() => {
		if (
			!elemento_em_foco.contains(btn_add_um_genero_livro) &&
			!elemento_em_foco.contains(genero_input)
		) {
			btn_add_um_genero_livro.style.display = "none"
			if (!genero_id.value) {mensagem_genero.textContent = "Nenhum gênero selecionado."}
			elemento_em_foco.focus()
		}
	}, 300);
})

	// document.addEventListener("focusin", function(e) {
	// 	elemento_em_foco = e.target
	// })

})

