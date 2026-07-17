from juego.core.juego import JuegoBase


LENGUAJE_ACTUAL = 'MySQL'
NIVEL_ACTUAL = 5
FONDO_ACTUAL = 'mysql'


class NivelMySQL05(JuegoBase):
    # Cada archivo conserva su propia configuración.
    LENGUAJE_ACTUAL = LENGUAJE_ACTUAL
    NIVEL_ACTUAL = NIVEL_ACTUAL
    FONDO_ACTUAL = FONDO_ACTUAL
    JUGADOR_X_INICIAL = 170

    # Usa valores pequeños.
    # Negativo = sube.
    # Positivo = baja.
    AJUSTE_Y_JUGADOR =0
    LONGITUD_NIVEL = 7000
    NPC_X = 860
    AJUSTE_Y_NPC = -8
    AJUSTE_Y_SPRITE_MONTANAS = 0
    AJUSTE_Y_SPRITE_SUELO = 0
    AJUSTE_Y_SPRITE_PLANTAS = 0
    PISOS = (
        (0, LONGITUD_NIVEL),
    )
    

    OBSTACULOS = (
         {
            'tipo': 'cofre',
            'imagen': 'mysql/cofre.png',
            'x': 500,
            'ajuste_y': 0,
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
            'x': 600,
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
            'x': 630,
            'cantidad': 4,
            'separacion': 230,
            'ajuste_y': -80,
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
            'x':800,
            'ajuste_y': -150,
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
            'x':500,
            'ajuste_y': -210,
            'ancho': 120,
            'alto': 36,
            'hitbox_offset_x': 10,
            'hitbox_offset_y': 10,
            'hitbox_reducir_ancho': 20,
            'hitbox_reducir_alto': 10,
        },
       
    )

    PRACTICAS = (
    
    )


CLASE_NIVEL = NivelMySQL05


def ejecutar_nivel(id_jugador: int = 1):
    juego = CLASE_NIVEL(id_jugador=id_jugador)
    juego.ejecutar()


if __name__ == "__main__":
    ejecutar_nivel()
