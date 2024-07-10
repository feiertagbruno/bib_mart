const btn_modo_edicao_regioes = document.querySelector("#modo-edicao-regioes")

document.addEventListener("DOMContentLoaded", function(dom) {

  window.onload = function() {  
    var scrollPosition = JSON.parse(sessionStorage.getItem('scrollPosition'));  
    if (scrollPosition) {  
      window.scrollTo(0, parseInt(scrollPosition));  
      sessionStorage.removeItem('scrollPosition');  
    }  
  }; 

  btn_modo_edicao_regioes.addEventListener("click", function(e) {
    
    const regioes_btn_edicao = document.querySelectorAll("#regioes_btn_edicao")
    
    if (
      regioes_btn_edicao[0].style.display === "none" ||
      !regioes_btn_edicao[0].style.display
    ) {
      for (let botao of regioes_btn_edicao) {
        botao.style.display = "flex"
      }
    } else if (regioes_btn_edicao[0].style.display === "flex") {
      for (let botao of regioes_btn_edicao) {
        botao.style.display = "none"
      }
    }

  })
  
  document.addEventListener("click", function(e) {
    if (e.target.className === "frase-estatica-purple") {
      e.preventDefault()
    }
    if (
      e.target.className === "regioes-nome frase-acende-purple" ||
      e.target.className === "btn-editar-regiao invisivel"
    ) {
      sessionStorage.setItem('scrollPosition', JSON.stringify(window.scrollY));
    }
  })

})