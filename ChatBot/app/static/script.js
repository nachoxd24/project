const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

const Toggle = document.querySelector(".sidebar-logo");

Toggle.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});


function validarFormulario() {
  var nombre = document.getElementById('nombre').value;

  // Verificar si el campo del nombre está vacío
  if (nombre === '') {
    alert('Por favor, ingresa tu nombre.');
    return false; // Evita que el formulario se envíe
  }

  // Si todo está bien, permite el envío del formulario
  return true;
}

