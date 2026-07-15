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
    NPCS = (
    {
        "nombre": "pinguino_1",
        "x": 720,
        "ajuste_y": -8,
        "orden_leccion": 1,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    {
        "nombre": "pinguino_2",
        "x": 1900,
        "ajuste_y": -60,
        "orden_leccion": 2,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 2,
    },
    {
        "nombre": "pinguino_3",
        "x": 3300,
        "ajuste_y": -8,
        "orden_leccion": 3,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 0,
    },
)

    OBSTACULOS = (
       

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
        # PÚAS NUEVAS
        # ----------------------------------------------------
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 1930,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },

        # ----------------------------------------------------
        # SEGUNDAS PÚAS
        # ----------------------------------------------------
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 2275,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },

        # ----------------------------------------------------
        # FRAGMENTO 2 BAJO
        # ----------------------------------------------------
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2520,
            "ancho": 130,
            "alto": 45,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 0,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },
# ========================================================
# PRIMER FRAGMENTO: CUADRO DE ABAJO
# ========================================================
{
    "tipo": "fragmento",
    "imagen": "python/obstaculo_fragmento2.png",

    # Más a la derecha
    "x": 2520,

    "ancho": 130,
    "alto": 45,

    # Más abajo, casi a nivel del suelo
    "ajuste_y": -20,

    "hitbox_offset_x": 4,
    "hitbox_offset_y": 0,
    "hitbox_reducir_ancho": 8,
    "hitbox_reducir_alto": 0,
},
# ========================================================
# PRIMER FRAGMENTO: CUADRO DE ABAJO
# ========================================================
{
    "tipo": "fragmento",
    "imagen": "python/obstaculo_fragmento2.png",

    # Más a la derecha
    "x": 2795,

    "ancho": 130,
    "alto": 45,

    # Más abajo, casi a nivel del suelo
    "ajuste_y": -20,

    "hitbox_offset_x": 4,
    "hitbox_offset_y": 0,
    "hitbox_reducir_ancho": 8,
    "hitbox_reducir_alto": 0,
},

# ========================================================
# SEGUNDO FRAGMENTO: CUADRO DE ARRIBA
# ========================================================
{
    "tipo": "fragmento",
    "imagen": "python/obstaculo_fragmento2.png",

    # Más a la derecha que el primero
    "x": 2655,

    "ancho": 130,
    "alto": 45,

    # Más arriba que el primero
    "ajuste_y": -85,

    "hitbox_offset_x": 4,
    "hitbox_offset_y": 0,
    "hitbox_reducir_ancho": 8,
    "hitbox_reducir_alto": 0,
},

    # Túmulo colocado después de los fragmentos
    {
        "tipo": "piedra",
        "imagen": "python/obstaculo_tumulo.png",
        "x": 3300,
        "ancho": 100,
        "alto": 25,
        "ajuste_y": 0,

        # Hitbox para que el jugador pueda pararse encima
        "hitbox_izquierda": 3,
        "hitbox_derecha": 3,
        "hitbox_arriba": 2,
        "hitbox_abajo": 2,
    },
    )
    PRACTICAS = (
        {
            "x": 1374,
            "y": 395,
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
