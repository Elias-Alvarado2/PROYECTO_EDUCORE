from pathlib import Path

import pygame


class CartelFinal:
    """
    Cartel reutilizable para terminar una lección.

    Flujo:
    1. El cartel permanece bloqueado hasta completar las prácticas.
    2. El jugador se acerca.
    3. Hace clic en el cartel o presiona ENTER.
    4. Aparecen las opciones:
       - Salir al menú.
       - Ir a la siguiente lección.
    """

    ACCION_MENU = "menu_niveles"
    ACCION_SIGUIENTE = "siguiente_leccion"
    EVENTO_CONSUMIDO = "__cartel_final_evento_consumido__"

    def __init__(
        self,
        x_mundo,
        suelo_y,
        ancho_pantalla=1920,
        alto_pantalla=1080,
        escala_juego=1.5,
        ruta_imagen=None,
        ruta_fuente=None,
        siguiente_disponible=True,
        mostrar_bloqueado=True,
    ):
        self.x_mundo = int(x_mundo)
        self.suelo_y = int(suelo_y)
        self.ancho_pantalla = int(ancho_pantalla)
        self.alto_pantalla = int(alto_pantalla)
        self.escala_juego = float(escala_juego)

        self.ruta_imagen = (
            Path(ruta_imagen)
            if ruta_imagen
            else None
        )
        self.ruta_fuente = (
            Path(ruta_fuente)
            if ruta_fuente
            else None
        )

        self.siguiente_disponible = bool(siguiente_disponible)
        self.mostrar_bloqueado = bool(mostrar_bloqueado)

        self.desbloqueado = False
        self.menu_visible = False
        self.jugador_cerca = False

        self.hover_menu = False
        self.hover_siguiente = False

        self.fuente_titulo = self._cargar_fuente(46)
        self.fuente_boton = self._cargar_fuente(31)
        self.fuente_texto = self._cargar_fuente(27)
        self.fuente_cartel = self._cargar_fuente(28)

        self.imagen = self._cargar_o_crear_imagen()
        self.rect = self.imagen.get_rect()
        self.rect.x = self.x_mundo
        self.rect.bottom = self.suelo_y

        margen_horizontal = round(95 * self.escala_juego)
        margen_vertical = round(45 * self.escala_juego)

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

    # ========================================================
    # CARGA Y CREACIÓN DEL CARTEL
    # ========================================================

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

    def _cargar_o_crear_imagen(self):
        if self.ruta_imagen and self.ruta_imagen.exists():
            imagen = pygame.image.load(
                str(self.ruta_imagen)
            ).convert_alpha()

            rect_visible = imagen.get_bounding_rect(min_alpha=8)

            if rect_visible.width > 0 and rect_visible.height > 0:
                imagen = imagen.subsurface(rect_visible).copy()

            ancho = max(
                1,
                round(imagen.get_width() * self.escala_juego),
            )
            alto = max(
                1,
                round(imagen.get_height() * self.escala_juego),
            )

            return pygame.transform.scale(
                imagen,
                (ancho, alto),
            )

        return self._crear_cartel_pixel()

    def _crear_cartel_pixel(self):
        """
        Crea un cartel pixel art sin necesitar una imagen PNG.

        Si después agregas assets/ui/cartel_final.png, el motor utilizará
        automáticamente esa imagen en lugar de este diseño.
        """
        ancho = round(190 * self.escala_juego)
        alto = round(145 * self.escala_juego)
        pixel = max(4, round(4 * self.escala_juego))

        superficie = pygame.Surface(
            (ancho, alto),
            pygame.SRCALPHA,
        )

        color_madera_oscura = (69, 38, 26)
        color_madera_media = (126, 72, 39)
        color_madera_clara = (195, 132, 69)
        color_tabla = (230, 195, 125)
        color_borde = (31, 27, 31)
        color_texto = (31, 27, 31)

        poste_ancho = round(22 * self.escala_juego)
        poste_alto = round(82 * self.escala_juego)
        poste_y = alto - poste_alto

        poste_izquierdo_x = round(28 * self.escala_juego)
        poste_derecho_x = ancho - poste_izquierdo_x - poste_ancho

        for poste_x in (poste_izquierdo_x, poste_derecho_x):
            pygame.draw.rect(
                superficie,
                color_borde,
                (
                    poste_x - pixel,
                    poste_y,
                    poste_ancho + pixel * 2,
                    poste_alto,
                ),
            )
            pygame.draw.rect(
                superficie,
                color_madera_media,
                (
                    poste_x,
                    poste_y,
                    poste_ancho,
                    poste_alto,
                ),
            )
            pygame.draw.rect(
                superficie,
                color_madera_clara,
                (
                    poste_x + pixel,
                    poste_y + pixel,
                    pixel,
                    poste_alto - pixel * 2,
                ),
            )
            pygame.draw.rect(
                superficie,
                color_madera_oscura,
                (
                    poste_x + poste_ancho - pixel * 2,
                    poste_y + pixel,
                    pixel,
                    poste_alto - pixel * 2,
                ),
            )

        tabla_rect = pygame.Rect(
            pixel,
            pixel,
            ancho - pixel * 2,
            round(77 * self.escala_juego),
        )

        pygame.draw.rect(
            superficie,
            color_borde,
            tabla_rect,
        )

        tabla_interior = tabla_rect.inflate(
            -pixel * 3,
            -pixel * 3,
        )
        pygame.draw.rect(
            superficie,
            color_madera_media,
            tabla_interior,
        )

        centro = tabla_interior.inflate(
            -pixel * 3,
            -pixel * 3,
        )
        pygame.draw.rect(
            superficie,
            color_tabla,
            centro,
        )

        pygame.draw.rect(
            superficie,
            color_madera_clara,
            (
                centro.x + pixel,
                centro.y + pixel,
                centro.width - pixel * 2,
                pixel,
            ),
        )

        texto = self.fuente_cartel.render(
            "FIN",
            False,
            color_texto,
        )
        superficie.blit(
            texto,
            texto.get_rect(center=centro.center),
        )

        return superficie

    # ========================================================
    # ESTADO
    # ========================================================

    def desbloquear(self):
        self.desbloqueado = True

    def bloquear(self):
        self.desbloqueado = False
        self.menu_visible = False

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

    # ========================================================
    # EVENTOS
    # ========================================================

    def manejar_evento(
        self,
        evento,
        jugador_rect_mundo,
        camara_x,
    ):
        """
        Devuelve:
        - None: el cartel no utilizó el evento.
        - EVENTO_CONSUMIDO: el cartel utilizó el evento.
        - ACCION_MENU: salir al menú de niveles.
        - ACCION_SIGUIENTE: abrir la siguiente lección.
        """
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

            # Mientras el menú está abierto, bloquea los controles del juego.
            if evento.type in (
                pygame.KEYUP,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEWHEEL,
            ):
                return self.EVENTO_CONSUMIDO

            return None

        if not self.desbloqueado or not self.jugador_cerca:
            return None

        if evento.type == pygame.KEYDOWN:
            if evento.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
            ):
                self.abrir_menu()
                return self.EVENTO_CONSUMIDO

        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):
            rect_pantalla = self.obtener_rect_pantalla(
                camara_x
            )

            if rect_pantalla.collidepoint(evento.pos):
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

    # ========================================================
    # INTERFAZ
    # ========================================================

    def _recalcular_interfaz(self):
        ancho_panel = min(
            self.ancho_pantalla - 120,
            round(920 * self.escala_juego),
        )
        alto_panel = min(
            self.alto_pantalla - 120,
            round(390 * self.escala_juego),
        )

        self.panel_rect = pygame.Rect(
            (self.ancho_pantalla - ancho_panel) // 2,
            (self.alto_pantalla - alto_panel) // 2,
            ancho_panel,
            alto_panel,
        )

        margen_x = round(70 * self.escala_juego)
        margen_inferior = round(62 * self.escala_juego)
        separacion = round(34 * self.escala_juego)

        ancho_boton = (
            self.panel_rect.width
            - margen_x * 2
            - separacion
        ) // 2
        alto_boton = round(78 * self.escala_juego)

        y_botones = (
            self.panel_rect.bottom
            - margen_inferior
            - alto_boton
        )

        self.boton_menu_rect = pygame.Rect(
            self.panel_rect.x + margen_x,
            y_botones,
            ancho_boton,
            alto_boton,
        )

        self.boton_siguiente_rect = pygame.Rect(
            self.boton_menu_rect.right + separacion,
            y_botones,
            ancho_boton,
            alto_boton,
        )

    def _dibujar_caja_pixel(
        self,
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
        pygame.draw.rect(
            pantalla,
            borde,
            rect,
        )
        pygame.draw.rect(
            pantalla,
            fondo,
            rect.inflate(-grosor * 2, -grosor * 2),
        )

        pixel = max(4, grosor - 1)

        for x, y in (
            (rect.x + pixel, rect.y + pixel),
            (rect.right - pixel * 2, rect.y + pixel),
            (rect.x + pixel, rect.bottom - pixel * 2),
            (rect.right - pixel * 2, rect.bottom - pixel * 2),
        ):
            pygame.draw.rect(
                pantalla,
                borde,
                (x, y, pixel, pixel),
            )

    def _dibujar_texto_centrado(
        self,
        pantalla,
        texto,
        fuente,
        color,
        centro,
    ):
        superficie = fuente.render(
            texto,
            False,
            color,
        )
        pantalla.blit(
            superficie,
            superficie.get_rect(center=centro),
        )

    def _dibujar_boton(
        self,
        pantalla,
        rect,
        texto,
        hover=False,
        habilitado=True,
    ):
        if not habilitado:
            fondo = (120, 124, 128)
            borde = (70, 74, 80)
            texto_color = (205, 207, 210)
        elif hover:
            fondo = (255, 220, 100)
            borde = (74, 48, 22)
            texto_color = (31, 27, 31)
        else:
            fondo = (240, 239, 224)
            borde = (18, 28, 45)
            texto_color = (18, 28, 45)

        self._dibujar_caja_pixel(
            pantalla,
            rect,
            fondo,
            borde=borde,
            grosor=6,
        )

        self._dibujar_texto_centrado(
            pantalla,
            texto,
            self.fuente_boton,
            texto_color,
            rect.center,
        )

    def dibujar_mundo(self, pantalla, camara_x):
        if not self.desbloqueado and not self.mostrar_bloqueado:
            return

        rect_pantalla = self.obtener_rect_pantalla(
            camara_x
        )

        pantalla.blit(
            self.imagen,
            rect_pantalla.topleft,
        )

        if not self.desbloqueado:
            capa_bloqueada = pygame.Surface(
                rect_pantalla.size,
                pygame.SRCALPHA,
            )
            capa_bloqueada.fill((25, 30, 38, 150))
            pantalla.blit(
                capa_bloqueada,
                rect_pantalla.topleft,
            )

            candado_ancho = round(34 * self.escala_juego)
            candado_alto = round(29 * self.escala_juego)
            candado = pygame.Rect(
                0,
                0,
                candado_ancho,
                candado_alto,
            )
            candado.center = rect_pantalla.center
            pygame.draw.rect(
                pantalla,
                (35, 39, 48),
                candado,
            )
            pygame.draw.rect(
                pantalla,
                (210, 172, 67),
                candado.inflate(-6, -6),
            )
            pygame.draw.arc(
                pantalla,
                (210, 172, 67),
                (
                    candado.x + 5,
                    candado.y - candado.height // 2,
                    candado.width - 10,
                    candado.height,
                ),
                0,
                3.14159,
                max(3, round(4 * self.escala_juego)),
            )

    def dibujar_interfaz(
        self,
        pantalla,
        camara_x,
        jugador_rect_mundo,
    ):
        self.actualizar_cercania(jugador_rect_mundo)

        if self.jugador_cerca and not self.menu_visible:
            if self.desbloqueado:
                mensaje = (
                    "Haz clic en el cartel o presiona ENTER"
                )
            else:
                mensaje = (
                    "Completa todas las prácticas para salir"
                )

            texto = self.fuente_texto.render(
                mensaje,
                False,
                (18, 28, 45),
            )

            ancho = texto.get_width() + 70
            alto = texto.get_height() + 34
            rect_mensaje = pygame.Rect(
                (self.ancho_pantalla - ancho) // 2,
                self.alto_pantalla - alto - 80,
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

        self._dibujar_caja_pixel(
            pantalla,
            self.panel_rect,
            (246, 242, 232),
            grosor=9,
        )

        titulo_y = self.panel_rect.y + round(
            72 * self.escala_juego
        )
        subtitulo_y = titulo_y + round(
            70 * self.escala_juego
        )

        self._dibujar_texto_centrado(
            pantalla,
            "¡LECCIÓN COMPLETADA!",
            self.fuente_titulo,
            (18, 28, 45),
            (self.panel_rect.centerx, titulo_y),
        )

        self._dibujar_texto_centrado(
            pantalla,
            "¿Qué deseas hacer ahora?",
            self.fuente_texto,
            (57, 76, 96),
            (self.panel_rect.centerx, subtitulo_y),
        )

        self._dibujar_boton(
            pantalla,
            self.boton_menu_rect,
            "SALIR AL MENÚ",
            hover=self.hover_menu,
            habilitado=True,
        )

        texto_siguiente = (
            "SIGUIENTE LECCIÓN"
            if self.siguiente_disponible
            else "ÚLTIMA LECCIÓN"
        )

        self._dibujar_boton(
            pantalla,
            self.boton_siguiente_rect,
            texto_siguiente,
            hover=self.hover_siguiente,
            habilitado=self.siguiente_disponible,
        )

        ayuda = self.fuente_texto.render(
            "ESC para cerrar",
            False,
            (92, 98, 108),
        )
        pantalla.blit(
            ayuda,
            (
                self.panel_rect.centerx
                - ayuda.get_width() // 2,
                self.panel_rect.bottom
                - round(30 * self.escala_juego),
            ),
        )
