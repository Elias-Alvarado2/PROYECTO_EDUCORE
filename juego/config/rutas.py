"""Rutas centrales del proyecto."""

from juego.core.motor import (
    BASE_DIR, ASSETS_DIR, FONDOS_DIR, PERSONAJES_DIR, OBSTACULOS_DIR,
    NPC_DIR, UI_DIR, FUENTES_DIR, MUSICA_DIR, EFECTOS_DIR, DISENOS_DIR,
)

__all__ = [name for name in globals() if name.isupper()]
