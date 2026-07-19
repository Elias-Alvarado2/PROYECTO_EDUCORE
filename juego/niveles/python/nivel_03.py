from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Python'
NIVEL_ACTUAL = 3
FONDO_ACTUAL = 'python'


class NivelPython03(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 6000
    NPC_X = 790
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
        "orden_leccion": 7,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
     {
        "nombre": "pinguino_2",
        "x": 2160,
        "ajuste_y": -180,
        "orden_leccion": 8,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 2,
    },
      {
        "nombre": "pinguino_3",
        "x": 3230,
        "ajuste_y": -145,
        "orden_leccion": 9,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 3,
    },
    
)
    OBSTACULOS = (
    # =========================================================
    # FRAGMENTO 1 - abajo izquierda
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 850,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -12,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # FRAGMENTO 3 - centro abajo
    # Rectángulo del centro inferior
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 990,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -95,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # FRAGMENTO 4 - centro medio
    # Rectángulo del medio
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 1160,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -135,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # FRAGMENTO 5 - derecha media
    # Rectángulo de la derecha
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 1345,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -80,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # FRAGMENTO 6 - abajo derecha
    # Último rectángulo de la foto
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 1525,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -12,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # PÚAS 1 - círculo izquierdo
    # =========================================================
    {
        "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 1000,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },

    # =========================================================
    # PÚAS 2 - círculo centro
    # =========================================================
    {
        "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 1200,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },

    # =========================================================
    # PÚAS 3 - círculo derecho
    # =========================================================
    {
        "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 1350,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
    #================================
    #=== continuacion 2 

        # =========================================================
    # FRAGMENTO 7 - plataforma inicial inferior
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 1760,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -75,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # PÚAS 4 - entre fragmentos 7 y 8
    # =========================================================
    {
        "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 1865,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },

    # =========================================================
    # FRAGMENTO 8 - plataforma superior izquierda
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 1970,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -135,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # PÚAS 5 - entre fragmentos 8 y 9
    # =========================================================
    {
        "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 2075,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },

    # =========================================================
    # FRAGMENTO 9 - plataforma superior central
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 2180,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -135,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # PÚAS 6 - entre fragmentos 9 y 10
    # =========================================================
    {
        "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 2285,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },

    # =========================================================
    # FRAGMENTO 10 - plataforma superior derecha
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 2390,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -135,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # PÚAS 7 - entre fragmentos 10 y 11
    # =========================================================
    {
        "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 2495,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },

    # =========================================================
    # FRAGMENTO 11 - plataforma final inferior
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 2560,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -75,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 2715,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -8,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
        # =========================================================
    # CACTUS 1 - círculo izquierdo
    # =========================================================

    # continuacion form 2 
        # =========================================================
    # CACTUS 1
    # Se usa tipo "puas" porque ya está soportado por el motor
    # =========================================================
    # =========================================================
    # CACTUS 2
    # =========================================================
    {
        "tipo": "puas",
        "imagen": "python/cactus.png",
        "x": 2860,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 70,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 20,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 22,
    },

    # =========================================================
    # FRAGMENTO 12 - inferior
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 3070,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -12,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # FRAGMENTO 13 - superior, donde estará la práctica
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 3240,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -100,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # FRAGMENTO 14 - derecho
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 3410,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -70,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 3550,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -15,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "puas",
        "imagen": "python/cactus.png",
        "x": 3200,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 70,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 20,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 22,
    },
     {
        "tipo": "puas",
        "imagen": "python/cactus.png",
        "x": 3330,
        "cantidad": 2,
        "separacion": 60,
        "ancho": 70,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 20,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 22,
    },
    #========================
    # despues del npc 3
        # =========================================================
    # ESPACIO VACÍO
    # Desde el último obstáculo anterior hasta x = 4050
    # =========================================================


    # =========================================================
    # FRAGMENTO 1 - rectángulo horizontal inferior
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4050,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -12,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # COLUMNA 1 - primera columna vertical
    # =========================================================
    {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 4230,
        "ancho": 50,
        "alto": 100,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # COLUMNA 2 - segunda columna vertical
    # =========================================================
    {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 4400,
        "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 7,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 14,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # FRAGMENTO 2 - rectángulo horizontal superior
    # =========================================================
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4490,
        "ancho": 110,
        "alto": 50,
        "ajuste_y": -220,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # COLUMNA 3 - tercera columna vertical
    # =========================================================
    {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 4650,
        "ancho": 85,
        "alto": 225,
        "ajuste_y": -2,

        "hitbox_offset_x": 7,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 14,
        "hitbox_reducir_alto": 8,
    },
    
)

    PRACTICAS = (
        {
        "x": 1375,
        "y": 400,

           "tipo": "seleccion_multiple",
        "pregunta": (
            "\n¿Qué sucederá con el código dentro del ciclo?\n\n"
            "contador = 5\n"
            "while contador < 3:\n"
            "   print(contador)\n"
            
        ),
        "opciones": [
            "Se ejecutará varias veces",
            "Se ejecutará una vez",
            "No se ejecutará",
        ],
        "respuesta_correcta": 3,
        "nombre": "practica_codigo_python_07",
    },
       {
        "x": 2745,
        "y": 450,
        "tipo": "verdadero_falso",
        "pregunta": (
            "¿El ciclo while repite sus instrucciones mientras "
            "su condición sea verdadera?"
        ),
        "respuesta_correcta": True,
        "nombre": "practica_codigo_python_08",
    },
        {
        "x": 3580,
        "y": 450,
        "tipo": "codigo",
        "pregunta": (
            "Arrastra las opciones correctas para completar el código. "
            "Crea un ciclo que muestre los números del 0 al 2."
        ),
        "nombre": "practica_codigo_python_09",
        "respuestas": {
            "ciclo": "while",
            "funcion": "print",
            "aumento": "+=",
        },
        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "contador = 0"},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "ciclo"},
                    {"texto": " contador < 3:"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"hueco": "funcion"},
                    {"texto": "(contador)"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"texto": "contador "},
                    {"hueco": "aumento"},
                    {"texto": " 1"},
                ],
            },
        ],
        "opciones": [
            "while",
            "print",
            "+=",
            "if",
            "input",
            "-=",
        ],
    },
    )


CLASE_NIVEL = NivelPython03


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
