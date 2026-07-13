from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pygame


PROYECTO_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROYECTO_DIR / "assets"
UI_DIR = ASSETS_DIR / "ui"
FUENTES_DIR = ASSETS_DIR / "FUENTES"
RUTA_FUENTE_PIXEL = FUENTES_DIR / "PixelOperator-Bold.ttf"

ANCHO = 1920
ALTO = 1080

ESTADOS_BOTON_FORMULARIO = ("normal", "hover", "clic")
BOTONES_RESPUESTA_FORMULARIO = ("falso", "verdadero", "responder")


@lru_cache(maxsize=None)
def cargar_fuente_pixel(tamano: int) -> pygame.font.Font:
    tamano = max(12, int(tamano))
    if RUTA_FUENTE_PIXEL.exists():
        return pygame.font.Font(str(RUTA_FUENTE_PIXEL), tamano)
    return pygame.font.SysFont("arial", tamano)


def cargar_imagen(ruta: Path, alpha: bool = True) -> pygame.Surface | None:
    if not ruta.exists():
        return None
    if alpha:
        return pygame.image.load(str(ruta)).convert_alpha()
    return pygame.image.load(str(ruta)).convert()


def recortar_transparencia_png(
    superficie: pygame.Surface | None,
    margen: int = 4,
) -> pygame.Surface | None:
    if superficie is None:
        return None

    superficie = superficie.convert_alpha()
    rect_visible = superficie.get_bounding_rect(min_alpha=8)

    if rect_visible.width <= 0 or rect_visible.height <= 0:
        return superficie

    rect_visible.x = max(0, rect_visible.x - margen)
    rect_visible.y = max(0, rect_visible.y - margen)
    rect_visible.width = min(
        superficie.get_width() - rect_visible.x,
        rect_visible.width + margen * 2,
    )
    rect_visible.height = min(
        superficie.get_height() - rect_visible.y,
        rect_visible.height + margen * 2,
    )

    recortada = pygame.Surface(
        (rect_visible.width, rect_visible.height),
        pygame.SRCALPHA,
    )
    recortada.blit(superficie, (0, 0), rect_visible)
    return recortada


def obtener_puntos_rect_pixel(
    rect: pygame.Rect,
    corte: int,
) -> list[tuple[int, int]]:
    return [
        (rect.x + corte, rect.y),
        (rect.right - corte, rect.y),
        (rect.right, rect.y + corte),
        (rect.right, rect.bottom - corte),
        (rect.right - corte, rect.bottom),
        (rect.x + corte, rect.bottom),
        (rect.x, rect.bottom - corte),
        (rect.x, rect.y + corte),
    ]


def dividir_lineas_por_ancho(
    texto: str,
    fuente: pygame.font.Font,
    ancho_max: int,
) -> list[str]:
    lineas: list[str] = []

    for bloque in str(texto).split("\n"):
        palabras = bloque.split(" ")
        linea = ""

        for palabra in palabras:
            prueba = linea + palabra + " "

            if fuente.size(prueba)[0] <= ancho_max:
                linea = prueba
            else:
                if linea:
                    lineas.append(linea)
                linea = palabra + " "

        if linea:
            lineas.append(linea)

    return lineas


