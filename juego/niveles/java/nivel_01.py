from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = "Java"
NIVEL_ACTUAL = 1

# Debe coincidir con la carpeta dentro de assets/fondos.
# Ejemplo: assets/fondos/java/java_cielo.png
FONDO_ACTUAL = "java"


class NivelJava01(JuegoBase):
    # ========================================================
    # IDENTIFICACIÓN DEL NIVEL
    # ========================================================

    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL

    # ========================================================
    # POSICIÓN DEL JUGADOR
    # ========================================================

    # Mayor = más a la derecha.
    # Menor = más a la izquierda.
    JUGADOR_X_INICIAL = 170

    # Negativo = sube al jugador y las colisiones del nivel.
    # Positivo = los baja.
    AJUSTE_Y_JUGADOR = 0
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

    # ========================================================
    # CONFIGURACIÓN DEL NIVEL
    # ========================================================

    LONGITUD_NIVEL = 5000

    NPC_X = 720
    AJUSTE_Y_NPC = -8

    PISOS = (
        (0, LONGITUD_NIVEL),
    )

    OBSTACULOS = (
        {
            "tipo": "tronco",
            "imagen": "tronco.png",
            "x": 500,
            "ajuste_y": 40,
            "hitbox_offset_x": 10,
            "hitbox_offset_y": 40,
            "hitbox_reducir_ancho": 20,
            "hitbox_reducir_alto": 70,
        },
    )

    PRACTICAS = (
        {
            "x": 1260,
            "y": None,
            "pregunta": (
                "En Java, una variable debe respetar "
                "el tipo de dato declarado."
            ),
            "respuesta_correcta": True,
            "nombre": "practica_java_01",
        },
    )


CLASE_NIVEL = NivelJava01


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
