import argparse
import multiprocessing

from juego.niveles.cargador import crear_nivel
from juego.sistemas.pantalla_carga import (
    _actualizar_progreso_compartido,
    _cerrar_pantalla_carga,
    _iniciar_pantalla_carga,
)


def abrir_nivel(
    id_jugador: int | None = None,
    lenguaje: str = "python",
    numero_nivel: int = 1,
    usar_pantalla_carga: bool = True,
    sesion: dict | None = None,
):
    proceso = None
    progreso = None
    evento = None

    if usar_pantalla_carga:
        proceso, progreso, evento = _iniciar_pantalla_carga()

    try:
        callback = None

        if progreso is not None:
            callback = lambda valor: _actualizar_progreso_compartido(
                progreso,
                valor,
            )

        juego = crear_nivel(
            lenguaje=lenguaje,
            numero_nivel=numero_nivel,
            id_jugador=id_jugador,
            sesion=sesion,
            actualizar_progreso_carga=callback,
        )

    except Exception:
        if proceso is not None:
            _cerrar_pantalla_carga(
                proceso,
                progreso,
                evento,
            )

        raise

    if proceso is not None:
        _cerrar_pantalla_carga(
            proceso,
            progreso,
            evento,
        )

    # El motor devuelve el control cuando se pulsa SALIR.
    resultado = juego.ejecutar()
    return resultado


def obtener_argumentos():
    parser = argparse.ArgumentParser(description="EduCore")

    parser.add_argument(
        "--jugador",
        type=int,
        default=1,
    )

    parser.add_argument(
        "--lenguaje",
        type=str,
        default="mysql",
    )

    parser.add_argument(
        "--nivel",
        type=int,
        default=
        4,
    )

    parser.add_argument(
        "--sin-carga",
        action="store_true",
        help="Inicia sin la pantalla de carga PyQt6",
    )

    return parser.parse_args()


def main():
    multiprocessing.freeze_support()

    args = obtener_argumentos()

    abrir_nivel(
        id_jugador=args.jugador,
        lenguaje=args.lenguaje,
        numero_nivel=args.nivel,
        usar_pantalla_carga=not args.sin_carga,
    )


if __name__ == "__main__":
    main()
