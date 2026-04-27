# 🧩 Fake Radar - Chrome Extension Module

Este módulo contiene el cliente de navegador para el sistema **Fake Radar**, desarrollado bajo el estándar **Manifest V3**. Su función principal es permitir al usuario analizar fragmentos de noticias en tiempo real mediante la extracción de texto y la comunicación directa con el backend asíncrono.

## 📂 Estructura de Archivos y Responsabilidades

* **`manifest.json`**: Configuración técnica de la extensión. Define los permisos de almacenamiento local (`storage`), menús contextuales (`contextMenus`) y la conexión permitida con el servidor local.
* **`background.js`**: Service worker encargado de la lógica de fondo. Crea la opción "Analizar con Fake Radar" en el menú de clic derecho y captura el texto seleccionado junto con la URL de origen.
* **`popup.html`**: Interfaz de usuario (UI) del popup. Proporciona el contenedor visual para el semáforo de veracidad y el resumen del análisis.
* **`popup.js`**: Controlador de la interfaz. Gestiona la petición `POST` hacia `http://localhost:8000/analyze` y procesa el JSON de respuesta para actualizar el estado visual.

## ✅ Cumplimiento de Requerimientos Técnicos

1.  **Extracción de Datos**: Captura exclusivamente texto plano de titulares y cuerpos de noticias.
2.  **Semáforo de Veracidad**: Consume el campo `global_assessment` para determinar el color del indicador (Rojo para "Falso").
3.  **Resumen Ejecutivo**: Muestra el `reasoning` del motor de hechos (Gemini API) para ofrecer una explicación rápida al usuario.

## 🛠️ Instalación y Pruebas

1.  Carga la carpeta `extension` en `chrome://extensions/` usando el **Modo de desarrollador**.
2.  Asegúrate de que el backend (Docker) esté activo en el puerto **8000**.
3.  Selecciona un texto en una noticia de política, haz clic derecho y selecciona **"Analizar con Fake Radar"**.
4.  Abre el popup de la extensión para ver el veredicto generado por la IA.

---

