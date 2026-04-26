import { useEffect, useState } from "react";
import GaugeChart from "../components/GaugeChart";
import AnalysisSummary from "../components/AnalysisSummary";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";
import ReferenceList from "../components/ReferenceList";
import NewsInput from "../components/NewsInput";
import { analyzeNews, getGeminiStatus } from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState("");
  const [geminiService, setGeminiService] = useState("Verificando...");
 const [currentText, setCurrentText] = useState("");

  useEffect(() => {
    const checkGemini = async () => {
      try {
        const status = await getGeminiStatus();
        setGeminiService(status.status || "OK");
      } catch {
        setGeminiService("NO DISPONIBLE");
      }
    };

    const fetchInitialAnalysis = async () => {
      try {
        setInitialLoading(true);
        setError("");

        const response = await analyzeNews(currentText);
        setData(response);
            } catch (err) {
        console.error("Error inicial:", err);
        setData(null);
        setError(
          "EL ANALISIS INICIAL FALLÓ. INTENTAR DE NUEVO O ANALIZAR OTRO TEXTO."
        );
      } finally {
        setInitialLoading(false);
      }
    };

    checkGemini();
    //fetchInitialAnalysis();
    setInitialLoading(false);
  }, []);

  const handleAnalyze = async (text) => {
    try {
      console.log("Analizando texto:", text);

      setLoading(true);
      setError("");
      setCurrentText(text);

      const response = await analyzeNews(text);

      console.log("Respuesta backend:", response);
      if (
  response?.global_assessment?.toLowerCase().includes("error") ||
  response?.analysis?.fact_check_analysis?.reasoning?.toLowerCase().includes("failed")
) {
  setData(null);
  setError("ERRO AL ANALIZAR LA NOTICIA. INTENTAR DE NUEVO O ANALIZAR OTRO TEXTO.");
  return;
}

      setData(response);
        } catch (err) {
      console.error("Error al analizar:", err);
      setData(null);
      setError(
        "ERROR AL ANALIZAR LA NOTICIA."
      );
    } finally {
      setLoading(false);
    }
  };

  const score = data?.analysis?.style_analysis?.fake_probability_score ?? 0;
  const verdict = data?.global_assessment ?? "Desconocido";
  const reasoning =
    data?.analysis?.fact_check_analysis?.reasoning ??
    "No se recibió razonamiento del backend.";
  const engine = data?.analysis?.style_analysis?.engine ?? "BETO NLP";
  const references = data?.analysis?.fact_check_analysis?.references ?? [];

  return (
    <main className="dashboard-page">
      <div className="dashboard-container">
        <header className="dashboard-header">
          <div>
            <h1 className="dashboard-title">Fake Radar</h1>
            <p className="dashboard-subtitle">
              Dashboard de análisis de veracidad de noticias
            </p>
          </div>
        </header>

        <NewsInput
          defaultText={currentText}
          onAnalyze={handleAnalyze}
          loading={loading}
        />

        {initialLoading ? (
          <LoadingState />
        ) : error && !data ? (
          <ErrorState message={error} />
        ) : (
          <>
            {loading && <LoadingState />}

            {error && <ErrorState message={error} />}

            {!loading && (
              <>
                <section className="dashboard-grid">
                  <GaugeChart score={score} />

                  <AnalysisSummary
                    verdict={verdict}
                    reasoning={reasoning}
                    score={score}
                    engine={engine}
                    geminiService={geminiService}
                  />
                </section>

                <section className="test-text-card">
                  <h2 className="test-text-title">Texto analizado</h2>
                  <p className="test-text-content">{currentText}</p>
                </section>

                <ReferenceList references={references} />
              </>
            )}
          </>
        )}
      </div>
    </main>
  );
}