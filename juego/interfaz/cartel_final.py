from pathlib import Path

import pygame


# ============================================================
# CONFIGURACION EDITABLE DEL CARTEL FINAL
# Todos los recursos y ajustes visuales de este componente viven aqui.
# ============================================================
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
UI_DIR = RAIZ_PROYECTO / "assets" / "ui"
FUENTES_DIR = RAIZ_PROYECTO / "assets" / "FUENTES"

RUTA_CARTEL = UI_DIR / "cartel_fin.png"
RUTA_CANDADO = UI_DIR / "candado_fin.png"
RUTA_PANEL = UI_DIR / "cuadro_preguntas" / "cuadro.png"
RUTA_BOTON_SALIR = UI_DIR / "botones_fin" / "boton_salir.png"
RUTA_BOTON_SIGUIENTE = (
    UI_DIR / "botones_fin" / "boton_siguiente.png"
)
RUTA_FUENTE = FUENTES_DIR / "PixelOperator-Bold.ttf"

# El cartel del mundo usa el 60 % de sus medidas base.
ESCALA_CARTEL_PREDETERMINADA = 0.60
ANCHO_CARTEL_BASE = 220
ALTO_CARTEL_BASE = 250
ANCHO_CANDADO_BASE = 78
ALTO_CANDADO_BASE = 105

ANCHO_PANEL_BASE = 700
ALTO_PANEL_BASE = 440
MARGEN_X_PANEL_PANTALLA = 140
MARGEN_Y_PANEL_PANTALLA = 100
CENTRO_X_PANEL = 0.50
CENTRO_Y_PANEL = 0.50

ANCHO_BOTON_BASE = 270
ALTO_BOTON_BASE = 50
SEPARACION_BOTONES_BASE = 24
MARGEN_INFERIOR_BOTONES_BASE = 90
DESPLAZAMIENTO_X_BOTONES_BASE = 0
DESPLAZAMIENTO_Y_BOTONES_BASE = 0

TAMANO_FUENTE_TITULO = 70
TAMANO_FUENTE_BOTON = 42
TAMANO_FUENTE_SUBTITULO = 38
TAMANO_FUENTE_MENSAJE = 27
TAMANO_FUENTE_AYUDA = 25

POSICION_Y_TITULO = 0.31
POSICION_Y_SUBTITULO = 0.45
MARGEN_INFERIOR_AYUDA_BASE = 42
POSICION_Y_CANDADO = 0.36
MARGEN_INFERIOR_MENSAJE_BASE = 80
RELLENO_X_MENSAJE = 70
RELLENO_Y_MENSAJE = 34

MARGEN_INTERACCION_X_BASE = 95
MARGEN_INTERACCION_Y_BASE = 45
INCREMENTO_COLOR_HOVER = (28, 28, 28, 0)

# Medidas de respaldo utilizadas solo si falta alguna imagen.
ANCHO_PANEL_RESPALDO_BASE = 920
ALTO_PANEL_RESPALDO_BASE = 390
ANCHO_BOTON_RESPALDO_BASE = 285
ALTO_BOTON_RESPALDO_BASE = 70
ANCHO_CARTEL_RESPALDO_BASE = 190
ALTO_CARTEL_RESPALDO_BASE = 145
ANCHO_CANDADO_RESPALDO_BASE = 58
ALTO_CANDADO_RESPALDO_BASE = 48


