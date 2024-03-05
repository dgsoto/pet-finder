document.addEventListener("DOMContentLoaded", function () {
  const nombreInput = document.getElementById("nombre");
  const apellidoInput = document.getElementById("apellido");
  const userInput = document.getElementById("user");
  const suggestedUsernameDiv = document.getElementById("suggestedUsername");

  // Función para generar el nombre de usuario sugerido
  function generarNombreUsuarioSugerido() {
    const nombre = nombreInput.value.trim().toLowerCase().replace(/\s+/g, "_");
    const apellido = apellidoInput.value
      .trim()
      .toLowerCase()
      .replace(/\s+/g, "_");
    const nombreUsuarioSugerido = `${nombre}.${apellido}`;

    userInput.value =
      nombreUsuarioSugerido !== ".." ? nombreUsuarioSugerido : "";
    suggestedUsernameDiv.innerText =
      nombreUsuarioSugerido !== ".."
        ? `Usuario sugerido: ${nombreUsuarioSugerido}`
        : "";
    suggestedUsernameDiv.style.display =
      nombreUsuarioSugerido !== ".." ? "block" : "none";
  }

  nombreInput.addEventListener("input", generarNombreUsuarioSugerido);
  apellidoInput.addEventListener("input", generarNombreUsuarioSugerido);

  document
    .getElementById("registerForm")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Evita el envío del formulario

      const password = document.getElementById("password").value.trim();
      const confirmPassword = document
        .getElementById("confirmPassword")
        .value.trim();

      // Comprueba si las contraseñas coinciden
      if (!validarContraseñas(password, confirmPassword)) {
        return;
      }

      // Limpia mensaje de error de contraseñas
      limpiarMensajeErrorContraseñas();

      // Registra al usuario
      registrarUsuario();
    });
});

function limpiarMensajeErrorContraseñas() {
  const passwordError = document.getElementById("passwordError");
  passwordError.innerText = "";
  passwordError.style.display = "none";
}

function validarContraseñas(password, confirmPassword) {
  const passwordError = document.getElementById("passwordError");

  if (password !== confirmPassword) {
    passwordError.innerText = "Las contraseñas no coinciden.";
    passwordError.style.display = "block";
    passwordError.style.color = "#ff5722";
    passwordError.style.fontWeight = "bold";
    return false; // Las contraseñas no coinciden
  }

  return true; // Las contraseñas coinciden
}

function registrarUsuario() {
  // Captura los valores de los campos del formulario
  const last_name = document.getElementById("apellido").value.trim();
  const first_name = document.getElementById("nombre").value.trim();
  const username = document.getElementById("user").value.trim();
  const email = document.getElementById("correo").value.trim();
  const address = document.getElementById("domicilio").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirmPassword = document
    .getElementById("confirmPassword")
    .value.trim();

  // Comprueba nuevamente si las contraseñas coinciden (por si acaso)
  if (!validarContraseñas(password, confirmPassword)) {
    alert("Las contraseñas no coinciden");
    return; // Detiene el proceso si las contraseñas no coinciden
  }

  // Crea un objeto con los datos a enviar al backend
  const datosUsuario = {
    username,
    email,
    password,
    first_name,
    last_name,
    address,
  };

  // Realiza una solicitud HTTP (POST) al backend con los datos del usuario
  fetch("http://127.0.0.1:5000/api/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datosUsuario),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error en la solicitud Fetch");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Respuesta del backend:", data);
      alert("Usuario registrado con éxito. Ahora puedes iniciar sesión.");

      // Hace visible el formulario de inicio de sesión
      document.getElementById("loginForm").classList.remove("hidden");

      // Oculta el formulario de registro si es necesario
      document.getElementById("registerForm").classList.add("hidden");
      localStorage.setItem("formType", "loginForm");
    })
    .catch((error) => {
      console.error("Error al enviar los datos:", error);
    });
}

function cancelar() {
  window.location.href = "../index.html";
  localStorage.removeItem("formType");
}
document.addEventListener("DOMContentLoaded", function () {
  const registerForm = document.getElementById("registerForm");
  const loginForm = document.getElementById("loginForm");

  // Recupera el tipo de formulario del localStorage
  let formType = localStorage.getItem("formType");

  const formInfo = document.querySelector(".form-info");
  const titleElement = formInfo.querySelector("h2");
  const subtitleElement = formInfo.querySelector("p");
  const linkElement = formInfo.querySelector(".link");

  function toggleForms() {
    if (formType === "registerForm") {
      titleElement.textContent = "Regístrate";
      subtitleElement.textContent = "¿Ya tenés cuenta?";
      linkElement.textContent = "Ingresá";

      registerForm.classList.remove("hidden");
      loginForm.classList.add("hidden");
    } else if (formType === "loginForm") {
      titleElement.textContent = "Inicia Sesión";
      subtitleElement.textContent = "¿No tenés cuenta?";
      linkElement.textContent = "Regístrate";

      registerForm.classList.add("hidden");
      loginForm.classList.remove("hidden");
    }
  }

  // Inicializar según el tipo de formulario recuperado del localStorage
  if (formType === "registerForm" || formType === "loginForm") {
    toggleForms();
  }

  // Asignar evento de clic al enlace desde JavaScript
  linkElement.addEventListener("click", function (event) {
    event.preventDefault();

    if (formType === "registerForm") {
      titleElement.textContent = "Inicia Sesión";
      subtitleElement.textContent = "¿No tenés cuenta?";
      linkElement.textContent = "Regístrate";

      registerForm.classList.add("hidden");
      loginForm.classList.remove("hidden");

      localStorage.setItem("formType", "loginForm");
    } else if (formType === "loginForm") {
      titleElement.textContent = "Regístrate";
      subtitleElement.textContent = "¿Ya tenés cuenta?";
      linkElement.textContent = "Ingresá";

      registerForm.classList.remove("hidden");
      loginForm.classList.add("hidden");
      localStorage.setItem("formType", "registerForm");
    }

    formType = localStorage.getItem("formType");
    console.log(formType);
  });
});
