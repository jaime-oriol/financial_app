# CLAUDE.md — FAPP

No vuelvas a leer archivos ya leidos en esta sesion a menos que te lo pida. Minimiza las llamadas a herramientas y trabaja con lo que ya tienes en contexto.

Cuando te pida el mensaje del commit, dame siempre para copy-paste un comando en una sola linea con este formato exacto:

IMPORTANTE: NUNCA MENCIONES A CLAUDE CODE!

```
git add . && git commit -m "MENSAJE EN 1 LINEA" && git push origin main
```

---

## Core Philosophy

Ve paso a paso, uno a uno. Despacio es el camino mas rapido. Escribe siempre el codigo lo mas compacto y conciso posible, y que cumpla exactamente lo pedido al 100%. Sin emojis ni florituras. Usa nombres claros y estandar. Incluye solo comentarios utiles y necesarios.

Antes de realizar cualquier tarea, revisa cuidadosamente el archivo CLAUDE.md.

Codigo: compacto, conciso, sin emojis, bien estructurado (modular, clases, metodos...), con comentarios utiles, escrito de forma "tonta" y humana, como para mi abuela.

### Development Principles

- **KISS**: Choose straightforward solutions over complex ones
- **YAGNI**: Implement features only when needed
- **Fail Fast**: Check for errors early and raise exceptions immediately
- **Single Responsibility**: Each function, class, and module has one clear purpose
- **Dependency Inversion**: High-level modules depend on abstractions, not implementations

---

## Coding Standards

### Style

```python
nombre_variable = "ejemplo"       # snake_case for variables/functions
class GestorUsuario:              # PascalCase for classes
MAX_REINTENTOS = 3                # UPPER_CASE for constants
_metodo_interno()                 # underscore for private

# Type hints required
def procesar_datos(datos: List[Dict]) -> pd.DataFrame:
    """Procesar con tipos claros."""
```

---

## Git Conventions

```bash
# Branch naming
feature/   fix/   docs/   refactor/   experiment/

# Commit format (conventional commits)
feat(modulo): descripcion corta
fix(modulo): descripcion corta
docs: descripcion corta
refactor(modulo): descripcion corta
```
