from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Python'
NIVEL_ACTUAL = 4
FONDO_ACTUAL = 'python'


class NivelPython04(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 6500
    NPC_X = 825
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
        "x": 700,
        "ajuste_y": -8,
        "orden_leccion": 10,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
     {
        "nombre": "pinguino_1",
        "x": 2600,
        "ajuste_y": -115,
        "orden_leccion": 11,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 2,
    },
      {
        "nombre": "pinguino_1",
        "x": 4200,
        "ajuste_y": -8,
        "orden_leccion": 12,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 3,
    },
    
)

    OBSTACULOS = (
    # =========================================================
    # COLUMNA 1
    # Primer rectángulo vertical
    # =========================================================
    {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 850,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -25,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
    {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 950,
        "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # HUESOS 1
    # Primer fuego de la referencia
    # =========================================================
    {
        "tipo": "huesos",
        "imagen": "python/huesos.png",
        "x": 1045,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 10,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 20,
        "hitbox_reducir_alto": 20,
    },
      {
        "tipo": "huesos",
        "imagen": "python/huesos.png",
        "x": 1145,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -8,

        "hitbox_offset_x": 10,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 20,
        "hitbox_reducir_alto": 20,
    },
     {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 1030,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -150,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
  

    # =========================================================
    # COLUMNA 2
    # Segunda columna, un poco más alta
    # =========================================================
   

    # =========================================================
    # HUESOS 2
    # Segundo fuego de la referencia
    # =========================================================
    {
        "tipo": "huesos",
        "imagen": "python/huesos.png",
        "x": 1265,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 10,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 20,
        "hitbox_reducir_alto": 20,
    },
     {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 1230,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -150,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },

    # =========================================================
    # FRAGMENTO FLOTANTE
    # Rectángulo horizontal
    # =========================================================
 

    # =========================================================
    # COLUMNA 3
    # Columna cercana al fragmento
    # =========================================================
    {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 1345,
        "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "huesos",
        "imagen": "python/huesos.png",
        "x": 1427,
        "ancho": 55,
        "alto": 50,
        "ajuste_y": -8,
         "cantidad": 3,
         "separacion": 70,
        "hitbox_offset_x": 10,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 20,
        "hitbox_reducir_alto": 20,
    },

    # =========================================================
    # PÚAS
    # Círculo de la referencia
    # =========================================================
   {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 1780,
        "ancho": 60,
        "alto": 130,
        "ajuste_y": -2,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
  
    {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 1430,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -190,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 1540,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -160,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
       {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 1660,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -120,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 1850,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -35,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
        {
        "tipo": "puas",
        "imagen": "python/cactus.png",
        "x": 1950,
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
        "x": 2250,
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
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 2400,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -35,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
        {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 2500,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -65,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
         {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 2600,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -90,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 2700,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -55,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
         {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 2800,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -25,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
    {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 3135,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -25,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 3250,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -80,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 3350,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -25,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
    {
  "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 3250,
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
 {
  "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 3650,
        "cantidad": 2,
        "separacion": 150,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
    {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 4350,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -10,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
    {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 4465,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -35,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 4560,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -70,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
    {
      "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 4600,
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

     {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 4700,
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
        "x": 4800,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -150,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
    {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 4900,
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
        "x": 4765,
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
     {
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 5000,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -150,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 5150,
        "ancho": 80,
        "alto": 45,
        "ajuste_y": -80,

        "hitbox_offset_x": 6,
        "hitbox_offset_y": 4,
        "hitbox_reducir_ancho": 12,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "columnas",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 5300,
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
        "x": 5100,
        "cantidad": 2,
        "separacion": 50,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -2,

        "hitbox_offset_x": 12,
        "hitbox_offset_y": 18,
        "hitbox_reducir_ancho": 24,
        "hitbox_reducir_alto": 20,
    },
  
)

    PRACTICAS = (
    # ====================================================
    # PRÁCTICA 1: VERDADERO O FALSO
    # ====================================================
    {
        "x": 1700,
        "y": 345,
        "tipo": "verdadero_falso",
        "pregunta": (
            "Observa el siguiente código:\n\n"
            "def saludar():\n"
            '    print("Hola")\n\n'
            "¿La palabra def se utiliza para crear una función?"
        ),
        "respuesta_correcta": True,
        "nombre": "python_funciones_vf_01",
    },

    # ====================================================
    # PRÁCTICA 2: SELECCIÓN MÚLTIPLE
    # ====================================================
    {
        "x": 2700,
        "y": None,
        "tipo": "eleccion_multiple",
        "pregunta": (
            "¿Cuál de las siguientes instrucciones ejecuta correctamente "
            "una función llamada saludar?"
        ),
        "opciones": [
            "saludar()",
            "def saludar",
            "print saludar",
        ],
        "respuesta_correcta": 1,
        "nombre": "python_funciones_multiple_02",
    },

    # ====================================================
    # PRÁCTICA 3: COMPLETAR CÓDIGO
    # ====================================================
    {
        "x": 4000,
        "y": None,
        "tipo": "codigo",
        "pregunta": (
            "Arrastra las opciones correctas para completar el código. "
            "Crea y ejecuta una función que muestre el mensaje Hola."
        ),
        "nombre": "python_funciones_codigo_03",
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
            "input",
            "while",
        ],
    },
)


CLASE_NIVEL = NivelPython04


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
