import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from quitar_barra import quitar
from Transicion import FormTransicion


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

ANCHO_BASE = 1366
ALTO_BASE = 768

VELOCIDAD_ANIMACION = 120  # Milisegundos entre cada frame


# ==========================================================
# FONDO RESPONSIVO
# ==========================================================

class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.pixmap_original = QtGui.QPixmap(
            str(ruta_imagen)
        )

        if self.pixmap_original.isNull():
            raise FileNotFoundError(
                f"No se pudo cargar el fondo:\n{ruta_imagen}"
            )

        self.setPixmap(self.pixmap_original)
        self.setScaledContents(True)

        self.setGeometry(
            0,
            0,
            ventana.width(),
            ventana.height()
        )

        # El fondo no debe bloquear los clics.
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


# ==========================================================
# CREAR UNA VERSIÓN APAGADA DEL PERSONAJE
# ==========================================================

def crear_pixmap_apagado(pixmap):
    """
    Convierte el personaje a escala de grises y reduce
    su opacidad, conservando el fondo transparente.
    """

    imagen = pixmap.toImage().convertToFormat(
        QtGui.QImage.Format.Format_ARGB32
    )

    for y in range(imagen.height()):
        for x in range(imagen.width()):
            color = imagen.pixelColor(x, y)

            if color.alpha() == 0:
                continue

            gris = round(
                color.red() * 0.299
                + color.green() * 0.587
                + color.blue() * 0.114
            )

            # Oscurecer un poco el personaje.
            gris = round(gris * 0.55)

            color_apagado = QtGui.QColor(
                gris,
                gris,
                gris,
                round(color.alpha() * 0.75)
            )

            imagen.setPixelColor(
                x,
                y,
                color_apagado
            )

    return QtGui.QPixmap.fromImage(imagen)


# ==========================================================
# PERSONAJE PEQUEÑO SELECCIONABLE
# ==========================================================

class TarjetaPersonaje(QtWidgets.QLabel):
    seleccionado = QtCore.pyqtSignal(str)
     
    def __init__(
        self,
        nombre,
        pixmap_personaje,
        parent=None
    ):
        super().__init__(parent)

        self.nombre = nombre

        # Imagen original.
        self.pixmap_original = pixmap_personaje

        # Imagen apagada.
        self.pixmap_apagado = crear_pixmap_apagado(
            pixmap_personaje
        )

        self.esta_seleccionado = False

        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )

        self.setStyleSheet(
            """
            QLabel {
                background: transparent;
                border: none;
            }
            """
        )

        # Inicialmente aparece apagado.
        self.marcar_seleccionado(False)

    def marcar_seleccionado(self, seleccionado):
        self.esta_seleccionado = seleccionado
        self.actualizar_imagen()

    def actualizar_imagen(self):
        if self.width() <= 0 or self.height() <= 0:
            return

        if self.esta_seleccionado:
            pixmap = self.pixmap_original
        else:
            pixmap = self.pixmap_apagado

        ancho_disponible = max(
            1,
            self.width() - 18
        )

        alto_disponible = max(
            1,
            self.height() - 18
        )

        pixmap_escalado = pixmap.scaled(
            ancho_disponible,
            alto_disponible,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.FastTransformation
        )

        self.setPixmap(pixmap_escalado)

    def mousePressEvent(self, evento):
        if (
            evento.button()
            == QtCore.Qt.MouseButton.LeftButton
        ):
            self.seleccionado.emit(self.nombre)

        super().mousePressEvent(evento)

    def resizeEvent(self, evento):
        self.actualizar_imagen()
        super().resizeEvent(evento)


# ==========================================================
# FORMULARIO PRINCIPAL
# ==========================================================

