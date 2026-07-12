from __future__ import annotations

from pathlib import Path

import pygame


PROYECTO_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROYECTO_DIR / "assets"
UI_DIR = ASSETS_DIR / "ui"
FUENTES_DIR = ASSETS_DIR / "FUENTES"
RUTA_FUENTE = FUENTES_DIR / "PixelOperator-Bold.ttf"


def _cargar_fuente(tamano: int) -> pygame.font.Font:
    tamano = max(12, int(tamano))
    if RUTA_FUENTE.exists():
        return pygame.font.Font(str(RUTA_FUENTE), tamano)
    return pygame.font.SysFont("consolas", tamano, bold=True)


def _cargar_png_recortado(ruta: Path) -> pygame.Surface | None:
    if not ruta.exists():
        return None

    try:
        imagen = pygame.image.load(str(ruta)).convert_alpha()
    except pygame.error:
        return None

    mascara = pygame.mask.from_surface(imagen)
    rects = mascara.get_bounding_rects()
    if not rects:
        return imagen

    rect_union = rects[0].copy()
    for rect in rects[1:]:
        rect_union.union_ip(rect)

    margen = 4
    rect_union.inflate_ip(margen * 2, margen * 2)
    rect_union = rect_union.clip(imagen.get_rect())
    return imagen.subsurface(rect_union).copy()


