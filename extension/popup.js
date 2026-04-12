// popup.js

document.addEventListener('DOMContentLoaded', () => {
  const semaforo = document.getElementById("semaforo");
  const resumen = document.getElementById("resumen");

  // Funcion que pinta la pantalla segun el estado del storage
  const actualizarInterfaz = (result) => {
    if (!result.estado) {
        resumen.innerText = "Selecciona un texto, da clic derecho y presiona 'Analizar con Fake Radar'.";
        return;
    }

    if (result.estado === "cargando") {
        semaforo.style.backgroundColor = "#9ca3af";
        semaforo.innerText = "ANALIZANDO...";
        resumen.innerText = "El motor de IA está trabajando en segundo plano...";
    } 
    
    else if (result.estado === "error") {
        semaforo.style.backgroundColor = "#333";
        semaforo.innerText = "ERROR DE CONEXIÓN";
        resumen.innerText = "Asegúrate de que Docker esté corriendo (localhost:8000).";
    } 
    
    else if (result.estado === "completado" && result.resultado) {
        const data = result.resultado;
        semaforo.innerText = "VEREDICTO: " + data.global_assessment.toUpperCase();
    
        if (data.global_assessment === "Falso") {
            semaforo.style.backgroundColor = "#ff4d4d";
        } else if (data.global_assessment === "Verdadero") {
            semaforo.style.backgroundColor = "#2ecc71";
        } else {
            semaforo.style.backgroundColor = "#f1c40f";
        }
    
        resumen.innerText = data.analysis.fact_check_analysis.reasoning;
    }
  };
  
  // Se lee el estado actual al abrir el popup
  chrome.storage.local.get(["estado", "resultado"], actualizarInterfaz);

  // Se escucha cualquier cambio en vivo (Si el usuario abre el popup MIENTRAS siguie cargando)
  chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === "local") {
      chrome.storage.local.get(["estado", "resultado"], actualizarInterfaz);
    }
  })
});