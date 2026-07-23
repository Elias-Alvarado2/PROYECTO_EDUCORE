from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Python'
NIVEL_ACTUAL = 5
FONDO_ACTUAL = 'python'


class NivelPython05(JuegoBase):
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
    NPC_X = 860
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 2
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    ENEMIGOS=(
         {
        "tipo": "fuego",
        "movimiento": "vertical",
        "x": 946,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -250,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -10,
    },
     {
        "tipo": "fuego",
        "movimiento": "vertical",
        "x": 1185,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -250,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -10,
    },
     {
            
        "tipo": "bolaazul",
        "x_inicial": 2504,
        "x_limite": 2667    ,
        "ajuste_y": 0,
        "ancho": 100,
        "alto": 68,
        "velocidad": 120,
        "hace_dano": True,
        "rebote_al_pisar": -20,
        "fps_animacion":8,

        },
          {      
        "tipo": "caracol",
        "x_inicial": 3975,
        "x_limite": 4100,
        "ajuste_y": 0,
        "ancho": 100,
        "alto": 68,
        "velocidad": 60,
        "hace_dano": True,
        "rebote_al_pisar": -20,
        "fps_animacion":6,

        },
         {
             
        "tipo": "serpiente",
        # Posiciones relativas al suelo
        "x_inicial": 4930,
        "x_limite": 5011,
        "ajuste_y": -240,
        "velocidad": 80,
        "ancho": 80,
        "alto": 48,
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
        "x": 600,
        "ajuste_y": -8,
        "orden_leccion": 13,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
     {
        "nombre": "pinguino_2",
        "x": 2247,
        "ajuste_y": -85,
        "orden_leccion": 14,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 2,
    },
      {
        "nombre": "pinguino_3",
        "x": 4200,
        "ajuste_y": -8,
        "orden_leccion": 15,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 3,
    },
        )
    CARTEL_FINAL = (
        {
    "x": 6000,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
    }
)
    

    OBSTACULOS = (
           {
    "tipo": "puas",
        "imagen": "python/puas_obstaculo.png",
        "x": 400,
        "cantidad": 1,
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
        "x": 850,
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
        "imagen": "python/puas_obstaculo.png",
        "x": 970,
        "cantidad": 1,
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
        "x": 1080,
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
        "imagen": "python/puas_obstaculo.png",
        "x": 1200,
        "cantidad": 1,
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
        "x": 1300,
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
        "x": 1450,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -70,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,     
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 1560,
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
        "x": 1400,
        "cantidad": 1,
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
        "x": 1600,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -140,
        "cantidad": 4,
        "separacion": 60,
        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
       {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 1671,
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
        "x": 1851,
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
        "x": 2000,
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
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 2249,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -60,
        "cantidad": 1,
        "separacion": 60,
        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
    {
        "tipo": "arena",
        "imagen": "python/arena.png",
        "x": 2431,
        "ancho": 100,
        "alto": 30,
        "ajuste_y": -37,
        "cantidad": 1,
        "separacion": 60,
        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
         {
    "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 2194,
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
        "x": 2370,
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
        "imagen": "python/columnas.png",
        "x": 3265,
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
        "x": 2760,
        "cantidad": 2,
        "separacion": 170,
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
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 3140,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -15,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 3396,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -15,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
      {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 3482,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -50,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
       {
        "tipo": "puas",
        "imagen": "python/huesos.png",
        "x": 2370,
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
        "imagen": "python/columnas.png",
        "x": 3788,
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
        "x": 3561,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -100,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
       {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 3655,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -150,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
       {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento.png",
        "x": 3901,
        "ancho": 100,
        "alto": 35,
        "ajuste_y": -15,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
       {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4345,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -35,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
          {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4460,
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
        "x": 4580,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -80,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4720,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -100,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4800,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -180,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
        {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 4950,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -200,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
        {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 5092,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -170,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
    
        {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 5241,
        "ancho": 100,
        "alto": 50,
        "ajuste_y": -150,

        "hitbox_offset_x": 4,
        "hitbox_offset_y": 3,
        "hitbox_reducir_ancho": 8,
        "hitbox_reducir_alto": 8,
    },
     {
        "tipo": "columnas",
        "imagen": "python/columnas.png",
        "x": 5355,
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
    "x": 4456,
    "ancho": 55,
    "alto": 50,
    "ajuste_y": -2,
    "cantidad": 8,
    "separacion": 60,
    "hitbox_offset_x": 7,
    "hitbox_offset_y": 4,
    "hitbox_reducir_ancho": 14,
    "hitbox_reducir_alto": 8,
},
       {
        "tipo": "fragmento",
        "imagen": "python/obstaculo_fragmento2.png",
        "x": 5457,
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
        "x": 5695,
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
    

    )

    PRACTICAS = (
        {
            "x": 1630,
            "y": 350,
            "tipo": "verdadero_falso",
        "pregunta": (
            "Observa el siguiente código:\n\n"
            'frutas = ["manzana", "pera", "uva"]\n\n'
            "¿La variable frutas contiene una lista de tres elementos?"
        ),
        "respuesta_correcta": True,
        "nombre": "python_listas_vf_01",
    },
     {
        "x": 3935,
        "y": 450,
        "tipo": "eleccion_multiple",
        "pregunta": (
            "Observa el siguiente código:\n"
            'frutas = ["manzana", "pera", "uva"]\n'
            "print(frutas[0])\n"
            "¿Qué elemento mostrará el programa?"
        ),
        "opciones": [
            "manzana",
            "pera",
            "uva",
        ],
        "respuesta_correcta": 1,
        "nombre": "python_listas_multiple_02",
    },

    # ====================================================
    # PRÁCTICA 3: COMPLETAR CÓDIGO
    # ====================================================
    {
        "x": 4976,
        "y": 261,
        "tipo": "codigo",
        "pregunta": (
            "Arrastra las opciones correctas para completar el código. "
            "Agrega uva al final de la lista y después muestra la lista."
        ),
        "nombre": "python_listas_codigo_03",
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


CLASE_NIVEL = NivelPython05


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
