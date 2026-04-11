// popup.js

document.addEventListener('DOMContentLoaded', () => {
  const semaforo = document.getElementById("semaforo");
  const resumen = document.getElementById("resumen");

  // 1. Leemos lo que guardó el background.js
  chrome.storage.local.get(["ultimoTexto", "ultimaUrl"], async (result) => {
    if (result.ultimoTexto) {
      
      // Mostramos estado de carga
      semaforo.className = "status gris"; 
      semaforo.style.backgroundColor = "#9ca3af"; // Color gris temporal
      semaforo.innerText = "ANALIZANDO...";
      resumen.innerText = "Conectando con el motor de IA. Por favor espera...";

      try {
        // 2. CONEXIÓN CON EL BACKEND (main.py)
        const response = await fetch("http://localhost:8000/analyze", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          // Mandamos el JSON tal cual lo pide AnalyzeRequest en models.py
          body: JSON.stringify({
            text: result.ultimoTexto,
            source_url: result.ultimaUrl
          })
        });

        if (!response.ok) throw new Error("Error en el servidor");

        // 3. RECIBIMOS LA RESPUESTA DE LA IA 
        const data = await response.json();

        // 4. PINTAMOS LOS RESULTADOS SEGÚN EL JSON DE models.py (AnalyzeResponse)
        semaforo.innerText = "VEREDICTO: " + data.global_assessment.toUpperCase();

        
        if (data.global_assessment === "Falso") {
          semaforo.style.backgroundColor = "#ff4d4d"; // Rojo
        } else if (data.global_assessment === "Verdadero") {
          semaforo.style.backgroundColor = "#2ecc71"; // Verde
        } else {
          semaforo.style.backgroundColor = "#f1c40f"; // Amarillo para Dudoso
        }

        // Mostramos el razonamiento del fact_check_analysis
        resumen.innerText = data.analysis.fact_check_analysis.reasoning;

      } catch (error) {
        semaforo.innerText = "ERROR DE CONEXIÓN";
        semaforo.style.backgroundColor = "#333";
        resumen.innerText = "Asegúrate de que Docker esté corriendo y el backend encendido (localhost:8000).";
        console.error(error);
      }
    } else {
      resumen.innerText = "Selecciona un texto, da clic derecho y presiona 'Analizar con Fake Radar'.";
    }
  });
});