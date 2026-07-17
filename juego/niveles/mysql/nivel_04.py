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
    LONGITUD_NIVEL = 6500
    NPC_X = 825
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    PISOS = (
        (0, LONGITUD_NIVEL),
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
            'x': 4480,
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
            'x': 4360,
            'ajuste_y': -195,
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
            'ajuste_y': -75,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
    )

    PRACTICAS = (
        {
            'x': 1500,
            'y': None,
            'pregunta': 'En MySQL, SELECT se utiliza para consultar datos de una tabla.',
            'respuesta_correcta': True,
            'nombre': 'practica_mysql_04',
        },
    )


CLASE_NIVEL = NivelMySQL04


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == '__main__':
    ejecutar_nivel()
