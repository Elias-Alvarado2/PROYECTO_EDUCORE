"""Nombres aceptados por el cargador de niveles."""

CARPETAS_LENGUAJES = {
    "python": "python",
    "java": "java",
    "c#": "csharp",
    "csharp": "csharp",
    "mysql": "mysql",
}


def normalizar_lenguaje(lenguaje: str) -> str:
    clave = lenguaje.strip().lower()
    if clave not in CARPETAS_LENGUAJES:
        raise ValueError(f"Lenguaje no reconocido: {lenguaje}")
    return CARPETAS_LENGUAJES[clave]
