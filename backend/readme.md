# ⚙️ Backend - Fake Radar API

Bienvenido al núcleo de "Fake Radar". Este módulo contiene la API REST desarrollada en FastAPI. 
[cite_start]Nuestra arquitectura es 100% Stateless (sin base de datos), por lo que cada petición de análisis inicia y termina en la memoria del servidor.

---

## 🛠️ Herramientas Necesarias (Pre-requisitos)
Antes de escribir la primera línea de código, asegúrate de tener instalado en tu computadora:
* **Python 3.10+** (Para el autocompletado en VS Code).
* **Docker Desktop** (Obligatorio para correr el servidor).
* **Visual Studio Code** con la extensión oficial de "Python".

---

## 🚀 Flujo de Configuración Inicial (Solo la primera vez)

Para evitar que VS Code marque errores de sintaxis (líneas amarillas) por no encontrar FastAPI, necesitamos crear un entorno virtual local. **Nota: Este entorno es solo para que VS Code lea las librerías; el código real siempre se ejecutará dentro de Docker.**

**1. Abre tu terminal en la carpeta `/backend` y crea el entorno:**
* **En Windows:** `python -m venv venv`
* **En Linux/Mac:** `python3 -m venv venv`

**2. Activa el entorno virtual:**
* **En Windows:** `.\venv\Scripts\activate`
* **En Linux/Mac:** `source venv/bin/activate`

**3. Instala las dependencias de desarrollo:**
`pip install -r requirements.txt`

**4. Configura VS Code:**
Presiona `Ctrl + Shift + P`, busca "Python: Select Interpreter" y selecciona la ruta de tu nuevo entorno `venv`.

---

## ⚡ Flujo de Trabajo Diario (Cómo encender el servidor)

Tu rutina de todos los días para programar será la siguiente:

**1. Iniciar Docker:**
Abre la aplicación de Docker Desktop en tu computadora y espera a que el motor esté en verde.

**2. Levantar la API:**
Abre la terminal en la **RAÍZ DEL PROYECTO** (fuera de la carpeta backend, donde está el archivo `docker-compose.yml`) y ejecuta:
`docker compose up --build`

**3. Verificar que funciona:**
Abre tu navegador y entra a la documentación interactiva:
👉 `http://localhost:8000/docs`

**4. Programar en tiempo real:**
Gracias a los volúmenes de Docker, no necesitas apagar el servidor si haces un cambio. Solo guarda tu archivo en VS Code y FastAPI se reiniciará automáticamente. 
*(Para apagar el servidor al final del día, presiona `Ctrl + C` en la terminal).*

---

## 📜 Reglas de Desarrollo
* **Ramas:** Todo desarrollo se hace en ramas tipo `feature/nombre-de-tarea`[cite: 32, 33]. [cite_start]Cero *commits* a `main`[cite: 30].
* **Validaciones:** Toda entrada y salida de datos debe estar estrictamente tipada en `models.py` usando Pydantic.
* **Cero Base de Datos:** No implementaremos ORMs ni conexiones a bases de datos. El sistema opera conectándose directamente a los motores de IA en tiempo real.