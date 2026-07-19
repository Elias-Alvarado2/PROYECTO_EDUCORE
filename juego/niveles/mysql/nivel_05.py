from juego.core.juego import JuegoBase

LENGUAJE_ACTUAL = "MySQL"
NIVEL_ACTUAL = 5
FONDO_ACTUAL = "mysql"


class NivelMySQL05(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR = 0
    LONGITUD_NIVEL = 6500
    NPC_X = 860
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    PISOS = ((0, LONGITUD_NIVEL),)
    CARTEL_FINAL = {
    "x": 5100,
    "ajuste_y": -10,
    "tamano":0.40,
    "mostrar_bloqueado": True,
}
    NPCS = (
        {
            "nombre": "pinguino_delete",
            "x": 350,
            "ajuste_y": -8,
            "orden_leccion": 14,
            "requiere_anterior": False,
            "repetible": True,
            "practicas": (1, 2,3),
        },
        {
            "nombre": "pinguino_where",
            "x": 1477,
            "ajuste_y": -106,
            "orden_leccion": 15,
            "requiere_anterior": True,
            "repetible": True,
            "practicas": (4,5),
        },
         {
            "nombre": "pinguino_where_multiple",
            "x": 4072,
            "ajuste_y": -8,
            "orden_leccion": 16,
            "requiere_anterior": True,
            "repetible": True,
            "practicas": (6),
        },
    )

    OBSTACULOS = (
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 1000,
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
            "x": 1100,
            "cantidad": 14,
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
            "x": 1130,
            "cantidad": 4,
            "separacion": 210,
            "ajuste_y": -80,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 1260,
            "ajuste_y": -150,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 1000,
            "ajuste_y": -210,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 1000,
            "ajuste_y": -240,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "tronco",
            "imagen": "mysql/tronco.png",
            "x": 975,
            "ajuste_y": -285,
            "ancho": 120,
            "alto": 30,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 15,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 20,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 1200,
            "cantidad": 4,
            "separacion": 210,
            "ajuste_y": -350,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 2400,
            "ajuste_y": -260,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 2600,
            "ajuste_y": -210,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 2800,
            "ajuste_y": -160,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "fragmento",
            "imagen": "mysql/plataforma.png",
            "x": 3000,
            "ajuste_y": -100,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 2350,
            "ajuste_y": 0,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 3200,
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
            "x": 3285,
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
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 3475,
            "ajuste_y": 0,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "columnas": 2,
            "separacion_y": -10,
            "x": 3600,
            "ajuste_y": 0,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "columnas": 3,
            "separacion_y": -10,
            "x": 3725,
            "ajuste_y": 0,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "columnas": 2,
            "separacion_y": -10,
            "x": 3850,
            "ajuste_y": 0,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
        {
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 4300,
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
            "x": 4385,
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
            "tipo": "cofre",
            "imagen": "mysql/cofre.png",
            "x": 4575,
            "ajuste_y": 0,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 10,
        },
    )

    PRACTICAS = (
        {
            "x": 1012,
            "y": 208,
            "tipo": "eleccion_multiple",
            "pregunta": (
                "DELETE FROM estudiantes"
                "WHERE edad < 10;"
                "¿Qué estudiantes se eliminan?"
            ),
            "opciones": [
                "Solo los de 15 años",
                "Solo los de 10 años",
                "Los menores a 10 años",
            ],
            "respuesta_correcta": 3,
            "nombre": "mysql_where_or_eleccion_04",
        },
        {
            "x": 1555,
            "y": 133,
            "tipo": "codigo",
            "pregunta": (
                "Arrastra las opciones correctas para eliminar "
                "al estudiante cuyo id_estudiante sea igual a 1."
            ),
            "nombre": "mysql_delete_codigo_03",
            "respuestas": {
                "comando": "DELETE",
                "origen": "FROM",
                "condicion": "WHERE",
                "valor": "1",
            },
            "codigo": [
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "comando"},
                        {"texto": " "},
                        {"hueco": "origen"},
                        {"texto": " estudiantes"},
                    ],
                },
                {
                    "indentacion": 0,
                    "segmentos": [
                        {"hueco": "condicion"},
                        {"texto": " id_estudiante = "},
                        {"hueco": "valor"},
                        {"texto": ";"},
                    ],
                },
            ],
            "opciones": [
                "DELETE",
                "SELECT",
                "FROM",
                "SET",
                "WHERE",
                "3",
                "1",
            ],
        },
        {
    "x": 1864,
    "y": 133,
    "tipo": "verdadero_falso",
    "pregunta": (
        "La instrucción DELETE elimina una fila completa "
        "con todos los datos que contiene."
    ),
    "respuesta_correcta": True,
    "nombre": "mysql_delete_verdadero_falso_01",
},
       {
            "x": 2590,
            "y": 500,
            "tipo": "eleccion_multiple",
            "pregunta": (
                "Que resultado tendra este comando\n"
                "UPDATE estudiantes\n"
                "SET ='Juan'\n"
                "WHERE id_estudiante=1;"
            ),
            "opciones": [
                "Cambia el nombre a Juan del estudiante1",
                "Cambia todos los nombres a Juan",
                "Un error",
            ],
            "respuesta_correcta": 3,
            "nombre": "mysql_update_leccion1",
        },
        {
    "x": 3731,
    "y": 389,
    "tipo": "codigo",
    "pregunta": (
        "Arrastra las opciones correctas para cambiar a Segundo "
        "el grado del estudiante cuyo id_estudiante sea igual a 3."
    ),
    "nombre": "mysql_update_codigo_06",
    "respuestas": {
        "comando": "UPDATE",
        "asignacion": "SET",
        "nuevo_grado": "'Segundo'",
        "condicion": "WHERE",
        "valor": "3",
    },
    "codigo": [
        {
            "indentacion": 0,
            "segmentos": [
                {"hueco": "comando"},
                {"texto": " estudiantes"},
            ],
        },
        {
            "indentacion": 0,
            "segmentos": [
                {"hueco": "asignacion"},
                {"texto": " grado = "},
                {"hueco": "nuevo_grado"},
            ],
        },
        {
            "indentacion": 0,
            "segmentos": [
                {"hueco": "condicion"},
                {"texto": " id_estudiante = "},
                {"hueco": "valor"},
                {"texto": ";"},
            ],
        },
    ],
    "opciones": [
        "UPDATE",
        "DELETE",
        "SET",
        "FROM",
        "WHERE",
        "'Primero'",
        "'Segundo'",
        "3",
        "5",
    ],
},
{
    "x": 4709,
    "y": 500,
    "tipo": "codigo",
    "pregunta": (
        "Arrastra las opciones correctas para cambiar el nombre a Ana, "
        "la edad a 16 y el grado a Segundo del estudiante "
        "cuyo id_estudiante sea igual a 5."
    ),
    "nombre": "mysql_update_varios_campos_codigo_05",
    "respuestas": {
        "comando": "UPDATE",
        "asignacion": "SET",
        "nombre": "'Ana'",
        "edad": "16",
        "grado": "'Segundo'",
        "condicion": "WHERE",
        "id": "5",
    },
    "codigo": [
        {
            "indentacion": 0,
            "segmentos": [
                {"hueco": "comando"},
                {"texto": " estudiantes"},
            ],
        },
        {
            "indentacion": 0,
            "segmentos": [
                {"hueco": "asignacion"},
                {"texto": " nombre = "},
                {"hueco": "nombre"},
                {"texto": ","},
            ],
        },
        {
            "indentacion": 0,
            "segmentos": [
                {"texto": "edad = "},
                {"hueco": "edad"},
                {"texto": ","},
            ],
        },
        {
            "indentacion": 0,
            "segmentos": [
                {"texto": "grado = "},
                {"hueco": "grado"},
            ],
        },
        {
            "indentacion": 0,
            "segmentos": [
                {"hueco": "condicion"},
                {"texto": " id_estudiante = "},
                {"hueco": "id"},
                {"texto": ";"},
            ],
        },
    ],
    "opciones": [
        "UPDATE",
        "DELETE",
        "SET",
        "FROM",
        "WHERE",
        "'Ana'",
        "'Carlos'",
        "16",
        "18",
        "'Segundo'",
        "'Primero'",
        "5",
    ],
},
        
    )


CLASE_NIVEL = NivelMySQL05


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
