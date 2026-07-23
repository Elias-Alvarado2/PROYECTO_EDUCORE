from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Java'
NIVEL_ACTUAL = 5
FONDO_ACTUAL = 'java'


class NivelJava05(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    CARTEL_FINAL = {
    "x": 5890,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
    }

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 7000
    NPC_X = 860
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
        "nombre": "guia_java_arreglos",
        "x": 400,  # Ajusta manualmente
        "ajuste_y": -8,
        "orden_leccion": 13,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    {
        "nombre": "guia_java_indices",
        "x": 2279,  # Ajusta manualmente
        "ajuste_y": -8,
        "orden_leccion": 14,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 2,
    },
    {
        "nombre": "guia_java_recorrido",
        "x": 4678,  # Ajusta manualmente
        "ajuste_y": -8,
        "orden_leccion": 15,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 3,
    },
    )

    ENEMIGOS = (
    # ====================================================
    # ENEMIGO 1: JABALÍ
    # Movimiento horizontal rápido
    # ====================================================
    {
        "tipo": "jabali",

        # Ajusta estas posiciones según tu diseño.
        "x_inicial": 968,
        "x_limite": 1456,

        "ajuste_y": 0,
        "velocidad": 100,
        "ancho": 125,
        "alto": 82,
        "fps_animacion": 9,
        "hace_dano": True,
        "rebote_al_pisar": -22,
    },
    # ====================================================
    # ENEMIGO 3: SERPIENTE
    # Movimiento horizontal rápido antes del cartel
    # ====================================================
    {
        "tipo": "serpiente",

        # Ajusta estas posiciones según tu recorrido.
        "x_inicial": 1662,
        "x_limite": 2000,

        "ajuste_y": 0,
        "velocidad": 90,
        "ancho": 110,
        "alto": 76,
        "fps_animacion": 9,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
    )

    OBSTACULOS = (
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 889,
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
            "x": 1077,
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
            "x": 1334,
            "ajuste_y": -150,
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
            "x": 1404,
            "ajuste_y": -200,
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
            "x": 1655,
            "ajuste_y": -250,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 2098,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 1559,
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
            "x": 2403,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
        {
            "tipo":"columnas",
            "imagen":"java/columna.png",
            "x": 2471,
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
            "tipo":"volcan",
            "imagen":"java/volcan.png",
            "x": 2534,
            "ajuste_y": -10,
            "ancho": 140,
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
            "x": 2700,
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
            "x": 2989,
            "ajuste_y": -155,
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
            "x": 3104,
            "ajuste_y": -155,
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
            "x": 3115,
            "ajuste_y": -390,
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
            "x": 3439,
            "ajuste_y": -205,
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
            "x": 3819,
            "ajuste_y": -260,
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
            "x": 4149,
            "ajuste_y": -100,
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
            "x": 4002,
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
            "x": 4543,
            "ajuste_y": -10,
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
            "x": 4888,
            "ajuste_y": -100,
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
            "x": 4800,
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
            "x": 5228,
            "ajuste_y": -150,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 2668,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 2765,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 2862,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 2959,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 3056,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 3153,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 3250,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 3347,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 3444,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 3541,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 3638,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 3735,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 4895,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 4992,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 5089,
            "ajuste_y": -10,
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
            "tipo":"pico_ardiente",
            "imagen":"java/pico_ardiente.png",
            "x": 5189,
            "ajuste_y": -10,
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
    # Tema: creación de arreglos
    # ====================================================
    {
        "x": 1720,  # Ajusta manualmente
        "y": 217,
        "nombre": "java_n5_p1_arreglos",
        "desbloqueada": False,
        "pregunta": (
            "En Java, todos los elementos de un arreglo "
            "deben ser del mismo tipo de dato."
        ),
        "respuesta_correcta": True,
    },

    # ====================================================
    # PRÁCTICA 2: ELECCIÓN MÚLTIPLE
    # Tema: índices
    # ====================================================
    {
        "x": 3875,  # Ajusta manualmente
        "y": 207,
        "tipo": "eleccion_multiple",
        "nombre": "java_n5_p2_indices",
        "desbloqueada": False,
        "pregunta": (
            "¿Qué expresión obtiene el primer elemento "
            "del arreglo personajes?"
        ),
        "opciones": [
            "personajes[0]",
            "personajes[1]",
            "personajes.first",
        ],
        "respuesta_correcta": 1,
    },

    # ====================================================
    # PRÁCTICA 3: COMPLETAR CÓDIGO
    # Tema: recorrer un arreglo
    # ====================================================
    {
        "x": 5547,  # Ajusta manualmente
        "y": None,
        "tipo": "codigo",
        "nombre": "java_n5_p3_recorrer_arreglo",
        "desbloqueada": False,
        "pregunta": (
            "Completa el ciclo que recorre y muestra "
            "todos los elementos del arreglo monedas."
        ),
        "respuestas": {
            "inicio": "0",
            "longitud": "monedas.length",
            "elemento": "monedas[i]",
        },
        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "int[] monedas = {5, 10, 15};"},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "for (int i = "},
                    {"hueco": "inicio"},
                    {"texto": "; i < "},
                    {"hueco": "longitud"},
                    {"texto": "; i++) {"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"texto": "System.out.println("},
                    {"hueco": "elemento"},
                    {"texto": ");"},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "}"},
                ],
            },
        ],
        "opciones": [
            "0",
            "monedas.length",
            "monedas[i]",
            "1",
            "monedas",
        ],
    },
)

CLASE_NIVEL = NivelJava05


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
