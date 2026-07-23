from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Java'
NIVEL_ACTUAL = 2
FONDO_ACTUAL = 'java'


class NivelJava02(JuegoBase):
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
    NPC_X = 755
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
        "nombre": "guia_java_if",
        "x": 400,  # Ajusta manualmente
        "ajuste_y": -8,
        "orden_leccion": 4,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    {
        "nombre": "guia_java_if_else",
        "x": 1790,  # Ajusta manualmente
        "ajuste_y": -290,
        "orden_leccion": 5,
        "requiere_anterior": True,
        "repetible": True,
        "practica": 2,
    },
    {
        "nombre": "guia_java_else_if",
        "x": 2800,  # Ajusta manualmente
        "ajuste_y": -102,
        "orden_leccion": 6,
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

        # Ajusta estas posiciones según tu recorrido.
        "x_inicial": 1113,
        "x_limite": 1573,

        "ajuste_y": -5,
        "velocidad": 75,
        "ancho": 120,
        "alto": 80,
        "fps_animacion": 7,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },

    # ====================================================
    # ENEMIGO 2: SERPIENTE
    # Movimiento horizontal
    # ====================================================
    {
        "tipo": "serpiente",

        # Ajusta estas posiciones manualmente.
        "x_inicial": 1779,
        "x_limite": 1937,

        "ajuste_y": -5,
        "velocidad": 65,
        "ancho": 110,
        "alto": 75,
        "fps_animacion": 7,
        "hace_dano": True,
        "rebote_al_pisar": -18,
    },

    {
        "tipo": "serpiente",
   
        # Ajusta estas posiciones manualmente.
        "x_inicial": 2349,
        "x_limite": 2603,
   
        "ajuste_y": -5,
        "velocidad": 65,
        "ancho": 110,
        "alto": 75,
        "fps_animacion": 7,
        "hace_dano": True,
        "rebote_al_pisar": -18,
    },
    )

    OBSTACULOS = (
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 954,
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
            "x": 1159,
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
            "x": 1456,
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
            "x": 1520,
            "ajuste_y": -152,
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
            "x": 1760,
            "ajuste_y": -240,
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
            "x": 1691,
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
            "x": 2032,
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
            "x": 2110,
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
            "x": 2277,
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
            "x": 2454,
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
            "x": 2691,
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
            "x": 2757,
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
            "tipo":"volcan",
            "imagen":"java/volcan.png",
            "x": 2930,
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
            "x": 3055,
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
            "x": 3211,
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
            "x": 3425,
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
            "x": 3454,
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
            "x": 3343,
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
            "x": 1009,
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
         # Tema: if
         # ====================================================
         {
             "x": 1220,  # Ajusta manualmente
             "y": 367,
             "nombre": "java_n2_p1_if",
             "desbloqueada": False,
             "pregunta": (
                 "En Java, el bloque de un if se ejecuta "
                 "solamente cuando su condición es verdadera."
             ),
             "respuesta_correcta": True,
         },
        
         # ====================================================
         # PRÁCTICA 2: ELECCIÓN MÚLTIPLE
         # Tema: if y else
         # ====================================================
         {
             "x": 2183,  # Ajusta manualmente
             "y": 413,
             "tipo": "eleccion_multiple",
             "nombre": "java_n2_p2_if_else",
             "desbloqueada": False,
             "pregunta": (
                 "¿Qué bloque se ejecuta cuando la condición "
                 "del if es falsa?"
             ),
             "opciones": [
                 "else",
                 "if",
                 "boolean",
             ],
             "respuesta_correcta": 1,
         },
        
         # ====================================================
         # PRÁCTICA 3: COMPLETAR CÓDIGO
         # Tema: else if
         # ====================================================
         {
             "x": 3684,  # Ajusta manualmente
             "y": None,
             "tipo": "codigo",
             "nombre": "java_n2_p3_else_if",
             "desbloqueada": False,
             "pregunta": (
                 "Completa la estructura que comprueba varias notas."
             ),
             "respuestas": {
                 "primera_condicion": "if",
                 "segunda_condicion": "else if",
                 "alternativa": "else",
             },
             "codigo": [
                 {
                     "indentacion": 0,
                     "segmentos": [
                         {"hueco": "primera_condicion"},
                         {"texto": " (nota >= 90) {"},
                     ],
                 },
                 {
                     "indentacion": 1,
                     "segmentos": [
                         {"texto": 'System.out.println("Excelente");'},
                     ],
                 },
                 {
                     "indentacion": 0,
                     "segmentos": [
                         {"texto": "} "},
                         {"hueco": "segunda_condicion"},
                         {"texto": " (nota >= 60) {"},
                     ],
                 },
                 {
                     "indentacion": 1,
                     "segmentos": [
                         {"texto": 'System.out.println("Aprobado");'},
                     ],
                 },
                 {
                     "indentacion": 0,
                     "segmentos": [
                         {"texto": "} "},
                         {"hueco": "alternativa"},
                         {"texto": " {"},
                     ],
                 },
                 {
                     "indentacion": 1,
                     "segmentos": [
                         {"texto": 'System.out.println("Reprobado");'},
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
                 "if",
                 "else if",
                 "else",
                 "while",
                 "switch",
             ],
         },
    )


CLASE_NIVEL = NivelJava02


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
