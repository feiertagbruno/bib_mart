function adicionaEventos() {
  const livros_mapa = document.querySelectorAll(".endereco-livros")
  const enderecos_mapa = document.querySelectorAll(".endereco-box")
  var endereco_id_original

  livros_mapa.forEach(livro_mapa => {
    livro_mapa.addEventListener("dragstart", eventoArrastar)
  })

  enderecos_mapa.forEach(endereco_mapa => {
    endereco_mapa.addEventListener("dragover", eventoDragover)
    endereco_mapa.addEventListener("drop", eventoDrop)
  })
}

function eventoArrastar(e) {
  if (e.target.classList[0] === "endereco-livros") {
    const livro_id_mapa = e.target.querySelector("#livro_id").value
    endereco_id_original = e.target.parentElement.querySelector("#endereco_id").value
    e.dataTransfer.setData("text/plain", livro_id_mapa)
    e.dataTransfer.effectAllowed = "move";
  }
}

function eventoDragover(e) {
  e.preventDefault()
  e.dataTransfer.dropEffect = "move";
}

function eventoDrop(e) {
  e.preventDefault()
  if (
    e.target.classList[0] === "endereco-livro-titulo" ||
    e.target.classList[0] === "endereco-descricao" ||
    e.target.classList[0] === "endereco-titulo"
  ) {
    const livro_id = e.dataTransfer.getData("text/plain")
    const endereco_id = e.target.parentElement.parentElement.querySelector("#endereco_id").value
    const form_enderecar = document.querySelector("#form_enderecar")
    if (endereco_id_original != endereco_id) {
      form_enderecar.querySelector("#livro_id_form").value = livro_id
      form_enderecar.querySelector("#endereco_id_form").value = endereco_id
      form_enderecar.submit()
    } else {
    }
  }
}

document.addEventListener("DOMContentLoaded", adicionaEventos)