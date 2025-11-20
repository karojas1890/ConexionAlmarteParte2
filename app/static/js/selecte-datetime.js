 function selectDate(element) {
            // Remove selected class from all date options
            document.querySelectorAll('.date-option').forEach(option => {
                option.classList.remove('selected');
            });
            // Add selected class to clicked option
            element.classList.add('selected');
        }

        function selectTime(element) {
            // Remove selected class from all time options
            document.querySelectorAll('.time-option').forEach(option => {
                option.classList.remove('selected');
            });
            // Add selected class to clicked option
            element.classList.add('selected');
        }

        function continueToPayment(button) {
            const selectedDate = document.querySelector('.date-option.selected')?.textContent;
            const selectedTime = document.querySelector('.time-option.selected')?.textContent;
            const paymentUrl = button.getAttribute('data-url');

            if (!selectedDate || !selectedTime) {
               alert("Por favor selecciona fecha y hora.");
           return;
        }

    localStorage.setItem('selectedDate', selectedDate);
    localStorage.setItem('selectedTime', selectedTime);

    window.location.href = paymentUrl;
}

document.addEventListener("DOMContentLoaded", () => {
    const summaryDiv = document.getElementById("service-summary-text");

    // Toma atos del localStorage
    const selectedService = localStorage.getItem('selectedServiceName'); 
    const selectedPrice = localStorage.getItem('selectedPrice'); 

    // covierte el monto a un nuemro valdo
    const precioNumero = parseFloat(selectedPrice);
    
    if (selectedService && !isNaN(precioNumero)) {
        summaryDiv.textContent = `${selectedService} - ₡${precioNumero.toLocaleString()}`;
    } else if (selectedService) {
        summaryDiv.textContent = `${selectedService} - ₡N/A`;
    } else {
        summaryDiv.textContent = "No has seleccionado un servicio aún";
    }
});


      document.addEventListener("DOMContentLoaded", () => {
    // carga la disponibilidad al iniciar
    fetchDisponibilidad();
});

function fetchDisponibilidad() {
    fetch(DISPONIBILIDAD_URL) 
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            renderDisponibilidad(data);
        })
        .catch(err => console.error("Error al cargar disponibilidad:", err));
}
function renderDisponibilidad(data) {
    const dateGrid = document.querySelector(".date-grid");
    const timeGrid = document.querySelector(".time-grid");

    const fechas = {};

    data.forEach(d => {
        if (d.estado !== 1) return; // solo disponibles
        if (!fechas[d.fecha]) fechas[d.fecha] = [];
        fechas[d.fecha].push(d);
    });

    dateGrid.innerHTML = "";
    timeGrid.innerHTML = "";

    const fechasArray = Object.keys(fechas).sort();

    // Crear botones de fecha
    fechasArray.forEach((fecha, i) => {
        const div = document.createElement("div");
        div.className = "date-option" + (i === 0 ? " selected" : "");
        div.textContent = new Date(fecha).toLocaleDateString("es-ES", {
            weekday: "short",
            day: "numeric",
            month: "long"
        });
        div.addEventListener("click", () => selectDate(div, fechas[fecha]));
        dateGrid.appendChild(div);
    });

    // Mostrar horas del primer día por defecto
    if (fechasArray.length > 0) renderHoras(fechas[fechasArray[0]]);
}

function selectDate(element, horarios) {
    document.querySelectorAll(".date-option").forEach(e => e.classList.remove("selected"));
    element.classList.add("selected");
    renderHoras(horarios);
}

function renderHoras(horarios) {
    const timeGrid = document.querySelector(".time-grid");
    timeGrid.innerHTML = "";

    horarios
        .filter(h => h.horainicio) // protección contra undefined
        .sort((a, b) => a.horainicio.localeCompare(b.horainicio))
        .forEach(h => {
            const div = document.createElement("div");
            div.className = "time-option";
            div.textContent = `${h.horainicio} - ${h.horafin}`;
            div.addEventListener("click", () => selectTime(div, h.id));
            timeGrid.appendChild(div);
        });
}

function selectTime(element, idDisponibilidad) {
    document.querySelectorAll(".time-option").forEach(e => e.classList.remove("selected"));
    element.classList.add("selected");
    localStorage.setItem("idDisponibilidadSeleccionada", idDisponibilidad);
}