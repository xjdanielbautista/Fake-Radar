chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzeText",
    title: "Analizar con Fake Radar",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "analyzeText") {
    // Capturamos el texto y la URL de la página donde está el usuario
    const textoParaAnalizar = info.selectionText;
    const urlDeOrigen = info.pageUrl; 
    
    // Guardamos ambos datos para que el popup los lea
    chrome.storage.local.set({ 
        "ultimoTexto": textoParaAnalizar,
        "ultimaUrl": urlDeOrigen
    }, () => {
      console.log("Texto y URL guardados para el análisis.");
    });
  }
});