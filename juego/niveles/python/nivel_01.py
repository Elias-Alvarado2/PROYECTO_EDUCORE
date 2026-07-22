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
    LONGITUD_NIVEL = 7000
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
        "x": 2940,
        "ajuste_y": -130,
        "orden_leccion": 2,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 2,
    },
    {
        "nombre": "pinguino_3",
        "x": 4510,
        "ajuste_y": -8,
        "orden_leccion": 3,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 3,
    },
         {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 5524,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -30,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
         {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 5635,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -55,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
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
            "hitbox_offset_y": 8,
        },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1080,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -75,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
        },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1210,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -115,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
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
            "hitbox_offset_y": 8,
        },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 1470,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -25,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
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
            "ancho": 100,
            "alto": 45,
            "ajuste_y": -20,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
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

    "ancho": 100,
    "alto": 45,

    # Más abajo, casi a nivel del suelo
    "ajuste_y": -20,

    "hitbox_offset_x": 4,
    "hitbox_offset_y": 8,
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

    "ancho": 100,
    "alto": 45,

    # Más abajo, casi a nivel del suelo
    "ajuste_y": -20,

    "hitbox_offset_x": 4,
    "hitbox_offset_y": 8,
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

    "ancho": 100,
    "alto": 45,

    # Más arriba que el primero
    "ajuste_y": -85,

    "hitbox_offset_x": 4,
    "hitbox_offset_y": 8,
    "hitbox_reducir_ancho": 8,
    "hitbox_reducir_alto": 0,
},

    # Túmulo colocado después de los fragmentos
   
      {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 2973,
            "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 3144,
            "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 3287,
            "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
 {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 3390,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -100,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
        },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 3550,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -100,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
        },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 3710,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -100,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
        },
        {
            "tipo": "fragmento",
            "imagen": "python/obstaculo_fragmento.png",
            "x": 3924,
            "ancho": 100,
            "alto": 35,
            "ajuste_y": -100,
            "hitbox_offset_x": 4,
            "hitbox_offset_y": 8,
        },
                  {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 3871,
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
        "x": 3050,
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
        "x": 3215,
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
            "x": 3427,
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
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4050,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -40,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
          {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 4380,
            "ancho": 95,
            "alto": 50,
            "cantidad": 2,
            "separacion":230,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },
               {
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4170,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -20,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
              {
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4861,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -20,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 4987,
            "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 5095,
            "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
             {
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 5190,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -20,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
      {
            "tipo": "puas",
            "imagen": "python/puas_obstaculo.png",
            "x": 5423,
            "ancho": 95,
            "alto": 50,
            "cantidad": 2,
            "separacion":200,
            "ajuste_y": 8,
            "hitbox_offset_x": 8,
            "hitbox_offset_y": 20,
            "hitbox_reducir_ancho": 16,
            "hitbox_reducir_alto": 24,
        },
    )
    PRACTICAS = (
        {
            "x": 2685,
            "y": 370,
            "pregunta": 'La variable siguiente guarda un número entero:'
            'cantidad = 10',
            "respuesta_correcta": True,
            "nombre": "practica_python_01",
        },
         {
        "x": 3960,
        "y": 370,
        "tipo": "eleccion_multiple",
        "pregunta": (
        "¿Qué tipo de información guarda la variable 'nombre'?\n"
        """nombre = 'Ana'"""
        ),
        "opciones": [
            "Un número entero",
            "Un texto",
            "Un valor verdadero o falso",
        ],
        "respuesta_correcta": 2,
        "nombre": "practica_codigo_python_02",
        },
       {
    "x": 5605,
    "y": 500,
    "tipo": "codigo",
    "pregunta": (
        "Arrastra las opciones correctas para completar el código. "
        "Crea una variable llamada edad que guarde el número 15."
    ),
    "nombre": "practica_codigo_python_03",
    "respuestas": {
        "variable": "edad",
        "valor": "15",
    },
    "codigo": [
        {
            "indentacion": 0,
            "segmentos": [
                {"hueco": "variable"},
                {"texto": " = "},
                {"hueco": "valor"},
            ],
        },
    ],
    "opciones": [
        "nombre",
        "edad",
        '"15"',
        "15",
    ],
},
    )


CLASE_NIVEL = NivelPython01


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
