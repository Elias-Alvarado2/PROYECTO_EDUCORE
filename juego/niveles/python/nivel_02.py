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

    LONGITUD_NIVEL = 7000

    NPC_X = 755
    AJUSTE_Y_NPC = -8

    AJUSTE_Y_SPRITE_MONTANAS = 2
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    ENEMIGOS=(
        {
             
        "tipo": "serpiente",
        # Posiciones relativas al suelo
        "x_inicial": 683,
        "x_limite": 963,

        "velocidad": 80,
        "ancho": 80,
        "alto": 48,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
      {      
        "tipo": "caracol",
        "x_inicial": 1613,
        "x_limite": 1765,
        "ajuste_y": 0,
        "ancho": 100,
        "alto": 68,
        "velocidad": 60,
        "hace_dano": True,
        "rebote_al_pisar": -20,
        "fps_animacion":6,

        },
         {
        "tipo": "fuego",
        "movimiento": "vertical",
        "x": 3120,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -200,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -10,
    },
        {
        "tipo": "jabali",
        # Posiciones relativas al suelo
        "x_inicial": 4843,
        "x_limite": 5280,

        "velocidad": 120,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
    )
    PISOS = (
        (0, LONGITUD_NIVEL),
    )

    NPCS = (
    {
        "nombre": "pinguino_1",
        "x": 355,
        "ajuste_y": -8,
        "orden_leccion": 4,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
     {
        "nombre": "pinguino_2",
        "x": 3225,
        "ajuste_y": -115,
        "orden_leccion": 5,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 2,
    },
      {
        "nombre": "pinguino_3",
        "x": 4419,
        "ajuste_y": -93,
        "orden_leccion": 6,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 3,
    },
            )
    CARTEL_FINAL = (
        {
    "x": 5400,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,}
    
)

    # ========================================================
    # OBSTÁCULOS
    # ========================================================

    OBSTACULOS = (
        # ========================================================
        # FRAGMENTO 1: ABAJO
        # ========================================================
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
          {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 1217,
        "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
           {
        "tipo": "puas",
        "imagen": "python/cactus.png",
        "x": 2567,
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

        # ========================================================
        # FRAGMENTO 2: MÁS ARRIBA
        # ========================================================
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1391,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -115,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 8,
        },

        # ========================================================
        # PRIMERAS PÚAS
        # ========================================================
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

        # ========================================================
        # SEGUNDAS PÚAS
        # ========================================================
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

        # ========================================================
        # FRAGMENTO SUPERIOR IZQUIERDO
        # ========================================================
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 1950,
            "ancho": 100,
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
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # ========================================================
        # PÚAS DESPUÉS DEL FRAGMENTO INFERIOR
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
        # FRAGMENTO SUPERIOR
        # ========================================================
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2200,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -110,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 8,
        },

        # ========================================================
        # FRAGMENTO A LA DERECHA
        # ========================================================
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2350,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # ========================================================
        # ESPACIO PARA CAMINAR
        # La siguiente sección comienza más adelante.
        # ========================================================

        # Fragmento bajo izquierdo
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 2830,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # Púas del lado izquierdo
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 2950,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },

        # Fragmento alto izquierdo
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 2970,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -85,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # Púas del centro
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 3120,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },

        # Fragmento alto derecho, donde estará el NPC
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 3240,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -85,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # Púas debajo del NPC
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 3270,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },

        # Fragmento bajo derecho
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 3390,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },
                # ========================================================
        # PÚAS DESPUÉS DE LA ÚLTIMA SECCIÓN
        # ========================================================

        # Púas 1: debajo de la roca
        {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 3650,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },
                # ========================================================
        # TÚMULOS DESPUÉS DE LA ÚNICA PÚA
        # ========================================================

        # Túmulo 1: abajo
        {
               "tipo": "arena",
        "imagen": "python/arena.png",
            "x": 3800,
            "ancho": 100,
            "alto": 25,
            "ajuste_y": 0,
            "hitbox_offset_x": 3,
            "hitbox_offset_y": 2,
            "hitbox_reducir_ancho": 6,
            "hitbox_reducir_alto": 2,
        },

         {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 3900,
        "ancho": 100,
        "alto": 25,
        "ajuste_y": -30,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

        # Túmulo 3: abajo
        {
            "tipo": "arena",
        "imagen": "python/arena.png",
            "x": 4000,
            "ancho": 100,
            "alto": 25,
            "ajuste_y": 0,
            "hitbox_offset_x": 3,
            "hitbox_offset_y": 2,
            "hitbox_reducir_ancho": 6,
            "hitbox_reducir_alto": 2,
        },
         # ========================================================
        # FRAGMENTO 1: ABAJO
        # Después de los tres túmulos
        # ========================================================
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 4350,
            "ancho": 90,
            "alto": 35,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # ========================================================
        # FRAGMENTO 2: MÁS ARRIBA
        # ========================================================
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 4430,
            "ancho": 90,
            "alto": 35,
            "ajuste_y": -60,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },

        # ========================================================
        # PÚAS DESPUÉS DE LOS DOS FRAGMENTOS
     
     
          {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 613,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },
               {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 1539,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -40,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
        {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 1290,
        "cantidad": 2,
        "separacion": 70,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 4573,
            "ancho": 100,
            "alto": 35,
            "cantidad": 2,
            "separacion": 100,
            "ajuste_y": -15,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 0,
        },
             {
        "tipo": "puas",
        "imagen": "python/cactus.png",
        "x": 4010,
        "cantidad": 1,
        "separacion": 0,
        "ancho": 70,
        "alto": 50,
        "ajuste_y": -25,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 20,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 22,
    },
          {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 4680,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },
              
    )
    # ========================================================
    # PRÁCTICAS
    # ========================================================

    PRACTICAS = (
      {
        "x": 2000,
        "y": 320,
        "tipo": "verdadero_falso",
        "pregunta": (
            '¿El siguiente código mostrará el mensaje "Mayor de edad"?\n\n'
            'edad = 20\n'
            'if edad >= 18:\n'
            '    print("Mayor de edad")'
        ),
        "respuesta_correcta": True,
        "nombre": "practica_python_04",
    },
      {
        "x": 3830,
        "y": 500,
        "tipo": "eleccion_multiple",
        "pregunta": (
        "¿Qué mensaje muestra este código?\n"
        "edad = 12\n"
        'if edad >= 18:\n'
        '    print("Mayor de edad")\n'
        'else:'
        '    print("Menor de edad")\n'
        
        ),
        "opciones": [
            "No muestra ningún mensaje",
            "Mayor de edad",
            "Menor de edad",
            
        ],
        "respuesta_correcta": 3,
        "nombre": "practica_codigo_python_05",
        },
        {
    "x": 4450,
    "y": 430,
    "tipo": "codigo",
    "pregunta": (
        "Arrastra las opciones correctas para completar el código. "
        "Comprueba si la edad es mayor o igual que 18 y muestra "
        "el mensaje correspondiente."
    ),
    "nombre": "practica_codigo_python_06",
    "respuestas": {
        "condicional": "if",
        "funcion": "print",
        "alternativa": "else",
    },
    "codigo": [
        {
            "indentacion": 0,
            "segmentos": [
                {"texto": "edad = 18"},
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
        {
            "indentacion": 0,
            "segmentos": [
                {"hueco": "alternativa"},
                {"texto": ":"},
            ],
        },
        {
            "indentacion": 1,
            "segmentos": [
                {"texto": 'print("Menor de edad")'},
            ],
        },
    ],
    "opciones": [
        "if",
        "print",
        "else",
        "while",
        "input",
        "elif",
    ],
},
    )


CLASE_NIVEL = NivelPython02


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()