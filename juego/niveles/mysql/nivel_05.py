from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'MySQL'
NIVEL_ACTUAL = 5
FONDO_ACTUAL = 'mysql'


class NivelMySQL05(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 7000
    NPC_X = 860
    AJUSTE_Y_NPC = -8

    PISOS = (
        (0, 1130),
        (1320, LONGITUD_NIVEL),
    )

    ABISMOS = (
        (1130, 1320),
    )

    OBSTACULOS = (
        {
            "tipo": "tronco",
            "imagen": "tronco.png",
            "x": 820,
            "ajuste_y": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 40,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 70,
        },
        {
            "tipo": "tronco",
            "imagen": "tronco.png",
            "x": 1810,
            "ajuste_y": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 40,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 70,
        },
        {
            "tipo": "tronco",
            "imagen": "tronco.png",
            "x": 2580,
            "ajuste_y": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 40,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 70,
        },
    )

    PRACTICAS = (
        {
            "x": 1580,
            "y": None,
            "pregunta": 'En MySQL, SELECT se utiliza para consultar datos de una tabla.',
            "respuesta_correcta": True,
            "nombre": "practica_mysql_05",
        },
    )


CLASE_NIVEL = NivelMySQL05


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
