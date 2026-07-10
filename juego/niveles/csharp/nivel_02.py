from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'C#'
NIVEL_ACTUAL = 2
FONDO_ACTUAL = 'c#'


class NivelCSharp02(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 5500
    NPC_X = 755
    AJUSTE_Y_NPC = -8

    PISOS = (
        (0, 920),
        (1080, LONGITUD_NIVEL),
    )

    ABISMOS = (
        (920, 1080),
    )

    OBSTACULOS = (
        {
            "tipo": "tronco",
            "imagen": "tronco.png",
            "x": 580,
            "ajuste_y": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 40,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 70,
        },
        {
            "tipo": "tronco",
            "imagen": "tronco.png",
            "x": 1450,
            "ajuste_y": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 40,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 70,
        },
    )

    PRACTICAS = (
        {
            "x": 1340,
            "y": None,
            "pregunta": 'En C#, una variable debe respetar el tipo de dato declarado.',
            "respuesta_correcta": True,
            "nombre": "practica_csharp_02",
        },
    )


CLASE_NIVEL = NivelCSharp02


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
