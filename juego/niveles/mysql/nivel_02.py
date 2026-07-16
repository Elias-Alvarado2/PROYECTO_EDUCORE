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
    },
    {
        "nombre": "pinguino_2",
        "x": 1800,
        "ajuste_y": -200,
        "orden_leccion": 5,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 2,
    },

    )

    OBSTACULOS = (
        {
            "tipo":"bloque",
            "imagen":"mysql/bloque.png",
            "x": 800,
            "ajuste_y":-5,
            "ancho": 100,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"cofre",
            "imagen":"mysql/cofre.png",
            "x": 820,
            "ajuste_y":-30,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 570,
            "ajuste_y":-120,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 1050,
            "ajuste_y":-120,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 1400,
            "ajuste_y":-160,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 1750,
            "ajuste_y":-200,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
    )

    PRACTICAS = (
    {
    "x": 610,
    "y": 385,
    "tipo": "ejemplo",
    "pregunta": "Observa esta tabla como ejemplo.",
    "imagen": "mysql/tabla_ejemplo1.png",
    "ancho": 750,
    "alto": 350,
    "nombre": "ejemplo_tabla_usuarios",
    },
    )


CLASE_NIVEL = NivelMySQL02


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
