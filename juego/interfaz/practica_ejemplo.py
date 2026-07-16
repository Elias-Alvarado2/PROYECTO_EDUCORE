from __future__ import annotations

from pathlib import Path

import pygame

from juego.interfaz.practica import (
    ALTO,
    ANCHO,
    PantallaPractica,
    cargar_fuente_pixel,
)


EJEMPLOS_DIR = Path(__file__).resolve().parents[1] / "ejemplos"


def resolver_ruta_ejemplo(nombre_imagen: str) -> Path:
    """Devuelve una ruta segura ubicada dentro de ``juego/ejemplos``."""
    nombre = str(nombre_imagen or "").strip()
    if not nombre:
        raise ValueError("Falta indicar la imagen del ejemplo.")

    if Path(nombre).is_absolute():
        raise ValueError(
            "La ruta de imagen debe ser relativa a juego/ejemplos."
        )

    ruta_base = EJEMPLOS_DIR.resolve()
    ruta = (ruta_base / nombre).resolve()

    try:
        ruta.relative_to(ruta_base)
    except ValueError as error:
        raise ValueError(
            "La imagen debe estar dentro de juego/ejemplos."
        ) from error

    if not ruta.is_file():
        raise FileNotFoundError(
            f"No se encontro la imagen de ejemplo: {ruta}"
        )

    return ruta


