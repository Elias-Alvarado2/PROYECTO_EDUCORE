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
    PISOS = (
        (0, LONGITUD_NIVEL),
    )
    NPCS = (
    {
        "nombre": "pinguino_1",
        "x": 600,
        "ajuste_y": -8,
        "orden_leccion": 4,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
     {
        "nombre": "pinguino_1",
        "x": 3225,
        "ajuste_y": -115,
        "orden_leccion": 5,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 2,
    },
      {
        "nombre": "pinguino_1",
        "x": 4200,
        "ajuste_y": -8,
        "orden_leccion": 6,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 3,
    },
    
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
        "x": 3159,
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
        "x": 3587,
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
        "tipo": "puas",
        "imagen": "python/cactus.png",
        "x": 3400,
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
            "x": 1580,
            "y": None,
            "pregunta": 'En Python, una variable sirve para almacenar un dato que puede utilizarse después.',
            "respuesta_correcta": True,
            "nombre": "practica_python_05",
        },
    )


CLASE_NIVEL = NivelPython05


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
