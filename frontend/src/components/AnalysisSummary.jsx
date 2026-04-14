function getVerdictClass(score) {
  if (score <= 25) return "verdict-safe";
  if (score <= 50) return "verdict-warning";
  if (score <= 75) return "verdict-alert";
  return "verdict-danger";
}

export default function AnalysisSummary({
  verdict,
  reasoning,
  score,
  engine,
  geminiService,
}) {
  const verdictClass = getVerdictClass(score);

  return (
    <div className="card glass-card">
      <div className="card-top">
        <h2 className="card-title">Resultado general</h2>
      </div>

      <div className={`result-badge ${verdictClass}`}>{verdict}</div>

      <p className="reasoning-text">{reasoning}</p>

      <div className="summary-divider"></div>

      <div className="summary-mini-stats">
        <div className="mini-stat">
          <span className="mini-stat-label">Motor</span>
          <strong>{engine}</strong>
        </div>

        <div className="mini-stat">
          <span className="mini-stat-label">Puntaje</span>
          <strong>{score}%</strong>
        </div>

        <div className="mini-stat">
          <span className="mini-stat-label">Gemini</span>
          <strong>{geminiService}</strong>
        </div>
      </div>
    </div>
  );
}