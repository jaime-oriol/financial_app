"""Theme central: colores, formateadores y constantes de UI.
Se importa desde todas las pages para mantener consistencia visual.
"""

# --- Colores principales (alineados con los wireframes) ---
PRIMARY = "#16213E"       # Header oscuro, titulos
SECONDARY = "#2675E3"     # Botones, acciones, tabs activos
ACCENT = "#27AE60"        # Exito, on-track, progreso positivo
WARNING = "#F39C12"       # Streak, behind-pace, alertas
ERROR = "#E74C3C"         # Gastos, sobre-presupuesto

# --- Grises y fondos ---
GREY_TEXT = "#7F8C8D"     # Texto secundario, labels
GREY_SOFT = "#BDC3C7"     # Placeholders, iconos disabled
GREY_BG = "#F0F2F5"       # Fondos de inputs y cards
BG = "#FAFBFD"            # Background de la app
WHITE = "#FFFFFF"

# --- Categorias (deben coincidir con seeds del backend) ---
CATEGORY_COLORS = {
    1: "#E74C3C",  # Food
    2: "#2980B9",  # Transport
    3: "#F1C40F",  # Entertainment
    4: "#1ABC9C",  # Health
    5: "#8E44AD",  # Education
    6: "#95A5A6",  # Other
}

CATEGORY_ICONS = {
    1: "restaurant",
    2: "directions_bus",
    3: "movie",
    4: "local_hospital",
    5: "school",
    6: "more_horiz",
}


def category_color(category_id: int) -> str:
    return CATEGORY_COLORS.get(category_id, GREY_SOFT)


def category_icon(category_id: int) -> str:
    return CATEGORY_ICONS.get(category_id, "category")


_INITIAL_COLORS = ["#2675E3", "#27AE60", "#E74C3C", "#F39C12", "#8E44AD", "#1ABC9C"]


def avatar_color(user_id: int) -> str:
    """Color estable por user_id para el fallback con inicial."""
    return _INITIAL_COLORS[user_id % len(_INITIAL_COLORS)]


def is_photo_avatar(avatar: str | None) -> bool:
    return bool(avatar and avatar.startswith("data:"))


def fmt_money(amount: float | int | str | None, decimals: int = 2) -> str:
    """Formatear cantidad como moneda. Acepta str (Decimal serializado)."""
    if amount is None:
        return "$0.00"
    try:
        n = float(amount)
    except (TypeError, ValueError):
        return "$0.00"
    return f"${n:,.{decimals}f}"
