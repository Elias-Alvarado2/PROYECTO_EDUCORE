from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'MySQL'
NIVEL_ACTUAL = 1
FONDO_ACTUAL = 'mysql'


class NivelMySQL01(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170
    
    CARTEL_FINAL = {
    "x": 4000,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
}
    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_SPRITE_SUELO =0
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 5000
    NPC_X = 720
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0

    PISOS = (
        (0, LONGITUD_NIVEL),
    )
    ENEMIGOS=(
    {
        "tipo": "fuego",
        "movimiento": "vertical",
        "x": 600,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -250,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
    {
        "tipo": "fuego",
        "movimiento": "vertical",
        "x": 785,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -250,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
    {
        "tipo": "serpiente",
        # Posiciones relativas al suelo
        "x_inicial": 1230,
        "x_limite": 975,

        "velocidad": 80,
        "ancho": 80,
        "alto": 48,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
    {
        "tipo": "serpiente",
        # Posiciones relativas al suelo
        "x_inicial": 1230,
        "x_limite": 975,

        "velocidad": 80,
        "ancho": 80,
        "alto": 48,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
    {
        "tipo": "fuego",
        "movimiento": "vertical",
        "x": 2540,

        # Posiciones relativas al suelo
        "y_inicial": 0,
        "y_limite": -300,

        "velocidad": 80,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -10,
    },
     {
        "tipo": "jabali",
        # Posiciones relativas al suelo
        "x_inicial": 3845,
        "x_limite": 3290,

        "velocidad": 120,
        "ancho": 100,
        "alto": 68,
        "hace_dano": True,
        "rebote_al_pisar": -20,
    },
     )
    
   

    
    NPCS = (
    {
        "nombre": "pinguino_1",
        "x": 300,
        "ajuste_y": -8,
        "orden_leccion": 1,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    {
        "nombre": "pinguino_2",
        "x": 1660,
        "ajuste_y": -8,
        "orden_leccion": 2,
        "requiere_anterior": True,
        "repetible": True,
        "practicas": (2,3)
    },
    {
        "nombre": "pinguino_3",
        "x": 3500,
        "ajuste_y": -8,
        "orden_leccion": 3,
        "requiere_anterior": True,
        "repetible": True,
    },
    )
    OBSTACULOS =(
        {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 500,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
         {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 700,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
         {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 900,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
        {
            "tipo":"cofre",
            "imagen":"mysql/cofre.png",
            "x": 1300,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 1420,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
        {
            "tipo":"bloque",
            "imagen":"mysql/bloque.png",
            "x": 1530,
            "ajuste_y":-5,
            "ancho": 100,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 1940,
            "ajuste_y":-40,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 2170,
            "ajuste_y":-80,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 2390,
            "ajuste_y":-120,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 2390,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
        {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 2480,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
        {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 2570,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
         {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 2660,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
         {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 2750,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
        {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 2700,
            "ajuste_y":-120,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 2970,
            "ajuste_y":-80,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 3190,
            "ajuste_y":-40,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
    )
    
    PRACTICAS = (
        {
            "x": 1100,
            "y": None,
            "pregunta": 'Una base de datos es un lenguaje de programacion.',
            "respuesta_correcta": False,
            "nombre": "practica_mysql_01",
        },
        {
        "x": 1840,
        "y": None,
        "tipo": "eleccion_multiple",
        "pregunta": (
        "¿Qué instrucción selecciona una base de datos "
        "para comenzar a trabajar en ella?"
        ),
        "opciones": [
            "SELECT",
            "USE",
            "CREATE",
        ],
        "respuesta_correcta": 2,
        "nombre": "mysql_eleccion_02",
        },
        {
            "x": 2730,
            "y": 370,
            "tipo": "codigo",
            "pregunta": (
                "Arrastra las opciones correctas para completar la instruccion "
                "que crea y empieza a usar una base de datos."
            ),
            "nombre": "practica_codigo_mysql_01",
            "respuestas": {
                "crear": "CREATE",
                "base": "DATABASE",
                "usar": "USE",
            },
            "codigo": [
                {   
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "crear"},
                        {"hueco": "base"},
                        {"texto": "educore;"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "usar"},
                        {"texto": " educore;"},
                    ],
                },
            ],
            "opciones": [
                "CREATE",
                "DATABASE",
                "USE",
                "USAR",
                "DABATASE",
                
            ],
        },
    )


    


CLASE_NIVEL = NivelMySQL01


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