class CartelFinal:
    """Cartel reutilizable para terminar una leccion."""

    ACCION_MENU = "menu_niveles"
    ACCION_SIGUIENTE = "siguiente_leccion"
    EVENTO_CONSUMIDO = "__cartel_final_evento_consumido__"

    @classmethod
    def desde_nivel(
        cls,
        nivel,
        *,
        ancho_pantalla=1920,
        alto_pantalla=1080,
        escala_juego=1.5,
        suelo_predeterminado=825,
    ):
        """Construye el cartel usando CARTEL_FINAL del nivel actual."""
        configuracion = getattr(nivel, "CARTEL_FINAL", {}) or {}

        if not isinstance(configuracion, dict):
            print(
                "[CARTEL_FINAL] La configuracion debe ser un "
                "diccionario. Se usara la configuracion automatica."
            )
            configuracion = {}

        longitud_nivel = float(
            getattr(nivel, "LONGITUD_NIVEL", 5000)
        )
        x_config = configuracion.get(
            "x",
            max(700, longitud_nivel - 250),
        )
        x_mundo = round(float(x_config) * escala_juego)
        ajuste_y = round(
            float(configuracion.get("ajuste_y", 0))
            * escala_juego
        )

        obtener_piso_nivel = getattr(
            nivel,
            "obtener_piso_colision_nivel",
            None,
        )
        suelo_y = (
            int(obtener_piso_nivel())
            if callable(obtener_piso_nivel)
            else int(suelo_predeterminado)
        )

        orden_solicitado = getattr(
            nivel,
            "orden_leccion_solicitado",
            None,
        )
        nivel_actual = int(
            getattr(
                nivel,
                "NIVEL_ACTUAL",
                orden_solicitado or 1,
            )
        )
        total_niveles = int(
            getattr(nivel, "TOTAL_NIVELES", 6)
        )
        factor_tamano = configuracion.get(
            "tamano",
            configuracion.get(
                "escala",
                ESCALA_CARTEL_PREDETERMINADA,
            ),
        )

        cartel = cls(
            x_mundo=x_mundo,
            suelo_y=suelo_y + ajuste_y,
            ancho_pantalla=ancho_pantalla,
            alto_pantalla=alto_pantalla,
            escala_juego=escala_juego,
            factor_tamano_cartel=factor_tamano,
            siguiente_disponible=(nivel_actual < total_niveles),
            mostrar_bloqueado=bool(
                configuracion.get("mostrar_bloqueado", True)
            ),
        )

        if bool(getattr(nivel, "leccion_ya_completada", False)):
            cartel.desbloquear()

        return cartel

    def __init__(
        self,
        x_mundo,
        suelo_y,
        ancho_pantalla=1920,
        alto_pantalla=1080,
        escala_juego=1.5,
        factor_tamano_cartel=None,
        ruta_imagen=None,
        ruta_fuente=None,
        ruta_candado=None,
        ruta_panel=None,
        ruta_boton_menu=None,
        ruta_boton_siguiente=None,
        siguiente_disponible=True,
        mostrar_bloqueado=True,
    ):
        self.x_mundo = int(x_mundo)
        self.suelo_y = int(suelo_y)
        self.ancho_pantalla = int(ancho_pantalla)
        self.alto_pantalla = int(alto_pantalla)
        self.escala_juego = float(escala_juego)
        if factor_tamano_cartel is None:
            factor_tamano_cartel = ESCALA_CARTEL_PREDETERMINADA
        try:
            factor_tamano_cartel = float(factor_tamano_cartel)
        except (TypeError, ValueError):
            factor_tamano_cartel = ESCALA_CARTEL_PREDETERMINADA
        self.factor_tamano_cartel = max(
            0.05,
            factor_tamano_cartel,
        )

        self.ruta_imagen = self._normalizar_ruta(
            RUTA_CARTEL if ruta_imagen is None else ruta_imagen
        )
        self.ruta_fuente = self._normalizar_ruta(
            RUTA_FUENTE if ruta_fuente is None else ruta_fuente
        )
        self.ruta_candado = self._normalizar_ruta(
            RUTA_CANDADO if ruta_candado is None else ruta_candado
        )
        self.ruta_panel = self._normalizar_ruta(
            RUTA_PANEL if ruta_panel is None else ruta_panel
        )
        self.ruta_boton_menu = self._normalizar_ruta(
            RUTA_BOTON_SALIR
            if ruta_boton_menu is None
            else ruta_boton_menu
        )
        self.ruta_boton_siguiente = self._normalizar_ruta(
            RUTA_BOTON_SIGUIENTE
            if ruta_boton_siguiente is None
            else ruta_boton_siguiente
        )

        self.siguiente_disponible = bool(siguiente_disponible)
        self.mostrar_bloqueado = bool(mostrar_bloqueado)
        self.desbloqueado = False
        self.menu_visible = False
        self.jugador_cerca = False
        self.hover_menu = False
        self.hover_siguiente = False

        self.fuente_titulo = self._cargar_fuente(TAMANO_FUENTE_TITULO)
        self.fuente_boton = self._cargar_fuente(TAMANO_FUENTE_BOTON)
        self.fuente_texto = self._cargar_fuente(TAMANO_FUENTE_SUBTITULO)
        self.fuente_mensaje = self._cargar_fuente(TAMANO_FUENTE_MENSAJE)
        self.fuente_ayuda = self._cargar_fuente(TAMANO_FUENTE_AYUDA)

        self.imagen = self._cargar_png_ajustado(
            self.ruta_imagen,
            max_ancho=round(
                ANCHO_CARTEL_BASE
                * self.factor_tamano_cartel
                * self.escala_juego
            ),
            max_alto=round(
                ALTO_CARTEL_BASE
                * self.factor_tamano_cartel
                * self.escala_juego
            ),
        )
        if self.imagen is None:
            self.imagen = self._crear_cartel_respaldo()

        self.imagen_candado = self._cargar_png_ajustado(
            self.ruta_candado,
            max_ancho=round(
                ANCHO_CANDADO_BASE
                * self.factor_tamano_cartel
                * self.escala_juego
            ),
            max_alto=round(
                ALTO_CANDADO_BASE
                * self.factor_tamano_cartel
                * self.escala_juego
            ),
        )
        self.imagen_panel = self._cargar_png_ajustado(
            self.ruta_panel,
            max_ancho=min(
                self.ancho_pantalla - MARGEN_X_PANEL_PANTALLA,
                round(ANCHO_PANEL_BASE * self.escala_juego),
            ),
            max_alto=min(
                self.alto_pantalla - MARGEN_Y_PANEL_PANTALLA,
                round(ALTO_PANEL_BASE * self.escala_juego),
            ),
        )

        max_ancho_boton = round(ANCHO_BOTON_BASE * self.escala_juego)
        max_alto_boton = round(ALTO_BOTON_BASE * self.escala_juego)
        self.imagen_boton_menu = self._cargar_png_ajustado(
            self.ruta_boton_menu,
            max_ancho=max_ancho_boton,
            max_alto=max_alto_boton,
        )
        self.imagen_boton_siguiente = (
            self._cargar_png_ajustado(
                self.ruta_boton_siguiente,
                max_ancho=max_ancho_boton,
                max_alto=max_alto_boton,
            )
        )
        self.imagen_boton_menu_hover = (
            self._crear_variante_hover(self.imagen_boton_menu)
        )
        self.imagen_boton_siguiente_hover = (
            self._crear_variante_hover(
                self.imagen_boton_siguiente
            )
        )
        self.imagen_boton_siguiente_bloqueado = (
            self._crear_variante_bloqueada(
                self.imagen_boton_siguiente
            )
        )

        self.rect = self.imagen.get_rect()
        self.rect.x = self.x_mundo
        self.rect.bottom = self.suelo_y
        margen_horizontal = round(MARGEN_INTERACCION_X_BASE * self.escala_juego)
        margen_vertical = round(MARGEN_INTERACCION_Y_BASE * self.escala_juego)
        self.zona_interaccion = self.rect.inflate(
            margen_horizontal * 2,
            margen_vertical * 2,
        )

        self.capa_oscura = pygame.Surface(
            (self.ancho_pantalla, self.alto_pantalla),
            pygame.SRCALPHA,
        )
        self.panel_rect = pygame.Rect(0, 0, 1, 1)
        self.boton_menu_rect = pygame.Rect(0, 0, 1, 1)
        self.boton_siguiente_rect = pygame.Rect(0, 0, 1, 1)
        self._recalcular_interfaz()

    @staticmethod
    def _normalizar_ruta(ruta):
        return Path(ruta) if ruta else None

    def _cargar_fuente(self, tamano):
        if self.ruta_fuente and self.ruta_fuente.exists():
            return pygame.font.Font(
                str(self.ruta_fuente),
                int(tamano),
            )
        return pygame.font.SysFont(
            "arial",
            int(tamano),
            bold=True,
        )

    @staticmethod
    def _rect_visible_principal(imagen):
        mascara = pygame.mask.from_surface(imagen, threshold=8)
        componentes = mascara.get_bounding_rects()
        if not componentes:
            return imagen.get_rect()
        return max(
            componentes,
            key=lambda rect: rect.width * rect.height,
        )

    def _cargar_png_ajustado(
        self,
        ruta,
        max_ancho,
        max_alto,
    ):
        if ruta is None or not ruta.exists():
            return None
        try:
            imagen = pygame.image.load(str(ruta)).convert_alpha()
        except pygame.error as error:
            print(f"[CARTEL_FINAL] No se pudo cargar {ruta}: {error}")
            return None

        rect_visible = self._rect_visible_principal(imagen)
        if rect_visible.width <= 0 or rect_visible.height <= 0:
            return None

        imagen = imagen.subsurface(rect_visible).copy()
        escala = min(
            float(max_ancho) / imagen.get_width(),
            float(max_alto) / imagen.get_height(),
        )
        ancho = max(1, round(imagen.get_width() * escala))
        alto = max(1, round(imagen.get_height() * escala))
        return pygame.transform.scale(imagen, (ancho, alto))

    @staticmethod
    def _crear_variante_hover(imagen):
        if imagen is None:
            return None
        variante = imagen.copy()
        variante.fill(
            INCREMENTO_COLOR_HOVER,
            special_flags=pygame.BLEND_RGBA_ADD,
        )
        return variante

    @staticmethod
    def _crear_variante_bloqueada(imagen):
        if imagen is None:
            return None
        variante = imagen.copy()
        variante.fill(
            (125, 125, 125, 210),
            special_flags=pygame.BLEND_RGBA_MULT,
        )
        return variante

    def _crear_cartel_respaldo(self):
        ancho = round(ANCHO_CARTEL_RESPALDO_BASE * self.escala_juego)
        alto = round(ALTO_CARTEL_RESPALDO_BASE * self.escala_juego)
        superficie = pygame.Surface(
            (ancho, alto),
            pygame.SRCALPHA,
        )
        tabla = pygame.Rect(4, 4, ancho - 8, alto // 2)
        poste = pygame.Rect(
            ancho // 2 - 10,
            tabla.bottom,
            20,
            alto - tabla.bottom,
        )
        pygame.draw.rect(superficie, (64, 37, 24), poste)
        pygame.draw.rect(superficie, (45, 29, 25), tabla)
        pygame.draw.rect(
            superficie,
            (205, 141, 73),
            tabla.inflate(-10, -10),
        )
        texto = self.fuente_titulo.render(
            "FIN",
            False,
            (45, 29, 25),
        )
        superficie.blit(
            texto,
            texto.get_rect(center=tabla.center),
        )
        return superficie

    def desbloquear(self):
        self.desbloqueado = True

    def bloquear(self):
        self.desbloqueado = False
        self.cerrar_menu()

    def cerrar_menu(self):
        self.menu_visible = False
        self.hover_menu = False
        self.hover_siguiente = False

    def abrir_menu(self):
        if not self.desbloqueado or not self.jugador_cerca:
            return False
        self.menu_visible = True
        self.hover_menu = False
        self.hover_siguiente = False
        return True

    def obtener_rect_pantalla(self, camara_x):
        return pygame.Rect(
            round(self.rect.x - camara_x),
            self.rect.y,
            self.rect.width,
            self.rect.height,
        )

    def obtener_zona_pantalla(self, camara_x):
        return pygame.Rect(
            round(self.zona_interaccion.x - camara_x),
            self.zona_interaccion.y,
            self.zona_interaccion.width,
            self.zona_interaccion.height,
        )

    def actualizar_cercania(self, jugador_rect_mundo):
        self.jugador_cerca = bool(
            jugador_rect_mundo
            and jugador_rect_mundo.colliderect(
                self.zona_interaccion
            )
        )
        return self.jugador_cerca

    def manejar_evento(
        self,
        evento,
        jugador_rect_mundo,
        camara_x,
    ):
        self.actualizar_cercania(jugador_rect_mundo)

        if self.menu_visible:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.cerrar_menu()
                return self.EVENTO_CONSUMIDO

            if evento.type == pygame.MOUSEMOTION:
                self._actualizar_hover(evento.pos)
                return self.EVENTO_CONSUMIDO

            if (
                evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):
                self._actualizar_hover(evento.pos)
                if self.boton_menu_rect.collidepoint(evento.pos):
                    return self.ACCION_MENU
                if (
                    self.siguiente_disponible
                    and self.boton_siguiente_rect.collidepoint(
                        evento.pos
                    )
                ):
                    return self.ACCION_SIGUIENTE
                return self.EVENTO_CONSUMIDO

            if evento.type in (
                pygame.KEYUP,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEWHEEL,
            ):
                return self.EVENTO_CONSUMIDO
            return None

        if not self.desbloqueado or not self.jugador_cerca:
            return None

        if (
            evento.type == pygame.KEYDOWN
            and evento.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
            )
        ):
            self.abrir_menu()
            return self.EVENTO_CONSUMIDO

        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.obtener_rect_pantalla(
                camara_x
            ).collidepoint(evento.pos)
        ):
            self.abrir_menu()
            return self.EVENTO_CONSUMIDO
        return None

    def _actualizar_hover(self, posicion):
        self.hover_menu = self.boton_menu_rect.collidepoint(
            posicion
        )
        self.hover_siguiente = (
            self.siguiente_disponible
            and self.boton_siguiente_rect.collidepoint(
                posicion
            )
        )

    def _recalcular_interfaz(self):
        if self.imagen_panel is not None:
            self.panel_rect = self.imagen_panel.get_rect(
                center=(
                    round(self.ancho_pantalla * CENTRO_X_PANEL),
                    round(self.alto_pantalla * CENTRO_Y_PANEL),
                )
            )
        else:
            ancho_panel = min(
                self.ancho_pantalla - MARGEN_X_PANEL_PANTALLA,
                round(ANCHO_PANEL_RESPALDO_BASE * self.escala_juego),
            )
            alto_panel = min(
                self.alto_pantalla - MARGEN_Y_PANEL_PANTALLA,
                round(ALTO_PANEL_RESPALDO_BASE * self.escala_juego),
            )
            self.panel_rect = pygame.Rect(
                round(self.ancho_pantalla * CENTRO_X_PANEL)
                - ancho_panel // 2,
                round(self.alto_pantalla * CENTRO_Y_PANEL)
                - alto_panel // 2,
                ancho_panel,
                alto_panel,
            )

        ancho_menu = (
            self.imagen_boton_menu.get_width()
            if self.imagen_boton_menu is not None
            else round(ANCHO_BOTON_RESPALDO_BASE * self.escala_juego)
        )
        alto_menu = (
            self.imagen_boton_menu.get_height()
            if self.imagen_boton_menu is not None
            else round(ALTO_BOTON_RESPALDO_BASE * self.escala_juego)
        )
        ancho_siguiente = (
            self.imagen_boton_siguiente.get_width()
            if self.imagen_boton_siguiente is not None
            else ancho_menu
        )
        alto_siguiente = (
            self.imagen_boton_siguiente.get_height()
            if self.imagen_boton_siguiente is not None
            else alto_menu
        )

        separacion = round(SEPARACION_BOTONES_BASE * self.escala_juego)
        ancho_total = ancho_menu + separacion + ancho_siguiente
        x_inicial = (
            self.panel_rect.centerx
            - ancho_total // 2
            + round(
                DESPLAZAMIENTO_X_BOTONES_BASE
                * self.escala_juego
            )
        )
        margen_inferior = round(
            MARGEN_INFERIOR_BOTONES_BASE * self.escala_juego
        )
        desplazamiento_y = round(
            DESPLAZAMIENTO_Y_BOTONES_BASE * self.escala_juego
        )
        y_menu = (
            self.panel_rect.bottom
            - margen_inferior
            - alto_menu
            + desplazamiento_y
        )
        y_siguiente = (
            self.panel_rect.bottom
            - margen_inferior
            - alto_siguiente
            + desplazamiento_y
        )

        self.boton_menu_rect = pygame.Rect(
            x_inicial,
            y_menu,
            ancho_menu,
            alto_menu,
        )
        self.boton_siguiente_rect = pygame.Rect(
            x_inicial + ancho_menu + separacion,
            y_siguiente,
            ancho_siguiente,
            alto_siguiente,
        )

    @staticmethod
    def _dibujar_caja_pixel(
        pantalla,
        rect,
        fondo,
        borde=(18, 28, 45),
        grosor=7,
    ):
        pygame.draw.rect(
            pantalla,
            (5, 10, 18),
            rect.move(8, 8),
        )
        pygame.draw.rect(pantalla, borde, rect)
        pygame.draw.rect(
            pantalla,
            fondo,
            rect.inflate(-grosor * 2, -grosor * 2),
        )

    @staticmethod
    def _dibujar_texto_centrado(
        pantalla,
        texto,
        fuente,
        color,
        centro,
    ):
        superficie = fuente.render(texto, False, color)
        pantalla.blit(
            superficie,
            superficie.get_rect(center=centro),
        )

    def _dibujar_boton(
        self,
        pantalla,
        rect,
        imagen,
        imagen_hover,
        texto,
        hover=False,
        habilitado=True,
    ):
        if imagen is not None:
            if not habilitado:
                superficie = self.imagen_boton_siguiente_bloqueado
                if superficie is None:
                    superficie = imagen
            elif hover and imagen_hover is not None:
                superficie = imagen_hover
            else:
                superficie = imagen

            pantalla.blit(
                superficie,
                superficie.get_rect(center=rect.center),
            )
            color_texto = (
                (255, 255, 255)
                if habilitado
                else (205, 208, 214)
            )
            sombra = self.fuente_boton.render(
                texto,
                False,
                (35, 43, 58),
            )
            rotulo = self.fuente_boton.render(
                texto,
                False,
                color_texto,
            )
            pantalla.blit(
                sombra,
                sombra.get_rect(
                    center=(rect.centerx + 2, rect.centery + 2)
                ),
            )
            pantalla.blit(
                rotulo,
                rotulo.get_rect(center=rect.center),
            )
            return

        fondo = (
            (120, 124, 128)
            if not habilitado
            else (255, 220, 100)
            if hover
            else (240, 239, 224)
        )
        self._dibujar_caja_pixel(
            pantalla,
            rect,
            fondo,
            grosor=6,
        )
        self._dibujar_texto_centrado(
            pantalla,
            texto,
            self.fuente_boton,
            (18, 28, 45),
            rect.center,
        )

    def _dibujar_candado_respaldo(
        self,
        pantalla,
        centro,
    ):
        ancho = round(ANCHO_CANDADO_RESPALDO_BASE * self.escala_juego)
        alto = round(ALTO_CANDADO_RESPALDO_BASE * self.escala_juego)
        cuerpo = pygame.Rect(0, 0, ancho, alto)
        cuerpo.center = centro
        pygame.draw.rect(
            pantalla,
            (218, 170, 49),
            cuerpo,
        )
        pygame.draw.rect(
            pantalla,
            (54, 45, 34),
            cuerpo,
            max(2, round(3 * self.escala_juego)),
        )
        pygame.draw.arc(
            pantalla,
            (218, 170, 49),
            (
                cuerpo.x + ancho // 5,
                cuerpo.y - alto // 2,
                ancho * 3 // 5,
                alto,
            ),
            0,
            3.14159,
            max(3, round(5 * self.escala_juego)),
        )

    def dibujar_mundo(self, pantalla, camara_x):
        if not self.desbloqueado and not self.mostrar_bloqueado:
            return

        rect_pantalla = self.obtener_rect_pantalla(camara_x)
        pantalla.blit(self.imagen, rect_pantalla.topleft)

        if self.desbloqueado:
            return

        centro_candado = (
            rect_pantalla.centerx,
            rect_pantalla.top
            + round(rect_pantalla.height * POSICION_Y_CANDADO),
        )
        if self.imagen_candado is not None:
            rect_candado = self.imagen_candado.get_rect(
                center=centro_candado
            )
            pantalla.blit(
                self.imagen_candado,
                rect_candado.topleft,
            )
        else:
            self._dibujar_candado_respaldo(
                pantalla,
                centro_candado,
            )

    def dibujar_interfaz(
        self,
        pantalla,
        camara_x,
        jugador_rect_mundo,
    ):
        self.actualizar_cercania(jugador_rect_mundo)

        if self.jugador_cerca and not self.menu_visible:
            mensaje = (
                "Haz clic en el cartel o presiona ENTER"
                if self.desbloqueado
                else "Completa todas las practicas para salir"
            )
            texto = self.fuente_mensaje.render(
                mensaje,
                False,
                (18, 28, 45),
            )
            ancho = texto.get_width() + RELLENO_X_MENSAJE
            alto = texto.get_height() + RELLENO_Y_MENSAJE
            rect_mensaje = pygame.Rect(
                (self.ancho_pantalla - ancho) // 2,
                self.alto_pantalla - alto - MARGEN_INFERIOR_MENSAJE_BASE,
                ancho,
                alto,
            )
            self._dibujar_caja_pixel(
                pantalla,
                rect_mensaje,
                (246, 242, 232),
                grosor=5,
            )
            pantalla.blit(
                texto,
                texto.get_rect(center=rect_mensaje.center),
            )

        if not self.menu_visible:
            return

        self.capa_oscura.fill((0, 0, 0, 175))
        pantalla.blit(self.capa_oscura, (0, 0))

        if self.imagen_panel is not None:
            pantalla.blit(
                self.imagen_panel,
                self.panel_rect.topleft,
            )
        else:
            self._dibujar_caja_pixel(
                pantalla,
                self.panel_rect,
                (246, 242, 232),
                grosor=9,
            )

        titulo_y = (
            self.panel_rect.y
            + round(self.panel_rect.height * POSICION_Y_TITULO)
        )
        subtitulo_y = (
            self.panel_rect.y
            + round(self.panel_rect.height * POSICION_Y_SUBTITULO)
        )
        self._dibujar_texto_centrado(
            pantalla,
            "\u00a1LECCI\u00d3N COMPLETADA!",
            self.fuente_titulo,
            (18, 28, 45),
            (self.panel_rect.centerx, titulo_y),
        )
        self._dibujar_texto_centrado(
            pantalla,
            "\u00bfQu\u00e9 deseas hacer ahora?",
            self.fuente_texto,
            (57, 76, 96),
            (self.panel_rect.centerx, subtitulo_y),
        )

        self._dibujar_boton(
            pantalla,
            self.boton_menu_rect,
            self.imagen_boton_menu,
            self.imagen_boton_menu_hover,
            "SALIR",
            hover=self.hover_menu,
            habilitado=True,
        )
        texto_siguiente = (
            "SIGUIENTE"
            if self.siguiente_disponible
            else "\u00daLTIMA LECCI\u00d3N"
        )
        self._dibujar_boton(
            pantalla,
            self.boton_siguiente_rect,
            self.imagen_boton_siguiente,
            self.imagen_boton_siguiente_hover,
            texto_siguiente,
            hover=self.hover_siguiente,
            habilitado=self.siguiente_disponible,
        )

        ayuda = self.fuente_ayuda.render(
            "ESC para cerrar",
            False,
            (92, 98, 108),
        )
        pantalla.blit(
            ayuda,
            ayuda.get_rect(
                center=(
                    self.panel_rect.centerx,
                    self.panel_rect.bottom
                    - round(MARGEN_INFERIOR_AYUDA_BASE * self.escala_juego),
                )
            ),
        )
