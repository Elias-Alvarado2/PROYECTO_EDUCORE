from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'MySQL'
NIVEL_ACTUAL = 6
FONDO_ACTUAL = 'mysql'


class NivelMySQL06(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 9500
    NPC_X = 895
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    CARTEL_FINAL = {
    "x": 9300,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
}
    PISOS = (
        (0, LONGITUD_NIVEL),
    )
    OBSTACULOS = (
        # ==========================================================
        # SECCIÓN 1: ENTRADA MIXTA
        # Calentamiento terrestre y subida corta.
        # ==========================================================
        {
            "tipo": "tronco",
            "imagen": "mysql/tronco.png",
            "x": 670,
            "ajuste_y": -5,
            "ancho": 120,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 15,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 20,
        },
        {
            "tipo": "puas",
            "imagen": "mysql/pinchos.png",
            "x": 820,
            "cantidad": 2,
            "separacion": 10,
            "ajuste_y": -5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto": 25,
        },
        {
            "tipo": "bloque",
            "imagen": "mysql/bloque.png",
            "x": 1170,
            "ajuste_y": -5,
            "ancho": 100,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 1180,
            "ajuste_y": -40,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 1280,
            "ajuste_y": -65,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 1470,
            "ajuste_y": -105,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 1690,
            "ajuste_y": -65,
            "ancho": 160,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },

        # ==========================================================
        # SECCIÓN 2: PUENTE SQL SUSPENDIDO
        # Río de pinchos con subida, bajada y plataformas variadas.
        # ==========================================================
        {
            "tipo": "puas",
            "imagen": "mysql/pinchos.png",
            "x": 2050,
            "cantidad": 15,
            "separacion": 10,
            "ajuste_y": -5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto": 25,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 2010,
            "ajuste_y": -45,
            "ancho": 160,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 2210,
            "ajuste_y": -95,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 2410,
            "ajuste_y": -135,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "tronco",
            "imagen": "mysql/tronco.png",
            "x": 2620,
            "ajuste_y": -105,
            "ancho": 150,
            "alto": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 15,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 2820,
            "ajuste_y": -135,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 3030,
            "ajuste_y": -95,
            "ancho": 160,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 3240,
            "ajuste_y": -55,
            "ancho": 160,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },

        # ==========================================================
        # SECCIÓN 3: CORREDOR DE COLUMNAS
        # Obstáculos terrestres con una torre central.
        # ==========================================================
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 3820,
            "ajuste_y": 0,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "puas",
            "imagen": "mysql/pinchos.png",
            "x": 3950,
            "cantidad": 2,
            "separacion": 10,
            "ajuste_y": -5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto": 25,
        },
        {
            "tipo": "bloque",
            "imagen": "mysql/bloque.png",
            "x": 4270,
            "ajuste_y": -5,
            "ancho": 100,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 4280,
            "ajuste_y": -40,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "puas",
            "imagen": "mysql/pinchos.png",
            "x": 4410,
            "cantidad": 2,
            "separacion": 10,
            "ajuste_y": -5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto": 25,
        },
        {
            "tipo": "tronco",
            "imagen": "mysql/tronco.png",
            "x": 4620,
            "ajuste_y": -5,
            "ancho": 120,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 15,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 20,
        },

        # ==========================================================
        # SECCIÓN 4: CORONA AÉREA
        # Conserva el salto hacia atrás y el descenso prolongado.
        # ==========================================================
        {
            "tipo": "puas",
            "imagen": "mysql/pinchos.png",
            "x": 5000,
            "cantidad": 18,
            "separacion": 10,
            "ajuste_y": -5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto": 25,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 4960,
            "ajuste_y": -45,
            "ancho": 160,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 5170,
            "ajuste_y": -95,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 5370,
            "ajuste_y": -135,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 5570,
            "ajuste_y": -175,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
    
        {
            "tipo": "tronco",
            "imagen": "mysql/tronco.png",
            "x": 5830,
            "ajuste_y": -175,
            "ancho": 150,
            "alto": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 12,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 15,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 6040,
            "ajuste_y": -135,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 6260,
            "ajuste_y": -95,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 6480,
            "ajuste_y": -55,
            "ancho": 160,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },

        # ==========================================================
        # SECCIÓN 5: DOBLE RUTA FINAL
        # Conserva la ruta terrestre y la ruta superior.
        # ==========================================================
        {
            "tipo": "tronco",
            "imagen": "mysql/tronco.png",
            "x": 6970,
            "ajuste_y": -5,
            "ancho": 120,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 15,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 20,
        },
    
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 7080,
            "ajuste_y": -70,
            "ancho": 160,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "bloque",
            "imagen": "mysql/bloque.png",
            "x": 7280,
            "ajuste_y": -120,
            "ancho": 140,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "bloque",
            "imagen": "mysql/bloque.png",
            "x": 7410,
            "ajuste_y": -5,
            "ancho": 100,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 7420,
            "ajuste_y": -40,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "puas",
            "imagen": "mysql/pinchos.png",
            "x": 7610,
            "cantidad": 6,
            "separacion": 10,
            "ajuste_y": -5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto": 25,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 7500,
            "ajuste_y": -70,
            "ancho": 160,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 7710,
            "ajuste_y": -120,
            "ancho": 150,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 7930,
            "ajuste_y": -60,
            "ancho": 160,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },

    )

    PRACTICAS = (

        # =========================================================
        # EJERCICIO 1 - VERDADERO O FALSO
        # =========================================================
        {
            "x": 750,
            "y": 470,
            "nombre": "prueba_final_mysql_01",
            "desbloqueada": True,

            "pregunta": (
                "La consulta USE escuela; selecciona la base de datos "
                "llamada escuela."
            ),

            "respuesta_correcta": True,
        },


        # =========================================================
        # EJERCICIO 2 - OPCIÓN MÚLTIPLE
        # =========================================================
        {
            "x": 1300,
            "y": 420,
            "tipo": "eleccion_multiple",
            "nombre": "prueba_final_mysql_02",
            "desbloqueada": True,

            "pregunta": (
                "¿Cuál consulta crea una base de datos llamada tienda?"
            ),

            "opciones": [
                "CREATE DATABASE tienda;",
                "CREATE TABLE tienda;",
                "USE DATABASE tienda;",
            ],

            "respuesta_correcta": 1,
        },


        # =========================================================
        # EJERCICIO 3 - COMPLETAR CÓDIGO
        # =========================================================
        {
            "x": 1850,
            "y": None,
            "tipo": "codigo",
            "nombre": "prueba_final_mysql_03",
            "desbloqueada": True,

            "pregunta": (
                "Completa el código para crear y seleccionar "
                "la base de datos biblioteca."
            ),

            "respuestas": {
                "crear": "CREATE",
                "usar": "USE",
            },

            "codigo": [
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "crear"},
                        {"texto": " DATABASE biblioteca;"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "usar"},
                        {"texto": " biblioteca;"},
                    ],
                },
            ],

            "opciones": [
                "CREATE",
                "USE",
                "SELECT",
                "TABLE",
                "INSERT",
            ],
        },


        # =========================================================
        # EJERCICIO 4 - VERDADERO O FALSO
        # =========================================================
        {
            "x": 2400,
            "y": 350,
            "nombre": "prueba_final_mysql_04",
            "desbloqueada": True,

            "pregunta": (
                "VARCHAR se utiliza para guardar textos como nombres, "
                "correos y direcciones."
            ),

            "respuesta_correcta": True,
        },


        # =========================================================
        # EJERCICIO 5 - OPCIÓN MÚLTIPLE
        # =========================================================
        {
            "x": 2950,
            "y": 350,
            "tipo": "eleccion_multiple",
            "nombre": "prueba_final_mysql_05",
            "desbloqueada": True,

            "pregunta": (
                "¿Qué tipo de dato es más adecuado para guardar "
                "un precio como 49.99?"
            ),

            "opciones": [
                "VARCHAR(20)",
                "DECIMAL(10,2)",
                "DATE",
            ],

            "respuesta_correcta": 2,
        },


        # =========================================================
        # EJERCICIO 6 - COMPLETAR CÓDIGO
        # =========================================================
        {
            "x": 3500,
            "y": None,
            "tipo": "codigo",
            "nombre": "prueba_final_mysql_06",
            "desbloqueada": True,

            "pregunta": (
                "Completa el código para crear la tabla libros."
            ),

            "respuestas": {
                "clave": "PRIMARY KEY",
                "incremento": "AUTO_INCREMENT",
                "texto": "VARCHAR(100)",
                "precio": "DECIMAL(10,2)",
            },

            "codigo": [
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"texto": "CREATE TABLE libros ("},
                    ],
                },
                {
                    "indentacion": 1,
                    "segmentos": [
                        {"texto": "id_libro INT "},
                        {"hueco": "clave"},
                        {"texto": " "},
                        {"hueco": "incremento"},
                        {"texto": ","},
                    ],
                },
                {
                    "indentacion": 1,
                    "segmentos": [
                        {"texto": "titulo "},
                        {"hueco": "texto"},
                        {"texto": " NOT NULL,"},
                    ],
                },
                {
                    "indentacion": 1,
                    "segmentos": [
                        {"texto": "precio "},
                        {"hueco": "precio"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"texto": ");"},
                    ],
                },
            ],

            "opciones": [
                "PRIMARY KEY",
                "AUTO_INCREMENT",
                "VARCHAR(100)",
                "DECIMAL(10,2)",
                "VALUES",
                "WHERE",
            ],
        },


        # =========================================================
        # EJERCICIO 7 - VERDADERO O FALSO
        # =========================================================
        {
            "x": 4050,
            "y": 470,
            "nombre": "prueba_final_mysql_07",
            "desbloqueada": True,

            "pregunta": (
                "Una columna declarada como PRIMARY KEY puede tener "
                "valores repetidos."
            ),

            "respuesta_correcta": False,
        },


        # =========================================================
        # EJERCICIO 8 - OPCIÓN MÚLTIPLE
        # =========================================================
        {
            "x": 4650,
            "y": 470,
            "tipo": "eleccion_multiple",
            "nombre": "prueba_final_mysql_08",
            "desbloqueada": True,

            "pregunta": (
                "¿Cuál consulta inserta correctamente un estudiante "
                "llamado Ana con 16 años?"
            ),

            "opciones": [
                (
                    "INSERT INTO estudiantes (nombre, edad) "
                    "VALUES ('Ana', 16);"
                ),
                (
                    "INSERT estudiantes VALUES "
                    "nombre = 'Ana', edad = 16;"
                ),
                (
                    "ADD INTO estudiantes "
                    "('Ana', 16);"
                ),
            ],

            "respuesta_correcta": 1,
        },


        # =========================================================
        # EJERCICIO 9 - COMPLETAR CÓDIGO
        # =========================================================
        {
            "x": 5150,
            "y": 390,
            "tipo": "codigo",
            "nombre": "prueba_final_mysql_09",
            "desbloqueada": True,

            "pregunta": (
                "Completa la consulta para insertar el producto "
                "Teclado con precio 150.50."
            ),

            "respuestas": {
                "insertar": "INSERT INTO",
                "valores": "VALUES",
            },

            "codigo": [
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "insertar"},
                        {"texto": " productos (nombre, precio)"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "valores"},
                        {"texto": " ('Teclado', 150.50);"},
                    ],
                },
            ],

            "opciones": [
                "INSERT INTO",
                "VALUES",
                "SELECT",
                "WHERE",
                "UPDATE",
                "CREATE",
            ],
        },


        # =========================================================
        # EJERCICIO 10 - VERDADERO O FALSO
        # =========================================================
        {
            "x": 5700,
            "y": 310,
            "nombre": "prueba_final_mysql_10",
            "desbloqueada": True,

            "pregunta": (
                "La cláusula WHERE permite seleccionar únicamente "
                "los registros que cumplen una condición."
            ),

            "respuesta_correcta": True,
        },


        # =========================================================
        # EJERCICIO 11 - OPCIÓN MÚLTIPLE
        # =========================================================
        {
            "x": 6250,
            "y": 390,
            "tipo": "eleccion_multiple",
            "nombre": "prueba_final_mysql_11",
            "desbloqueada": True,

            "pregunta": (
                "¿Cuál consulta muestra estudiantes de 18 años o más "
                "que además tengan estado Activo?"
            ),

            "opciones": [
                (
                    "SELECT * FROM estudiantes "
                    "WHERE edad >= 18 AND estado = 'Activo';"
                ),
                (
                    "SELECT * FROM estudiantes "
                    "WHERE edad >= 18 OR estado = 'Activo';"
                ),
                (
                    "SELECT * FROM estudiantes "
                    "edad >= 18 AND estado = 'Activo';"
                ),
            ],

            "respuesta_correcta": 1,
        },


        # =========================================================
        # EJERCICIO 12 - COMPLETAR CÓDIGO
        # =========================================================
        {
            "x": 6800,
            "y": None,
            "tipo": "codigo",
            "nombre": "prueba_final_mysql_12",
            "desbloqueada": True,

            "pregunta": (
                "Completa la consulta para mostrar productos con precio "
                "menor que 100 o existencia igual a 0."
            ),

            "respuestas": {
                "condicion": "WHERE",
                "comparador": "<",
                "operador": "OR",
            },

            "codigo": [
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"texto": "SELECT * FROM productos"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "condicion"},
                        {"texto": " precio "},
                        {"hueco": "comparador"},
                        {"texto": " 100"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "operador"},
                        {"texto": " existencia = 0;"},
                    ],
                },
            ],

            "opciones": [
                "WHERE",
                "<",
                ">",
                "AND",
                "OR",
                "UPDATE",
            ],
        },


        # =========================================================
        # EJERCICIO 13 - VERDADERO O FALSO
        # =========================================================
        {
            "x": 7350,
            "y": 365,
            "nombre": "prueba_final_mysql_13",
            "desbloqueada": True,

            "pregunta": (
                "La consulta DELETE FROM usuarios; elimina todos "
                "los registros de la tabla usuarios."
            ),

            "respuesta_correcta": True,
        },


        # =========================================================
        # EJERCICIO 14 - OPCIÓN MÚLTIPLE
        # =========================================================
        {
            "x": 7900,
            "y": 425,
            "tipo": "eleccion_multiple",
            "nombre": "prueba_final_mysql_14",
            "desbloqueada": True,

            "pregunta": (
                "¿Cuál consulta elimina solamente al estudiante "
                "cuyo id_estudiante es 4?"
            ),

            "opciones": [
                (
                    "DELETE estudiantes "
                    "WHERE id_estudiante = 4;"
                ),
                (
                    "DELETE FROM estudiantes "
                    "WHERE id_estudiante = 4;"
                ),
                "DELETE FROM estudiantes;",
            ],

            "respuesta_correcta": 2,
        },


        # =========================================================
        # EJERCICIO 15 - COMPLETAR CÓDIGO
        # =========================================================
        {
            "x": 8200,
            "y": None,
            "tipo": "codigo",
            "nombre": "prueba_final_mysql_15",
            "desbloqueada": True,

            "pregunta": (
                "Completa la consulta para cambiar el nombre y el precio "
                "del producto cuyo id_producto es 3."
            ),

            "respuestas": {
                "actualizar": "UPDATE",
                "asignar": "SET",
                "condicion": "WHERE",
            },

            "codigo": [
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "actualizar"},
                        {"texto": " productos"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "asignar"},
                        {"texto": " nombre = 'Mouse inalámbrico',"},
                    ],
                },
                {
                    "indentacion": 1,
                    "segmentos": [
                        {"texto": "precio = 125.00"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "condicion"},
                        {"texto": " id_producto = 3;"},
                    ],
                },
            ],

            "opciones": [
                "UPDATE",
                "SET",
                "WHERE",
                "VALUES",
                "DELETE",
                "SELECT",
            ],
        },


        # =========================================================
        # EJERCICIO 16 - VERDADERO O FALSO
        # =========================================================
        {
            "x": 8400,
            "y": None,
            "nombre": "prueba_final_mysql_16",
            "desbloqueada": True,

            "pregunta": (
                "La consulta UPDATE productos SET precio = 0; modifica "
                "el precio de todos los registros de productos."
            ),

            "respuesta_correcta": True,
        },


        # =========================================================
        # EJERCICIO 17 - OPCIÓN MÚLTIPLE
        # =========================================================
        {
            "x": 8580,
            "y": None,
            "tipo": "eleccion_multiple",
            "nombre": "prueba_final_mysql_17",
            "desbloqueada": True,

            "pregunta": (
                "¿Cuál consulta muestra solamente las columnas nombre "
                "y precio de la tabla productos?"
            ),

            "opciones": [
                "SELECT nombre, precio FROM productos;",
                "SELECT * FROM productos;",
                "SHOW nombre, precio FROM productos;",
            ],

            "respuesta_correcta": 1,
        },


        # =========================================================
        # EJERCICIO 18 - COMPLETAR CÓDIGO
        # =========================================================
        {
            "x": 8760,
            "y": None,
            "tipo": "codigo",
            "nombre": "prueba_final_mysql_18",
            "desbloqueada": True,

            "pregunta": (
                "Completa la consulta para cambiar la existencia a 20 "
                "solamente en el producto cuyo id_producto es 5."
            ),

            "respuestas": {
                "actualizar": "UPDATE",
                "asignar": "SET",
                "condicion": "WHERE",
            },

            "codigo": [
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "actualizar"},
                        {"texto": " productos"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "asignar"},
                        {"texto": " existencia = 20"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "condicion"},
                        {"texto": " id_producto = 5;"},
                    ],
                },
            ],

            "opciones": [
                "UPDATE",
                "SET",
                "WHERE",
                "VALUES",
                "DELETE",
                "SELECT",
            ],
        },


        # =========================================================
        # EJERCICIO 19 - VERDADERO O FALSO
        # =========================================================
        {
            "x": 8940,
            "y": None,
            "nombre": "prueba_final_mysql_19",
            "desbloqueada": True,

            "pregunta": (
                "Una columna definida con NOT NULL no permite guardar "
                "un valor nulo."
            ),

            "respuesta_correcta": True,
        },


        # =========================================================
        # EJERCICIO 20 - OPCIÓN MÚLTIPLE
        # =========================================================
        {
            "x": 9120,
            "y": None,
            "tipo": "eleccion_multiple",
            "nombre": "prueba_final_mysql_20",
            "desbloqueada": True,

            "pregunta": (
                "¿Cuál consulta elimina únicamente los usuarios cuyo "
                "estado es Inactivo?"
            ),

            "opciones": [
                (
                    "DELETE FROM usuarios "
                    "WHERE estado = 'Inactivo';"
                ),
                "DELETE FROM usuarios;",
                "REMOVE usuarios WHERE estado = 'Inactivo';",
            ],

            "respuesta_correcta": 1,
        },

    )


CLASE_NIVEL = NivelMySQL06


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()