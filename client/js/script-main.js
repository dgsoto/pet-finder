var btnRegistro = document.getElementById("btn-registro");
var headerElement = document.getElementById("header");



// Función para manejar la visibilidad del botón y la subraya en el menú
function toggleBtnRegistro() {
  var currentSection = getCurrentSection();

  if (currentSection && currentSection.id === "home") {
    // Si estamos en la sección "home", oculta el botón
    btnRegistro.style.display = "none";
    headerElement.style.backgroundColor="transparent";
   
  } else {
    // En otras secciones o al inicio de la página, muestra el botón
    btnRegistro.style.display = "block";
    headerElement.style.backgroundColor="white";
  }

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


    function redirecToForm(formType) {
      localStorage.setItem('formType', formType);
     
       window.location.href = 'html/register-login.html'
    }

