const mockData = {
  status: "success",
  global_assessment: "Falso",
  analysis: {
    style_analysis: {
      engine: "BETO NLP",
      fake_probability_score: 92.5,
    },
    fact_check_analysis: {
      verdict: "Desinformación",
      reasoning: "No existe evidencia real del evento reportado."
    }
  }
};

export default mockData;