class Personajes(QtWidgets.QWidget):
    """
    Esta variable permite conservar el jugador cuando
    FormTransicion abre la clase sin parámetros.
    """

    jugador_pendiente = None

    def __init__(self, jugador=None):
        super().__init__()
        quitar(self)
        if jugador is None:
            jugador = Personajes.jugador_pendiente

        Personajes.jugador_pendiente = None

        self.jugador = jugador

        self.personaje_actual = None
        self.indice_frame = 0

        self.transicion = None
        self.clase_menu_destino = None

        # --------------------------------------------------
        # RUTAS PRINCIPALES
        # --------------------------------------------------

        # Carpeta PROYECTO_EDUCORE/CODIGOS
        base_dir = Path(__file__).resolve().parent

        # Carpeta PROYECTO_EDUCORE
        proyecto_dir = base_dir.parent

        self.proyecto_dir = proyecto_dir

        ruta_ui = (
            proyecto_dir
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "Personaje.ui"
        )

        ruta_fondo = (
            proyecto_dir
            / "assets"
            / "DISEÑOS"
            / "Personaje.png"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el formulario:\n{ruta_ui}"
            )

        if not ruta_fondo.exists():
            raise FileNotFoundError(
                f"No se encontró el fondo:\n{ruta_fondo}"
            )

        # Cargar el archivo de Qt Designer.
        uic.loadUi(str(ruta_ui), self)

        self.setWindowTitle(
            "Selección de personajes"
        )

        self.setMinimumSize(
            900,
            506
        )

        # Fondo completo.
        self.fondo = FondoImagen(
            self,
            ruta_fondo
        )

        # --------------------------------------------------
        # CONFIGURACIÓN DE LOS PERSONAJES
        # --------------------------------------------------
        #
        # La estructura recomendada es:
        #
        # PROYECTO_EDUCORE/
        # └── assets/
        #     └── personajes/
        #         ├── cerdo/
        #         ├── gato/
        #         └── pato/
        #
        # El código también busca en otras carpetas comunes.
        # --------------------------------------------------

        self.raices_personajes = [
            proyecto_dir
            / "assets"
            / "personajes",

            proyecto_dir
            / "ASSETS"
            / "PERSONAJES",

            proyecto_dir
            / "juego"
            / "assets"
            / "personajes",

            proyecto_dir
            / "EXPO-DISEÑOS"
            / "DISEÑOS"
            / "PERSONAJES",
        ]

        self.config_personajes = {
            # CERDO:
            # jugador_caminar1.png hasta jugador_caminar4.png
            "cerdo": {
                "carpetas": (
                    "cerdo",
                    "cerdito",
                    "jugador",
                ),

                "frames": [
                    (
                        "jugador_caminar1.png",
                    ),
                    (
                        "jugador_caminar2.png",
                    ),
                    (
                        "jugador_caminar3.png",
                    ),
                    (
                        "jugador_caminar4.png",
                    ),
                ],
            },

            # GATO/BANANO:
            # La animación comienza en gato_caminar2.png
            # y termina en gato_caminar8.png.
            "gato": {
                "carpetas": (
                    "gato",
                    "banano",
                ),

                "frames": [
                    (
                        "gato_caminar2.png",
                    ),
                    (
                        "gato_caminar3.png",
                    ),
                    (
                        "gato_caminar4.png",
                    ),
                    (
                        "gato_caminar5.png",
                    ),
                    (
                        "gato_caminar6.png",
                    ),
                    (
                        "gato_caminar7.png",
                    ),
                    (
                        "gato_caminar8.png",
                    ),
                ],
            },

            # PATO:
            # Pato_Caminar1.png hasta Pato_Caminar5.png
            "pato": {
                "carpetas": (
                    "pato",
                    "patito",
                ),

                "frames": [
                    (
                        "Pato_Caminar1.png",
                        "pato_caminar1.png",
                    ),
                    (
                        "Pato_Caminar2.png",
                        "pato_caminar2.png",
                    ),
                    (
                        "Pato_Caminar3.png",
                        "pato_caminar3.png",
                    ),
                    (
                        "Pato_Caminar4.png",
                        "pato_caminar4.png",
                    ),
                    (
                        "Pato_Caminar5.png",
                        "pato_caminar5.png",
                    ),
                ],
            },
        }

        # Cargar todos los frames.
        self.frames_personajes = (
            self.cargar_todos_los_personajes()
        )

        # --------------------------------------------------
        # CUADRO GRANDE
        # --------------------------------------------------

        self.vista_personaje = QtWidgets.QLabel(
            self
        )

        self.vista_personaje.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.vista_personaje.setStyleSheet(
            """
            QLabel {
                background: transparent;
                border: none;
            }
            """
        )

        # --------------------------------------------------
        # TARJETAS PEQUEÑAS
        # --------------------------------------------------

        self.tarjetas = {}

        for nombre in (
            "cerdo",
            "gato",
            "pato"
        ):
            primer_frame = (
                self.frames_personajes[nombre][0]
            )

            tarjeta = TarjetaPersonaje(
                nombre,
                primer_frame,
                self
            )

            tarjeta.seleccionado.connect(
                self.seleccionar_personaje
            )

            self.tarjetas[nombre] = tarjeta

        # --------------------------------------------------
        # TEMPORIZADOR DE LA ANIMACIÓN
        # --------------------------------------------------

        self.timer_animacion = QtCore.QTimer(
            self
        )

        self.timer_animacion.setInterval(
            VELOCIDAD_ANIMACION
        )

        self.timer_animacion.timeout.connect(
            self.actualizar_animacion
        )

        # --------------------------------------------------
        # BOTÓN VOLVER
        # --------------------------------------------------

        self.configurar_boton_volver()

        # Colocar todos los objetos.
        self.actualizar_geometrias()
        self.actualizar_capas()

        # Estado inicial:
        # todos apagados y cuadro grande vacío.
        self.vista_personaje.clear()

    # ======================================================
    # BUSCAR Y CARGAR SPRITES
    # ======================================================

    def buscar_frame(
        self,
        nombres_carpetas,
        nombres_archivo
    ):
        for raiz in self.raices_personajes:
            if not raiz.exists():
                continue

            for nombre_carpeta in nombres_carpetas:
                carpeta = raiz / nombre_carpeta

                if not carpeta.exists():
                    continue

                # Primero busca directamente.
                for nombre_archivo in nombres_archivo:
                    ruta = carpeta / nombre_archivo

                    if ruta.exists():
                        return ruta

                # Después busca dentro de subcarpetas.
                for nombre_archivo in nombres_archivo:
                    encontrados = list(
                        carpeta.rglob(nombre_archivo)
                    )

                    if encontrados:
                        return encontrados[0]

        return None

    def cargar_todos_los_personajes(self):
        personajes_cargados = {}

        for nombre, configuracion in (
            self.config_personajes.items()
        ):
            frames_cargados = []

            for opciones_nombre in configuracion["frames"]:
                ruta_frame = self.buscar_frame(
                    configuracion["carpetas"],
                    opciones_nombre
                )

                if ruta_frame is None:
                    nombres = "\n".join(
                        f"• {archivo}"
                        for archivo in opciones_nombre
                    )

                    carpetas = "\n".join(
                        f"• {carpeta}"
                        for carpeta
                        in configuracion["carpetas"]
                    )

                    raise FileNotFoundError(
                        f"No se encontró un frame de "
                        f"'{nombre}'.\n\n"
                        f"Carpetas buscadas:\n"
                        f"{carpetas}\n\n"
                        f"Nombres buscados:\n"
                        f"{nombres}"
                    )

                pixmap = QtGui.QPixmap(
                    str(ruta_frame)
                )

                if pixmap.isNull():
                    raise FileNotFoundError(
                        f"No se pudo abrir este frame:\n"
                        f"{ruta_frame}"
                    )

                frames_cargados.append(pixmap)

            personajes_cargados[nombre] = (
                frames_cargados
            )

        return personajes_cargados

    # ======================================================
    # BOTÓN VOLVER
    # ======================================================

    def configurar_boton_volver(self):
        nombres_posibles = (
            "btnVolver",
            "btn_volver",
            "btn_Volver",
            "botonVolver"
        )

        self.btn_volver = None

        for nombre in nombres_posibles:
            boton = self.findChild(
                QtWidgets.QPushButton,
                nombre
            )

            if boton is not None:
                self.btn_volver = boton
                break

        # Si no existe en el .ui, se crea encima
        # del botón dibujado en el fondo.
        if self.btn_volver is None:
            self.btn_volver = (
                QtWidgets.QPushButton(self)
            )

        self.btn_volver.setText("")

        self.btn_volver.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )

        self.btn_volver.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(
                    255,
                    255,
                    255,
                    25
                );
            }

            QPushButton:pressed {
                background-color: rgba(
                    0,
                    0,
                    0,
                    18
                );
            }
            """
        )

        self.btn_volver.clicked.connect(
            self.volver_menu_usuario
        )

    def volver_menu_usuario(self):
        self.timer_animacion.stop()

        # Import local para evitar importación circular.
        from MenuUsuario import MenuUsuario

        jugador_actual = self.jugador

        # FormTransicion abre una clase sin parámetros.
        # Esta clase auxiliar conserva el jugador actual.
        class MenuUsuarioDestino(MenuUsuario):
            def __init__(self):
                super().__init__(
                    jugador=jugador_actual
                )

        self.clase_menu_destino = (
            MenuUsuarioDestino
        )

        self.transicion = FormTransicion(
            self,
            self.clase_menu_destino
        )

    # ======================================================
    # SELECCIÓN DE PERSONAJES
    # ======================================================

    def seleccionar_personaje(self, nombre):
        if nombre not in self.frames_personajes:
            return

        self.personaje_actual = nombre
        self.indice_frame = 0

        # El seleccionado recupera el color.
        # Los demás vuelven a estar apagados.
        for nombre_tarjeta, tarjeta in (
            self.tarjetas.items()
        ):
            tarjeta.marcar_seleccionado(
                nombre_tarjeta == nombre
            )

        self.timer_animacion.stop()

        # Mostrar inmediatamente el primer frame.
        self.mostrar_frame_actual()

        # Comenzar la animación.
        if (
            len(self.frames_personajes[nombre])
            > 1
        ):
            self.timer_animacion.start()

        print(
            f"Personaje seleccionado: {nombre}"
        )

    # ======================================================
    # ANIMACIÓN DEL CUADRO GRANDE
    # ======================================================

    def actualizar_animacion(self):
        if self.personaje_actual is None:
            return

        frames = self.frames_personajes[
            self.personaje_actual
        ]

        if not frames:
            return

        self.indice_frame += 1

        if self.indice_frame >= len(frames):
            self.indice_frame = 0

        self.mostrar_frame_actual()

    def mostrar_frame_actual(self):
        if self.personaje_actual is None:
            self.vista_personaje.clear()
            return

        frames = self.frames_personajes[
            self.personaje_actual
        ]

        if not frames:
            self.vista_personaje.clear()
            return

        pixmap = frames[self.indice_frame]

        ancho_disponible = max(
            1,
            self.vista_personaje.width() - 30
        )

        alto_disponible = max(
            1,
            self.vista_personaje.height() - 20
        )

        pixmap_escalado = pixmap.scaled(
            ancho_disponible,
            alto_disponible,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.FastTransformation
        )

        self.vista_personaje.setPixmap(
            pixmap_escalado
        )

    # ======================================================
    # POSICIONES RESPONSIVAS
    # ======================================================

    def escalar_rectangulo(
        self,
        x,
        y,
        ancho,
        alto
    ):
        escala_x = self.width() / ANCHO_BASE
        escala_y = self.height() / ALTO_BASE

        return QtCore.QRect(
            round(x * escala_x),
            round(y * escala_y),
            round(ancho * escala_x),
            round(alto * escala_y)
        )

    def actualizar_geometrias(self):
        if not hasattr(self, "btn_volver"):
            return

        # Botón volver.
        self.btn_volver.setGeometry(
            self.escalar_rectangulo(
                60,
                52,
                202,
                67
            )
        )

        # Cuadro grande.
        self.vista_personaje.setGeometry(
            self.escalar_rectangulo(
                527,
                171,
                312,
                245
            )
        )

        # Primer cuadro: cerdo.
        self.tarjetas["cerdo"].setGeometry(
            self.escalar_rectangulo(
                432,
                458,
                111,
                142
            )
        )

        # Segundo cuadro: gato.
        self.tarjetas["gato"].setGeometry(
            self.escalar_rectangulo(
                558,
                458,
                111,
                142
            )
        )

        # Tercer cuadro: pato.
        self.tarjetas["pato"].setGeometry(
            self.escalar_rectangulo(
                684,
                458,
                111,
                142
            )
        )

        for tarjeta in self.tarjetas.values():
            tarjeta.actualizar_imagen()

        self.mostrar_frame_actual()

    def actualizar_capas(self):
        self.fondo.lower()

        self.vista_personaje.raise_()

        for tarjeta in self.tarjetas.values():
            tarjeta.raise_()

        self.btn_volver.raise_()

    # ======================================================
    # EVENTOS DEL FORMULARIO
    # ======================================================

    def resizeEvent(self, evento):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

        if hasattr(self, "tarjetas"):
            self.actualizar_geometrias()
            self.actualizar_capas()

        super().resizeEvent(evento)

    def hideEvent(self, evento):
        if hasattr(self, "timer_animacion"):
            self.timer_animacion.stop()

        super().hideEvent(evento)

    def showEvent(self, evento):
        if (
            hasattr(self, "timer_animacion")
            and self.personaje_actual is not None
        ):
            self.timer_animacion.start()

        super().showEvent(evento)


# ==========================================================
# EJECUTAR PERSONAJES.PY DIRECTAMENTE
# ==========================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = Personajes()
    ventana.showMaximized()

    sys.exit(app.exec())