from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'MySQL'
NIVEL_ACTUAL = 6
FONDO_ACTUAL = 'mysql'
ES_PRUEBA_FINAL = True

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
    LONGITUD_NIVEL = 10000
    NPC_X = 895
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    CARTEL_FINAL = {
    "x": 8900,
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



    )


CLASE_NIVEL = NivelMySQL06


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()