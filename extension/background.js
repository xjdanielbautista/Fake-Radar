chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzeText",
    title: "Analizar con Fake Radar",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "analyzeText") {
    // Capturamos el texto y la URL de la página donde está el usuario
    const textoParaAnalizar = info.selectionText;
    const urlDeOrigen = info.pageUrl; 
    
    // Guardamos ambos datos para que el popup los lea
    chrome.storage.local.set({ 
      "estado": "cargando",
      "ultimoTexto": textoParaAnalizar
    });

    try {

      // La peticion empieza a ocurrir en segundo plano
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: textoParaAnalizar,
            source_url: urlDeOrigen
        })
      });

      if (!response.ok) throw new Error("Error en la respuesta del servidor");

      const data = await response.json();

      // Se guarda el resultado para que el popup lo muestre
      chrome.storage.local.set({ 
        "estado": "completado",
        "resultado": data
      });

    } catch (error) {
      console.error("Fallo de conexión en background", error);
      chrome.storage.local.set({ 
        "estado": "error"
      });
    }
  }
});