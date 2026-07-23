from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'Java'
NIVEL_ACTUAL = 6
FONDO_ACTUAL = 'java'


class NivelJava06(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    ES_PRUEBA_FINAL =True

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
    NPC_X = 895
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
        "nombre": "guia_prueba_final_java",
        "x": 450,  # Ajusta según el espacio de tu nivel
        "ajuste_y": -8,
        "orden_leccion": 16,
        "requiere_anterior": False,
        "repetible": True,

        # Desbloquea las cinco preguntas.
        "practica": (1, 2, 3, 4, 5),
    },
 )

    ENEMIGOS = (
    # ====================================================
    # ENEMIGO 1: JABALÍ
    # Movimiento horizontal rápido
    # ====================================================
    {
        "tipo": "jabali",

        # Ajusta el recorrido según tus obstáculos.
        "x_inicial": 3599,
        "x_limite": 3709,

        "ajuste_y": -5,
        "velocidad": 105,
        "ancho": 125,
        "alto": 82,
        "fps_animacion": 9,
        "hace_dano": True,
        "rebote_al_pisar": -22,
    },

    # ====================================================
    # ENEMIGO 2: FUEGO
    # Movimiento vertical
    # ====================================================
    {
        "tipo": "jabali",
    
        # Ajusta el recorrido según tus obstáculos.
        "x_inicial": 4598,
        "x_limite": 4725,
        "ajuste_y": -5,
        "velocidad": 105,
        "ancho": 125,
        "alto": 82,
        "fps_animacion": 9,
        "hace_dano": True,
        "rebote_al_pisar": -22,
    },

    # ====================================================
    # ENEMIGO 3: BOLA AZUL
    # Movimiento horizontal rápido antes del cartel
    # ====================================================
    {
        "tipo": "bolaazul",

        # Ajusta el recorrido según tu diseño.
        "x_inicial": 4906,
        "x_limite": 5186,

        "ajuste_y": -5,
        "velocidad": 95,
        "ancho": 100,
        "alto": 72,
        "fps_animacion": 10,
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
            # Varia el tamaño segun nivel o segun se desee
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 1655,
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
            "x": 1976,
            "ajuste_y": -250,
            "ancho": 175,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        #----------------------------------------------------------------------
        {
            # Varia el tamaño segun nivel o segun se desee
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 2370,
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
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 2691,
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
            "x": 3012,
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
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 3333,
            "ajuste_y": -100,
            "ancho": 175,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        *(
        {
            "tipo": "pico_ardiente",
            "imagen": "java/pico_ardiente.png",
            "x": 968 + (i * 97),
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 15,
        }
        for i in range(26)
        ),
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 3527,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
        {
            "tipo":"estatua",
            "imagen":"java/estatua.png",
            "x": 3789,
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
            "x": 3977,
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
            "x": 4234,
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
            "tipo":"volcan",
            "imagen":"java/volcan.png",
            "x": 4457,
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
            "x": 4807,
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
            "x": 4862,
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
            "tipo":"plataforma_flotante",
            "imagen":"java/plataforma_flotante.png",
            "x": 5021,
            "ajuste_y": -100,
            "ancho": 175,
            "alto": 60,
            "hitbox_offset_x": 5,
            "hitbox_offset_y": 18,
            "hitbox_reducir_ancho": 10,
            "hitbox_reducir_alto": 18,
        },
        {
            "tipo":"arco",
            "imagen":"java/arco.png",
            "x": 5275,
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
            "x": 5429,
            "ajuste_y": -10,
            "ancho": 100,
            "alto": 60,
            "hitbox_offset_x": 15,
            "hitbox_offset_y": 14,
            "hitbox_reducir_ancho": 35,
            "hitbox_reducir_alto":14,
        },
    )
    #97
    PRACTICAS = (
         # ====================================================
    # PREGUNTA 1: VARIABLES Y TIPOS DE DATOS
    # Verdadero o falso
    # ====================================================
    {
        "x": 1395,  # Ajusta manualmente
        "y": 317,
        "nombre": "java_final_p1_variables",
        "desbloqueada": False,
        "pregunta": (
            "En Java, String se utiliza para guardar texto."
        ),
        "respuesta_correcta": True,
    },

    # ====================================================
    # PREGUNTA 2: CONDICIONALES
    # Elección múltiple
    # ====================================================
    {
        "x": 2745,  # Ajusta manualmente
        "y": 267,
        "tipo": "eleccion_multiple",
        "nombre": "java_final_p2_condicionales",
        "desbloqueada": False,
        "pregunta": (
            "¿Qué estructura permite comprobar otra condición "
            "cuando el primer if es falso?"
        ),
        "opciones": [
            "else if",
            "while",
            "return",
        ],
        "respuesta_correcta": 1,
    },

    # ====================================================
    # PREGUNTA 3: CICLOS
    # Completar código
    # ====================================================
    {
        "x": 4187,  # Ajusta manualmente
        "y": None,
        "tipo": "codigo",
        "nombre": "java_final_p3_ciclos",
        "desbloqueada": False,
        "pregunta": (
            "Completa el ciclo que muestra los números del 1 al 3."
        ),
        "respuestas": {
            "inicio": "1",
            "condicion": "i <= 3",
            "aumento": "i++",
        },
        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "for (int i = "},
                    {"hueco": "inicio"},
                    {"texto": "; "},
                    {"hueco": "condicion"},
                    {"texto": "; "},
                    {"hueco": "aumento"},
                    {"texto": ") {"},
                ],
            },
            {
                "indentacion": 1,
                "segmentos": [
                    {"texto": "System.out.println(i);"},
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
            "1",
            "i <= 3",
            "i++",
            "i >= 3",
            "i--",
        ],
    },

    # ====================================================
    # PREGUNTA 4: MÉTODOS
    # Elección múltiple
    # ====================================================
    {
        "x": 5089,  # Ajusta manualmente
        "y": 367,
        "tipo": "eleccion_multiple",
        "nombre": "java_final_p4_metodos",
        "desbloqueada": False,
        "pregunta": (
            "¿Qué palabra se utiliza para devolver un valor "
            "desde un método?"
        ),
        "opciones": [
            "return",
            "void",
            "static",
        ],
        "respuesta_correcta": 1,
    },

    # ====================================================
    # PREGUNTA 5: ARREGLOS
    # Completar código
    # ====================================================
    {
        "x": 5621,  # Ajusta manualmente
        "y": None,
        "tipo": "codigo",
        "nombre": "java_final_p5_arreglos",
        "desbloqueada": False,
        "pregunta": (
            "Completa el código que obtiene el primer elemento "
            "del arreglo nombres."
        ),
        "respuestas": {
            "tipo": "String[]",
            "indice": "0",
        },
        "codigo": [
            {
                "indentacion": 0,
                "segmentos": [
                    {"hueco": "tipo"},
                    {"texto": ' nombres = {"Ana", "Luis", "Carlos"};'},
                ],
            },
            {
                "indentacion": 0,
                "segmentos": [
                    {"texto": "System.out.println(nombres["},
                    {"hueco": "indice"},
                    {"texto": "]);"},
                ],
            },
        ],
        "opciones": [
            "String[]",
            "0",
            "String",
            "1",
            "int[]",
        ],
    },
    )


CLASE_NIVEL = NivelJava06


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
