document.addEventListener("DOMContentLoaded", () => {
      try {
    // inicializamos Choices con el select vacio
    const emotionSelect = new Choices('#emotionSelect', { searchEnabled: true, itemSelectText: '', shouldSort: false });
    const copingSelect = new Choices('#copingSelect', { searchEnabled: true, itemSelectText: '', shouldSort: false });
    const strategySelect = new Choices('#strategySelect', { searchEnabled: true, itemSelectText: '', shouldSort: false });

    // funcion auxiliar para cargar datos en Choices
    const loadChoices = (selectInstance, data, valueKey, labelKey) => {
        const choices = data.map(item => ({ value: item[valueKey], label: item[labelKey] }));
        // limpia primero
        selectInstance.clearStore();
        // setea nuevas opciones
        selectInstance.setChoices(choices, 'value', 'label', true);
    };
 
    fetch(URL_EMOCIONES)
        .then(res => res.json())
        .then(emociones => loadChoices(emotionSelect, emociones, 'id', 'nombre'))
        .catch(err => console.error("Error cargando emociones:", err));
      
    fetch(URL_AFRONTAMIENTO)
        .then(res => res.json())
        .then(conductas => loadChoices(copingSelect, conductas, 'id', 'nombre'))
        .catch(err => console.error("Error cargando conductas:", err));

   
    fetch(URL_RECOMENDACIONES)
        .then(res => res.json())
        .then(recomendaciones => loadChoices(strategySelect, recomendaciones, 'idrecomendacion', 'nombre'))
        .catch(err => console.error("Error cargando recomendaciones:", err));

 
    const form = document.getElementById("triggerForm");
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const data = {
            situacion: document.getElementById("situationInput").value,
            emocion_id: emotionSelect.getValue(true),      
            afrontamiento_id: copingSelect.getValue(true), 
            estrategia_id: strategySelect.getValue(true),  
            efectividad: document.getElementById("effectivenessInput").value,
            tiporegistro: 0
        };

        console.log("Datos a enviar:", data); // Para debugging

        fetch(URL_GuardarEvento, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(res => {
            console.log("Respuesta HTTP:", res.status);
            return res.json();
        })
        .then(response => {
            console.log("Respuesta del servidor:", response); 
            
           
            if (response.success) {
                showModal("Éxito", "Se guardó de forma correcta.", "success"); 
               
              
                setTimeout(() => { 
                    window.location.href = URL_DIARY; 
                }, 3000);
            } else if (response.error) {
                showModal("Error", "Error: " + response.error, "error");
           
            } else {
                showModal("Error", "Respuesta inesperada del servidor", "error");
            }
        })
        .catch(err => {
            console.error("Error al enviar los datos:", err);
            showModal("Error", "Ocurrió un error al guardar el registro.", "error");
        });
    });

  } catch (error) {
        console.error("Error general:", error);
        alert("Error al cargar la página: " + error.message);
    }
});