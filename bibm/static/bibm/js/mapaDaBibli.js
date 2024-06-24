function adicionaEventos() {
  const livros_mapa = document.querySelectorAll(".endereco-livros")
  const enderecos_mapa = document.querySelectorAll(".endereco-box")
  var endereco_id_mapa

  livros_mapa.forEach(livro_mapa => {
    livro_mapa.addEventListener("dragstart", eventoArrastar)
  })

  enderecos_mapa.forEach(endereco_mapa => {
    endereco_mapa.addEventListener("dragover", eventoDragover)
    endereco_mapa.addEventListener("drop", eventoDrop)
  })
}

function eventoArrastar(e) {
  const livro_id_mapa = e.target.querySelector("#livro_id").value
  e.dataTransfer.setData("text/plain", livro_id_mapa)
  e.dataTransfer.effectAllowed = "move";
}

function eventoDragover(e) {
  e.preventDefault()
  endereco_id_mapa = e.target.querySelector("#endereco_id").value
  e.dataTransfer.dropEffect = "move";
}

function eventoDrop(e) {
  e.preventDefault()
  livro_id = e.dataTransfer.getData("text/plain")
  console.log(endereco_id_mapa)
}

document.addEventListener("DOMContentLoaded", adicionaEventos)