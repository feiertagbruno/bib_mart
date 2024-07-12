const btn_abrir_anotacao = document.querySelector("#btn_abrir_anotacao")

document.addEventListener("DOMContentLoaded", function(dom) {
  
  window.onload = function(){
    var historico_id = JSON.parse(localStorage.getItem("historico_id"))
    console.log(historico_id)
    if (historico_id) {
      const posicao_elemento = document.querySelector(`#historico_id_${historico_id}`)
      if (posicao_elemento) {
        window.scrollTo({
          top: posicao_elemento.offsetTop,
          behavior: "smooth"
        })
        localStorage.removeItem("historico_id")
      }
    }
  }

  document.addEventListener("click", function(e) {
    if (e.target.id === "btn_abrir_anotacao") {
      localStorage.setItem("historico_id", JSON.stringify(
        e.target.parentElement.querySelector("[name='historico_id']").value
      ))
    }
  })

})
