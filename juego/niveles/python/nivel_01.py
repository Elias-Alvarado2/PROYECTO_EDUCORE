from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Python'
NIVEL_ACTUAL = 1
FONDO_ACTUAL = 'python'


class NivelPython01(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 5000
    NPC_X = 720
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 2
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    PISOS = (
        (0, LONGITUD_NIVEL),
    )

    OBSTACULOS = (
        # ----------------------------------------------------
        # CACTUS
        # ----------------------------------------------------
        {
            "tipo": "cactus",
            "imagen": "python/cactus_obstaculo.png",
            "x": 700,
            "ancho": 65,
            "alto": 55,
            "ajuste_y": 0,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 8,
        },

        # ----------------------------------------------------
        # FRAGMENTOS FLOTANTES
        # ----------------------------------------------------
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 950,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -35,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 4,
        },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1080,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -75,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 4,
        },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1210,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -115,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 4,
        },

        # Escalera para bajar
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1340,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -70,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 4,
        },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1470,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -25,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 4,
        },

        # ----------------------------------------------------
        # PIEDRA
        # ----------------------------------------------------
        {
            "tipo": "piedra",
            "imagen": "python/piedra_obstaculo.png",
            "x": 1750,
            "ancho": 75,
            "alto": 45,
            "ajuste_y": 0,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 6,
        },

        # ----------------------------------------------------
        # PÚAS
        # ----------------------------------------------------
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 2050,
            "ancho": 85,
            "alto": 38,
            "ajuste_y": 0,
            "hitbox_offset_x": 7,
            "hitbox_offset_y": 8,
        },

        # ----------------------------------------------------
        # RUEDA
        # ----------------------------------------------------
        {
            "tipo": "rueda",
            "imagen": "python/rueda_obstaculo.png",
            "x": 2350,
            "ancho": 65,
            "alto": 45,
            "ajuste_y": 0,
            "hitbox_offset_x": 7,
            "hitbox_offset_y": 6,
        },

        # ----------------------------------------------------
        # TRONCO
        # ----------------------------------------------------
        {
            "tipo": "tronco",
            "imagen": "python/tronco.png",
            "x": 2650,
            "ancho": 105,
            "alto": 60,
            "ajuste_y": 0,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 8,
        },
    )
    PRACTICAS = (
        {
            "x": 2000,
            "y": None,
            "pregunta": 'En Python, una variable sirve para almacenar un dato que puede utilizarse después.',
            "respuesta_correcta": True,
            "nombre": "practica_python_01",
        },
        {
            "x": 1900,
            "y": None,
            "tipo": "codigo",
            "pregunta": (
                "Arrastra las opciones correctas para completar el código "
                "que comprueba si edad es mayor o igual que 18."
            ),
            "nombre": "practica_codigo_python_01",
            "respuestas": {
                "variable": "edad",
                "condicional": "if",
                "funcion": "print",
            },
            "codigo": [
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "variable"},
                        {"texto": " = 18"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "condicional"},
                        {"texto": " edad >= 18:"},
                    ],
                },
                {
                    "indentacion": 1,
                    "segmentos": [
                        {"hueco": "funcion"},
                        {"texto": '("Mayor de edad")'},
                    ],
                },
            ],
            "opciones": [
                "while",
                "print",
                "edad",
                "input",
                "if",
                "18",
            ],
        },
    )


CLASE_NIVEL = NivelPython01


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
