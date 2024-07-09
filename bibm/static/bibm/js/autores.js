document.addEventListener("DOMContentLoaded", function(dom) {
  const btn_modo_edicao_autores = document.querySelector("#modo-edicao-autores")

  window.onload = function() {  
    var scrollPosition = JSON.parse(sessionStorage.getItem('scrollPosition'));  
    if (scrollPosition) {  
      window.scrollTo(0, parseInt(scrollPosition));  
      sessionStorage.removeItem('scrollPosition');  
    }  
  }; 
  
  history.scrollRestoration = "smooth";

  if (document.querySelector("#filtro").value === "regiao") {
    document.querySelector("#ordem-alfabetica").style.display = "none"
  }

  btn_modo_edicao_autores.addEventListener("click", function(e) {
    
    const autores_btn_edicao = document.querySelectorAll("#autores_btn_edicao")
    
    if (
      autores_btn_edicao[0].style.display === "none" ||
      !autores_btn_edicao[0].style.display
    ) {
      for (let botao of autores_btn_edicao) {
        botao.style.display = "flex"
      }
    } else if (autores_btn_edicao[0].style.display === "flex") {
      for (let botao of autores_btn_edicao) {
        botao.style.display = "none"
      }
    }

  })

  document.addEventListener("click", function(e) {
    if (e.target.className === "frase-acende-dourado paragrafo") {
      sessionStorage.setItem('scrollPosition', JSON.stringify(window.scrollY));
    }
  })

})
