from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'MySQL'
NIVEL_ACTUAL = 3
FONDO_ACTUAL = 'mysql'


class NivelMySQL03(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 6000
    NPC_X = 790
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    PISOS = (
        (0, LONGITUD_NIVEL),
    )
    NPCS=(

    {
        "nombre": "pinguino_1",
        "x": 400,
        "ajuste_y": -160,
        "orden_leccion": 8,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    {
        "nombre": "pinguino_1",
        "x": 1200,
        "ajuste_y": -160,
        "orden_leccion": 8,
        "requiere_anterior": False,
        "repetible": True,
        "practica": 1,
    },
    )
    OBSTACULOS = (
        {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 600,
            "ajuste_y":-60,
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
            "x": 400,
            "ajuste_y":-130,
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
            "x": 900,
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
            "x": 1500,
            "ajuste_y":-60,
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
            "x": 1200,
            "ajuste_y":-145,
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
            "x": 1700,
            "ajuste_y":-130,
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
            "x": 1550,
            "ajuste_y":-275,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"bloque",
            "imagen":"mysql/bloque.png",
            "x": 1710,
            "ajuste_y":-150,
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
            "x": 1720,
            "ajuste_y":-180,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo": "puas",
            "imagen": "mysql/pinchos.png",
            "x": 900,
            "cantidad": 30,  
            "ajuste_y": -5,
            "ancho": 80,
            "alto": 50,
            "hitbox_offset_x": 25,
            "hitbox_offset_y": 30,
            "hitbox_reducir_ancho": 45,
            "hitbox_reducir_alto": 25,
        },
         {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 1900,
            "ajuste_y":-255,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"cofre",
            "imagen":"mysql/cofre.png",
            "x": 2100,
            "ajuste_y":-180,
            "ancho": 40,
            "alto": 25,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"cofre",
            "imagen":"mysql/cofre.png",
            "x": 2390,
            "ajuste_y":-180,
            "ancho": 40,
            "alto": 25,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"cofre",
            "imagen":"mysql/cofre.png",
            "x": 2680,
            "ajuste_y":-180,
            "ancho": 40,
            "alto": 25,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
         {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 2900,
            "ajuste_y":-215,
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
            "x": 3100,
            "ajuste_y":-170,
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
            "x": 3400,
            "ajuste_y":-210,
            "ancho": 120,
            "alto": 36,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 10,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":10,
        },
        {
            "tipo":"tronco",
            "imagen":"mysql/tronco.png",
            "x": 3400,
            "ajuste_y":-230,
            "ancho": 120,
            "alto": 30,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 15,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto":20,
        },
        {
            "tipo":"fragmento",
            "imagen":"mysql/plataforma.png",
            "x": 3700,
            "ajuste_y":-210,
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
        "x": 1230,
        "y": 350,
        "tipo": "eleccion_multiple",
        "pregunta": (
        "¿Qué sentencia SQL permite indicar los valores en una inserción? "
        ),
        "opciones": [
            "SELECT",
            "INSERT INTO",
            "VALUES",
        ],
        "respuesta_correcta": 3,
        "nombre": "mysql_eleccion_01",
        },
    )


CLASE_NIVEL = NivelMySQL03


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
