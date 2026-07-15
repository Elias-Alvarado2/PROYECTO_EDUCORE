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
        "practica": 2,  
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
        "x": 1800,
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
    )


    


CLASE_NIVEL = NivelMySQL01


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
