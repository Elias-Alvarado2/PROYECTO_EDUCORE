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
    PISOS = (
        (0, LONGITUD_NIVEL),
    )
    NPCS = (
    {
        "nombre": "pinguino_1",
        "x": 640,
        "ajuste_y": -130,
        "orden_leccion": 4,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 13,
    },
     {
        "nombre": "pinguino_1",
        "x": 3225,
        "ajuste_y": -115,
        "orden_leccion": 5,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 14,
    },
      {
        "nombre": "pinguino_1",
        "x": 4200,
        "ajuste_y": -8,
        "orden_leccion": 6,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 15,
    },
       {
        "nombre": "pinguino_1",
        "x": 4200,
        "ajuste_y": -8,
        "orden_leccion": 6,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 16,
    },
       {
        "nombre": "pinguino_1",
        "x": 4200,
        "ajuste_y": -8,
        "orden_leccion": 6,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 17,
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

        # Parte superior izquierda
        {
              "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2420,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -275,

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
            "ajuste_y": -275,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },

        # Primer escalón de bajada
        {
              "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 2680,
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
            "ajuste_y": -165,

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
            "ajuste_y": -110,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },

        # Último escalón
        {
              "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento2.png",
            "x": 3070,
            "ancho": 100,
            "alto": 42,
            "ajuste_y": -55,

            "hitbox_offset_x": 6,
            "hitbox_offset_y": 5,
            "hitbox_reducir_ancho": 12,
            "hitbox_reducir_alto": 9,
        },
    )

    PRACTICAS = (
        # ====================================================
    # PREGUNTA 1: VARIABLES Y TIPOS DE DATOS
    # VERDADERO O FALSO
    # ====================================================
    {
        "numero": 1,
        "tipo": "verdadero_falso",
        "pregunta": (
            "Observa el siguiente código:\n\n"
            'nombre = "Ana"\n\n'
            "¿La variable nombre guarda un texto?"
        ),
        "respuesta_correcta": True,
        "tema": "Variables y tipos de datos",
        "nombre": "prueba_python_vf_01",
    },

    # ====================================================
    # PREGUNTA 2: CONDICIONALES
    # SELECCIÓN MÚLTIPLE
    # ====================================================
    {
        "numero": 2,
        "tipo": "eleccion_multiple",
        "pregunta": (
            "Observa el siguiente código:\n\n"
            "edad = 16\n\n"
            "if edad >= 18:\n"
            '    print("Mayor de edad")\n'
            "else:\n"
            '    print("Menor de edad")\n\n'
            "¿Qué mensaje mostrará el programa?"
        ),
        "opciones": [
            "Mayor de edad",
            "Menor de edad",
            "No muestra ningún mensaje",
        ],
        "respuesta_correcta": 2,
        "tema": "Condicionales",
        "nombre": "prueba_python_multiple_02",
    },

    # ====================================================
    # PREGUNTA 3: CICLOS
    # SELECCIÓN MÚLTIPLE
    # ====================================================
    {
        "numero": 3,
        "tipo": "eleccion_multiple",
        "pregunta": (
            "Observa el siguiente código:\n\n"
            "contador = 0\n\n"
            "while contador < 3:\n"
            "    print(contador)\n"
            "    contador += 1\n\n"
            "¿Qué valores mostrará el programa?"
        ),
        "opciones": [
            "0, 1 y 2",
            "1, 2 y 3",
            "0, 1, 2 y 3",
        ],
        "respuesta_correcta": 1,
        "tema": "Ciclos",
        "nombre": "prueba_python_multiple_03",
    },

    # ====================================================
    # PREGUNTA 4: FUNCIONES
    # COMPLETAR CÓDIGO
    # ====================================================
    {
        "numero": 4,
        "tipo": "codigo",
        "pregunta": (
            "Arrastra las opciones correctas para completar el código. "
            "Crea y ejecuta una función llamada saludar."
        ),
        "tema": "Funciones",
        "nombre": "prueba_python_codigo_04",
        "respuestas": {
            "definicion": "def",
            "funcion": "print",
            "llamada": "saludar",
        },
        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "definicion"},
                    {"texto": " saludar():"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"hueco": "funcion"},
                    {"texto": '("Hola")'},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "llamada"},
                    {"texto": "()"},
                ],
            },
        ],
        "opciones": [
            "def",
            "print",
            "saludar",
            "if",
            "while",
            "input",
        ],
    },

    # ====================================================
    # PREGUNTA 5: LISTAS
    # COMPLETAR CÓDIGO
    # ====================================================
    {
        "numero": 5,
        "tipo": "codigo",
        "pregunta": (
            "Arrastra las opciones correctas para completar el código. "
            "Agrega uva a la lista y muestra todos sus elementos."
        ),
        "tema": "Listas",
        "nombre": "prueba_python_codigo_05",
        "respuestas": {
            "metodo": "append",
            "funcion": "print",
        },
        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": 'frutas = ["manzana", "pera"]'},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "frutas."},
                    {"hueco": "metodo"},
                    {"texto": '("uva")'},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "funcion"},
                    {"texto": "(frutas)"},
                ],
            },
        ],
        "opciones": [
            "append",
            "print",
            "remove",
            "input",
            "while",
            "if",
        ],
    },
)
    


CLASE_NIVEL = NivelPython06


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
