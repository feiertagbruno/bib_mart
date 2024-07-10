const btn_modo_edicao_generos = document.querySelector("#modo-edicao-generos")

document.addEventListener("DOMContentLoaded", function(dom) {

  window.onload = function() {  
    var scrollPosition = JSON.parse(sessionStorage.getItem('scrollPosition'));  
    if (scrollPosition) {  
      window.scrollTo(0, parseInt(scrollPosition));  
      sessionStorage.removeItem('scrollPosition');  
    }  
  }; 

  btn_modo_edicao_generos.addEventListener("click", function(e) {
    
    const generos_btn_edicao = document.querySelectorAll("#generos_btn_edicao")
    
    if (
      generos_btn_edicao[0].style.display === "none" ||
      !generos_btn_edicao[0].style.display
    ) {
      for (let botao of generos_btn_edicao) {
        botao.style.display = "flex"
      }
    } else if (generos_btn_edicao[0].style.display === "flex") {
      for (let botao of generos_btn_edicao) {
        botao.style.display = "none"
      }
    }

  })
  
  document.addEventListener("click", function(e) {
    if (e.target.className === "frase-estatica-verde") {
      e.preventDefault()
    }
    if (
      e.target.className === "generos-nome frase-acende-verde" ||
      e.target.className === "btn-editar-regiao invisivel"
    ) {
      sessionStorage.setItem('scrollPosition', JSON.stringify(window.scrollY));
    }
  })

})