
//Validacion

document.getElementById("formulario").addEventListener("submit", function (event) {

  event.preventDefault();
  const nombre = document.getElementById("nombre").value.trim();
  const apellido = document.getElementById("apellido").value.trim();
  const email = document.getElementById("email").value.trim();
  const motivo = document.getElementById("motivo").value.trim();
  const mayorEdad = document.getElementById("mayorEdad").checked;

  if (nombre === "" || apellido === "" || email === "" || motivo === "" || !mayorEdad) {
    alert("Por favor, complete todos los campos y confirme que tiene 18 años o más.");
    return false;
  }

  let emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  if (!emailRegex.test(email)) {
    alert("Por favor, ingrese un correo electrónico válido.");
    return false;
  }

  alert("Gracias por enviar el formulario!");
  this.submit();

});