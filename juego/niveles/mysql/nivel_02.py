from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'MySQL'
NIVEL_ACTUAL = 2
FONDO_ACTUAL = 'mysql'


class NivelMySQL02(JuegoBase):
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
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    PISOS = (
        (0, LONGITUD_NIVEL),
    )

    NPCS = (
    {
        "nombre": "pinguino_1",
        "x": 200,
        "ajuste_y": -8,
        "orden_leccion": 4,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },)

    OBSTACULOS = (
    )

    PRACTICAS = (
    {
    "x": 2200,
    "y": None,
    "tipo": "ejemplo",
    "pregunta": "Observa cómo se organizan los datos en esta tabla.",
    "imagen": "mysql/tabla_usuarios.png",
    "ancho": 1000,
    "alto": 500,
    "nombre": "ejemplo_tabla_usuarios",
},
    )


CLASE_NIVEL = NivelMySQL02


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
