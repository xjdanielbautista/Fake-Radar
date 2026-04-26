// popup.js

document.addEventListener("DOMContentLoaded", () => {
  const semaforo = document.getElementById("semaforo");
  const resumen = document.getElementById("resumen");

  // Función que pinta la pantalla según el estado guardado
  const actualizarInterfaz = (result) => {
    if (!result.estado) {
      semaforo.style.background = "linear-gradient(135deg, #9333ea, #c026d3)";
      semaforo.innerText = "ESPERANDO...";
      resumen.innerText =
        "Selecciona un texto, da clic derecho y elige “Analizar con Fake Radar”.";
      return;
    }

    if (result.estado === "cargando") {
      semaforo.style.background = "linear-gradient(135deg, #64748b, #475569)";
      semaforo.innerText = "ANALIZANDO...";
      resumen.innerText =
        "Estamos revisando la noticia. Esto puede tardar unos segundos.";
      return;
    }

    if (result.estado === "error") {
      semaforo.style.background = "linear-gradient(135deg, #ef4444, #991b1b)";
      semaforo.innerText = "NO SE PUDO ANALIZAR";
      resumen.innerText =
        "Ocurrió un problema al procesar la noticia. Intenta nuevamente en unos momentos.";
      return;
    }

    if (result.estado === "completado" && result.resultado) {
      const data = result.resultado;

      const verdict = data.global_assessment || "Desconocido";
      const reasoning =
        data.analysis?.fact_check_analysis?.reasoning ||
        "No se recibió una explicación del análisis.";

      if (
        verdict.toLowerCase().includes("error") ||
        reasoning.toLowerCase().includes("failed")
      ) {
        semaforo.style.background = "linear-gradient(135deg, #ef4444, #991b1b)";
        semaforo.innerText = "NO SE PUDO ANALIZAR";
        resumen.innerText =
          "El análisis no se pudo completar. Intenta nuevamente o prueba con otro texto.";
        return;
      }

      semaforo.innerText = "VEREDICTO: " + verdict.toUpperCase();

      if (verdict === "Falso") {
        semaforo.style.background = "linear-gradient(135deg, #ef4444, #b91c1c)";
      } else if (verdict === "Verdadero") {
        semaforo.style.background = "linear-gradient(135deg, #22c55e, #15803d)";
      } else {
        semaforo.style.background = "linear-gradient(135deg, #f59e0b, #b45309)";
      }

      resumen.innerText = reasoning;
    }
  };

  // Se lee el estado actual al abrir el popup
  chrome.storage.local.get(["estado", "resultado"], actualizarInterfaz);

  // Se escucha cualquier cambio en vivo
  chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === "local") {
      chrome.storage.local.get(["estado", "resultado"], actualizarInterfaz);
    }
  });
});