from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'MySQL'
NIVEL_ACTUAL = 2
FONDO_ACTUAL = 'mysql'


class NivelMySQL02(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 5500
    NPC_X = 755
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    CARTEL_FINAL = {
    "x": 4400,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
}
    PISOS = (
        (0, LONGITUD_NIVEL),
    )

    NPCS = (
    {
        "nombre": "pinguino_1",
        "x": 300,
        "ajuste_y": -8,
        "orden_leccion": 4,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    {
        "nombre": "pinguino_2",
        "x": 1750,
        "ajuste_y": -225,
        "orden_leccion": 5,
        "requiere_anterior": True,
        "repetible": True,
        "practica": (2,3),
    },
    {
        "nombre": "pinguino_3",
        "x": 2850,
        "ajuste_y": -8,
        "orden_leccion": 6,
        "requiere_anterior": True,
        "repetible": True,
        "practica": (4,5),
    },
    {
        "nombre": "pinguino_4",
        "x": 3700,
        "ajuste_y": -8,
        "orden_leccion": 7,
        "requiere_anterior": True,
        "repetible": True,
        "practica": (6),
    },

    )

    OBSTACULOS = (
        {
            "tipo":"bloque",
            "imagen":"mysql/bloque.png",
            "x": 800,
            "ajuste_y":-5,
            "ancho": 100,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"cofre",
            "imagen":"mysql/cofre.png",
            "x": 820,
            "ajuste_y":-30,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 570,
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
            "x": 1050,
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
            "x": 1400,
            "ajuste_y":-160,
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
            "x": 1750,
            "ajuste_y":-200,
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
            "x": 2010,
            "cantidad": 3,
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
            "x": 2080,
            "ajuste_y":-60,
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
            "x": 2550,
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
            "tipo":"tronco",
            "imagen":"mysql/tronco.png",
            "x": 3000,
            "ajuste_y":-5,
            "ancho": 120,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 15,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":20,
        },
        {
            "tipo":"puas",
            "imagen":"mysql/pinchos.png",
            "x": 3120,
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
            "x": 3225,
            "ajuste_y":-5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto":25,
        },
         {
            "tipo":"tronco",
            "imagen":"mysql/tronco.png",
            "x": 3300,
            "ajuste_y":-5,
            "ancho": 120,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 15,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":20,
        },
         {
            "tipo":"bloque",
            "imagen":"mysql/bloque.png",
            "x": 3850,
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
            "x": 4000,
            "ajuste_y":-60,
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
    "x": 610,
    "y": 385,
    "tipo": "ejemplo",
    "pregunta": "Observa esta tabla como ejemplo.",
    "imagen": "mysql/tabla_ejemplo1.png",
    "ancho": 750,
    "alto": 350,
    "nombre": "ejemplo_tabla_usuarios",
    },
    {
        "x": 2120,
        "y": 430,
        "tipo": "eleccion_multiple",
        "pregunta": (
        "¿Qué tipo de dato almacena numeros enteros? "
        ),
        "opciones": [
            "INT",
            "VARCHAR",
            "DATE",
        ],
        "respuesta_correcta": 1,
        "nombre": "mysql_eleccion_01",
        },
    {
            "x": 2430,
            "y": None,
            "tipo": "codigo",
            "pregunta": (
                "Arrastra las opciones correctas para completar la instruccion "
                "que crea una tabla."
            ),
            "nombre": "practica_codigo_mysql_01",
            "respuestas": {
                "tabla": "TABLE",
                "par": "(",
                "id":"id_estudiante",
                "varchar":"VARCHAR(50)"
            },
            "codigo": [
                {   
                    "indentacion": 0,
                    "segmentos": [
                        {"texto": "CREATE "},
                        {"hueco": "tabla"},
                        {"texto": " estudiantes "},
                        {"hueco": "par"}
                    ],
                },
                {
                    "indentacion": 1,
                    "segmentos": [
                        {"hueco": "id"},
                        {"texto": " INT,"},
                    ],
                },
                {
                    "indentacion": 1,
                    "segmentos": [
                        {"texto": "nombre "},
                        {"hueco": "varchar"},
                    ],
                },
                {
                    "indentacion": 1,
                    "segmentos": [
                        {"texto": ");"},
                    ],
                },
            ],
            "opciones": [
                "TABLE",
                "(",
                "id_estudiante",
                "USAR",
                "INT",
                "VARCHAR(50)",
                
            ],
        },
        {
        "x": 3450,
        "y": None,
        "tipo": "eleccion_multiple",
        "pregunta": (
        "¿Qué valores tendrá el campo id INT AUTO_INCREMENT PRIMARY KEY? "
        ),
        "opciones": [
            "1,2,3...",
            "2,5,4...",
            "10,15,20...",
        ],
        "respuesta_correcta": 1,
        "nombre": "mysql_eleccion_01",
        },
        {
            "x": 3500,
            "y": None,
            "pregunta": 'Cuando usamos PRIMARY KEY pueden haber dos registros con la misma Clave primaria.',
            "respuesta_correcta": False,
            "nombre": "practica_mysql_01",
        },
        {
            "x": 4040,
            "y": 440,
            "pregunta": '¿El siguiente campo puede quedar vacio? \n edad INT NOT NULL',
            "respuesta_correcta": False,
            "nombre": "practica_mysql_01",
        },
    )


CLASE_NIVEL = NivelMySQL02


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
