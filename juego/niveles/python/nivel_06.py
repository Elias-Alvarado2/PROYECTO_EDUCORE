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
    AJUSTE_Y_SPRITE_MONTANAS = 2
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    CARTEL_FINAL = (
        {
    "x": 9300,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
    }
)
    PISOS = (
        (0, LONGITUD_NIVEL),
    )
    ENEMIGOS=(
         {      
        "tipo": "caracol",
        "x_inicial": 894,
        "x_limite": 1115,
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
        "x": 1311,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -100,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -10,
    },
    {
        "tipo": "fuego",
        "movimiento": "vertical",
        "x": 2400,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -300,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -10,
    },
    {
        "tipo": "fuego",
        "movimiento": "vertical",
        "x": 2650,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -300,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -10,
    },
     {
        "tipo": "jabali",
        # Posiciones relativas al suelo
        "x_inicial": 3300,
        "x_limite": 3416,

        "velocidad": 140,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
     {
             
        "tipo": "serpiente",
        # Posiciones relativas al suelo
        "x_inicial": 4263,
        "x_limite": 4400,
        "ajuste_y": 0,
        "velocidad": 80,
        "ancho": 80,
        "alto": 48,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
    {
        "tipo": "fuego",
        "movimiento": "vertical",
        "x": 4822,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -300,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -10,
    },
    )
    NPCS = (
        {
            "nombre": "pinguino_1",
            "x": 640,
            "ajuste_y": -130,
            "orden_leccion": 4,
            "requiere_anterior": False,
            "repetible": False,

            # Al terminar el diálogo, este único NPC desbloquea
            # las diez prácticas de la prueba final.
            "practicas": (
                1, 2, 3, 4, 5,
                6, 7, 8, 9, 10,
            ),
        },
    )

    OBSTACULOS = (
        {
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 565,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -8,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
          {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 671,
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
            "imagen": "python/puas_obstaculo.png",
            "x": 750,
            "ancho": 95,
            "alto": 50,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },
         {
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 845,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -8,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
           {
        "tipo": "puas",
        "imagen": "python/cactus.png",
        "x": 350,
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
       # Primer escalón
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 1900,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -55,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },

        # Segundo escalón
        {  "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2030,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -110,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },

        {
              "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 1784,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -15,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },
           {
                    "tipo": "puas",
                    "imagen": "python/puas_obstaculo.png",
                    "x": 2010,
                    "ancho": 95,
                    "alto": 50,
                    "cantidad": 3,
                    "separacion":50,
                    "ajuste_y": 8,
                    "hitbox_offset_x": 8,
                    "hitbox_offset_y": 20,
                    "hitbox_reducir_ancho": 16,
                    "hitbox_reducir_alto": 24,
                },
                                  {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 2474,
        "cantidad": 1,
        "separacion": 150,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
         
                      
      
                                                      {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 2738,
        "cantidad": 1,
        "separacion": 150,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
             {
                        "tipo": "puas",
                        "imagen": "python/puas_obstaculo.png",
                        "x": 2900,
                        "ancho": 95,
                        "alto": 50,
                        "cantidad": 2,
                        "separacion":50,
                        "ajuste_y": 8,
                        "hitbox_offset_x": 8,
                        "hitbox_offset_y": 20,
                        "hitbox_reducir_ancho": 16,
                        "hitbox_reducir_alto": 24,
                    },
                          {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 2600,
        "cantidad": 1,
        "separacion": 150,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
        # Tercer escalón
        {
              "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2160,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -165,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },

        # Cuarto escalón
        {
              "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2290,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -220,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },


        # Parte superior derecha
        {
              "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2550,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -220,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },


        # Segundo escalón de bajada
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2810,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -220,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },

        # Tercer escalón de bajada
        {
              "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2940,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -150,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },
        {
              "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 3070,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -65,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },
          # Último escalón
                {
                      "tipo": "fragmento",
                    "imagen": "python/obstaculo_fragmento2.png",
                    "x": 3230,
                    "ancho": 100,
                    "alto": 42,
                    "ajuste_y": -30,
        
                    "hitbox_offset_x": 6,
                    "hitbox_offset_y": 5,
                    "hitbox_reducir_ancho": 12,
                    "hitbox_reducir_alto": 9,
                },
               {
                "tipo": "arena",
                "imagen": "python/arena.png",
                "x": 1200,
                "ancho": 100,
                "alto": 30,
                "ajuste_y": -15,
        
                "hitbox_offset_x": 4,
                "hitbox_offset_y": 3,
                "hitbox_reducir_ancho": 8,
                "hitbox_reducir_alto": 8,
            },
           {
            "tipo": "arena",
            "imagen": "python/arena.png",
            "x": 1440,
            "ancho": 100,
            "alto": 30,
            "ajuste_y": -30,
    
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 3,
            "hitbox_reducir_ancho": 8,
            "hitbox_reducir_alto": 8,
        },
              {
            "tipo": "puas",
            "imagen": "python/cactus.png",
            "x": 1620,
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
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 3501,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -8,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
                  {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 3620,
        "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,
        "cantidad": 4,
        "separacion": 90,
        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },   
                                      {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 3850,
        "cantidad": 1,
        "separacion": 150,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
                                      {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 3716,
        "cantidad": 1,
        "separacion": 150,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
                                      {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 4015,
        "cantidad": 1,
        "separacion": 150,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
       {
            "tipo": "columnas",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 4215,
            "ancho": 80,
            "alto": 45,
            "ajuste_y": -8,
    
            "hitbox_offset_x": 6,
            "hitbox_offset_y": 4,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 8,
        },
             {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 4487,
            "ancho": 95,
            "alto": 50,
            "cantidad": 4,
            "separacion": 130,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },
             {
                "tipo": "fragmento",
                "imagen": "python/obstaculo_fragmento.png",
                "x": 5441,
                "ancho": 100,
                "alto": 30,
                "ajuste_y": -35,
                "cantidad": 4,
                "separacion": 100,
                "hitbox_offset_x": 4,
                "hitbox_offset_y": 3,
                "hitbox_reducir_ancho": 8,
                "hitbox_reducir_alto": 8,
            },
          {
        "tipo": "puas",
        "imagen": "python/cactus.png",
        "x": 5560,
        "cantidad": 3,
        "separacion": 130,
        "ancho": 70,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 20,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 22,
    },
       
    )

    PRACTICAS = (
    # ====================================================
    # PREGUNTA 1: CICLOS
    # SELECCIÓN MÚLTIPLE
    # ====================================================
    {
        "numero": 1,
        "x": 1475,
        "ajuste_y": -50,

        "tipo": "eleccion_multiple",
        "tema": "Ciclos",
        "nombre": "prueba_python_multiple_01",

        "pregunta": (
            "Observa el siguiente código:\n"
            "for numero in range(1, 4):\n"
            "    print(numero)\n"
            "¿Qué valores mostrará el programa?"
        ),

        "opciones": [
            "1, 2 y 3",
            "0, 1, 2 y 3",
            "1, 2, 3 y 4",
        ],

        # Las respuestas de selección múltiple comienzan en 1.
        "respuesta_correcta": 1,
    },

    # ====================================================
    # PREGUNTA 2: VARIABLES Y TIPOS DE DATOS
    # VERDADERO O FALSO
    # ====================================================
    {
        "numero": 2,
        "x": 2065,
        "ajuste_y": -150,

        "tipo": "verdadero_falso",
        "tema": "Variables y tipos de datos",
        "nombre": "prueba_python_vf_02",

        "pregunta": (
            "Observa el siguiente código:\n"
            "dato = 20\n"
            'dato = "Python"\n'
            "¿Python permite que una variable cambie el tipo "
            "de dato que almacena?"
        ),

        "respuesta_correcta": True,
    },

    # ====================================================
    # PREGUNTA 3: FUNCIONES
    # COMPLETAR CÓDIGO
    # ====================================================
    {
        "numero": 3,
        "x": 2585,
        "ajuste_y": -250,

        "tipo": "codigo",
        "tema": "Funciones",
        "nombre": "prueba_python_codigo_03",

        "pregunta": (
            "Arrastra las opciones correctas para completar una función "
            "que sume dos números y muestre el resultado."
        ),

        "respuestas": {
            "definicion": "def",
            "retorno": "return",
            "mostrar": "print",
        },

        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "definicion"},
                    {"texto": " sumar(a, b):"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"hueco": "retorno"},
                    {"texto": " a + b"},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "mostrar"},
                    {"texto": "(sumar(2, 3))"},
                ],
            },
        ],

        "opciones": [
            "def",
            "return",
            "print",
            "if",
            "while",
            "input",
        ],
    },

    # ====================================================
    # PREGUNTA 4: LISTAS
    # SELECCIÓN MÚLTIPLE
    # ====================================================
    {
        "numero": 4,
        "x": 3100,
        "ajuste_y": -80,

        "tipo": "eleccion_multiple",
        "tema": "Listas",
        "nombre": "prueba_python_multiple_04",

        "pregunta": (
            "Observa el siguiente código:\n"
            'colores = ["rojo", "verde", "azul"]\n'
            "print(colores[1])\n"
            "¿Qué valor mostrará el programa?"
        ),

        "opciones": [
            "rojo",
            "verde",
            "azul",
        ],

        "respuesta_correcta": 2,
    },

    # ====================================================
    # PREGUNTA 5: CONDICIONALES
    # VERDADERO O FALSO
    # ====================================================
    {
        "numero": 5,
        "x": 3636,
        "ajuste_y": -130,

        "tipo": "verdadero_falso",
        "tema": "Condicionales",
        "nombre": "prueba_python_vf_05",

        "pregunta": (
            "Observa el siguiente código:\n"
            "nota = 70\n"
            "if nota >= 60:\n"
            '    print("Aprobado")\n'
            "else:\n"
            '    print("Reprobado")\n'
            "¿El programa mostrará Aprobado?"
        ),

        "respuesta_correcta": True,
    },

    # ====================================================
    # PREGUNTA 6: VARIABLES Y TIPOS DE DATOS
    # SELECCIÓN MÚLTIPLE
    # ====================================================
    {
        "numero": 6,
        "x": 3935,
        "ajuste_y": -130,

        "tipo": "eleccion_multiple",
        "tema": "Variables y tipos de datos",
        "nombre": "prueba_python_multiple_06",

        "pregunta": (
            "Observa la siguiente variable:\n"
            "precio = 15.50\n"
            "¿Qué tipo de dato almacena la variable precio?"
        ),

        "opciones": [
            "int",
            "float",
            "str",
        ],

        "respuesta_correcta": 2,
    },

    # ====================================================
    # PREGUNTA 7: CICLOS
    # COMPLETAR CÓDIGO
    # ====================================================
    {
        "numero": 7,
        "x": 4640,
        "ajuste_y": -8,

        "tipo": "codigo",
        "tema": "Ciclos",
        "nombre": "prueba_python_codigo_07",

        "pregunta": (
            "Arrastra las opciones correctas para crear un ciclo "
            "que muestre los números 0, 1 y 2."
        ),

        "respuestas": {
            "ciclo": "for",
            "secuencia": "range",
            "mostrar": "print",
        },

        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "ciclo"},
                    {"texto": " numero in "},
                    {"hueco": "secuencia"},
                    {"texto": "(3):"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"hueco": "mostrar"},
                    {"texto": "(numero)"},
                ],
            },
        ],

        "opciones": [
            "for",
            "range",
            "print",
            "if",
            "input",
            "return",
        ],
    },

    # ====================================================
    # PREGUNTA 8: LISTAS
    # VERDADERO O FALSO
    # ====================================================
    {
        "numero": 8,
        "x": 5093,
        "ajuste_y": -30,

        "tipo": "verdadero_falso",
        "tema": "Listas",
        "nombre": "prueba_python_vf_08",

        "pregunta": (
            "Observa el siguiente código:\n"
            'animales = ["gato", "perro"]\n'
            'animales.append("pato")\n'
            "¿El método append agrega pato al final de la lista?"
        ),

        "respuesta_correcta": True,
    },

    # ====================================================
    # PREGUNTA 9: CONDICIONALES
    # COMPLETAR CÓDIGO
    # ====================================================
    {
        "numero": 9,
        "x": 5480,
        "ajuste_y": -35,

        "tipo": "codigo",
        "tema": "Condicionales",
        "nombre": "prueba_python_codigo_09",

        "pregunta": (
            "Arrastra las opciones correctas para completar una decisión "
            "que determine si una persona es mayor o menor de edad."
        ),

        "respuestas": {
            "condicion": "if",
            "alternativa": "else",
            "mostrar": "print",
        },

        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "edad = 15"},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "condicion"},
                    {"texto": " edad >= 18:"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"texto": 'mensaje = "Mayor de edad"'},
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
                    {"texto": 'mensaje = "Menor de edad"'},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "mostrar"},
                    {"texto": "(mensaje)"},
                ],
            },
        ],

        "opciones": [
            "if",
            "else",
            "print",
            "for",
            "return",
            "append",
        ],
    },

    # ====================================================
    # PREGUNTA 10: FUNCIONES
    # SELECCIÓN MÚLTIPLE
    # ====================================================
    {
        "numero": 10,
        "x": 6095,
        "ajuste_y": -30,

        "tipo": "eleccion_multiple",
        "tema": "Funciones",
        "nombre": "prueba_python_multiple_10",

        "pregunta": (
            "Observa el siguiente código:\n"
            "def multiplicar(a, b):\n"
            "    return a * b\n"
            "resultado = multiplicar(4, 2)\n"
            "¿Qué valor se guardará en resultado?"
        ),

        "opciones": [
            "6",
            "8",
            "42",
        ],

        "respuesta_correcta": 2,
    },
)
    


CLASE_NIVEL = NivelPython06


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()