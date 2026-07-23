from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Java'
NIVEL_ACTUAL = 4
FONDO_ACTUAL = 'java'


class NivelJava04(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    CARTEL_FINAL = {
    "x": 5400,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
    }

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 6500
    NPC_X = 825
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
        "nombre": "guia_java_metodos",
        "x": 400,  # Ajusta manualmente
        "ajuste_y": -8,
        "orden_leccion": 10,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    {
        "nombre": "guia_java_parametros",
        "x": 2579,  # Ajusta manualmente
        "ajuste_y": -188,
        "orden_leccion": 11,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 2,
    },
    {
        "nombre": "guia_java_retorno",
        "x": 4520,  # Ajusta manualmente
        "ajuste_y": -8,
        "orden_leccion": 12,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 3,
    },
    )

    ENEMIGOS = (
    # ====================================================
    # ENEMIGO 1: CARACOL
    # Zona inicial, movimiento lento
    # ====================================================
    {
        "tipo": "caracol",
        "x_inicial": 961,
        "x_limite": 1468,
        "ajuste_y": -5,
        "velocidad": 60,
        "ancho": 100,
        "alto": 68,
        "fps_animacion": 6,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },

    # ====================================================
    # ENEMIGO 2: BOLA AZUL
    # Movimiento horizontal medio
    # ====================================================
    {
        "tipo": "bolaazul",
        "x_inicial": 1702,
        "x_limite": 2107,
        "ajuste_y": -5,
        "velocidad": 75,
        "ancho": 100,
        "alto": 72,
        "fps_animacion": 8,
        "hace_dano": True,
        "rebote_al_pisar": -18,
    },

    # ====================================================
    # ENEMIGO 3: JABALÍ
    # Movimiento horizontal rápido
    # ====================================================
    {
        "tipo": "jabali",
        "x_inicial": 2400,
        "x_limite": 3199,
        "ajuste_y": -5,
        "velocidad": 95,
        "ancho": 125,
        "alto": 82,
        "fps_animacion": 8,
        "hace_dano": True,
        "rebote_al_pisar": -22,
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
            "tipo":"volcan",
            "imagen":"java/volcan.png",
            "x": 1571,
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
            "x": 1368,
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
            "x": 1700,
            "ajuste_y": -200,
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
            "x": 2011,
            "ajuste_y": -170,
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
            "x": 2357,
            "ajuste_y": -140,
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
            "x": 2472,
            "ajuste_y": -140,
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
            "x": 2587,
            "ajuste_y": -140,
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
            "x": 2423,
            "ajuste_y": -188,
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
            "x": 2931,
            "ajuste_y": -140,
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
            "x": 3299,
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
            "x": 3365,
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
            "x": 2215,
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
            "x": 2295,
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
            "x": 3643,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
        {
            "tipo":"arco",
            "imagen":"java/arco.png",
            "x": 3699,
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
            "x": 3872,
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
            "x": 3965,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":15,
        },
        {
            "tipo":"arco",
            "imagen":"java/arco.png",
            "x": 4052,
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
            "x": 4400,
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
            "x": 4210,
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
            "x": 4687,
            "ajuste_y": -10,
            "ancho": 200,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            "tipo":"columnas",
            "imagen":"java/columna.png",
            "x": 4859,
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
            "x": 4909,
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
            "x": 5039,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
    )

    PRACTICAS = (
        # ====================================================
    # PRÁCTICA 1: VERDADERO O FALSO
    # Tema: creación y llamada de métodos
    # ====================================================
    {
        "x": 1760,  # Ajusta manualmente
        "y": 267,
        "nombre": "java_n4_p1_metodos",
        "desbloqueada": False,
        "pregunta": (
            "En Java, para ejecutar un método se escribe "
            "su nombre seguido de paréntesis."
        ),
        "respuesta_correcta": True,
    },

    # ====================================================
    # PRÁCTICA 2: ELECCIÓN MÚLTIPLE
    # Tema: parámetros y argumentos
    # ====================================================
    {
        "x": 3517,  # Ajusta manualmente
        "y": None,
        "tipo": "eleccion_multiple",
        "nombre": "java_n4_p2_parametros",
        "desbloqueada": False,
        "pregunta": (
            "¿Cuáles son los parámetros del siguiente método? "
            "mostrarJugador(String nombre, int vidas)"
        ),
        "opciones": [
            "String nombre e int vidas",
            '"Ana" y 5',
            "mostrarJugador",
        ],
        "respuesta_correcta": 1,
    },

    # ====================================================
    # PRÁCTICA 3: COMPLETAR CÓDIGO
    # Tema: retorno de valores
    # ====================================================
    {
        "x": 5199,  # Ajusta manualmente
        "y": None,
        "tipo": "codigo",
        "nombre": "java_n4_p3_retorno",
        "desbloqueada": False,
        "pregunta": (
            "Completa el método que suma dos números "
            "y devuelve el resultado."
        ),
        "respuestas": {
            "tipo_retorno": "int",
            "nombre_metodo": "sumar",
            "devolver": "return",
        },
        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"text": "public static "},
                    {"hueco": "tipo_retorno"},
                    {"texto": " "},
                    {"hueco": "nombre_metodo"},
                    {"texto": "(int a, int b) {"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"hueco": "devolver"},
                    {"texto": " a + b;"},
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
            "int",
            "sumar",
            "return",
            "void",
            "System.out.println",
        ],
    },
    )


CLASE_NIVEL = NivelJava04


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
