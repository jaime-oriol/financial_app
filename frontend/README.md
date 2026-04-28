# FAPP — Frontend (NiceGUI · Python)

Web app en Python que consume el backend FastAPI. Se ejecuta como un proceso
Python normal y se ve y siente como una app móvil (centrado, bottom nav,
Material Design vía Quasar). Reemplaza el frontend Flutter (`frontend_v2/`).

## Stack

- **NiceGUI 2.x** — UI declarativa en Python (Quasar + Vue por debajo)
- **httpx** — cliente HTTP async para hablar con el backend
- **shared backend**: `https://fapp-api.onrender.com/api`

## Estructura

```
frontend/
├── app.py        # Entry point, registra rutas y lanza ui.run()
├── api.py        # Cliente HTTP centralizado (JWT, errores)
├── state.py      # Sesión persistente (app.storage.user)
├── theme.py      # Colores, iconos, formato de moneda
├── layout.py     # App shell + bottom nav + helpers de UI
└── pages/
    ├── auth.py    # /login, /register
    ├── home.py    # /
    ├── budget.py  # /budget
    ├── goals.py   # /goals
    └── profile.py # /profile
```

## Setup

```bash
cd frontend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # opcional
python app.py
```

Abre `http://localhost:8080`.

## Variables de entorno

| Variable | Default | Descripción |
|---|---|---|
| `API_URL` | `https://fapp-api.onrender.com/api` | URL del backend |
| `STORAGE_SECRET` | dev-only | Secreto para cookies de sesión |
| `PORT` | `8080` | Puerto del servidor |

## Deploy en Render

`render.yaml` ya está preparado:

```yaml
services:
  - type: web
    name: fapp-web
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
```

Solo configura `STORAGE_SECRET` como secret en el dashboard de Render.
