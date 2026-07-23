from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = "Java"
NIVEL_ACTUAL = 1

# Debe coincidir con la carpeta dentro de assets/fondos.
# Ejemplo: assets/fondos/java/java_cielo.png
FONDO_ACTUAL = "java"


class NivelJava01(JuegoBase):
    # ========================================================
    # IDENTIFICACIÓN DEL NIVEL
    # ========================================================

    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL

    CARTEL_FINAL = {
    "x": 3890,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
    }
    # ========================================================
    # POSICIÓN DEL JUGADOR
    # ========================================================

    # Mayor = más a la derecha.
    # Menor = más a la izquierda.
    JUGADOR_X_INICIAL = 170

    # Negativo = sube al jugador y las colisiones del nivel.
    # Positivo = los baja.
    AJUSTE_Y_JUGADOR = 0
    AJUSTE_Y_SPRITE_MONTANAS = 10
    # ========================================================
    # AJUSTES VISUALES DEL FONDO
    # ========================================================

    # Solo mueve visualmente el PNG del suelo de este nivel.
    # Positivo = baja. Negativo = sube.
    # No modifica la hitbox.
    AJUSTE_Y_SPRITE_SUELO = 55

    # Solo mueve visualmente la capa de plantas de este nivel.
    # Positivo = baja. Negativo = sube.
    # No modifica hitboxes ni otros objetos.
    AJUSTE_Y_SPRITE_PLANTAS = -41

    # ========================================================
    # CONFIGURACIÓN DEL NIVEL
    # ========================================================

    LONGITUD_NIVEL = 5000

    NPC_X = 720
    AJUSTE_Y_NPC = -8

    PISOS = (
        (0, LONGITUD_NIVEL),
    )

    NPCS = (
    {
        "nombre": "guia_java_variables",
        "x": 350,
        "ajuste_y": -8,
        "orden_leccion": 1,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    {
        "nombre": "guia_java_tipos",
        "x": 1890,
        "ajuste_y": -8,
        "orden_leccion": 2,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 2,
    },
    {
    "nombre": "guia_java_asignacion",
    "x": 2767, 
    "ajuste_y": -52,
    "orden_leccion": 3,
    "requiere_anterior": True,
    "repetible": True,
    "practica": 3,
    },
    )

    ENEMIGOS = (
    {
        "tipo": "caracol",

        # Recorrido horizontal
        # Cambiar segun el diseño
        "x_inicial": 3111,
        "x_limite": 3236,

        # Altura respecto al suelo.
        # Negativo = sube; positivo = baja
        "ajuste_y": -5,

        "velocidad": 55,
        "ancho": 100,
        "alto": 68,
        "fps_animacion": 6,

        # Permite que el jugador pierda una vida al tocarlo de lado
        "hace_dano": True,

        # Salto que recibe el jugador al pisarlo
        "rebote_al_pisar": -20,
    },
    {
        "tipo": "bolaazul",
        "x_inicial": 3547,
        "x_limite": 3768,
        "ajuste_y": -5,
        "velocidad": 65,
        "ancho": 95,
        "alto": 70,
        "fps_animacion": 8,
        "hace_dano": True,
        "rebote_al_pisar": -18,
    },
    {
        "tipo": "serpiente",
        "x_inicial": 1136,
        "x_limite": 1595,
        "ajuste_y": -5,
        "velocidad": 70,
        "ancho": 110,
        "alto": 78,
        "fps_animacion": 7,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
    )

    OBSTACULOS = (
        {
            "tipo":"plataforma",
            "imagen":"java/plataforma.png",
            "x": 955,
            "ajuste_y": -10,
            "ancho": 200,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 1230,
            "ajuste_y": -100,
            "ancho": 175,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 1480,
            "ajuste_y": -190,
            "ancho": 175,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 1230,
            "ajuste_y": -280,
            "ancho": 175,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            # Colocar en comentario tamaños de obstaculo
            "tipo":"pico",
            "imagen":"java/pico.png",
            "x": 1694,
            "ajuste_y": -5,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":15,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            # Colocar en comentario tamaños de obstaculo
            "tipo":"pico",
            "imagen":"java/pico.png",
            "x": 1773,
            "ajuste_y": -5,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":15,
        },
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 1980,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            # Colocar en comentario tamaños de obstaculo
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 2050,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":15,
        },
        {
            "tipo":"columnas",
            "imagen":"java/columna.png",
            "x": 2260,
            "ajuste_y": -10,
            "ancho": 50,
            "alto": 100,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":12,
        },
        {
            "tipo":"arco",
            "imagen":"java/arco.png",
            "x": 2470,
            "ajuste_y": -10,
            "ancho": 200,
            "alto": 100,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 2410,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            "tipo":"volcan",
            "imagen":"java/volcan.png",
            "x": 2295,
            "ajuste_y": -10,
            "ancho": 140,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 2628,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
        {
            "tipo":"plataforma",
            "imagen":"java/plataforma.png",
            "x": 2714,
            "ajuste_y": -10,
            "ancho": 200,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 3038,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            # no borrar este de aca
            "tipo":"volcan",
            "imagen":"java/volcan.png",
            "x": 2900,
            "ajuste_y": -10,
            "ancho": 140,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
       {
            "tipo":"arco",
            "imagen":"java/arco.png",
            "x": 3330,
            "ajuste_y": -10,
            "ancho": 200,
            "alto": 100,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto": 14,
        },
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 3487,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 3639,
            "ajuste_y": -100,
            "ancho": 175,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
    )

    PRACTICAS = (
        {
        "x": 1292,
        "y": 187,
        "nombre": "java_n1_p1_variables",
        "desbloqueada": False,
        "pregunta": (
            "En la declaración int vidas = 5;, "
            "int indica el tipo de dato de la variable."
        ),
        "respuesta_correcta": True,
    },
    {
        "x": 2190,
        "y": None,
        "tipo": "eleccion_multiple",
        "nombre": "java_n1_p2_tipos",
        "desbloqueada": False,
        "pregunta": (
            "¿Qué tipo de dato se utiliza normalmente para "
            "guardar números enteros en Java?"
        ),
        "opciones": [
            "int",
            "String",
            "boolean",
        ],
        "respuesta_correcta": 1,
    },
    {
    "x": 3701,  # posicion para mi practica
    "y": 367,
    "tipo": "codigo",
    "nombre": "java_n1_p3_asignacion",
    "desbloqueada": False,
    "pregunta": "Completa la declaración de una variable de texto.",
    "respuestas": {
        "tipo": "String",
        "variable": "nombre",
        "valor": '"Ana"',
    },
    "codigo": [
        {
            "indentacion": 0,
            "segmentos": [
                {"hueco": "tipo"},
                {"texto": " "},
                {"hueco": "variable"},
                {"texto": " = "},
                {"hueco": "valor"},
                {"texto": ";"},
            ],
        },
    ],
    "opciones": [
        "String",
        "nombre",
        '"Ana"',
        "int",
        "System.out.println",
    ],
},
    )


CLASE_NIVEL = NivelJava01


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
