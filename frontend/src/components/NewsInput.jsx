import { useState } from "react";

export default function NewsInput({ defaultText = "", onAnalyze, loading }) {
  const [text, setText] = useState(defaultText);

  const handleSubmit = (e) => {
  e.preventDefault();

  const cleanText = text.trim();

  console.log("Botón presionado");
  console.log("Texto enviado:", cleanText);

  if (!cleanText) {
    console.log("No hay texto");
    return;
  }

  onAnalyze(cleanText);
};

  return (
    <section className="test-text-card input-section">
      <h2 className="test-text-title">NOTICIA A ANALIZAR:</h2>
      <p className="dashboard-subtitle input-subtitle">
        Pegar aquí el titular o cuerpo de la noticia que deseas analizar. Asegúrate de incluir suficiente contexto para obtener un análisis preciso.    
      </p>

      <form onSubmit={handleSubmit} className="news-form">
        <textarea
          className="news-textarea"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Ejemplo: Se filtra documento donde..."
          rows={8}
        />

        <div className="news-form-actions">
          <button
            type="submit"
            className="analyze-button"
            disabled={loading || !text.trim()}
          >
            {loading ? "Analizando..." : "Analizar noticia"}
          </button>
        </div>
      </form>
    </section>
  );
}