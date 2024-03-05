document.addEventListener("DOMContentLoaded", function () {

    let currentPage = 1; // pagina actual.
    let totalPages = 1;  // aqui almacenamos el total de paginas disponibles
    const perPage = 10;  // Numero de mascotas por pagina.

    function ListPetsByPage(page) {
        //aqui la logica del fetch {{endpoint}}/pets?page=3&per_page=10
        console.log("paginacion: " + page);
        fetch(`http://127.0.0.1:5000/api/pets?page=${page}&per_page=${perPage}`)
        .then((response) => response.json())
        .then((data) => {
            // actualizamos el total de paginas disponibles
            totalPages = data.total_pages;
            // aqui actualizamos el estado de los botones de paginas disponibles.
            updateNavigationButtons();

            const mascotas = data.pets; // Tomar todas las mascotas recuperadas

            const swiperWrapper = document.querySelector(".swiper-wrapper");
            mascotas.forEach((mascota, index) => {
                const swiperSlide = document.createElement("div");
                swiperSlide.classList.add("swiper-slide");

                const img = document.createElement("img");
                img.src = mascota.image_url;
                img.alt = mascota.name;

                const cardDescription = document.createElement("div");
                cardDescription.classList.add("card-description");

                const cardTitle = document.createElement("div");
                cardTitle.classList.add("card-title");
                cardTitle.innerHTML = `<h5>${mascota.name}</h5>`;

                const cardText = document.createElement("div");
                cardText.classList.add("card-text");
                cardText.innerHTML = `<p>${mascota.location}</p><p>${mascota.date_lost}</p>`;

                cardDescription.appendChild(cardTitle);
                cardDescription.appendChild(cardText);

                swiperSlide.appendChild(img);
                swiperSlide.appendChild(cardDescription);

                const token = localStorage.getItem("token");

                if (token) {
                    const cardLink = document.createElement("div");
                    cardLink.classList.add("card-link");
                    const btnVerMas = document.createElement("button");
                    btnVerMas.type = "button";
                    btnVerMas.classList.add("btn", "btn-link", "btn-sm");
                    btnVerMas.dataset.toggle = "modal";
                    btnVerMas.dataset.target = "#exampleModal";
                    btnVerMas.textContent = "Ver más";
                    btnVerMas.addEventListener("click", () => {
                        handleVerMasClick(index); // Llama a la función con el índice de la mascota  
                    });
                    cardLink.appendChild(btnVerMas);
                    cardDescription.appendChild(cardLink);
                }
                swiperWrapper.appendChild(swiperSlide);
            }); // fin foreach mascotas

            const swiper = new Swiper(".mySwiper", {
                loop: true,
                navigation: {
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev",
                },
            }); //fin controles swiper

            function handleVerMasClick(index) {
                console.log("Número de card:", index);
                const mascotaSeleccionada =  mascotas[index];
                console.log(mascotaSeleccionada)
                
                // Actualiza el contenido del modal con los datos de la mascota
                const modalTitle = document.querySelector(".modal-title");
                modalTitle.textContent = mascotaSeleccionada.name;

                const modalImg = document.querySelector(".modal-body img");
                modalImg.src = mascotaSeleccionada.image_url;

                const nameElement = document.getElementById('petName');
                nameElement.textContent = `Nombre: ${mascotaSeleccionada.name}`;
    
                const breedElement = document.getElementById("petBreed");
                breedElement.textContent=`Raza: ${mascotaSeleccionada.breed}`;
                
                const petLocation = document.getElementById("petLocation");
                petLocation.textContent =`Zona: ${mascotaSeleccionada.location}`;

                const petAge = document.getElementById("petAge");
                petAge.textContent = `Edad: ${mascotaSeleccionada.age}`;

                const petSize = document.getElementById("petSize");
                petSize.textContent = `Tamaño: ${mascotaSeleccionada.size}`; 

                const petType = document.getElementById("petType")
                if (mascotaSeleccionada == "Wanted"){
                    petType.textContent ="Buscada"                
                }else{
                    petType.textContent="Encontrada";
                }
                $('#exampleModal').modal('show');
            } // fin funcion handleVerMasClick
            
        }).catch((error) => {
            console.error("Error al obtener los datos de la API de mascotas:", error);
        }); // fin list pets
    } // fin funcion ListPetsByPage
    
    
    // Función para actualizar el estado de los botones de navegación
    function updateNavigationButtons() {
        const prevPageBtn = document.querySelector('.prev-page-btn');
        const nextPageBtn = document.querySelector('.next-page-btn');

        // Deshabilitar el botón de página anterior si estamos en la primera página
        if (currentPage === 1) {
            prevPageBtn.disabled = true;
        } else {
            prevPageBtn.disabled = false;
        }

        // Deshabilitar el botón de página siguiente si estamos en la última página
        if (currentPage === totalPages) {
            nextPageBtn.disabled = true;
        } else {
            nextPageBtn.disabled = false;
        }
    }

    // Manejar clics en los botones de navegación de la paginación
    document.querySelector('.next-page-btn').addEventListener('click', function() {
        currentPage++;
        ListPetsByPage(currentPage);
    });

    document.querySelector('.prev-page-btn').addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            ListPetsByPage(currentPage);
        }
    });

    // Cargar mascotas de la primera página al cargar la página
    ListPetsByPage(currentPage);

}); // fin DOMContentLoaded event listener
