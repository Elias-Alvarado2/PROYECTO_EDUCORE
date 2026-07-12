from __future__ import annotations

from copy import deepcopy

from juego.core import motor
from juego.interfaz.practica_codigo import PantallaPracticaCodigo


class JuegoBase(motor.JuegoEduCore):
    """Motor compartido para los 24 niveles.

    Cada archivo de nivel hereda de esta clase y reemplaza solamente las
    variables de configuración: lenguaje, fondo, posición del jugador,
    piso, obstáculos, NPC y prácticas.
    """

    # ========================================================
    # CONFIGURACIÓN PREDETERMINADA
    # Cada nivel puede reemplazar estos valores.
    # ========================================================

    LENGUAJE_ACTUAL = "Python"
    NIVEL_ACTUAL = 1
    FONDO_ACTUAL = "python"

    # Posición horizontal inicial del jugador.
    # Mayor = más a la derecha. Menor = más a la izquierda.
    JUGADOR_X_INICIAL = 170

    # Ajuste vertical del piso de colisión para este nivel.
    # Negativo = sube al jugador y las colisiones del nivel.
    # Positivo = baja al jugador y las colisiones del nivel.
    AJUSTE_Y_JUGADOR = 0

    # Mueve únicamente la imagen del suelo.
    # No cambia la hitbox, las plataformas ni el jugador.
    # Positivo = baja el PNG. Negativo = lo sube.
    AJUSTE_Y_SPRITE_SUELO = 0

    # Mueve únicamente la imagen de la capa de plantas.
    # No modifica hitboxes, obstáculos, jugador, NPC ni suelo.
    # Positivo = baja el PNG. Negativo = lo sube.
    AJUSTE_Y_SPRITE_PLANTAS = 0

    # Mueve únicamente la imagen de la capa de montañas.
    # No modifica hitboxes, obstáculos, jugador, NPC ni suelo.
    # Positivo = baja el PNG. Negativo = lo sube.
    AJUSTE_Y_SPRITE_MONTANAS = 0

    LONGITUD_NIVEL = 5000

    NPC_X = 720
    AJUSTE_Y_NPC = -8

    # Coordenadas sin ESCALA_JUEGO.
    # JuegoBase aplica la escala automáticamente.
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
                "En Python, una variable sirve para guardar datos "
                "que puedes usar después en el programa."
            ),
            "respuesta_correcta": True,
            "nombre": "moneda_variable",
        },
    )

    # ========================================================
    # INICIALIZACIÓN
    # ========================================================

    def __init__(
        self,
        id_jugador: int = 1,
        actualizar_progreso_carga=None,
    ):
        # El motor original consulta esta constante al actualizar el NPC.
        motor.CONFIGURACION_NPC = int(self.AJUSTE_Y_NPC)

        super().__init__(
            id_jugador=id_jugador,
            nombre_lenguaje=self.LENGUAJE_ACTUAL,
            orden_leccion=self.NIVEL_ACTUAL,
            actualizar_progreso_carga=actualizar_progreso_carga,
        )

    # ========================================================
    # ESCALA Y PISO DEL NIVEL
    # ========================================================

    @staticmethod
    def escalar(valor: int | float) -> int:
        """Aplica ESCALA_JUEGO a una coordenada del nivel."""
        return round(valor * motor.ESCALA_JUEGO)

    def obtener_piso_colision_nivel(self) -> int:
        """Devuelve la altura del piso de colisión para este nivel."""
        return (
            motor.PISO_COLISION_Y
            + self.escalar(self.AJUSTE_Y_JUGADOR)
        )

    # ========================================================
    # POSICIÓN DEL JUGADOR POR NIVEL
    # ========================================================

    def colocar_jugador_en_inicio(self):
        """Coloca al jugador en la posición configurada por el nivel."""

        self.jugador.x_pantalla = self.escalar(
            self.JUGADOR_X_INICIAL
        )

        self.jugador.colocar_sobre_piso(
            self.obtener_piso_colision_nivel()
        )

        self.jugador.velocidad_y = 0
        self.jugador.en_suelo = True
        self.camara_x = 0

    def reiniciar(self):
        """Reinicia conservando la posición configurada por el nivel."""
        super().reiniciar()
        self.colocar_jugador_en_inicio()

    # ========================================================
    # CREACIÓN DEL MUNDO
    # ========================================================

    def _inicializar_mundo(self):
        self.capas = []
        self.capa_suelo = None

        self.cargar_fondo_personalizado()

        # ----------------------------------------------------
        # JUGADOR
        # ----------------------------------------------------

        self.jugador = motor.Jugador(
            self.personaje_elegido,
            escala_default=5.1,
        )

        piso_nivel = self.obtener_piso_colision_nivel()
        self.limite_camara_x = max(
            0,
            self.escalar(self.LONGITUD_NIVEL) - motor.ANCHO,
        )

        # ----------------------------------------------------
        # PISOS
        # ----------------------------------------------------

        self.plataformas = [
            motor.PlataformaInvisible(
                self.escalar(inicio),
                self.escalar(fin),
                piso_nivel,
            )
            for inicio, fin in self.PISOS
        ]

        # ----------------------------------------------------
        # OBSTÁCULOS
        # ----------------------------------------------------

        self.obstaculos = [
            self._crear_obstaculo(config)
            for config in deepcopy(self.OBSTACULOS)
        ]

        self.colocar_jugador_en_inicio()

        # ----------------------------------------------------
        # NPC
        # ----------------------------------------------------

        self.npc = motor.NPC(
            x_mundo=self.escalar(self.NPC_X),
            suelo_y=(
                piso_nivel
                + self.escalar(self.AJUSTE_Y_NPC)
            ),
            escala=3.6,
        )

        # ----------------------------------------------------
        # DIÁLOGO Y PRÁCTICA
        # ----------------------------------------------------

        self.caja_dialogo = motor.CajaDialogo()
        self.caja_dialogo.redimensionar(
            motor.ANCHO,
            motor.ALTO,
        )

        self.practica = motor.PantallaPractica()
        self.practica_codigo = PantallaPracticaCodigo(
            motor.ANCHO,
            motor.ALTO,
        )

        self.objeto_practica_actual = None
        self.objeto_en_contacto = None
        self.objetos_practica = []

    # ========================================================
    # CREACIÓN DE OBSTÁCULOS
    # ========================================================

    def _crear_obstaculo(self, config: dict):
        ancho = self.escalar(
            config.get("ancho", motor.TAMANO_TILE)
        )
        alto = self.escalar(
            config.get("alto", motor.TAMANO_TILE)
        )

        # Si no se indica un tamaño personalizado, conserva el actual.
        if "ancho" not in config:
            ancho = motor.TAMANO_OBSTACULO

        if "alto" not in config:
            alto = motor.TAMANO_OBSTACULO

        reducir_ancho = self.escalar(
            config.get("hitbox_reducir_ancho", 0)
        )
        reducir_alto = self.escalar(
            config.get("hitbox_reducir_alto", 0)
        )

        return motor.Obstaculo(
            x=self.escalar(config["x"]),
            y=(
                self.obtener_piso_colision_nivel()
                - alto
                + self.escalar(config.get("ajuste_y", 0))
            ),
            ancho=ancho,
            alto=alto,
            tipo=config["tipo"],
            ruta_imagen=(
                motor.OBSTACULOS_DIR
                / config["imagen"]
            ),
            hitbox_offset_x=self.escalar(
                config.get("hitbox_offset_x", 0)
            ),
            hitbox_offset_y=self.escalar(
                config.get("hitbox_offset_y", 0)
            ),
            hitbox_ancho=max(
                1,
                ancho - reducir_ancho,
            ),
            hitbox_alto=max(
                1,
                alto - reducir_alto,
            ),
        )

    # ========================================================
    # FONDOS DEL MUNDO
    # ========================================================

    def cargar_fondo_personalizado(self):
        carpeta = (
            motor.FONDOS_DIR
            / self.FONDO_ACTUAL
        )

        ruta_cielo = (
            carpeta
            / f"{self.FONDO_ACTUAL}_cielo.png"
        )
        ruta_montanas = (
            carpeta
            / f"{self.FONDO_ACTUAL}_montanas.png"
        )
        ruta_plantas = (
            carpeta
            / f"{self.FONDO_ACTUAL}_plantas.png"
        )
        ruta_suelo = (
            carpeta
            / f"{self.FONDO_ACTUAL}_suelo.png"
        )

        configuraciones = (
            (
                ruta_cielo,
                0.10,
                (100, 195, 245),
                False,
                0,
            ),
            (
                ruta_montanas,
                0.30,
                (0, 0, 0, 0),
                True,

                # Posición base de la capa de montañas
                # más el ajuste definido por cada nivel.
                (
                    round(6 * motor.ESCALA_JUEGO)
                    + self.escalar(
                        self.AJUSTE_Y_SPRITE_MONTANAS
                    )
                ),
            ),
            (
                ruta_plantas,
                0.70,
                (0, 0, 0, 0),
                True,

                # Posición base de la capa de plantas
                # más el ajuste definido por cada nivel.
                (
                    round(26 * motor.ESCALA_JUEGO)
                    + self.escalar(
                        self.AJUSTE_Y_SPRITE_PLANTAS
                    )
                ),
            ),
        )

        self.capas = []

        for ruta, factor, color, limpiar, offset_y in configuraciones:
            self.capas.append(
                motor.CapaParallax(
                    ruta,
                    factor,
                    motor.ANCHO_FONDO,
                    motor.ALTO_FONDO,
                    color,
                    limpiar_fondo_falso=limpiar,
                    offset_y=round(
                        offset_y * motor.ESCALA_RENDER_FONDO
                    ),
                )
            )

        self.capa_suelo = motor.CapaParallax(
            ruta_suelo,
            1.00,
            motor.ANCHO_FONDO,
            motor.ALTO_FONDO,
            (0, 0, 0, 0),
            limpiar_fondo_falso=True,
            cortar_arriba_y=round(
                (
                    self.obtener_piso_colision_nivel()
                    - round(70 * motor.ESCALA_JUEGO)
                )
                * motor.ESCALA_RENDER_FONDO
            ),

            # Este desplazamiento afecta únicamente al dibujo del PNG.
            # Se convierte a la resolución interna del fondo optimizado.
            offset_y=round(
                self.escalar(self.AJUSTE_Y_SPRITE_SUELO)
                * motor.ESCALA_RENDER_FONDO
            ),
        )

    # ========================================================
    # OBJETOS DE PRÁCTICA
    # ========================================================

    def crear_objeto_practica_prueba(self):
        """Crea las prácticas definidas dentro del archivo del nivel."""
        objetos = []
        tamano_objeto = round(
            48 * motor.ESCALA_JUEGO
        )

        for indice, config in enumerate(
            self.PRACTICAS,
            start=1,
        ):
            y_config = config.get("y")

            if y_config is None:
                y = (
                    self.obtener_piso_colision_nivel()
                    - tamano_objeto
                    - round(18 * motor.ESCALA_JUEGO)
                )
            else:
                y = self.escalar(y_config)

            objetos.append(
                motor.ObjetoPractica(
                    x=self.escalar(config["x"]),
                    y=y,
                    pregunta=config["pregunta"],
                    respuesta_correcta=bool(
                        config.get("respuesta_correcta", True)
                    ),
                    nombre=config.get(
                        "nombre",
                        f"practica_{indice}",
                    ),
                    tipo=config.get(
                        "tipo",
                        "verdadero_falso",
                    ),
                    configuracion_codigo={
                        "respuestas": deepcopy(
                            config.get("respuestas", {})
                        ),
                        "codigo": deepcopy(
                            config.get("codigo", [])
                        ),
                        "opciones": deepcopy(
                            config.get("opciones", [])
                        ),
                    },
                )
            )

        self.objetos_practica = objetos
