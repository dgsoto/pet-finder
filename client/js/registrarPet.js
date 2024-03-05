const formulario = document.getElementById('formulario');
// Obtener el token de sesión almacenado en sessionStorage
const token = localStorage.getItem('token');

// Variables para almacenar datos relevantes
let imageUrl;
let datosPet;
let pet_id_ref;

// Agrega un event listener para el envío del formulario
formulario.addEventListener('submit', function(event) {
  event.preventDefault(); // Evita el envío del formulario

  // Toma los datos del formulario
  const type = document.getElementById('type').value;
  const date_lost = document.getElementById('date_lost').value;
  const location = document.getElementById('location').value;
  const name = document.getElementById('namePet').value;
  const breed = document.getElementById('breed').value;
  const age = document.getElementById('age').value;
  const size = document.getElementById('size').value;
  const facebook = document.getElementById('facebook').value;
  const instagram = document.getElementById('instagram').value;
  const description = document.getElementById('description').value;
  const hashtags = document.getElementById('hashtags').value;

  // Crea un objeto FormData para enviar los datos del formulario
  const formData = new FormData();
  formData.append('image', formulario.picturePet.files[0]); // Obtén el archivo de la imagen
  
  // API Request para subir la imagen a ImgBB
  const apiKey = 'b8630093227cc0bf57935c135bbf6f9c'; // Reemplaza 'TU_API_KEY' con tu clave API de ImgBB

  // Verificar si el token está presente
  if (!token) {
    console.error("Token de sesión no encontrado en sessionStorage");
  } else {
    // API request to upload image in imgbb
    fetch('https://api.imgbb.com/1/upload?key=' + apiKey, {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      // Guarda la URL de la imagen subida en una variable
      imageUrl = data.data.url;
      console.log('URL for IMGBB de la imagen subida:', imageUrl);

      // Arma un objeto con los datos del formulario incluyendo la URL de la imagen subida
      datosPet = {
        image_url: imageUrl,
        type,
        date_lost,
        location,
        name,
        breed,
        age,
        size,
        description,
        //hashtags
      };

      // Solicitud POST al backend para crear PET
      fetch("http://127.0.0.1:5000/api/pets/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` // Agrega el token de sesión como token de autorización Bearer
        },
        body: JSON.stringify(datosPet),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error("Error en la solicitud Fetch: " + response);
        }
        return response.json();
      })
      .then(data => {
        pet_id_ref = data.id;
        console.log("Respuesta del backend API crear Pet:", data);

        const datosRedes = {
          pet_id: pet_id_ref,
          social_media: "Facebook",
          profile_url: facebook
        }
        
        // Solicitud POST al backend para crear redsocial
        fetch("http://127.0.0.1:5000/api/networks/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` // Agrega el token de sesión como token de autorización Bearer
          },
          body: JSON.stringify(datosRedes),
        })
        .then(response => {
          if (!response.ok) {
            throw new Error("Error en la solicitud Fetch: " + response);
          }
          return response.json();
        })
        .then(data => {
          console.log("Respuesta del backend API crear red social:", data);
          // Ejecutar función para redirigir a index después de 3 segundos
          setTimeout(function() {
            // Redirige a index.html
            window.location.href = "../index.html";
          }, 3000);
        })
        .catch(error => {
          console.error("Error al enviar los datos:", error);
        });


      })
      .catch(error => {
        console.error("Error al enviar los datos:", error);
      }); // fin request fetch pet


    })
    .catch(error => {
      console.error('Error:', error);
    }); // fin request fetch imgbb

  } // fin if
  window.location.href = "../html/logued.html";

}); //fin del formulario




function cancelarRegistro (){
  window.location.href = "../html/logued.html";
}




function displayImage() {
  var input = document.getElementById("picturePet");
  var img = document.getElementById("display_image");
  var file = input.files[0];
  var reader = new FileReader();

  reader.onloadend = function () {
      img.src = reader.result;
  };

  if (file) {
      reader.readAsDataURL(file);
     
  } else {
      img.src = "../img/logo.png"; // Puedes establecer la imagen predeterminada si no se selecciona ninguna imagen
  }
}
