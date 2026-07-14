from pathlib import Path
import sys


CODIGOS_DIR = Path(__file__).resolve().parents[2] / "CODIGOS"

if str(CODIGOS_DIR) not in sys.path:
    sys.path.insert(0, str(CODIGOS_DIR))

from ConexionBD import ConexionBD


VIDAS_MAXIMAS = 5


def verificar_recuperacion_vidas(id_jugador):
    """
    Comprueba en MySQL si ya pasó una hora y devuelve
    la cantidad actual de vidas del jugador.
    """
    if id_jugador is None:
        return VIDAS_MAXIMAS

    return ConexionBD().verificar_recuperacion_vidas(
        id_jugador
    )
