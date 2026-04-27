import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const analyzeNews = async (text, sourceUrl = null) => {
  const payload = { text };

  if (sourceUrl && sourceUrl.trim() !== "") {
    payload.source_url = sourceUrl;
  }

  const response = await api.post("/analyze", payload);
  return response.data;
};

export const getGeminiStatus = async () => {
  const response = await api.get("/gemini-status");
  return response.data;
};

export default api;