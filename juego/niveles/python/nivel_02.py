from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = "Python"
NIVEL_ACTUAL = 2
FONDO_ACTUAL = "python"


class NivelPython02(JuegoBase):
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL

    JUGADOR_X_INICIAL = 170
    AJUSTE_Y_JUGADOR = 0

    LONGITUD_NIVEL = 5500

    NPC_X = 755
    AJUSTE_Y_NPC = -8

    AJUSTE_Y_SPRITE_MONTANAS = 2
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0

    PISOS = (
        (0, LONGITUD_NIVEL),
    )

    NPCS = (
    {
        "nombre": "pinguino_1",
        "x": 2990,
        "ajuste_y": -126,
        "orden_leccion": 1,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
)
    # ========================================================
    # OBSTÁCULOS
    # ========================================================

    OBSTACULOS = (
        # Fragmento 1: abajo
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1050,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -25,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 8,
        },

        # Fragmento 2: más arriba
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1230,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -115,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 8,
        },
{
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 1525,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },
        # Púas
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 1850,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },

        # Fragmento 3
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2200,
            "ancho": 130,
            "alto": 35,
            "ajuste_y": -110,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 8,
        },
{
    "tipo": "fragmento",
    "imagen": "python/obstaculo_fragmento2.png",
    "x": 1950,
    "ancho": 130,
    "alto": 35,
    "ajuste_y": -170,
    "hitbox_offset_x": 4,
    "hitbox_offset_y": 8,
    "hitbox_reducir_ancho": 8,
    "hitbox_reducir_alto": 0,
},

# ========================================================
# FRAGMENTO INFERIOR
# ========================================================
{
    "tipo": "fragmento",
    "imagen": "python/obstaculo_fragmento2.png",
    "x": 2050,
    "ancho": 130,
    "alto": 35,
    "ajuste_y": -20,
    "hitbox_offset_x": 4,
    "hitbox_offset_y": 8,
    "hitbox_reducir_ancho": 8,
    "hitbox_reducir_alto": 0,
},
# ========================================================
        # FRAGMENTO INFERIOR
        # ========================================================
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2050,
            "ancho": 130,
            "alto": 35,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # ========================================================
        # PÚAS NUEVAS
        # ========================================================
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 2180,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },

        # ========================================================
        # FRAGMENTO NUEVO A LA DERECHA
        # ========================================================
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2350,
            "ancho": 130,
            "alto": 35,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },
         # Fragmento bajo izquierdo
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 2580,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # Fragmento alto izquierdo
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 2720,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -85,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # Púas al centro
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 2870,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },

        # Fragmento alto derecho
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 2990,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -85,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # Fragmento bajo derecho
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 3140,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },
    )

    # ========================================================
    # PRÁCTICAS
    # ========================================================

    PRACTICAS = (
        {
            "x": 1340,
            "y": None,
            "tipo": "verdadero_falso",
            "pregunta": (
                "En Python, una variable sirve para almacenar "
                "un dato que puede utilizarse después."
            ),
            "respuesta_correcta": True,
            "nombre": "practica_python_02",
        },
        
    )


CLASE_NIVEL = NivelPython02


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()