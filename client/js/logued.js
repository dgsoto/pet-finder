function checkAuthentication() {
  const token = localStorage.getItem('token');
  
  if (!token) {
      // Redirigir a la página de inicio de sesión
      window.location.href = '../html/register-login.html#login';
  }
}

checkAuthentication();

const nombreUsuario = localStorage.getItem('username');


  // Actualiza el contenido del elemento con el nombre de usuario
  const usuarioDropdown = document.getElementById('usuarioDropdown');
 
    usuarioDropdown.innerText = nombreUsuario;

function abrirPublicacion() {
  window.location.href = "../html/publicacion.html";
}

// Función para cerrar sesión y limpiar el token del localStorage
function cerrarSesion() {
  // Remover el token del localStorage
  localStorage.removeItem("token");
  localStorage.removeItem("username");

  // Redirigir al usuario a la página de inicio de sesión o a donde desees
  window.location.href = "../index.html";
}


//------------------------------------------



var headerElement = document.getElementById("header");

console.log(headerElement)

// Función para manejar la visibilidad del botón y la subraya en el menú
function toggleBtnRegistro() {
  var currentSection = getCurrentSection();

  // Remover la clase 'active' de todos los elementos del menú
  var navItems = document.querySelectorAll('.navbar-nav .nav-item');
  navItems.forEach(function (item) {
    item.classList.remove('active');
  });

  // Agregar la clase 'active' a la sección correspondiente en el menú
  if (currentSection) {
    var correspondingNavItem = document.querySelector('.navbar-nav .nav-item a[href="#' + currentSection.id + '"]');
    if (correspondingNavItem) {
      correspondingNavItem.parentElement.classList.add('active');
    }
  }
}

// Función para obtener la sección actual
function getCurrentSection() {
  var sections = document.querySelectorAll("section");
  for (var i = 0; i < sections.length; i++) {
    var rect = sections[i].getBoundingClientRect();
    if (rect.top <= window.innerHeight / 2 && rect.bottom >= window.innerHeight / 2) {
      return sections[i];
    }
  }
  return null;
}

// Llamamos a la función al cargar la página y en el evento de scroll
toggleBtnRegistro();
window.addEventListener("scroll", toggleBtnRegistro);

// Llamamos a la función al cargar la página y en el evento de scroll
toggleBtnRegistro();
window.addEventListener("scroll", toggleBtnRegistro);


var swiper = new Swiper('.swiper-container', {
	navigation: {
	  nextEl: '.swiper-button-next',
	  prevEl: '.swiper-button-prev'
	},
	slidesPerView: 1,
	spaceBetween: 10,
	// init: false,
	pagination: {
	  el: '.swiper-pagination',
	  clickable: true,
	},

  
	breakpoints: {
	  620: {
		slidesPerView: 1,
		spaceBetween: 20,
	  },
	  680: {
		slidesPerView: 2,
		spaceBetween: 40,
	  },
	  920: {
		slidesPerView: 3,
		spaceBetween: 40,
	  },
	  1240: {
		slidesPerView: 4,
		spaceBetween: 50,
	  },
	} 
    });



