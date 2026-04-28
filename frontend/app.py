"""FAPP frontend entry point. Importa todas las pages (que se auto-registran via
@ui.page) y arranca el servidor NiceGUI.

Local:  python app.py
Render: gunicorn no aplica; usar `python app.py` (NiceGUI tiene su propio runner).
"""

import os

from dotenv import load_dotenv
from nicegui import ui

load_dotenv()

# Importar pages = registrar rutas. Orden no importa.
import pages.auth   # noqa: F401, E402  /login, /register
import pages.home   # noqa: F401, E402  /
import pages.budget  # noqa: F401, E402  /budget
import pages.challenges  # noqa: F401, E402  /challenges
import pages.quiz  # noqa: F401, E402  /quiz/{id}
import pages.simulation  # noqa: F401, E402  /simulation/{id}
import pages.goals   # noqa: F401, E402  /goals
import pages.profile  # noqa: F401, E402  /profile


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="FAPP",
        favicon="💰",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        storage_secret=os.getenv("STORAGE_SECRET", "fapp-dev-storage-secret-change-me"),
        reload=False,
        show=False,
    )
