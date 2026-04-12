export default function ReferenceList({ references = [] }) {
  if (!references.length) {
    return (
      <section className="test-text-card">
        <h2 className="test-text-title">Fuentes de contraste</h2>
        <p className="test-text-content">
          No se encontraron referencias disponibles para este análisis.
        </p>
      </section>
    );
  }

  return (
    <section className="test-text-card">
      <h2 className="test-text-title">Fuentes de contraste</h2>

      <div className="references-grid">
        {references.map((ref, index) => (
          <a
            key={`${ref.url}-${index}`}
            href={ref.url}
            target="_blank"
            rel="noreferrer"
            className="reference-card"
          >
            <span className="reference-domain">{ref.domain}</span>
            <h3 className="reference-title">{ref.title}</h3>
            <p className="reference-link">{ref.url}</p>
          </a>
        ))}
      </div>
    </section>
  );
}