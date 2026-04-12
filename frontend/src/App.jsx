import { useEffect, useState } from "react";
import Dashboard from "./pages/Dashboard";
import "./App.css";

function App() {
  const getSystemTheme = () => {
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  };

  const [theme, setTheme] = useState(getSystemTheme());

  // Aplicar tema
  useEffect(() => {
    document.body.setAttribute("data-theme", theme);
  }, [theme]);

  // Escuchar cambios del sistema
  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

    const handleChange = (e) => {
      setTheme(e.matches ? "dark" : "light");
    };

    mediaQuery.addEventListener("change", handleChange);

    return () => mediaQuery.removeEventListener("change", handleChange);
  }, []);

  return <Dashboard theme={theme} />;
}

export default App;