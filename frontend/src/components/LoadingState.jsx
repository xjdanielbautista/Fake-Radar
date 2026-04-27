export default function LoadingState() {
  return (
    <div className="loading-card">
      <div className="spinner"></div>
      <h2 className="loading-title">Analizando noticia...</h2>
      <p className="loading-text">
        Fake Radar está procesando el análisis lingüístico y verificando el contenido.
      </p>
    </div>
  );
}