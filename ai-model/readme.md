
# 🤖 Fake Radar — Módulo de IA (BETO)

**Responsable:** B. Aguayo — Ingeniería IA / NLP  
**Proyecto:** Fake Radar: Sistema Inteligente de Detección de Desinformación  
**Instituto Tecnológico de Tijuana — Enero-Junio 2026**

---

## ¿Qué hace este módulo?

Fine-tuning del modelo BETO (`dccuchile/bert-base-spanish-wwm-uncased`) sobre un dataset real de noticias en español para clasificar si una noticia es **Fake** o **Verdadera**.

---

## Modelo

| Parámetro | Valor |
|---|---|
| Modelo base | BETO (BERT en español) |
| Dataset | 676 noticias balanceadas (338 Fake / 338 Real) |
| Épocas | 3 |
| Dispositivo | CPU |
| Idioma | Español |

---

## Estructura del módulo

```
ai/
├── fake_radar_beto.ipynb
├── train.xlsx
├── beto_fakenews_model/
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   └── special_tokens_map.json
├── plot_07_curvas_entrenamiento.png
├── plot_08_evaluacion_beto.png
└── README.md
```

---

## Requisitos

- Python 3.11
- Las siguientes librerías:

```bash
pip install transformers torch pandas openpyxl matplotlib seaborn scikit-learn
```

---

## ¿Cómo correr el entrenamiento?

Asegúrate de tener Python 3.11 y las dependencias instaladas antes de comenzar.

**1. Instala las dependencias:**

```bash
pip install transformers torch pandas openpyxl matplotlib seaborn scikit-learn
```

**2. Coloca el dataset en la misma carpeta que el notebook:**

```
fake_radar_beto.ipynb
train.xlsx  ← aquí
```

**3. Abre Jupyter y ejecuta todas las celdas en orden:**

```bash
jupyter notebook
```

⚠️ El entrenamiento corre en CPU y toma entre 30 y 90 minutos dependiendo del equipo. Al finalizar, el modelo se guarda automáticamente en `beto_fakenews_model/`.

---

## Métricas del modelo

El modelo fue evaluado al finalizar las 3 épocas de entrenamiento sobre el conjunto de validación. Los resultados se generan automáticamente al correr el notebook y se guardan como gráficas en:

- `plot_07_curvas_entrenamiento.png` — evolución del loss y accuracy por época
- `plot_08_evaluacion_beto.png` — matriz de confusión y métricas finales

---

## Fundamento teórico

El módulo se sustenta en dos paradigmas fundamentales de la teoría de la computación e inteligencia artificial:

- **Autómata Finito Determinista (AFD)** — el tokenizador de BETO valida y estructura la entrada transformando el texto en tokens numéricos mediante transiciones de estado deterministas basadas en las reglas morfológicas del español.
- **Red Semántica Neuronal** — BETO representa relaciones semánticas del español mediante mecanismos de atención multi-cabeza (multi-head attention), permitiendo al modelo distinguir patrones lingüísticos propios de la desinformación de aquellos característicos del periodismo verificado.

---

## Nota para el equipo de backend

El modelo entrenado está listo para integrarse con la API. La carpeta `beto_fakenews_model/` contiene todos los archivos necesarios para cargarlo con HuggingFace Transformers. Consultar con la Ingeniera de IA para detalles de integración.

---

*Fake Radar — Instituto Tecnológico de Tijuana — Enero-Junio 2026*
