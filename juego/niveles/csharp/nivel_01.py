from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = "C#"
NIVEL_ACTUAL = 1

# Debe coincidir con el nombre de la carpeta dentro de assets/fondos.
# Ejemplo: assets/fondos/c#/c#_cielo.png
FONDO_ACTUAL = "c#"


class NivelCSharp01(JuegoBase):
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

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR = 0

    # Solo mueve visualmente el PNG del suelo de este nivel.
    # Positivo = baja. Negativo = sube. No modifica la hitbox.
    AJUSTE_Y_SPRITE_SUELO =0

    # ========================================================
    # CONFIGURACIÓN DEL NIVEL
    # ========================================================

    LONGITUD_NIVEL = 5000

    NPC_X = 720
    AJUSTE_Y_NPC = -8

    PISOS = (
        (0, 850),
        (1000, LONGITUD_NIVEL),
    )

    ABISMOS = (
        (850, 1000),
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
                "En C#, una variable debe respetar "
                "el tipo de dato declarado."
            ),
            "respuesta_correcta": True,
            "nombre": "practica_csharp_01",
        },
    )


CLASE_NIVEL = NivelCSharp01


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()