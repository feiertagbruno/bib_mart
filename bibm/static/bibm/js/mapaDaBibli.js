function adicionaEventos() {
  const livros_mapa = document.querySelectorAll(".endereco-livros")
  const enderecos_mapa = document.querySelectorAll(".endereco-box")

  livros_mapa.forEach(livro_mapa => {
    livro_mapa.addEventListener("dragstart", eventoArrastar())
  })
}

function eventoArrastar(e) {
  // e.dataTransfer.setData("text/plain", e.target.id)
  console.log(e)
}

document.addEventListener("DOMContentLoaded", adicionaEventos)