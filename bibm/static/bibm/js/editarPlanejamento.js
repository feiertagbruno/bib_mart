const caixa_de_pesquisa = document.querySelector(".search-input")
document.addEventListener("DOMContentLoaded", function(dom) {

  window.onload = function () {
    posicao = JSON.parse(localStorage.getItem("retornaPosicao"))
    if (posicao) {
      localStorage.removeItem("retornaPosicao")
      window.scrollTo({
        top: caixa_de_pesquisa.getBoundingClientRect().top,
      })
    }
  }

  document.addEventListener("click", function(e) {
    if (e.target.id === "btn_filtro_id") {
      localStorage.setItem("retornaPosicao", JSON.stringify("True"))
    }
  })

})