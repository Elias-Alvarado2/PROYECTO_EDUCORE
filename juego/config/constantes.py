"""Constantes generales reutilizadas por todos los niveles."""

from juego.core.motor import (
    ANCHO, ALTO, FPS, ESCALA_JUEGO, PISO_Y, PISO_COLISION_Y,
    TAMANO_TILE, TAMANO_OBSTACULO, ESCALA_OBSTACULOS,
    VELOCIDAD_CAMINAR, VELOCIDAD_AIRE, VIDAS_MAXIMAS,
)

__all__ = [name for name in globals() if name.isupper()]
