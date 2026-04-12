export default function ErrorState({ message }) {
  return (
    <div className="error-card">
      <h2 className="error-title">Ocurrió un error</h2>
      <p className="error-text">{message}</p>
    </div>
  );
}