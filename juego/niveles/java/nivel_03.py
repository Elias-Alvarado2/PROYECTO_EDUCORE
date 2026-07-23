from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Java'
NIVEL_ACTUAL = 3
FONDO_ACTUAL = 'java'


class NivelJava03(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    CARTEL_FINAL = {
    "x": 3890,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
    }
    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 5000
    NPC_X = 790
    AJUSTE_Y_NPC = -8
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

    PISOS = (
        (0, LONGITUD_NIVEL),
    )

    NPCS = (
    {
        "nombre": "guia_java_while",
        "x": 400,  # Ajusta esta posición
        "ajuste_y": -8,
        "orden_leccion": 7,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    {
        "nombre": "guia_java_for",
        "x": 1923,  # Ajusta esta posición
        "ajuste_y": -328,
        "orden_leccion": 8,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 2,
    },
    {
        "nombre": "guia_java_do_while",
        "x": 3070,  # Ajusta esta posición
        "ajuste_y": -288,
        "orden_leccion": 9,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 3,
    },
    )

    ENEMIGOS = (
    # ====================================================
    # ENEMIGO 1: BOLA AZUL
    # Movimiento horizontal
    # ====================================================
    {
        "tipo": "bolaazul",
        "x_inicial": 1148,
        "x_limite": 1371,
        "ajuste_y": -5,
        "velocidad": 70,
        "ancho": 100,
        "alto": 72,
        "fps_animacion": 8,
        "hace_dano": True,
        "rebote_al_pisar": -18,
    },

    # ====================================================
    # ENEMIGO 2: JABALÍ
    # Movimiento horizontal más rápido
    # ====================================================
    {
        "tipo": "jabali",
        "x_inicial": 1557,
        "x_limite": 1716,
        "ajuste_y": -5,
        "velocidad": 85,
        "ancho": 125,
        "alto": 82,
        "fps_animacion": 8,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },

    # ====================================================
    # ENEMIGO 3: SERPIENTE
    # Movimiento horizontal
    # ====================================================
    {
        "tipo": "serpiente",
        "x_inicial": 1909,
        "x_limite": 2014,
        "ajuste_y": -5,
        "velocidad": 75,
        "ancho": 110,
        "alto": 76,
        "fps_animacion": 7,
        "hace_dano": True,
        "rebote_al_pisar": -18,
    },
    {
        "tipo": "serpiente",
        "x_inicial": 2810,
        "x_limite": 3154,
        "ajuste_y": -5,
        "velocidad": 75,
        "ancho": 110,
        "alto": 76,
        "fps_animacion": 7,
        "hace_dano": True,
        "rebote_al_pisar": -18,
    },
)

    OBSTACULOS = (
        {
            # Varia el tamaño segun nivel o segun se desee
            # Colocar en comentario tamaños de obstaculo
            "tipo":"pico",
            "imagen":"java/pico.png",
            "x": 867,
            "ajuste_y": -5,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":15,
        },
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
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 1048,
            "ajuste_y": -55,
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
            "x": 1271,
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
            "x": 1555,
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
            # Colocar en comentario tamaños de obstaculo
            "tipo":"pico",
            "imagen":"java/pico.png",
            "x": 1479,
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
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 1895,
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
            "x": 1809,
            "ajuste_y": -5,
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
            "x": 2253,
            "ajuste_y": -10,
            "ancho": 50,
            "alto": 100,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":12,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            # Colocar en comentario tamaños de obstaculo
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 2164,
            "ajuste_y": -10,
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
            "x": 2090,
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
            "x": 2300,
            "ajuste_y": -10,
            "ancho": 200,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            "tipo":"arco",
            "imagen":"java/arco.png",
            "x": 2579,
            "ajuste_y": -10,
            "ancho": 200,
            "alto": 100,
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
            "x": 2485,
            "ajuste_y": -10,
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
            "x": 2736,
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
            "x": 2919,
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
            "x": 3049,
            "ajuste_y": -100,
            "ancho": 175,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            "tipo":"columnas",
            "imagen":"java/columna.png",
            "x": 3144,
            "ajuste_y": -149,
            "ancho": 50,
            "alto": 100,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":12,
        },
        {
            # Varia el tamaño segun nivel o segun se desee
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 3049,
            "ajuste_y": -240,
            "ancho": 175,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 2941,
            "ajuste_y": -149,
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
            "tipo":"pico",
            "imagen":"java/pico.png",
            "x": 3270,
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
            "x": 3539,
            "ajuste_y": -5,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":15,
        },
    )

    PRACTICAS = (
      # ====================================================
    # PRÁCTICA 1: VERDADERO O FALSO
    # Tema: ciclo while
    # ====================================================
    {
        "x": 1340,  
        "y": 367,
        "nombre": "java_n3_p1_while",
        "desbloqueada": False,
        "pregunta": (
            "En Java, el ciclo while repite sus instrucciones "
            "mientras su condición sea verdadera."
        ),
        "respuesta_correcta": True,
    },

    # ====================================================
    # PRÁCTICA 2: ELECCIÓN MÚLTIPLE
    # Tema: ciclo for
    # ====================================================
    {
        "x": 2365,  # Ajusta esta posición
        "y": 457,
        "tipo": "eleccion_multiple",
        "nombre": "java_n3_p2_for",
        "desbloqueada": False,
        "pregunta": (
            "¿Qué ciclo es más apropiado cuando conocemos "
            "la cantidad de repeticiones?"
        ),
        "opciones": [
            "for",
            "while",
            "if",
        ],
        "respuesta_correcta": 1,
    },

    # ====================================================
    # PRÁCTICA 3: COMPLETAR CÓDIGO
    # Tema: ciclo do-while
    # ====================================================
    {
        "x": 3420,  # Ajusta esta posición
        "y": None,
        "tipo": "codigo",
        "nombre": "java_n3_p3_do_while",
        "desbloqueada": False,
        "pregunta": (
            "Completa el ciclo que muestra los números del 1 al 5."
        ),
        "respuestas": {
            "inicio": "do",
            "aumento": "numero++",
            "condicion": "while",
        },
        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "int numero = 1;"},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "inicio"},
                    {"texto": " {"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"texto": "System.out.println(numero);"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"hueco": "aumento"},
                    {"texto": ";"},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "} "},
                    {"hueco": "condicion"},
                    {"texto": " (numero <= 5);"},
                ],
            },
        ],
        "opciones": [
            "do",
            "numero++",
            "while",
            "for",
            "numero--",
        ],
    },
    )


CLASE_NIVEL = NivelJava03


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