class PantallaPractica:
    def __init__(self):
        self.visible = False

        self.pregunta = ""
        self.respuesta_correcta = True
        self.seleccion = None

        self.respondido = False
        self.resultado = ""
        self.respuesta_final = None
        self.intento_incorrecto_pendiente = False

        # Las fuentes se recalculan según el tamaño real del formulario.
        # Así, cuando el formulario se hace más pequeño, el texto y los
        # botones también bajan de tamaño y no se salen del panel.
        self.fuente_titulo = cargar_fuente_pixel(24)
        self.fuente_pregunta = cargar_fuente_pixel(22)
        self.fuente_boton = cargar_fuente_pixel(26)
        self.fuente_resultado = cargar_fuente_pixel(18)
        self.fuente_x = cargar_fuente_pixel(24)

        self.panel = pygame.Rect(0, 0, 0, 0)
        self.rect_cerrar = pygame.Rect(0, 0, 0, 0)
        self.rect_titulo = pygame.Rect(0, 0, 0, 0)
        self.rect_pregunta = pygame.Rect(0, 0, 0, 0)
        self.rect_falso = pygame.Rect(0, 0, 0, 0)
        self.rect_verdadero = pygame.Rect(0, 0, 0, 0)
        self.rect_responder = pygame.Rect(0, 0, 0, 0)
        self.rect_resultado = pygame.Rect(0, 0, 0, 0)

        # Referencia tomada de tu imagen del formulario.
        # Así las piezas quedan en la misma posición aunque la ventana cambie de tamaño.
        self.diseno_ancho = 1448
        self.diseno_alto = 1086
        self.escala_x = 1
        self.escala_y = 1

        # Área donde quieres que aparezca el formulario, tomada de tu
        # segunda imagen con el rectángulo rojo.
        # Valores relativos para que siga funcionando si cambias ANCHO/ALTO.
        self.area_practica_relativa = (0.312, 0.167, 0.389, 0.541)

        self.boton_presionado = None

        # ====================================================
        # ANIMACION DE REBOTE DE LOS BOTONES DEL FORMULARIO
        # ====================================================
        # El desplazamiento se adapta al tamano real del formulario.
        self.desplazamiento_rebote = 10
        self.duracion_subida_rebote = 0.10
        self.duracion_bajada_rebote = 0.34

        self.estados_rebote = {
            nombre: {
                "encima_anterior": False,
                "animando": False,
                "tiempo": 0.0,
                "offset_y": 0,
            }
            for nombre in ("cerrar", *BOTONES_RESPUESTA_FORMULARIO)
        }

        self._cache_imagenes_escaladas = {}
        self._sombra_fondo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        self._sombra_fondo.fill((0, 0, 0, 75))

        # Carga las piezas PNG. Si alguna no existe, el juego dibuja un respaldo
        # para que el archivo siga siendo ejecutable.
        self.img_formulario = None
        self.img_pregunta = None
        self.img_titulo = None
        self.img_cerrar = {}
        self.img_botones = {
            nombre: {} for nombre in BOTONES_RESPUESTA_FORMULARIO
        }

        self._carpetas_formulario = self._crear_carpetas_formulario()
        self.cargar_assets_formulario()
        self.calcular_rects()

    # --------------------------------------------------------
    # CARGA DE ASSETS DEL FORMULARIO
    # --------------------------------------------------------

    @staticmethod
    def _crear_carpetas_formulario():
        return (
            UI_DIR,
            UI_DIR / "formulario",
            UI_DIR / "Formulario",
            UI_DIR / "practica",
            UI_DIR / "Practica",
            UI_DIR / "cuadro_preguntas",
            UI_DIR / "cuadro_pregunta",
            UI_DIR / "cuadro_celes",
            UI_DIR / "cuadro_celeste",
            UI_DIR / "btn_cerrar",
            UI_DIR / "btn_falso",
            UI_DIR / "btn_verdadero",
            UI_DIR / "btn_responder",
            UI_DIR / "formulario_practica",
            UI_DIR / "Formulario_Practica",
        )

    def obtener_carpetas_formulario(self):
        return list(self._carpetas_formulario)

    def normalizar_nombre(self, texto):
        return (
            texto.lower()
            .replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
            .replace("ñ", "n")
            .replace(" ", "_")
            .replace("-", "_")
        )

    def buscar_png(self, nombres, subcarpetas=None):
        if subcarpetas is None:
            subcarpetas = [""]

        nombres_normalizados = [self.normalizar_nombre(nombre) for nombre in nombres]

        for carpeta in self._carpetas_formulario:
            for subcarpeta in subcarpetas:
                carpeta_actual = carpeta / subcarpeta if subcarpeta else carpeta

                for nombre in nombres:
                    ruta = carpeta_actual / nombre
                    if ruta.exists():
                        return ruta

                if not carpeta_actual.exists():
                    continue

                for archivo in carpeta_actual.glob("*.png"):
                    nombre_archivo = self.normalizar_nombre(archivo.name)
                    stem_archivo = self.normalizar_nombre(archivo.stem)

                    if nombre_archivo in nombres_normalizados or stem_archivo in nombres_normalizados:
                        return archivo

        # Busqueda extra: revisa subcarpetas internas.
        # Esto ayuda cuando las carpetas estan organizadas diferente.
        # Ejemplo:
        # assets/ui/formulario/normal/falso.png
        # assets/ui/formulario/hover/falso.png
        # assets/ui/formulario/clic/falso.png
        for carpeta in self._carpetas_formulario:
            if not carpeta.exists():
                continue

            for archivo in carpeta.rglob("*.png"):
                nombre_archivo = self.normalizar_nombre(archivo.name)
                stem_archivo = self.normalizar_nombre(archivo.stem)

                if nombre_archivo in nombres_normalizados or stem_archivo in nombres_normalizados:
                    return archivo

        return None

    def buscar_png_por_palabras(self, palabras):
        palabras_normalizadas = [self.normalizar_nombre(p) for p in palabras]

        for carpeta in self._carpetas_formulario:
            if not carpeta.exists():
                continue

            for archivo in carpeta.rglob("*.png"):
                texto = self.normalizar_nombre(str(archivo.relative_to(carpeta)))

                if all(palabra in texto for palabra in palabras_normalizadas):
                    return archivo

        return None

    def buscar_primer_png_en_subcarpetas(
        self,
        subcarpetas,
        excluir_palabras=None,
        preferir_mas_grande=False,
        recortar=False,
    ):
        if excluir_palabras is None:
            excluir_palabras = []

        candidatos = []
        excluir_normalizadas = [self.normalizar_nombre(p) for p in excluir_palabras]

        for carpeta_base in self._carpetas_formulario:
            if not carpeta_base.exists():
                continue

            for subcarpeta in subcarpetas:
                carpeta = carpeta_base / subcarpeta if subcarpeta else carpeta_base
                if not carpeta.exists() or not carpeta.is_dir():
                    continue

                for archivo in carpeta.rglob("*.png"):
                    ruta_norm = self.normalizar_nombre(str(archivo.relative_to(carpeta_base)))
                    if any(p in ruta_norm for p in excluir_normalizadas):
                        continue
                    candidatos.append(archivo)

        if not candidatos:
            return None

        if preferir_mas_grande:
            def area_png(ruta):
                imagen = cargar_imagen(ruta)
                if imagen is None:
                    return 0
                return imagen.get_width() * imagen.get_height()
            candidatos.sort(key=area_png, reverse=True)
        else:
            candidatos.sort(key=lambda r: (len(r.parts), r.name.lower()))

        ruta = candidatos[0]
        imagen = cargar_imagen(ruta)
        if imagen is not None and recortar:
            imagen = recortar_transparencia_png(imagen, margen=6)

        return imagen

    def cargar_png_formulario(self, nombres, subcarpetas=None, recortar=False):
        ruta = self.buscar_png(nombres, subcarpetas)

        if ruta is None:
            return None

        imagen = cargar_imagen(ruta)

        if imagen is not None and recortar:
            imagen = recortar_transparencia_png(imagen, margen=6)

        return imagen

    def cargar_boton_estado(self, boton, estado):
        estado_extra = "click" if estado == "clic" else estado

        nombres = [
            f"{boton}_{estado}.png",
            f"{boton}_{estado_extra}.png",
            f"btn_{boton}_{estado}.png",
            f"btn_{boton}_{estado_extra}.png",
            f"boton_{boton}_{estado}.png",
            f"boton_{boton}_{estado_extra}.png",
            f"{estado}.png",
            f"{estado_extra}.png",
            f"{boton}.png",
            f"btn_{boton}.png",
            f"boton_{boton}.png",
        ]

        # Acepta las dos formas:
        # 1) assets/ui/formulario/falso/normal.png
        # 2) assets/ui/formulario/normal/falso.png
        subcarpetas = [
            boton,
            boton.capitalize(),
            f"boton_{boton}",
            f"btn_{boton}",
            estado,
            estado.capitalize(),
            estado_extra,
            estado_extra.capitalize(),
            "botones",
            "Botones",
            "",
        ]

        imagen = self.cargar_png_formulario(nombres, subcarpetas, recortar=True)
        if imagen is not None:
            return imagen

        # Busqueda flexible por palabras en ruta completa.
        # Ejemplo valido: normal/boton_falso.png, falso/normal.png,
        # boton_falso_normal.png, botones/normal/falso.png, etc.
        ruta = self.buscar_png_por_palabras([boton, estado])
        if ruta is None and estado != estado_extra:
            ruta = self.buscar_png_por_palabras([boton, estado_extra])

        if ruta is None:
            return None

        imagen = cargar_imagen(ruta)
        if imagen is not None:
            imagen = recortar_transparencia_png(imagen, margen=6)

        return imagen

    def cargar_desde_rutas_exactas(self, rutas, recortar=False):
        for ruta in rutas:
            if ruta.exists():
                imagen = cargar_imagen(ruta)
                if imagen is not None and recortar:
                    imagen = recortar_transparencia_png(imagen, margen=6)
                if imagen is not None:
                    return imagen
        return None

    def _cargar_panel_formulario(self):
        return self.cargar_desde_rutas_exactas(
            [
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
            ],
            recortar=False,
        )

    def _cargar_cuadro_pregunta(self):
        imagen = self.cargar_desde_rutas_exactas(
            [
                UI_DIR / "cuadro_celes" / "cuadro_celeste.png",
                UI_DIR / "cuadro_celes" / "cuadro.png",
                UI_DIR / "cuadro_celes" / "pregunta.png",
                UI_DIR / "cuadro_celeste" / "cuadro_celeste.png",
                UI_DIR / "cuadro_celeste" / "cuadro.png",
                UI_DIR / "cuadro_celeste" / "pregunta.png",
                UI_DIR / "cuadro_preguntas" / "cuadro.png",
                UI_DIR / "cuadro_preguntas" / "cuadro_pregunta.png",
                UI_DIR / "cuadro_preguntas" / "cuadro_preguntas.png",
                UI_DIR / "cuadro_preguntas" / "pregunta.png",
                UI_DIR / "cuadro_pregunta" / "cuadro.png",
                UI_DIR / "cuadro_pregunta" / "cuadro_pregunta.png",
                UI_DIR / "cuadro_pregunta" / "pregunta.png",
            ],
            recortar=True,
        )

        if imagen is not None:
            return imagen

        return self.cargar_png_formulario(
            [
                "cuadro.png",
                "pregunta.png",
                "cuadro_pregunta.png",
                "cuadro_preguntas.png",
                "caja_pregunta.png",
                "panel_pregunta.png",
                "rect_pregunta.png",
                "cuadro_celeste.png",
                "cuadro_celeste_claro.png",
            ],
            [
                "cuadro_celes",
                "cuadro_celeste",
                "cuadro_preguntas",
                "cuadro_pregunta",
                "pregunta",
                "Pregunta",
            ],
            recortar=True,
        )

    def _cargar_titulo_practica(self):
        imagen = self.cargar_desde_rutas_exactas(
            [
                UI_DIR / "practica" / "practica_cuadro.png",
                UI_DIR / "practica" / "cuadro_practica.png",
                UI_DIR / "practica" / "titulo_practica.png",
                UI_DIR / "practica" / "practica.png",
                UI_DIR / "practica_cuadro.png",
                UI_DIR / "cuadro_practica.png",
                UI_DIR / "titulo_practica.png",
            ],
            recortar=True,
        )

        if imagen is not None:
            return imagen

        return self.cargar_png_formulario(
            [
                "practica_cuadro.png",
                "cuadro_practica.png",
                "titulo_practica.png",
                "practica.png",
                "practica_normal.png",
                "etiqueta_practica.png",
                "label_practica.png",
            ],
            ["practica", "Practica", "titulo", "Titulo"],
            recortar=True,
        )

    def _cargar_estados_botones_formulario(self):
        for estado in ESTADOS_BOTON_FORMULARIO:
            self.img_cerrar[estado] = self.cargar_boton_estado("cerrar", estado)

            for boton in BOTONES_RESPUESTA_FORMULARIO:
                self.img_botones[boton][estado] = self.cargar_boton_estado(
                    boton,
                    estado,
                )

    def cargar_assets_formulario(self):
        # IMPORTANTE:
        # El diseno base siempre se queda en 1448x1086.
        # No usamos el tamano de los PNG para calcular posiciones,
        # porque si un PNG solo es una pieza pequena, todo el formulario se mueve.
        self.diseno_ancho = 1448
        self.diseno_alto = 1086

        # Fondo beige completo del formulario.
        # Este NO debe buscar dentro de cuadro_preguntas ni practica,
        # porque esas carpetas son piezas, no el fondo completo.
        self.img_formulario = self._cargar_panel_formulario()

        # Cuadro celeste de la pregunta. Acepta tus dos estructuras:
        # assets/ui/cuadro_celes/cuadro_celeste.png
        # assets/ui/cuadro_preguntas/cuadro.png
        self.img_pregunta = self._cargar_cuadro_pregunta()

        # Cuadro/etiqueta naranja de PRACTICA: tu ruta actual es
        # assets/ui/practica/practica_cuadro.png
        self.img_titulo = self._cargar_titulo_practica()

        # Si no encuentra las rutas exactas, usa búsqueda flexible solo para estas piezas.
        # El fondo beige no usa búsqueda flexible para evitar que se cargue por error
        # el cuadro celeste como fondo completo.
        self._cargar_estados_botones_formulario()

    # --------------------------------------------------------
    # RECTÁNGULOS Y ESCALADO
    # --------------------------------------------------------

    def rect_relativo(self, x, y, ancho, alto):
        return pygame.Rect(
            self.panel.x + round(x * self.escala_x),
            self.panel.y + round(y * self.escala_y),
            round(ancho * self.escala_x),
            round(alto * self.escala_y)
        )

    def actualizar_fuentes(self):
        # Tamaños base del diseño 1448x1086.
        # Se multiplican por escala_y para que todo se reduzca junto
        # con el panel de práctica.
        self.fuente_titulo = cargar_fuente_pixel(max(16, round(42 * self.escala_y)))
        self.fuente_pregunta = cargar_fuente_pixel(max(15, round(34 * self.escala_y)))
        self.fuente_boton = cargar_fuente_pixel(max(17, round(48 * self.escala_y)))
        self.fuente_resultado = cargar_fuente_pixel(max(14, round(30 * self.escala_y)))
        self.fuente_x = cargar_fuente_pixel(max(16, round(42 * self.escala_y)))

    def calcular_rects(self):
        # Siempre usamos la referencia 1448x1086 para que las piezas
        # queden en el mismo lugar que tu diseño original.
        proporcion = self.diseno_ancho / self.diseno_alto

        # Área marcada con rojo en tu captura.
        area_x = round(ANCHO * self.area_practica_relativa[0])
        area_y = round(ALTO * self.area_practica_relativa[1])
        area_ancho = round(ANCHO * self.area_practica_relativa[2])
        area_alto = round(ALTO * self.area_practica_relativa[3])
        area_practica = pygame.Rect(area_x, area_y, area_ancho, area_alto)

        # El formulario entra completo dentro del rectángulo rojo,
        # manteniendo su proporción para que no se deforme.
        panel_ancho = area_practica.width
        panel_alto = int(panel_ancho / proporcion)

        if panel_alto > area_practica.height:
            panel_alto = area_practica.height
            panel_ancho = int(panel_alto * proporcion)

        self.panel = pygame.Rect(0, 0, panel_ancho, panel_alto)
        self.panel.center = area_practica.center

        self.escala_x = self.panel.width / self.diseno_ancho
        self.escala_y = self.panel.height / self.diseno_alto
        self.actualizar_fuentes()

        # Coordenadas medidas sobre el diseño base 1448x1086.
        self.rect_cerrar = self.rect_relativo(45, 38, 78, 72)
        self.rect_titulo = self.rect_relativo(140, 48, 245, 56)
        self.rect_pregunta = self.rect_relativo(57, 138, 1334, 330)
        self.rect_falso = self.rect_relativo(56, 484, 1338, 94)
        self.rect_verdadero = self.rect_relativo(56, 604, 1338, 94)
        self.rect_responder = self.rect_relativo(430, 890, 590, 100)
        self.rect_resultado = self.rect_relativo(80, 725, 1288, 125)

    # --------------------------------------------------------
    # CONTROL
    # --------------------------------------------------------

    def reiniciar_rebotes(self):
        for estado in self.estados_rebote.values():
            estado["encima_anterior"] = False
            estado["animando"] = False
            estado["tiempo"] = 0.0
            estado["offset_y"] = 0

    def iniciar(self, pregunta, respuesta_correcta):
        self.visible = True
        self.pregunta = pregunta
        self.respuesta_correcta = respuesta_correcta
        self.seleccion = None
        self.respondido = False
        self.resultado = ""
        self.respuesta_final = None
        self.intento_incorrecto_pendiente = False
        self.boton_presionado = None
        self.reiniciar_rebotes()
        self.calcular_rects()

    def cerrar(self):
        self.visible = False
        self.boton_presionado = None
        self.reiniciar_rebotes()

    def reintentar(self):
        """Permite escoger FALSO o VERDADERO nuevamente."""
        self.seleccion = None
        self.respondido = False
        self.respuesta_final = None
        self.resultado = ""
        self.boton_presionado = None
        self.reiniciar_rebotes()

    def consumir_intento_incorrecto(self):
        """Devuelve True una sola vez por cada respuesta incorrecta."""
        if not self.intento_incorrecto_pendiente:
            return False

        self.intento_incorrecto_pendiente = False
        return True

    def responder(self):
        if self.seleccion is None:
            self.resultado = "Selecciona FALSO o VERDADERO"
            return

        self.respondido = True
        self.respuesta_final = self.seleccion == self.respuesta_correcta

        if self.respuesta_final:
            self.resultado = "Correcto!"
        else:
            self.resultado = "Incorrecto!"
            self.intento_incorrecto_pendiente = True

    def obtener_boton_en_posicion(self, pos):
        if self.rect_cerrar.collidepoint(pos):
            return "cerrar"

        if self.rect_falso.collidepoint(pos):
            return "falso"

        if self.rect_verdadero.collidepoint(pos):
            return "verdadero"

        if self.rect_responder.collidepoint(pos):
            return "responder"

        return None

    def manejar_click_boton(self, boton):
        if boton == "cerrar":
            self.cerrar()
            return

        if boton == "falso" and not self.respondido:
            self.seleccion = False
            self.resultado = ""
            return

        if boton == "verdadero" and not self.respondido:
            self.seleccion = True
            self.resultado = ""
            return

        if boton == "responder":
            if self.respondido and self.respuesta_final:
                self.cerrar()
            elif self.respondido:
                self.reintentar()
            else:
                self.responder()

    def manejar_evento(self, evento):
        if not self.visible:
            return False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.cerrar()
                return True

            if not self.respondido:
                if evento.key == pygame.K_f:
                    self.seleccion = False
                    self.resultado = ""
                    return True

                if evento.key == pygame.K_v:
                    self.seleccion = True
                    self.resultado = ""
                    return True

            if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if self.respondido and self.respuesta_final:
                    self.cerrar()
                elif self.respondido:
                    self.reintentar()
                else:
                    self.responder()
                return True

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self.boton_presionado = self.obtener_boton_en_posicion(evento.pos)
            return True

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            boton = self.obtener_boton_en_posicion(evento.pos)

            if boton is not None and boton == self.boton_presionado:
                self.manejar_click_boton(boton)

            self.boton_presionado = None
            return True

        return True

    @staticmethod
    def _ease_out_bounce(progreso):
        """Curva equivalente a OutBounce de Qt."""
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

    def actualizar(self, dt):
        """Actualiza el rebote mientras la pantalla de practica esta visible."""
        if not self.visible:
            return

        mouse_pos = pygame.mouse.get_pos()
        rects = {
            "cerrar": self.rect_cerrar,
            "falso": self.rect_falso,
            "verdadero": self.rect_verdadero,
            "responder": self.rect_responder,
        }

        desplazamiento = max(
            8,
            round(self.desplazamiento_rebote * self.escala_y),
        )

        for nombre, rect in rects.items():
            estado = self.estados_rebote[nombre]
            encima = rect.collidepoint(mouse_pos)

            # Se activa una vez cuando el cursor entra al boton.
            if encima and not estado["encima_anterior"]:
                estado["animando"] = True
                estado["tiempo"] = 0.0

            estado["encima_anterior"] = encima

            if not estado["animando"]:
                estado["offset_y"] = 0
                continue

            estado["tiempo"] += max(0.0, dt)
            tiempo = estado["tiempo"]

            if tiempo <= self.duracion_subida_rebote:
                progreso = min(
                    tiempo / self.duracion_subida_rebote,
                    1.0,
                )
                suavizado = 1.0 - (1.0 - progreso) ** 2
                estado["offset_y"] = -round(
                    desplazamiento * suavizado
                )
                continue

            tiempo_bajada = tiempo - self.duracion_subida_rebote

            if tiempo_bajada <= self.duracion_bajada_rebote:
                progreso = min(
                    tiempo_bajada / self.duracion_bajada_rebote,
                    1.0,
                )
                rebote = self._ease_out_bounce(progreso)
                estado["offset_y"] = -round(
                    desplazamiento * (1.0 - rebote)
                )
                continue

            estado["animando"] = False
            estado["tiempo"] = 0.0
            estado["offset_y"] = 0

    def obtener_desplazamiento_rebote(self, nombre):
        estado = self.estados_rebote.get(nombre)

        if estado is None:
            return 0

        return int(estado.get("offset_y", 0))

    # --------------------------------------------------------
    # DIBUJO DE RESPALDO SI FALTAN PNG
    # --------------------------------------------------------

    def puntos_pixel(self, rect, corte):
        corte = max(4, min(corte, rect.width // 4, rect.height // 3))
        return obtener_puntos_rect_pixel(rect, corte)

    def dibujar_caja_pixel(self, pantalla, rect, color_fondo, color_borde, sombra=True):
        corte = max(6, round(16 * self.escala_y))

        if sombra:
            desplazamiento_sombra = max(2, round(6 * self.escala_y))
            rect_sombra = rect.move(desplazamiento_sombra, desplazamiento_sombra)
            pygame.draw.polygon(
                pantalla,
                (52, 35, 30),
                self.puntos_pixel(rect_sombra, corte)
            )

        pygame.draw.polygon(pantalla, color_borde, self.puntos_pixel(rect, corte))

        rect_medio = rect.inflate(-8, -8)
        pygame.draw.polygon(pantalla, (255, 255, 255), self.puntos_pixel(rect_medio, corte - 4))

        rect_interno = rect.inflate(-16, -16)
        pygame.draw.polygon(pantalla, color_fondo, self.puntos_pixel(rect_interno, corte - 8))

    def dibujar_panel_respaldo(self, pantalla):
        corte_panel = max(10, round(32 * self.escala_y))
        desplazamiento_sombra = max(3, round(8 * self.escala_y))
        panel_sombra = self.panel.move(desplazamiento_sombra, desplazamiento_sombra)

        pygame.draw.polygon(pantalla, (5, 21, 45), self.puntos_pixel(panel_sombra, corte_panel))
        pygame.draw.polygon(pantalla, (8, 35, 70), self.puntos_pixel(self.panel, corte_panel))

        panel_interno = self.panel.inflate(-16, -16)
        pygame.draw.polygon(pantalla, (255, 239, 214), self.puntos_pixel(panel_interno, corte_panel - 8))

    def obtener_rect_escalado(self, imagen, rect, mantener_aspecto=False):
        if imagen is None:
            return rect

        if not mantener_aspecto:
            return pygame.Rect(rect)

        ancho_img = max(1, imagen.get_width())
        alto_img = max(1, imagen.get_height())

        escala = min(rect.width / ancho_img, rect.height / alto_img)
        ancho = max(1, round(ancho_img * escala))
        alto = max(1, round(alto_img * escala))

        rect_escalado = pygame.Rect(0, 0, ancho, alto)
        rect_escalado.center = rect.center
        return rect_escalado

    def dibujar_imagen_ajustada(self, pantalla, imagen, rect, mantener_aspecto=False):
        if imagen is None:
            return False

        rect_dibujo = self.obtener_rect_escalado(
            imagen,
            rect,
            mantener_aspecto=mantener_aspecto,
        )
        tamano = (max(1, rect_dibujo.width), max(1, rect_dibujo.height))
        clave_cache = (id(imagen), tamano)
        imagen_escalada = self._cache_imagenes_escaladas.get(clave_cache)

        if imagen_escalada is None:
            # Para pixel art usamos scale, no smoothscale.
            imagen_escalada = pygame.transform.scale(imagen, tamano)
            self._cache_imagenes_escaladas[clave_cache] = imagen_escalada

        pantalla.blit(imagen_escalada, rect_dibujo.topleft)
        return True

    def obtener_estado_boton(self, nombre, rect):
        mouse_pos = pygame.mouse.get_pos()
        encima = rect.collidepoint(mouse_pos)

        if self.boton_presionado == nombre and encima:
            return "clic"

        if nombre == "falso" and self.seleccion is False:
            return "clic"

        if nombre == "verdadero" and self.seleccion is True:
            return "clic"

        if encima:
            return "hover"

        return "normal"

    def dibujar_boton(self, pantalla, nombre, rect, texto, color):
        """Dibuja el PNG, el texto y el rebote como una sola pieza."""
        estado = self.obtener_estado_boton(nombre, rect)

        # La zona de clic conserva el rect original. Solo se desplaza el
        # dibujo, por lo que el boton no cambia de ancho ni de alto.
        offset_y = self.obtener_desplazamiento_rebote(nombre)
        rect_animado = pygame.Rect(rect).move(0, offset_y)

        if nombre == "cerrar":
            imagen = self.img_cerrar.get(estado) or self.img_cerrar.get("normal")
        else:
            imagen = (
                self.img_botones[nombre].get(estado)
                or self.img_botones[nombre].get("normal")
            )

        # La imagen y el texto utilizan el mismo rect animado.
        if imagen is not None:
            rect_texto = self.obtener_rect_escalado(
                imagen,
                rect_animado,
                mantener_aspecto=True,
            )
            self.dibujar_imagen_ajustada(
                pantalla,
                imagen,
                rect_animado,
                mantener_aspecto=True,
            )
        else:
            # Respaldo visual si falta alguna imagen del botón.
            rect_texto = pygame.Rect(rect_animado)
            borde = (7, 35, 70)

            if estado == "hover":
                borde = (255, 255, 255)

            if estado == "clic":
                rect_texto = rect_texto.move(
                    0,
                    max(1, round(4 * self.escala_y)),
                )

            self.dibujar_caja_pixel(
                pantalla,
                rect_texto,
                color,
                borde,
                sombra=True,
            )

        # El botón de cerrar ya incluye su símbolo en el PNG.
        # Los textos que se agregan dinámicamente son FALSO,
        # VERDADERO, RESPONDER y CONTINUAR.
        if nombre == "cerrar":
            return

        texto_boton = str(texto).upper()
        render = self.fuente_boton.render(
            texto_boton,
            False,
            (255, 255, 255),
        )

        # Evita que un texto largo se salga del botón.
        margen_x = max(8, round(28 * self.escala_x))
        margen_y = max(4, round(12 * self.escala_y))
        ancho_maximo = max(1, rect_texto.width - margen_x * 2)
        alto_maximo = max(1, rect_texto.height - margen_y * 2)

        if (
            render.get_width() > ancho_maximo
            or render.get_height() > alto_maximo
        ):
            escala_texto = min(
                ancho_maximo / max(1, render.get_width()),
                alto_maximo / max(1, render.get_height()),
            )
            nuevo_ancho = max(1, round(render.get_width() * escala_texto))
            nuevo_alto = max(1, round(render.get_height() * escala_texto))
            render = pygame.transform.scale(
                render,
                (nuevo_ancho, nuevo_alto),
            )

        posicion_texto = render.get_rect(center=rect_texto.center)
        posicion_texto.y -= max(0, round(2 * self.escala_y))
        pantalla.blit(render, posicion_texto)

    def dividir_lineas(self, texto, fuente, ancho_max):
        return dividir_lineas_por_ancho(texto, fuente, ancho_max)

    def dibujar_texto_centrado(self, pantalla, texto, fuente, rect, color):
        lineas = self.dividir_lineas(texto, fuente, rect.width - round(70 * self.escala_x))
        salto = fuente.get_height() + round(6 * self.escala_y)
        alto_total = len(lineas) * salto
        y = rect.centery - alto_total // 2

        for linea in lineas:
            render = fuente.render(linea, False, color)
            pantalla.blit(
                render,
                (
                    rect.centerx - render.get_width() // 2,
                    y
                )
            )
            y += salto

    def dibujar_titulo_respaldo(self, pantalla):
        self.dibujar_caja_pixel(
            pantalla,
            self.rect_titulo,
            (255, 112, 0),
            (170, 55, 0),
            sombra=True
        )

        texto = self.fuente_titulo.render("PRACTICA", False, (255, 255, 255))
        pantalla.blit(
            texto,
            (
                self.rect_titulo.centerx - texto.get_width() // 2,
                self.rect_titulo.centery - texto.get_height() // 2
            )
        )

    def dibujar_resultado(self, pantalla):
        if self.resultado == "":
            return

        if self.resultado == "Correcto!":
            color = (0, 120, 75)
        elif self.resultado == "Incorrecto!":
            color = (210, 45, 45)
        else:
            color = (16, 35, 65)

        self.dibujar_texto_centrado(
            pantalla,
            self.resultado,
            self.fuente_resultado,
            self.rect_resultado,
            color
        )

    # --------------------------------------------------------
    # DIBUJO PRINCIPAL
    # --------------------------------------------------------

    def dibujar(self, pantalla):
        if not self.visible:
            return

        # Oscurece el juego detrás del formulario, pero deja ver el nivel.
        pantalla.blit(self._sombra_fondo, (0, 0))

        if not self.dibujar_imagen_ajustada(pantalla, self.img_formulario, self.panel, mantener_aspecto=False):
            self.dibujar_panel_respaldo(pantalla)

        if not self.dibujar_imagen_ajustada(pantalla, self.img_titulo, self.rect_titulo, mantener_aspecto=True):
            self.dibujar_titulo_respaldo(pantalla)

        self.dibujar_boton(
            pantalla,
            "cerrar",
            self.rect_cerrar,
            "X",
            (255, 70, 70)
        )

        if not self.dibujar_imagen_ajustada(pantalla, self.img_pregunta, self.rect_pregunta, mantener_aspecto=False):
            self.dibujar_caja_pixel(
                pantalla,
                self.rect_pregunta,
                (207, 244, 250),
                (8, 35, 70),
                sombra=True
            )

        self.dibujar_texto_centrado(
            pantalla,
            self.pregunta,
            self.fuente_pregunta,
            self.rect_pregunta,
            (16, 35, 65)
        )

        self.dibujar_boton(
            pantalla,
            "falso",
            self.rect_falso,
            "FALSO",
            (0, 125, 235)
        )

        self.dibujar_boton(
            pantalla,
            "verdadero",
            self.rect_verdadero,
            "VERDADERO",
            (0, 190, 175)
        )

        self.dibujar_resultado(pantalla)

        if self.respondido and self.respuesta_final:
            texto_boton = "CONTINUAR"
        elif self.respondido:
            texto_boton = "REINTENTAR"
        else:
            texto_boton = "RESPONDER"

        self.dibujar_boton(
            pantalla,
            "responder",
            self.rect_responder,
            texto_boton,
            (255, 105, 0)
        )

# ============================================================
# 15. SISTEMA REUTILIZABLE DE INTERACCIONES
# ============================================================



__all__ = ["PantallaPractica"]
