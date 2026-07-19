from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'MySQL'
NIVEL_ACTUAL = 4
FONDO_ACTUAL = 'mysql'


class NivelMySQL04(JuegoBase):
    # Cada archivo conserva su propia configuracion.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequenos.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR = 0
    LONGITUD_NIVEL = 6900
    NPC_X = 825
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    CARTEL_FINAL = {
    "x": 5700,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
}
    PISOS = (
        (0, LONGITUD_NIVEL),
    )

    # La lección 4 se divide en cuatro diálogos breves. Cada pingüino aparece
    # en el orden del recorrido y desbloquea solamente las prácticas del tema
    # que acaba de explicar.
    NPCS = (
        {
            'nombre': 'pinguino_where',
            'x': 400,
            'ajuste_y': -8,
            'orden_leccion': 10,
            'requiere_anterior': False,
            'repetible': True,
            'practicas': (1, 2),
        },
        {
            'nombre': 'pinguino_comparadores',
            'x': 2030,
            # Esta plataforma usa ajuste_y=-115. Los 30 puntos adicionales
            # apoyan correctamente los pies del NPC sobre su superficie.
            'ajuste_y': -145,
            'orden_leccion': 11,
            'requiere_anterior': True,
            'repetible': True,
            'practicas': (3, 4),
        },
        {
            'nombre': 'pinguino_and',
            'x': 3700,
            'ajuste_y': -80,
            'orden_leccion': 12,
            'requiere_anterior': True,
            'repetible': True,
            'practicas': (5, 6),
        },
        {
            'nombre': 'pinguino_not',
            'x': 4730,
            'ajuste_y': -270,
            'orden_leccion': 13,
            'requiere_anterior': True,
            'repetible': True,
            'practicas': (7, 8),
        },
    )

    OBSTACULOS = (
        # ACTO 1: CAMINO DE APRENDIZAJE
        # Todos los obstaculos estan escritos completos, igual que en los
        # niveles anteriores. Los espacios de paso son de 120 y 130 unidades.
        {
            'tipo': 'puas',
            'imagen': 'mysql/pinchos.png',
            'x': 930,
            'ajuste_y': -5,
            'ancho': 80,
            'alto': 50,
            'hitbox_offset_x': 25,
            'hitbox_offset_y': 30,
            'hitbox_reducir_ancho': 45,
            'hitbox_reducir_alto': 25,
        },
        {
            'tipo': 'cofre',
            'imagen': 'mysql/cofre.png',
            'x': 1130,
            'ajuste_y': -5,
            'ancho': 80,
            'alto': 50,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'puas',
            'imagen': 'mysql/pinchos.png',
            'x': 1340,
            'ajuste_y': -5,
            'ancho': 80,
            'alto': 50,
            'hitbox_offset_x': 25,
            'hitbox_offset_y': 30,
            'hitbox_reducir_ancho': 45,
            'hitbox_reducir_alto': 25,
        },

        # La practica en x=1500 queda libre. Este bloque y cofre forman el
        # altar que prepara el primer recorrido aereo.
        {
            'tipo': 'bloque',
            'imagen': 'mysql/bloque.png',
            'x': 1680,
            'ajuste_y': -5,
            'ancho': 100,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'cofre',
            'imagen': 'mysql/cofre.png',
            'x': 1690,
            'ajuste_y': -41,
            'ancho': 80,
            'alto': 50,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },

        # ACTO 2: TORRE DE RETORNO
        # Los pinchos son la unica configuracion que usa cantidad.
        {
            'tipo': 'puas',
            'imagen': 'mysql/pinchos.png',
            'x': 1880,
            'cantidad': 14,
            'separacion': 10,
            'ajuste_y': -5,
            'ancho': 80,
            'alto': 50,
            'hitbox_offset_x': 25,
            'hitbox_offset_y': 30,
            'hitbox_reducir_ancho': 45,
            'hitbox_reducir_alto': 25,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 1800,
            'ajuste_y': -60,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 2030,
            'ajuste_y': -115,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },

        # Primer salto hacia atras: x=2030 -> x=1910.
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 2250,
            'ajuste_y': -170,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },

        # Segundo salto hacia atras: x=2050 -> x=1930.
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 2400,
            'ajuste_y': -250,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },

        # Descenso aereo.
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 2700,
            'ajuste_y': -300,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'cofre',
            'imagen': 'mysql/cofre.png',
            'x': 3100,
            'ajuste_y': -221,
            'ancho': 40,
            'alto': 25,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 3400,
            'ajuste_y': -155,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 3900,
            'ajuste_y': -100,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 3700,
            'ajuste_y': -50,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },

        # ACTO 3: CORREDOR TERRESTRE
        # El personaje mas ancho mide 89.3 unidades. Aqui todos los espacios
        # de paso o aterrizaje miden entre 100 y 110 unidades.
        {
            'tipo': 'tronco',
            'imagen': 'mysql/tronco.png',
            'x': 3230,
            'ajuste_y': -5,
            'ancho': 120,
            'alto': 50,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 15,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 20,
        },
        {
            'tipo': 'puas',
            'imagen': 'mysql/pinchos.png',
            'x': 3450,
            'cantidad': 2,
            'separacion': 10,
            'ajuste_y': -5,
            'ancho': 80,
            'alto': 50,
            'hitbox_offset_x': 25,
            'hitbox_offset_y': 30,
            'hitbox_reducir_ancho': 45,
            'hitbox_reducir_alto': 25,
        },

        {
            'tipo': 'puas',
            'imagen': 'mysql/pinchos.png',
            'x': 3920,
            'ajuste_y': -5,
            'ancho': 80,
            'alto': 50,
            'hitbox_offset_x': 25,
            'hitbox_offset_y': 30,
            'hitbox_reducir_ancho': 45,
            'hitbox_reducir_alto': 25,
        },
        {
            'tipo': 'bloque',
            'imagen': 'mysql/bloque.png',
            'x': 4110,
            'ajuste_y': -5,
            'ancho': 100,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'cofre',
            'imagen': 'mysql/cofre.png',
            'x': 4120,
            'ajuste_y': -41,
            'ancho': 80,
            'alto': 50,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },

        # ACTO 4: GANCHO AEREO
        {
            'tipo': 'puas',
            'imagen': 'mysql/pinchos.png',
            'x': 4320,
            'cantidad': 10,
            'separacion': 10,
            'ajuste_y': -5,
            'ancho': 80,
            'alto': 50,
            'hitbox_offset_x': 25,
            'hitbox_offset_y': 30,
            'hitbox_reducir_ancho': 45,
            'hitbox_reducir_alto': 25,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 4250,
            'ajuste_y': -60,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 4460,
            'ajuste_y': -125,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },

        # Tercer salto hacia atras: x=4480 -> x=4360.
        {
            'tipo': 'cofre',
            'imagen': 'mysql/cofre.png',
            'x': 4250,
            'ajuste_y': -210,
            'ancho': 40,
            'alto': 25,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 4500,
            'ajuste_y': -240,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 4730,
            'ajuste_y': -240,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'cofre',
            'imagen': 'mysql/cofre.png',
            'x': 4900,
            'ajuste_y': -196,
            'ancho': 40,
            'alto': 25,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 5050,
            'ajuste_y': -130,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
        {
            'tipo': 'fragmento',
            'imagen': 'mysql/plataforma.png',
            'x': 5280,
            'ajuste_y': -60,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
    )

    PRACTICAS = (
        # WHERE -------------------------------------------------------------
        {
            'x': 700,
            'y': None,
            'pregunta': (
                'WHERE se escribe después de FROM y filtra las filas que '
                'cumplen una condición.'
            ),
            'respuesta_correcta': True,
            'nombre': 'mysql_04_where_verdadero_falso',
        },
        {
            'x': 1560,
            'y': None,
            'tipo': 'codigo',
            'pregunta': (
                'Completa la consulta que muestra a los estudiantes de grado '
                'Tercero.'
            ),
            'nombre': 'mysql_04_where_codigo',
            'respuestas': {
                'campos': '*',
                'tabla': 'estudiantes',
                'where': 'WHERE',
                'condicion': "grado = 'Tercero';",
            },
            'codigo': [
                {
                    'indentacion': 0,
                    'segmentos': [
                        {'texto': 'SELECT '},
                        {'hueco': 'campos'},
                        {'texto': ' FROM '},
                        {'hueco': 'tabla'},
                    ],
                },
                {
                    'indentacion': 0,
                    'segmentos': [
                        {'hueco': 'where'},
                        {'texto': ' '},
                        {'hueco': 'condicion'},
                    ],
                },
            ],
            'opciones': [
                '*',
                'nombre',
                'estudiantes',
                'cursos',
                'WHERE',
                'ORDER BY',
                "grado = 'Tercero';",
                "grado <> 'Tercero';",
            ],
        },

        # OPERADORES DE COMPARACIÓN ----------------------------------------
        {
            'x': 2425,
            'y': 245,
            'tipo': 'eleccion_multiple',
            'pregunta': '¿Qué registros selecciona WHERE edad >= 15?',
            'opciones': [
                'Estudiantes de 15 años o más.',
                'Estudiantes con mas de 15 años.',
                'Estudiantes de 15 años.',
            ],
            'respuesta_correcta': 1,
            'nombre': 'mysql_04_comparadores_eleccion',
        },
        {
            'x': 2745,
            'y': 195,
            'tipo': 'codigo',
            'pregunta': (
                'Completa la consulta que muestra el nombre de estudiantes '
                'menores de 18 años.'
            ),
            'nombre': 'mysql_04_comparadores_codigo',
            'respuestas': {
                'campo': 'nombre',
                'where': 'WHERE',
                'operador': '<',
                'limite': '18;',
            },
            'codigo': [
                {
                    'indentacion': 0,
                    'segmentos': [
                        {'texto': 'SELECT '},
                        {'hueco': 'campo'},
                        {'texto': ' FROM estudiantes'},
                    ],
                },
                {
                    'indentacion': 0,
                    'segmentos': [
                        {'hueco': 'where'},
                        {'texto': ' edad '},
                        {'hueco': 'operador'},
                        {'hueco': 'limite'},
                    ],
                },
            ],
            'opciones': [
                'nombre',
                '*',
                'WHERE',
                'VALUES',
                '<',
                '>=',
                '18;',
                '15;',
            ],
        },

        # AND ---------------------------------------------------------------
        {
            'x': 3945,
            'y': 390,
            'tipo': 'eleccion_multiple',
            'pregunta': (
                '¿Qué filas devuelve una consulta cuando dos condiciones '
                'están unidas con AND?'
            ),
            'opciones': [
                'Las que cumplen las dos condiciones.',
                'Las que cumplen al menos una condición.',
                'Todas las filas de la tabla.',
            ],
            'respuesta_correcta': 1,
            'nombre': 'mysql_04_and_eleccion',
        },
        {
            'x': 4155,
            'y': 435,
            'tipo': 'codigo',
            'pregunta': (
                'Completa el filtro para buscar estudiantes de Tercero que '
                'tengan 15 años o más.'
            ),
            'nombre': 'mysql_04_and_codigo',
            'respuestas': {
                'where': 'WHERE',
                'grado': "grado = 'Tercero'",
                'and': 'AND',
                'edad': 'edad >= 15;',
            },
            'codigo': [
                {
                    'indentacion': 0,
                    'segmentos': [
                        {'texto': 'SELECT * FROM estudiantes'},
                    ],
                },
                {
                    'indentacion': 0,
                    'segmentos': [
                        {'hueco': 'where'},
                        {'texto': ' '},
                        {'hueco': 'grado'},
                    ],
                },
                {
                    'indentacion': 1,
                    'segmentos': [
                        {'hueco': 'and'},
                        {'texto': ' '},
                        {'hueco': 'edad'},
                    ],
                },
            ],
            'opciones': [
                'WHERE',
                'HAVING',
                "grado = 'Tercero'",
                "grado <> 'Tercero'",
                'AND',
                'OR',
                'edad >= 15;',
                'edad < 15;',
            ],
        },

        # OR Y AGRUPACIÓN ---------------------------------------------------
        {
    "x": 5090,
    "y": 370,
    "tipo": "eleccion_multiple",
    "pregunta": (
        "En la consulta: SELECT * FROM estudiantes "
        "WHERE edad = 15 OR grado = 'Primero'; "
        "¿Qué estudiantes se muestran?"
    ),
    "opciones": [
        "Solo los de 15 años",
        "Solo los de Primero",
        "Los de 15 o Primero",
    ],
    "respuesta_correcta": 3,
    "nombre": "mysql_where_or_eleccion_04",
},
        {
            'x': 5310,
            'y': 420,
            'tipo': 'codigo',
            'pregunta': (
                'Completa la consulta: estudiantes de Primero o Segundo que '
                'tengan 15 años o más.'
            ),
            'nombre': 'mysql_04_and_or_codigo',
            'respuestas': {
                'where': 'WHERE',
                'or': 'OR',
                'and': 'AND',
                'comparador': '>=',
            },
            'codigo': [
                {
                    'indentacion': 0,
                    'segmentos': [
                        {'texto': 'SELECT nombre FROM estudiantes'},
                    ],
                },
                {
                    'indentacion': 0,
                    'segmentos': [
                        {'hueco': 'where'},
                        {'texto': " (grado = 'Primero'"},
                    ],
                },
                {
                    'indentacion': 1,
                    'segmentos': [
                        {'hueco': 'or'},
                        {'texto': " grado = 'Segundo')"},
                    ],
                },
                {
                    'indentacion': 1,
                    'segmentos': [
                        {'hueco': 'and'},
                        {'texto': ' edad '},
                        {'hueco': 'comparador'},
                        {'texto': ' 15;'},
                    ],
                },
            ],
            'opciones': [
                'WHERE',
                'HAVING',
                'OR',
                'NOT',
                'AND',
                '>=',
                '<',
            ],
        },
    )


CLASE_NIVEL = NivelMySQL04


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == '__main__':
    ejecutar_nivel()
