from importlib import import_module

from juego.config.mundos import normalizar_lenguaje


def cargar_clase_nivel(lenguaje: str, numero_nivel: int):
    if not 1 <= int(numero_nivel) <= 6:
        raise ValueError("El nivel debe estar entre 1 y 6.")

    carpeta = normalizar_lenguaje(lenguaje)
    modulo = import_module(
        f"juego.niveles.{carpeta}.nivel_{int(numero_nivel):02d}"
    )
    return modulo.CLASE_NIVEL


def crear_nivel(
    lenguaje: str,
    numero_nivel: int,
    id_jugador: int = 1,
    actualizar_progreso_carga=None,
):
    clase_nivel = cargar_clase_nivel(lenguaje, numero_nivel)
    return clase_nivel(
        id_jugador=id_jugador,
        actualizar_progreso_carga=actualizar_progreso_carga,
    )