class PantallaPracticaEjemplo(PantallaPractica):
    """Pantalla informativa con texto, imagen y un boton CONTINUAR.

    La configuracion se declara dentro de ``PRACTICAS`` en cualquier nivel::

        {
            "tipo": "ejemplo",
            "pregunta": "Observa la siguiente tabla:",
            "imagen": "mysql/tabla_usuarios.png",
            "ancho": 1000,
            "alto": 500,
        }

    ``imagen`` siempre es relativa a ``juego/ejemplos``. ``ancho`` y
    ``alto`` usan las medidas del diseno base (1448 x 1080) y se adaptan
    automaticamente a la resolucion de la ventana.
    """

    def __init__(self):
        # Reutiliza el panel, titulo y estados de botones de las practicas.
        super().__init__()
        self.configuracion: dict = {}
        self.imagen_ejemplo: pygame.Surface | None = None
        self.ruta_imagen: Path | None = None
        self.error_imagen = ""
        self.ancho_imagen: float | None = None
        self.alto_imagen: float | None = None

    def calcular_rects(self) -> None:
        """Usa las proporciones grandes de la practica de codigo."""
        panel_alto = min(round(ALTO * 0.82), 890)
        panel_ancho = round(panel_alto * (1448 / 1080))

        if panel_ancho > round(ANCHO * 0.86):
            panel_ancho = round(ANCHO * 0.86)
            panel_alto = round(panel_ancho * (1080 / 1448))

        self.panel = pygame.Rect(0, 0, panel_ancho, panel_alto)
        self.panel.center = (ANCHO // 2, ALTO // 2)

        self.escala_x = self.panel.width / self.diseno_ancho
        self.escala_y = self.panel.height / self.diseno_alto
        self.actualizar_fuentes()

        self.rect_cerrar = self.rect_relativo(38, 35, 78, 72)
        self.rect_titulo = self.rect_relativo(132, 43, 255, 62)
        self.rect_texto = self.rect_relativo(95, 145, 1258, 125)
        self.rect_area_imagen = self.rect_relativo(95, 292, 1258, 550)
        self.rect_responder = self.rect_relativo(885, 882, 415, 90)

        # Conserva los atributos esperados por PantallaPractica.
        self.rect_pregunta = self.rect_texto
        self.rect_falso = pygame.Rect(0, 0, 0, 0)
        self.rect_verdadero = pygame.Rect(0, 0, 0, 0)
        self.rect_resultado = pygame.Rect(0, 0, 0, 0)

    @staticmethod
    def _leer_dimension(configuracion: dict, nombre: str) -> float | None:
        valor = configuracion.get(nombre)
        if valor is None:
            valor = configuracion.get(f"{nombre}_imagen")
        if valor is None:
            return None

        try:
            numero = float(valor)
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"{nombre} debe ser un numero mayor que cero."
            ) from error

        if numero <= 0:
            raise ValueError(
                f"{nombre} debe ser un numero mayor que cero."
            )

        return numero

    def _cargar_imagen_ejemplo(self, nombre_imagen: str) -> None:
        self.imagen_ejemplo = None
        self.ruta_imagen = None
        self.error_imagen = ""

        try:
            self.ruta_imagen = resolver_ruta_ejemplo(nombre_imagen)
            self.imagen_ejemplo = pygame.image.load(
                str(self.ruta_imagen)
            ).convert_alpha()
        except (FileNotFoundError, ValueError, pygame.error) as error:
            self.error_imagen = str(error)
            print(f"[PRACTICA_EJEMPLO] {self.error_imagen}")

    def iniciar(self, texto: str, configuracion: dict) -> None:
        self.visible = True
        self.pregunta = str(texto)
        self.configuracion = dict(configuracion or {})
        self.respondido = False
        self.respuesta_final = None
        self.resultado = ""
        self.intento_incorrecto_pendiente = False
        self.boton_presionado = None

        self.ancho_imagen = self._leer_dimension(
            self.configuracion,
            "ancho",
        )
        self.alto_imagen = self._leer_dimension(
            self.configuracion,
            "alto",
        )
        self._cargar_imagen_ejemplo(
            self.configuracion.get("imagen", "")
        )
        self._cache_imagenes_escaladas.clear()
        self.reiniciar_rebotes()
        self.calcular_rects()

    def continuar(self) -> None:
        self.respondido = True
        self.respuesta_final = True
        self.cerrar()

    def obtener_boton_en_posicion(self, posicion) -> str | None:
        if self.rect_cerrar.collidepoint(posicion):
            return "cerrar"
        if self.rect_responder.collidepoint(posicion):
            return "responder"
        return None

    def manejar_click_boton(self, boton: str) -> None:
        if boton == "cerrar":
            self.cerrar()
        elif boton == "responder":
            self.continuar()

    def manejar_evento(self, evento: pygame.event.Event) -> bool:
        if not self.visible:
            return False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.cerrar()
                return True
            if evento.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
                pygame.K_SPACE,
            ):
                self.continuar()
                return True

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self.boton_presionado = self.obtener_boton_en_posicion(
                evento.pos
            )
            return True

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            boton = self.obtener_boton_en_posicion(evento.pos)
            if boton is not None and boton == self.boton_presionado:
                self.manejar_click_boton(boton)
            self.boton_presionado = None
            return True

        return True

    def _obtener_rect_imagen(self) -> pygame.Rect | None:
        imagen = self.imagen_ejemplo
        if imagen is None:
            return None

        ancho_original = max(1, imagen.get_width())
        alto_original = max(1, imagen.get_height())
        ancho = (
            round(self.ancho_imagen * self.escala_x)
            if self.ancho_imagen is not None
            else None
        )
        alto = (
            round(self.alto_imagen * self.escala_y)
            if self.alto_imagen is not None
            else None
        )

        usar_todo_el_espacio = ancho is None and alto is None

        if usar_todo_el_espacio:
            ancho = ancho_original
            alto = alto_original
        elif ancho is None:
            ancho = round(ancho_original * (alto / alto_original))
        elif alto is None:
            alto = round(alto_original * (ancho / ancho_original))

        escala_limite = min(
            self.rect_area_imagen.width / max(1, ancho),
            self.rect_area_imagen.height / max(1, alto),
        )
        if not usar_todo_el_espacio:
            escala_limite = min(1.0, escala_limite)

        ancho = max(1, round(ancho * escala_limite))
        alto = max(1, round(alto * escala_limite))
        rect = pygame.Rect(0, 0, ancho, alto)
        rect.center = self.rect_area_imagen.center
        return rect

    def _dibujar_texto(self, pantalla: pygame.Surface) -> None:
        fuente = self.fuente_pregunta
        margen = max(8, round(12 * self.escala_x))
        ancho_maximo = self.rect_texto.width - margen * 2
        lineas = self.dividir_lineas(
            self.pregunta,
            fuente,
            ancho_maximo,
        )

        # Reduce la fuente solamente cuando el texto no entra en su area.
        for _ in range(12):
            if fuente.get_height() * len(lineas) <= self.rect_texto.height:
                break

            tamano = fuente.get_height() - 2
            if tamano < 14:
                break

            fuente_nueva = cargar_fuente_pixel(tamano)
            if fuente_nueva.get_height() >= fuente.get_height():
                break

            fuente = fuente_nueva
            lineas = self.dividir_lineas(
                self.pregunta,
                fuente,
                ancho_maximo,
            )

        salto = fuente.get_height() + max(2, round(5 * self.escala_y))
        alto_total = max(0, len(lineas) * salto - (salto - fuente.get_height()))
        y = self.rect_texto.centery - alto_total // 2

        for linea in lineas:
            render = fuente.render(str(linea).rstrip(), False, (16, 35, 65))
            pantalla.blit(render, (self.rect_texto.x + margen, y))
            y += salto

    def _dibujar_error_imagen(self, pantalla: pygame.Surface) -> None:
        self.dibujar_caja_pixel(
            pantalla,
            self.rect_area_imagen,
            (255, 238, 214),
            (8, 35, 70),
            sombra=False,
        )
        mensaje = self.error_imagen or "No se pudo cargar la imagen"
        self.dibujar_texto_centrado(
            pantalla,
            mensaje,
            self.fuente_resultado,
            self.rect_area_imagen,
            (180, 45, 45),
        )

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if not self.visible:
            return

        pantalla.blit(self._sombra_fondo, (0, 0))

        if not self.dibujar_imagen_ajustada(
            pantalla,
            self.img_formulario,
            self.panel,
            mantener_aspecto=False,
        ):
            self.dibujar_panel_respaldo(pantalla)

        if not self.dibujar_imagen_ajustada(
            pantalla,
            self.img_titulo,
            self.rect_titulo,
            mantener_aspecto=True,
        ):
            self.dibujar_titulo_respaldo(pantalla)

        self.dibujar_boton(
            pantalla,
            "cerrar",
            self.rect_cerrar,
            "X",
            (255, 70, 70),
        )
        self._dibujar_texto(pantalla)

        rect_imagen = self._obtener_rect_imagen()
        if rect_imagen is None:
            self._dibujar_error_imagen(pantalla)
        else:
            self.dibujar_imagen_ajustada(
                pantalla,
                self.imagen_ejemplo,
                rect_imagen,
                mantener_aspecto=False,
            )

        self.dibujar_boton(
            pantalla,
            "responder",
            self.rect_responder,
            "CONTINUAR",
            (255, 105, 0),
        )


__all__ = ["PantallaPracticaEjemplo", "resolver_ruta_ejemplo"]