def _puntos_pixel(rect: pygame.Rect, corte: int = 8) -> list[tuple[int, int]]:
    corte = max(2, min(corte, rect.width // 4, rect.height // 4))
    return [
        (rect.left + corte, rect.top),
        (rect.right - corte, rect.top),
        (rect.right, rect.top + corte),
        (rect.right, rect.bottom - corte),
        (rect.right - corte, rect.bottom),
        (rect.left + corte, rect.bottom),
        (rect.left, rect.bottom - corte),
        (rect.left, rect.top + corte),
    ]


def _dividir_texto(texto: str, fuente: pygame.font.Font, ancho: int) -> list[str]:
    palabras = str(texto).split()
    if not palabras:
        return [""]

    lineas: list[str] = []
    actual = palabras[0]

    for palabra in palabras[1:]:
        prueba = f"{actual} {palabra}"
        if fuente.size(prueba)[0] <= ancho:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra

    lineas.append(actual)
    return lineas


class HuecoCodigo:
    def __init__(
        self,
        identificador: str,
        respuesta: str,
        rect: pygame.Rect,
        ancho_base: int,
        alto_base: int,
    ):
        self.identificador = identificador
        self.respuesta = str(respuesta)
        self.rect = pygame.Rect(rect)
        self.ancho_base = int(ancho_base)
        self.alto_base = int(alto_base)
        self.token_id: int | None = None

    def dibujar(self, superficie: pygame.Surface) -> None:
        sombra = self.rect.move(3, 4)
        pygame.draw.polygon(
            superficie,
            (3, 12, 23),
            _puntos_pixel(sombra, 7),
        )
        pygame.draw.polygon(
            superficie,
            (145, 208, 231),
            _puntos_pixel(self.rect, 7),
        )
        interior = self.rect.inflate(-6, -6)
        pygame.draw.polygon(
            superficie,
            (31, 48, 64),
            _puntos_pixel(interior, 5),
        )


class TokenCodigo:
    def __init__(
        self,
        identificador: int,
        texto: str,
        fuente: pygame.font.Font,
    ):
        self.identificador = int(identificador)
        self.texto = str(texto)
        self.fuente = fuente

        ancho_texto, alto_texto = fuente.size(self.texto)
        self.rect = pygame.Rect(
            0,
            0,
            max(70, ancho_texto + 34),
            max(48, alto_texto + 20),
        )

        self.hueco_actual: str | None = None
        self.arrastrando = False

    def dibujar(
        self,
        superficie: pygame.Surface,
        bloqueado: bool = False,
        estado: str = "normal",
        rect_dibujo: pygame.Rect | None = None,
    ) -> None:
        """Dibuja la opción sin alterar su rectángulo lógico.

        ``rect_dibujo`` permite aplicar el mismo rebote usado por los botones
        FALSO, VERDADERO y RESPONDER del formulario original. La zona de
        arrastre permanece en ``self.rect`` para que la animación no cambie
        las colisiones.
        """
        rect = pygame.Rect(rect_dibujo or self.rect)

        sombra = rect.move(3, 4)
        pygame.draw.polygon(
            superficie,
            (8, 28, 45),
            _puntos_pixel(sombra, 8),
        )

        color_borde = (17, 53, 80)
        color_fondo = (170, 220, 240)
        color_texto = (14, 38, 58)

        if estado == "hover" and not bloqueado:
            color_borde = (245, 252, 255)
            color_fondo = (190, 232, 248)

        if estado == "clic" and not bloqueado:
            color_borde = (10, 39, 61)
            color_fondo = (137, 202, 229)

        if bloqueado:
            color_fondo = (151, 188, 202)
            color_texto = (52, 73, 86)

        pygame.draw.polygon(
            superficie,
            color_borde,
            _puntos_pixel(rect, 8),
        )
        interior = rect.inflate(-6, -6)
        pygame.draw.polygon(
            superficie,
            color_fondo,
            _puntos_pixel(interior, 6),
        )

        texto = self.fuente.render(self.texto, False, color_texto)
        rect_texto = texto.get_rect(center=rect.center)

        if estado == "clic" and not bloqueado:
            rect_texto.y += 2

        superficie.blit(texto, rect_texto)

class PantallaPracticaCodigo:
    """Formulario de arrastrar y soltar para completar código.

    Usa el fondo y los estados normal/hover/clic existentes de assets/ui.
    Las opciones aparecen directamente sobre el fondo beige y todos los
    botones utilizan la misma animación de rebote de la práctica original.
    """

    def __init__(self, ancho: int = 1920, alto: int = 1080):
        self.ancho = int(ancho)
        self.alto = int(alto)
        self.visible = False
        self.respondido = False
        self.respuesta_final: bool | None = None
        self.resultado = ""

        self.pregunta = ""
        self.configuracion: dict = {}
        self.fragmentos: list[dict] = []
        self.huecos: dict[str, HuecoCodigo] = {}
        self.tokens: list[TokenCodigo] = []
        self.token_arrastrado: TokenCodigo | None = None
        self.offset_arrastre = (0, 0)
        self.boton_presionado: str | None = None

        # Misma animación de rebote del formulario FALSO/VERDADERO.
        self.desplazamiento_rebote = 10
        self.duracion_subida_rebote = 0.10
        self.duracion_bajada_rebote = 0.34
        self.estados_rebote: dict[str, dict[str, float | bool | int]] = {}
        self._reiniciar_rebotes()

        self._cache_escalado: dict[tuple[int, int, int], pygame.Surface] = {}
        self._sombra = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self._sombra.fill((0, 0, 0, 75))

        self.img_panel = self._cargar_panel()
        self.img_titulo = _cargar_png_recortado(
            UI_DIR / "practica" / "practica_cuadro.png"
        )
        self.img_cerrar = {
            estado: _cargar_png_recortado(
                UI_DIR / "btn_cerrar" / f"cerrar_{estado}.png"
            )
            for estado in ("normal", "hover", "clic")
        }
        self.img_verificar = {
            estado: _cargar_png_recortado(
                UI_DIR / "btn_responder" / f"responder_{estado}.png"
            )
            for estado in ("normal", "hover", "clic")
        }

        self.panel = pygame.Rect(0, 0, 0, 0)
        self.rect_cerrar = pygame.Rect(0, 0, 0, 0)
        self.rect_titulo = pygame.Rect(0, 0, 0, 0)
        self.rect_pregunta = pygame.Rect(0, 0, 0, 0)
        self.rect_codigo = pygame.Rect(0, 0, 0, 0)
        self.rect_opciones = pygame.Rect(0, 0, 0, 0)
        self.rect_resultado = pygame.Rect(0, 0, 0, 0)
        self.rect_verificar = pygame.Rect(0, 0, 0, 0)

        self.fuente_pregunta = _cargar_fuente(29)
        self.fuente_codigo = _cargar_fuente(31)
        self.fuente_opciones = _cargar_fuente(25)
        self.fuente_boton = _cargar_fuente(28)
        self.fuente_resultado = _cargar_fuente(25)
        self.calcular_rects()

    @staticmethod
    def _cargar_panel() -> pygame.Surface | None:
        """Carga únicamente un fondo completo de formulario.

        Usa las mismas rutas que la práctica de VERDADERO/FALSO. No carga
        ``cuadro_preguntas/cuadro.png`` porque ese PNG es una pieza interna,
        no el fondo beige completo.
        """
        rutas = (
            UI_DIR / "formulario.png",
            UI_DIR / "formulario_cuadro.png",
            UI_DIR / "cuadro_formulario.png",
            UI_DIR / "base_formulario.png",
            UI_DIR / "beige.png",
            UI_DIR / "fondo_beige.png",
            UI_DIR / "fondo.png",
            UI_DIR / "panel.png",
            UI_DIR / "formulario" / "formulario.png",
            UI_DIR / "formulario" / "formulario_cuadro.png",
            UI_DIR / "formulario" / "cuadro_formulario.png",
            UI_DIR / "formulario" / "base_formulario.png",
            UI_DIR / "formulario" / "beige.png",
            UI_DIR / "formulario" / "fondo_beige.png",
            UI_DIR / "formulario" / "fondo.png",
            UI_DIR / "formulario" / "panel.png",
        )

        for ruta in rutas:
            if not ruta.exists():
                continue
            try:
                return pygame.image.load(str(ruta)).convert_alpha()
            except pygame.error:
                continue

        return None

    def calcular_rects(self) -> None:
        panel_alto = min(round(self.alto * 0.82), 890)
        panel_ancho = round(panel_alto * (1448 / 1080))

        if panel_ancho > round(self.ancho * 0.86):
            panel_ancho = round(self.ancho * 0.86)
            panel_alto = round(panel_ancho * (1080 / 1448))

        self.panel = pygame.Rect(0, 0, panel_ancho, panel_alto)
        self.panel.center = (self.ancho // 2, self.alto // 2)

        sx = self.panel.width / 1448
        sy = self.panel.height / 1080

        def rr(x: int, y: int, w: int, h: int) -> pygame.Rect:
            return pygame.Rect(
                self.panel.x + round(x * sx),
                self.panel.y + round(y * sy),
                round(w * sx),
                round(h * sy),
            )

        self.rect_cerrar = rr(38, 35, 78, 72)
        self.rect_titulo = rr(132, 43, 255, 62)
        self.rect_pregunta = rr(95, 145, 1258, 115)
        self.rect_codigo = rr(90, 282, 1268, 355)
        self.rect_opciones = rr(95, 670, 1258, 180)
        self.rect_resultado = rr(105, 882, 745, 90)
        self.rect_verificar = rr(885, 882, 415, 90)

        escala_fuente = min(sx, sy)
        self.fuente_pregunta = _cargar_fuente(round(38 * escala_fuente))
        self.fuente_codigo = _cargar_fuente(round(42 * escala_fuente))
        self.fuente_opciones = _cargar_fuente(round(34 * escala_fuente))
        self.fuente_boton = _cargar_fuente(round(38 * escala_fuente))
        self.fuente_resultado = _cargar_fuente(round(33 * escala_fuente))

    def iniciar(self, pregunta: str, configuracion: dict) -> None:
        self.visible = True
        self.respondido = False
        self.respuesta_final = None
        self.resultado = ""
        self.pregunta = str(pregunta)
        self.configuracion = dict(configuracion or {})
        self.token_arrastrado = None
        self.boton_presionado = None
        self.huecos = {}
        self.fragmentos = []
        self.tokens = []
        self.calcular_rects()
        self._crear_tokens()
        self._reiniciar_rebotes()
        self._recalcular_codigo()
        self._organizar_tokens()

    def cerrar(self) -> None:
        self.visible = False
        self.boton_presionado = None
        self.token_arrastrado = None
        self._reiniciar_rebotes()

    def _crear_tokens(self) -> None:
        for indice, opcion in enumerate(self.configuracion.get("opciones", [])):
            texto = opcion.get("texto", "") if isinstance(opcion, dict) else opcion
            self.tokens.append(TokenCodigo(indice, str(texto), self.fuente_opciones))

    def _obtener_token(self, token_id: int | None) -> TokenCodigo | None:
        if token_id is None:
            return None
        for token in self.tokens:
            if token.identificador == token_id:
                return token
        return None

    def _recalcular_codigo(self) -> None:
        huecos_anteriores = self.huecos
        self.fragmentos = []
        nuevos_huecos: dict[str, HuecoCodigo] = {}

        respuestas = self.configuracion.get("respuestas", {})
        lineas = self.configuracion.get("codigo", [])
        x_inicial = self.rect_codigo.x + 42
        y = self.rect_codigo.y + 38
        alto_linea = max(56, self.fuente_codigo.get_height() + 28)
        ancho_indentacion = max(35, round(self.fuente_codigo.size("    ")[0] * 0.78))

        for linea in lineas:
            x = x_inicial + int(linea.get("indentacion", 0)) * ancho_indentacion

            for segmento in linea.get("segmentos", []):
                if "texto" in segmento:
                    texto = str(segmento["texto"])
                    render = self.fuente_codigo.render(
                        texto,
                        False,
                        (241, 246, 250),
                    )
                    self.fragmentos.append({"superficie": render, "posicion": (x, y)})
                    x += render.get_width()
                    continue

                if "hueco" not in segmento:
                    continue

                identificador = str(segmento["hueco"])
                respuesta = str(respuestas.get(identificador, ""))
                ancho_respuesta, alto_respuesta = self.fuente_codigo.size(respuesta)
                ancho_base = int(
                    segmento.get("ancho", max(72, ancho_respuesta + 34))
                )
                alto_base = max(50, alto_respuesta + 20)

                token_id = None
                if identificador in huecos_anteriores:
                    token_id = huecos_anteriores[identificador].token_id

                token = self._obtener_token(token_id)
                ancho_hueco = ancho_base
                alto_hueco = alto_base

                if token is not None:
                    ancho_hueco = max(ancho_base, token.rect.width + 12)
                    alto_hueco = max(alto_base, token.rect.height + 10)

                rect = pygame.Rect(x, y - 8, ancho_hueco, alto_hueco)
                hueco = HuecoCodigo(
                    identificador,
                    respuesta,
                    rect,
                    ancho_base,
                    alto_base,
                )
                hueco.token_id = token_id
                nuevos_huecos[identificador] = hueco
                x += ancho_hueco + 8

            y += alto_linea

        self.huecos = nuevos_huecos
        self._actualizar_tokens_colocados()

    def _organizar_tokens(self) -> None:
        libres = [
            token
            for token in self.tokens
            if token.hueco_actual is None and not token.arrastrando
        ]
        x = self.rect_opciones.x
        y = self.rect_opciones.y + 8
        limite = self.rect_opciones.right
        separacion_x = 16
        separacion_y = 14

        for token in libres:
            if x + token.rect.width > limite:
                x = self.rect_opciones.x
                y += token.rect.height + separacion_y
            token.rect.topleft = (x, y)
            x += token.rect.width + separacion_x

    def _actualizar_tokens_colocados(self) -> None:
        for token in self.tokens:
            if token.arrastrando or token.hueco_actual is None:
                continue
            hueco = self.huecos.get(token.hueco_actual)
            if hueco is not None:
                token.rect.center = hueco.rect.center

    def _iniciar_arrastre(self, token: TokenCodigo, posicion: tuple[int, int]) -> None:
        if self.respondido:
            return

        token.arrastrando = True
        self.token_arrastrado = token
        self.offset_arrastre = (
            posicion[0] - token.rect.x,
            posicion[1] - token.rect.y,
        )

        if token.hueco_actual is not None:
            hueco = self.huecos.get(token.hueco_actual)
            if hueco is not None:
                hueco.token_id = None
            token.hueco_actual = None
            self._recalcular_codigo()
            self._organizar_tokens()

        self.resultado = ""

    def _terminar_arrastre(self) -> None:
        if self.token_arrastrado is None:
            return

        token = self.token_arrastrado
        destino: HuecoCodigo | None = None

        for hueco in self.huecos.values():
            if hueco.rect.colliderect(token.rect):
                destino = hueco
                break

        if destino is not None:
            anterior = self._obtener_token(destino.token_id)
            if anterior is not None and anterior is not token:
                anterior.hueco_actual = None

            destino.token_id = token.identificador
            token.hueco_actual = destino.identificador
        else:
            token.hueco_actual = None

        token.arrastrando = False
        self.token_arrastrado = None
        self._recalcular_codigo()
        self._organizar_tokens()

    def verificar(self) -> None:
        if self.respondido:
            self.cerrar()
            return

        if any(hueco.token_id is None for hueco in self.huecos.values()):
            self.resultado = "Completa todos los espacios"
            return

        correcto = True
        for hueco in self.huecos.values():
            token = self._obtener_token(hueco.token_id)
            if token is None or token.texto != hueco.respuesta:
                correcto = False
                break

        self.respondido = True
        self.respuesta_final = correcto
        self.resultado = "Correcto!" if correcto else "Incorrecto!"

    def manejar_evento(self, evento: pygame.event.Event) -> bool:
        if not self.visible:
            return False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.cerrar()
                return True
            if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.verificar()
                return True

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_cerrar.collidepoint(evento.pos):
                self.boton_presionado = "cerrar"
                return True
            if self.rect_verificar.collidepoint(evento.pos):
                self.boton_presionado = "verificar"
                return True

            if not self.respondido:
                for token in reversed(self.tokens):
                    if token.rect.collidepoint(evento.pos):
                        self._iniciar_arrastre(token, evento.pos)
                        return True
            return True

        if evento.type == pygame.MOUSEMOTION and self.token_arrastrado is not None:
            mx, my = evento.pos
            ox, oy = self.offset_arrastre
            self.token_arrastrado.rect.topleft = (mx - ox, my - oy)
            return True

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.token_arrastrado is not None:
                self._terminar_arrastre()
                return True

            if (
                self.boton_presionado == "cerrar"
                and self.rect_cerrar.collidepoint(evento.pos)
            ):
                self.cerrar()
            elif (
                self.boton_presionado == "verificar"
                and self.rect_verificar.collidepoint(evento.pos)
            ):
                self.verificar()

            self.boton_presionado = None
            return True

        return True

    @staticmethod
    def _crear_estado_rebote() -> dict[str, float | bool | int]:
        return {
            "encima_anterior": False,
            "animando": False,
            "tiempo": 0.0,
            "offset_y": 0,
        }

    def _reiniciar_rebotes(self) -> None:
        nombres = ["cerrar", "verificar"]
        nombres.extend(f"token_{token.identificador}" for token in self.tokens)
        self.estados_rebote = {
            nombre: self._crear_estado_rebote()
            for nombre in nombres
        }

    @staticmethod
    def _ease_out_bounce(progreso: float) -> float:
        """Curva OutBounce idéntica a la usada por la práctica original."""
        n1 = 7.5625
        d1 = 2.75

        if progreso < 1 / d1:
            return n1 * progreso * progreso
        if progreso < 2 / d1:
            progreso -= 1.5 / d1
            return n1 * progreso * progreso + 0.75
        if progreso < 2.5 / d1:
            progreso -= 2.25 / d1
            return n1 * progreso * progreso + 0.9375

        progreso -= 2.625 / d1
        return n1 * progreso * progreso + 0.984375

    def actualizar(self, dt: float) -> None:
        if not self.visible:
            return

        mouse_pos = pygame.mouse.get_pos()
        rects: dict[str, pygame.Rect] = {
            "cerrar": self.rect_cerrar,
            "verificar": self.rect_verificar,
        }

        if not self.respondido:
            for token in self.tokens:
                if not token.arrastrando:
                    rects[f"token_{token.identificador}"] = token.rect

        desplazamiento = max(8, round(self.desplazamiento_rebote * (self.panel.height / 1080)))

        # Los botones que ya no están activos vuelven a su posición normal.
        for nombre, estado in self.estados_rebote.items():
            if nombre not in rects:
                estado["encima_anterior"] = False
                estado["animando"] = False
                estado["tiempo"] = 0.0
                estado["offset_y"] = 0

        for nombre, rect in rects.items():
            estado = self.estados_rebote.setdefault(
                nombre,
                self._crear_estado_rebote(),
            )
            encima = rect.collidepoint(mouse_pos)

            if encima and not bool(estado["encima_anterior"]):
                estado["animando"] = True
                estado["tiempo"] = 0.0

            estado["encima_anterior"] = encima

            if not bool(estado["animando"]):
                estado["offset_y"] = 0
                continue

            estado["tiempo"] = float(estado["tiempo"]) + max(0.0, float(dt))
            tiempo = float(estado["tiempo"])

            if tiempo <= self.duracion_subida_rebote:
                progreso = min(tiempo / self.duracion_subida_rebote, 1.0)
                suavizado = 1.0 - (1.0 - progreso) ** 2
                estado["offset_y"] = -round(desplazamiento * suavizado)
                continue

            tiempo_bajada = tiempo - self.duracion_subida_rebote
            if tiempo_bajada <= self.duracion_bajada_rebote:
                progreso = min(tiempo_bajada / self.duracion_bajada_rebote, 1.0)
                rebote = self._ease_out_bounce(progreso)
                estado["offset_y"] = -round(desplazamiento * (1.0 - rebote))
                continue

            estado["animando"] = False
            estado["tiempo"] = 0.0
            estado["offset_y"] = 0

    def _obtener_offset_rebote(self, nombre: str) -> int:
        estado = self.estados_rebote.get(nombre)
        if estado is None:
            return 0
        return int(estado.get("offset_y", 0))

    def _rect_animado(self, nombre: str, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(rect).move(0, self._obtener_offset_rebote(nombre))

    def _estado_boton(self, nombre: str, rect: pygame.Rect) -> str:
        encima = rect.collidepoint(pygame.mouse.get_pos())
        if self.boton_presionado == nombre and encima:
            return "clic"
        if encima:
            return "hover"
        return "normal"

    def _estado_token(self, token: TokenCodigo) -> str:
        if token.arrastrando:
            return "clic"
        if not self.respondido and token.rect.collidepoint(pygame.mouse.get_pos()):
            return "hover"
        return "normal"

    def _blit_escalado(
        self,
        superficie: pygame.Surface,
        imagen: pygame.Surface | None,
        rect: pygame.Rect,
    ) -> bool:
        if imagen is None:
            return False
        clave = (id(imagen), rect.width, rect.height)
        escalada = self._cache_escalado.get(clave)
        if escalada is None:
            escalada = pygame.transform.scale(imagen, rect.size)
            self._cache_escalado[clave] = escalada
        superficie.blit(escalada, rect)
        return True

    def _dibujar_panel_respaldo(self, superficie: pygame.Surface) -> None:
        """Dibuja el mismo fondo beige del formulario VERDADERO/FALSO."""
        escala_y = self.panel.height / 1086
        corte = max(10, round(32 * escala_y))
        desplazamiento = max(3, round(8 * escala_y))

        sombra = self.panel.move(desplazamiento, desplazamiento)
        pygame.draw.polygon(
            superficie,
            (5, 21, 45),
            _puntos_pixel(sombra, corte),
        )
        pygame.draw.polygon(
            superficie,
            (8, 35, 70),
            _puntos_pixel(self.panel, corte),
        )

        interior = self.panel.inflate(-16, -16)
        pygame.draw.polygon(
            superficie,
            (255, 239, 214),
            _puntos_pixel(interior, max(2, corte - 8)),
        )

    def _dibujar_panel_codigo(self, superficie: pygame.Surface) -> None:
        sombra = self.rect_codigo.move(5, 6)
        pygame.draw.polygon(superficie, (6, 17, 29), _puntos_pixel(sombra, 13))
        borde = self.rect_codigo.inflate(7, 7)
        pygame.draw.polygon(superficie, (222, 238, 241), _puntos_pixel(borde, 14))
        pygame.draw.polygon(superficie, (12, 43, 72), _puntos_pixel(self.rect_codigo, 12))
        interior = self.rect_codigo.inflate(-7, -7)
        pygame.draw.polygon(superficie, (10, 23, 38), _puntos_pixel(interior, 10))

    def _dibujar_texto_pregunta(self, superficie: pygame.Surface) -> None:
        lineas = _dividir_texto(
            self.pregunta,
            self.fuente_pregunta,
            self.rect_pregunta.width,
        )
        salto = self.fuente_pregunta.get_height() + 5
        alto = len(lineas) * salto
        y = self.rect_pregunta.centery - alto // 2
        for linea in lineas:
            render = self.fuente_pregunta.render(linea, False, (18, 47, 70))
            superficie.blit(render, (self.rect_pregunta.x, y))
            y += salto

    def _dibujar_boton_verificar(self, superficie: pygame.Surface) -> None:
        estado = self._estado_boton(
            "verificar",
            self.rect_verificar,
        )

        rect_animado = self._rect_animado(
            "verificar",
            self.rect_verificar,
        )

        imagen = (
            self.img_verificar.get(estado)
            or self.img_verificar.get("normal")
        )

        # Dibuja únicamente el PNG del botón.
        # El texto ya viene incluido en la imagen.
        self._blit_escalado(
            superficie,
            imagen,
            rect_animado,
        )
        if self.respondido:
            texto_boton="CONTINUAR"
        else:
            texto_boton="RESPONDER"
        texto=self.fuente_boton.render(
            texto_boton,
            False,
            (255,255,255)
        )
        rect_texto = texto.get_rect(
            center=rect_animado.center
        )
        superficie.blit(texto,rect_texto)

    def _dibujar_cerrar(self, superficie: pygame.Surface) -> None:
        estado = self._estado_boton("cerrar", self.rect_cerrar)
        rect_animado = self._rect_animado("cerrar", self.rect_cerrar)
        imagen = self.img_cerrar.get(estado) or self.img_cerrar.get("normal")
        if self._blit_escalado(superficie, imagen, rect_animado):
            return

        pygame.draw.polygon(
            superficie,
            (130, 25, 25),
            _puntos_pixel(rect_animado, 9),
        )
        interior = rect_animado.inflate(-6, -6)
        pygame.draw.polygon(superficie, (240, 65, 55), _puntos_pixel(interior, 7))
        fuente = _cargar_fuente(max(18, rect_animado.height // 2))
        x = fuente.render("X", False, (255, 255, 255))
        superficie.blit(x, x.get_rect(center=rect_animado.center))

    def dibujar(self, superficie: pygame.Surface) -> None:
        if not self.visible:
            return

        superficie.blit(self._sombra, (0, 0))
        if not self._blit_escalado(superficie, self.img_panel, self.panel):
            self._dibujar_panel_respaldo(superficie)

        self._blit_escalado(superficie, self.img_titulo, self.rect_titulo)
        self._dibujar_cerrar(superficie)
        self._dibujar_texto_pregunta(superficie)

        self._dibujar_panel_codigo(superficie)

        for fragmento in self.fragmentos:
            superficie.blit(fragmento["superficie"], fragmento["posicion"])

        for hueco in self.huecos.values():
            hueco.dibujar(superficie)

        self._actualizar_tokens_colocados()

        for token in self.tokens:
            if token.arrastrando:
                continue

            nombre = f"token_{token.identificador}"
            rect_animado = self._rect_animado(nombre, token.rect)
            token.dibujar(
                superficie,
                bloqueado=self.respondido,
                estado=self._estado_token(token),
                rect_dibujo=rect_animado,
            )

        if self.token_arrastrado is not None:
            self.token_arrastrado.dibujar(
                superficie,
                estado="clic",
                rect_dibujo=self.token_arrastrado.rect,
            )

        if self.resultado:
            if self.resultado == "Correcto!":
                color = (20, 145, 78)
            elif self.resultado == "Incorrecto!":
                color = (205, 48, 48)
            else:
                color = (145, 91, 20)

            render = self.fuente_resultado.render(self.resultado, False, color)
            superficie.blit(render, render.get_rect(center=self.rect_resultado.center))

        self._dibujar_boton_verificar(superficie)