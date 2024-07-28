document.addEventListener("DOMContentLoaded", function(dom) {

  const checkbox_presencial = document.querySelector("#presencial_id")
  const mensagem_presencial = document.querySelector("#mensagem_presencial")

  if (!checkbox_presencial.checked) {
    mensagem_presencial.style.display = "block"
  } else {
    mensagem_presencial.style.display = "none"
  }

  checkbox_presencial.addEventListener("click", function(e) {
    if (!e.target.checked) {
      mensagem_presencial.style.display = "block"
    } else {
      mensagem_presencial.style.display = "none"
    }
  })

})

