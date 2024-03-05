document.getElementById("loginForm").addEventListener("submit", function (event) {
  event.preventDefault();

  var username = document.getElementById("user_log").value.trim();
  var password = document.getElementById("psw_log").value.trim();

  fetch("http://127.0.0.1:5000/api/auth/login", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({
          username: username,
          password: password,
      }),
  })
  .then((response) => {
      if (!response.ok) {
          if (response.status === 401) {
              throw new Error("Nombre de usuario o contraseña incorrecta");
          }
          throw new Error("Error en la solicitud. Estado: " + response.status);
      }
      return response.json();
  })
  .then((data) => {
      let token = data.access_token;
      console.log(token);
      localStorage.setItem("token", token);
      localStorage.setItem('username', username);
      window.location.href = "../html/logued.html";
  })
  .catch((error) => {
      console.error("Error en la solicitud:", error.message);
      alert(error.message);
      
      // Limpiar el formulario después de aceptar el alert
      document.getElementById("user_log").value = "";
      document.getElementById("psw_log").value = "";
  });
});