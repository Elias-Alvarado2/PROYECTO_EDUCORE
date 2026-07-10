from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Python'
NIVEL_ACTUAL = 6
FONDO_ACTUAL = 'python'


class NivelPython06(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 7500
    NPC_X = 895
    AJUSTE_Y_NPC = -8

    PISOS = (
        (0, 1200),
        (1400, LONGITUD_NIVEL),
    )

    ABISMOS = (
        (1200, 1400),
    )

    OBSTACULOS = (
        {
            "tipo": "tronco",
            "imagen": "tronco.png",
            "x": 900,
            "ajuste_y": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 40,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 70,
        },
        {
            "tipo": "tronco",
            "imagen": "tronco.png",
            "x": 1930,
            "ajuste_y": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 40,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 70,
        },
        {
            "tipo": "tronco",
            "imagen": "tronco.png",
            "x": 2760,
            "ajuste_y": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 40,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 70,
        },
    )

    PRACTICAS = (
        {
            "x": 1660,
            "y": None,
            "pregunta": 'En Python, una variable sirve para almacenar un dato que puede utilizarse después.',
            "respuesta_correcta": True,
            "nombre": "practica_python_06",
        },
    )


CLASE_NIVEL = NivelPython06


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
