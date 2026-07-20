from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui, QtCore

from Alertas import Alertas
from AjusteResponsive import BotonesResponsivos
from Transicion import FormTransicion
from quitar_barra import quitar
from LogoReutilizable import LogoReutilizable
from Ajustes import Ajustes
from ConexionBD import ConexionBD

VELOCIDAD_ANIMACION_PERSONAJE = 130

class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.ruta_imagen = ruta_imagen

        self.pixmap_original = QtGui.QPixmap(
            str(self.ruta_imagen)
        )

        if self.pixmap_original.isNull():
            raise FileNotFoundError(
                f"No se pudo cargar el fondo:\n"
                f"{self.ruta_imagen}"
            )

        self.setScaledContents(True)

        self.setGeometry(
            0,
            0,
            ventana.width(),
            ventana.height()
        )

        self.setPixmap(
            self.pixmap_original
        )

        # Evita que el fondo bloquee clics.
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


def recortar_pixmap_transparente(
    pixmap: QtGui.QPixmap,
    margen: int = 2,
    alpha_minimo: int = 5,
) -> QtGui.QPixmap:
    """
    Recorta el espacio transparente alrededor del sprite.

    Esto permite que CERDO, GATO y PATO se centren por su
    contenido visible y no por el tamaño completo del archivo.
    """

    if pixmap is None or pixmap.isNull():
        return pixmap

    imagen = pixmap.toImage().convertToFormat(
        QtGui.QImage.Format.Format_ARGB32
    )

    ancho = imagen.width()
    alto = imagen.height()

    minimo_x = ancho
    minimo_y = alto
    maximo_x = -1
    maximo_y = -1

    for y in range(alto):
        for x in range(ancho):
            if imagen.pixelColor(x, y).alpha() < alpha_minimo:
                continue

            minimo_x = min(minimo_x, x)
            minimo_y = min(minimo_y, y)
            maximo_x = max(maximo_x, x)
            maximo_y = max(maximo_y, y)

    # La imagen es completamente transparente.
    if maximo_x < minimo_x or maximo_y < minimo_y:
        return pixmap

    margen = max(0, int(margen))

    izquierda = max(0, minimo_x - margen)
    arriba = max(0, minimo_y - margen)
    derecha = min(ancho - 1, maximo_x + margen)
    abajo = min(alto - 1, maximo_y + margen)

    return pixmap.copy(
        QtCore.QRect(
            izquierda,
            arriba,
            derecha - izquierda + 1,
            abajo - arriba + 1,
        )
    )



class MarcoNombrePersonaje(QtWidgets.QWidget):
    """
    Dibuja un cuadro pixel art detrás del nombre del personaje.
    El diseño está inspirado en el marco color crema y salmón
    mostrado como referencia, sin depender de una imagen externa.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground,
            True
        )

        self.setAutoFillBackground(False)

    @staticmethod
    def _crear_poligono_pixel(rectangulo, paso):
        """Crea la silueta escalonada del marco."""

        x = rectangulo.x()
        y = rectangulo.y()
        ancho = rectangulo.width()
        alto = rectangulo.height()

        derecha = x + ancho
        abajo = y + alto
        centro_x = x + ancho // 2

        paso = max(2, paso)

        puntos = (
            (x + 4 * paso, y + 2 * paso),
            (centro_x - 2 * paso, y + 2 * paso),
            (centro_x - 2 * paso, y + paso),
            (centro_x - paso, y + paso),
            (centro_x - paso, y),
            (centro_x + paso, y),
            (centro_x + paso, y + paso),
            (centro_x + 2 * paso, y + paso),
            (centro_x + 2 * paso, y + 2 * paso),
            (derecha - 4 * paso, y + 2 * paso),
            (derecha - 4 * paso, y + 3 * paso),
            (derecha - 2 * paso, y + 3 * paso),
            (derecha - 2 * paso, y + 5 * paso),
            (derecha - paso, y + 5 * paso),
            (derecha - paso, abajo - 5 * paso),
            (derecha - 2 * paso, abajo - 5 * paso),
            (derecha - 2 * paso, abajo - 3 * paso),
            (derecha - 4 * paso, abajo - 3 * paso),
            (derecha - 4 * paso, abajo - 2 * paso),
            (centro_x + 2 * paso, abajo - 2 * paso),
            (centro_x + 2 * paso, abajo - paso),
            (centro_x + paso, abajo - paso),
            (centro_x + paso, abajo),
            (centro_x - paso, abajo),
            (centro_x - paso, abajo - paso),
            (centro_x - 2 * paso, abajo - paso),
            (centro_x - 2 * paso, abajo - 2 * paso),
            (x + 4 * paso, abajo - 2 * paso),
            (x + 4 * paso, abajo - 3 * paso),
            (x + 2 * paso, abajo - 3 * paso),
            (x + 2 * paso, abajo - 5 * paso),
            (x + paso, abajo - 5 * paso),
            (x + paso, y + 5 * paso),
            (x + 2 * paso, y + 5 * paso),
            (x + 2 * paso, y + 3 * paso),
            (x + 4 * paso, y + 3 * paso),
        )

        return QtGui.QPolygon(
            [QtCore.QPoint(px, py) for px, py in puntos]
        )

    def paintEvent(self, event):
        super().paintEvent(event)

        ancho = self.width()
        alto = self.height()

        if ancho < 40 or alto < 30:
            return

        pintor = QtGui.QPainter(self)
        pintor.setRenderHint(
            QtGui.QPainter.RenderHint.Antialiasing,
            False
        )

        pintor.setPen(QtCore.Qt.PenStyle.NoPen)

        paso = max(
            3,
            min(
                ancho // 55,
                alto // 13
            )
        )

        rect_exterior = QtCore.QRect(
            0,
            0,
            ancho - 1,
            alto - 1
        )

        poligono_exterior = self._crear_poligono_pixel(
            rect_exterior,
            paso
        )

        # Borde principal azul marino de EduCore.
        pintor.setBrush(QtGui.QColor("#082B63"))
        pintor.drawPolygon(poligono_exterior)

        margen_medio = paso
        rect_medio = rect_exterior.adjusted(
            margen_medio,
            margen_medio,
            -margen_medio,
            -margen_medio
        )

        poligono_medio = self._crear_poligono_pixel(
            rect_medio,
            max(2, paso - 1)
        )

        # Segunda capa azul del logotipo.
        pintor.setBrush(QtGui.QColor("#4D68A8"))
        pintor.drawPolygon(poligono_medio)

        margen_interior = paso * 2
        rect_interior = rect_exterior.adjusted(
            margen_interior,
            margen_interior,
            -margen_interior,
            -margen_interior
        )

        poligono_interior = self._crear_poligono_pixel(
            rect_interior,
            max(2, paso - 1)
        )

        # Interior crema para conservar buena legibilidad.
        pintor.setBrush(QtGui.QColor("#FFF0D8"))
        pintor.drawPolygon(poligono_interior)

        # Detalles pixelados con los colores del logo EduCore.
        ancho_acento = max(paso * 5, ancho // 9)
        alto_acento = max(paso, 3)

        # Naranja, lado izquierdo.
        pintor.setBrush(QtGui.QColor("#FF7A1A"))
        pintor.drawRect(
            paso * 5,
            paso * 3,
            ancho_acento,
            alto_acento,
        )
        pintor.drawRect(
            paso * 3,
            paso * 5,
            alto_acento,
            max(paso * 3, alto // 4),
        )

        # Turquesa, lado derecho.
        pintor.setBrush(QtGui.QColor("#18A89D"))
        pintor.drawRect(
            max(0, ancho - paso * 5 - ancho_acento),
            max(0, alto - paso * 4),
            ancho_acento,
            alto_acento,
        )
        pintor.drawRect(
            max(0, ancho - paso * 4),
            max(0, alto - paso * 5 - max(paso * 3, alto // 4)),
            alto_acento,
            max(paso * 3, alto // 4),
        )

        pintor.end()

class EfectoHoverBoton(QtCore.QObject):
    """
    Agranda ligeramente el botón y aumenta su sombra
    cuando el cursor pasa sobre él.
    """

    def __init__(
        self,
        boton,
        factor=1.035,
        duracion=120,
        parent=None
    ):
        super().__init__(
            parent if parent is not None else boton
        )

        self.boton = boton
        self.factor = factor
        self.duracion = duracion
        self.cursor_encima = False

        self.geometria_normal = QtCore.QRect(
            self.boton.geometry()
        )

        self.animacion_geometria = (
            QtCore.QPropertyAnimation(
                self.boton,
                b"geometry",
                self
            )
        )

        self.animacion_geometria.setDuration(
            self.duracion
        )

        self.animacion_geometria.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        # Sombra del botón.
        self.sombra = (
            QtWidgets.QGraphicsDropShadowEffect(
                self.boton
            )
        )

        self.sombra.setColor(
            QtGui.QColor(0, 0, 0, 170)
        )

        self.sombra.setBlurRadius(10)
        self.sombra.setOffset(0, 3)

        self.boton.setGraphicsEffect(
            self.sombra
        )

        self.animacion_sombra = (
            QtCore.QPropertyAnimation(
                self.sombra,
                b"blurRadius",
                self
            )
        )

        self.animacion_sombra.setDuration(
            self.duracion
        )

        self.animacion_sombra.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        self.boton.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )

        self.boton.installEventFilter(
            self
        )

    def obtener_geometria_grande(self):
        rectangulo = self.geometria_normal

        ancho_nuevo = round(
            rectangulo.width() * self.factor
        )

        alto_nuevo = round(
            rectangulo.height() * self.factor
        )

        diferencia_ancho = (
            ancho_nuevo - rectangulo.width()
        )

        diferencia_alto = (
            alto_nuevo - rectangulo.height()
        )

        return QtCore.QRect(
            rectangulo.x()
            - diferencia_ancho // 2,

            rectangulo.y()
            - diferencia_alto // 2,

            ancho_nuevo,
            alto_nuevo
        )

    def animar_geometria(self, destino):
        self.animacion_geometria.stop()

        self.animacion_geometria.setStartValue(
            self.boton.geometry()
        )

        self.animacion_geometria.setEndValue(
            destino
        )

        self.animacion_geometria.start()

    def animar_sombra(self, radio):
        self.animacion_sombra.stop()

        self.animacion_sombra.setStartValue(
            self.sombra.blurRadius()
        )

        self.animacion_sombra.setEndValue(
            radio
        )

        self.animacion_sombra.start()

    def actualizar_geometria_base(self):
        """
        Guarda la posición asignada por
        BotonesResponsivos.
        """

        self.animacion_geometria.stop()

        self.geometria_normal = QtCore.QRect(
            self.boton.geometry()
        )

        if self.cursor_encima:
            self.boton.setGeometry(
                self.obtener_geometria_grande()
            )

    def eventFilter(self, objeto, evento):
        if objeto is self.boton:

            if (
                evento.type()
                == QtCore.QEvent.Type.Enter
                and self.boton.isEnabled()
            ):
                self.cursor_encima = True

                self.boton.raise_()

                self.animar_geometria(
                    self.obtener_geometria_grande()
                )

                self.animar_sombra(28)

            elif (
                evento.type()
                == QtCore.QEvent.Type.Leave
            ):
                self.cursor_encima = False

                self.animar_geometria(
                    self.geometria_normal
                )

                self.animar_sombra(10)

        return super().eventFilter(
            objeto,
            evento
        )

class MenuUsuario(QtWidgets.QWidget):
    def __init__(self, jugador=None):
        super().__init__()

        quitar(self)

        self.jugador = jugador or {}
        self.db = ConexionBD()

        # Ventanas y transiciones.
        self.ventana_lecciones = None
        self.ventana_login = None

        self.form_ajustes = None
        self.transicion_ajustes = None

        # Referencias de la ventana de perfil.
        self.form_perfil = None
        self.transicion_perfil = None

        self.transicion_personajes = None

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        # Rutas y referencias utilizadas para mostrar el
        # personaje seleccionado por el usuario.
        self.base_dir = BASE_DIR
        self.proyecto_dir = PROYECTO_DIR

        # Fuente usada para el nombre del personaje.
        # Primero intenta cargar Pixel Operator Bold desde
        # el proyecto y después busca la fuente instalada.
        self.familia_fuente_personaje = (
            self.cargar_fuente_pixel_operator()
        )

        self.pixmap_personaje_original = None
        self.lbl_nombre_personaje_actual = None
        self.lbl_imagen_personaje_actual = None

        # Marco pixel art que se dibuja detrás del nombre.
        self.marco_nombre_personaje = None
        self._geometria_nombre_personaje_base = None

        # Animación del personaje en el menú.
        self.frames_personaje_menu = []
        self.indice_frame_personaje = 0
        self.personaje_animado_actual = None

        self.timer_animacion_personaje = QtCore.QTimer(
            self
        )
        self.timer_animacion_personaje.setInterval(
            VELOCIDAD_ANIMACION_PERSONAJE
        )
        self.timer_animacion_personaje.timeout.connect(
            self.actualizar_animacion_personaje
        )

        ruta_ui = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "Menu-Jugador.ui"
        )

        ruta_imagen = (
            PROYECTO_DIR
            / "assets"
            / "DISEÑOS"
            / "Menu-Usuario.png"
        )

        ruta_logo = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "Logo"
            / "logo_confondo.png"
        )

        ruta_botones = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "Botones"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n"
                f"{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n"
                f"{ruta_imagen}"
            )

        if not ruta_botones.exists():
            raise FileNotFoundError(
                "No se encontró la carpeta de botones:"
                f"\n{ruta_botones}"
            )

        if not ruta_logo.exists():
            raise FileNotFoundError(
                f"No se encontró el logo:\n"
                f"{ruta_logo}"
            )

        uic.loadUi(
            str(ruta_ui),
            self
        )

        # Recupera nuevamente el jugador para asegurar que
        # el personaje mostrado sea el guardado en MySQL.
        self.actualizar_jugador_desde_bd()

        # Configura los QLabel donde aparecerán el nombre
        # y la imagen del personaje guardado.
        self.configurar_vista_personaje()
        self.mostrar_personaje_usuario()

        # Corregir las rutas relativas de Qt Designer.
        self.corregir_rutas_stylesheet(
            ruta_botones
        )

        self.resize(
            1920,
            1080
        )

        self.setMinimumSize(
            0,
            0
        )

        self.setMaximumSize(
            16777215,
            16777215
        )

        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        self.logo_reutilizable = (
            LogoReutilizable(
                self,
                ruta_logo
            )
        )

        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        self.botones_menu = [
            self.btnJugar,
            self.btnAjustes,
            self.btnPerfil,
            self.btnCerrarSesion,

            self.btn_personaje,
        ]

        self.botones_responsivos = (
            BotonesResponsivos(
                ventana=self,
                botones=self.botones_menu,
                ancho_base=1920,
                alto_base=1080,
                escalar_iconos=True,
                escalar_fuentes=False,
            )
        )

        self.configurar_botones()

        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor=1.035,
                duracion=120,
                parent=self
            )
            for boton in self.botones_menu
        ]

        # Espera a que BotonesResponsivos coloque
        # correctamente los botones.
        QtCore.QTimer.singleShot(
            0,
            self.actualizar_hover_botones
        )

        self.conectar_eventos()

        # Ejecuta otra actualización cuando todos los widgets
        # ya tengan su tamaño y posición definitivos.
        QtCore.QTimer.singleShot(
            0,
            self.actualizar_tarjeta_personaje
        )


    # ======================================================
    # INFORMACIÓN DEL PERSONAJE SELECCIONADO
    # ======================================================

    def buscar_label_por_nombres(self, nombres):
        """
        Busca un QLabel usando varios objectName posibles.
        """

        for nombre in nombres:
            etiqueta = self.findChild(
                QtWidgets.QLabel,
                nombre
            )

            if etiqueta is not None:
                return etiqueta

        return None

    def cargar_fuente_pixel_operator(self):
        """
        Carga Pixel Operator Bold desde una carpeta de fuentes
        del proyecto. Si no encuentra el archivo, utiliza la
        fuente instalada en Windows.

        Nombres de archivo admitidos:
            PixelOperator-Bold.ttf
            PixelOperatorBold.ttf
            Pixel Operator Bold.ttf
            Pixel Operator - Bold.ttf
            pixel_operator_bold.ttf
        """

        nombres_archivo = (
            "PixelOperator-Bold.ttf",
            "PixelOperatorBold.ttf",
            "Pixel Operator Bold.ttf",
            "Pixel Operator - Bold.ttf",
            "pixel_operator_bold.ttf",
            "PixelOperator-Bold.otf",
            "Pixel Operator Bold.otf",
        )

        carpetas_fuentes = (
            self.proyecto_dir / "assets" / "FUENTES",
            self.proyecto_dir / "assets" / "fuentes",
            self.proyecto_dir / "ASSETS" / "FUENTES",
            self.proyecto_dir / "EXPO-DISEÑOS" / "FUENTES",
            self.proyecto_dir / "EXPO-DISEÑOS" / "Fuentes",
        )

        # Primero intenta cargar el archivo desde el proyecto.
        for carpeta in carpetas_fuentes:
            for nombre_archivo in nombres_archivo:
                ruta_fuente = carpeta / nombre_archivo

                if not ruta_fuente.exists():
                    continue

                id_fuente = (
                    QtGui.QFontDatabase.addApplicationFont(
                        str(ruta_fuente)
                    )
                )

                if id_fuente == -1:
                    continue

                familias = (
                    QtGui.QFontDatabase.applicationFontFamilies(
                        id_fuente
                    )
                )

                if familias:
                    familia = familias[0]

                    print(
                        "Fuente Pixel Operator cargada desde:",
                        ruta_fuente
                    )
                    print(
                        "Familia reconocida por PyQt6:",
                        familia
                    )

                    return familia

        # Si no existe el archivo, busca la fuente instalada.
        familias_instaladas = (
            QtGui.QFontDatabase.families()
        )

        nombres_preferidos = (
            "Pixel Operator",
            "Pixel Operator Bold",
            "Pixel Operator - Bold",
            "PixelOperator",
            "PixelOperator-Bold",
        )

        # Coincidencia exacta.
        for nombre_preferido in nombres_preferidos:
            for familia in familias_instaladas:
                if (
                    familia.casefold()
                    == nombre_preferido.casefold()
                ):
                    print(
                        "Fuente Pixel Operator instalada:",
                        familia
                    )
                    return familia

        # Coincidencia parcial.
        for familia in familias_instaladas:
            nombre_normalizado = familia.casefold()

            if (
                "pixel" in nombre_normalizado
                and "operator" in nombre_normalizado
            ):
                print(
                    "Fuente Pixel Operator encontrada:",
                    familia
                )
                return familia

        print(
            "ADVERTENCIA: Pixel Operator Bold no está instalada "
            "y tampoco se encontró su archivo en assets/FUENTES."
        )

        return "Arial"

    def crear_fuente_nombre_personaje(self):
        """
        Crea la fuente Pixel Operator Bold con un tamaño
        proporcional al alto del QLabel.
        """

        etiqueta = self.lbl_nombre_personaje_actual

        if etiqueta is None:
            return QtGui.QFont(
                self.familia_fuente_personaje
            )

        tamano_pixel = max(
            22,
            min(
                40,
                round(
                    etiqueta.height() * 0.36
                )
            )
        )

        fuente = QtGui.QFont(
            self.familia_fuente_personaje
        )

        # Algunos archivos registran la familia como
        # "Pixel Operator" y el estilo aparte como "Bold".
        fuente.setStyleName("Bold")

        fuente.setWeight(
            QtGui.QFont.Weight.Bold
        )

        fuente.setBold(True)

        # El tamaño en píxeles mantiene una apariencia más
        # consistente para una tipografía pixel art.
        fuente.setPixelSize(
            tamano_pixel
        )

        return fuente

    def configurar_vista_personaje(self):
        """
        Localiza y configura los QLabel creados en Qt Designer.

        ObjectName usados en tu formulario:
            lbl_nombrepersonaje
            lbl_imagenpersonaje
        """

        self.lbl_nombre_personaje_actual = (
            self.buscar_label_por_nombres(
                (
                    "lbl_nombrepersonaje",
                    "lbl_personaje",
                    "lbl_nombre_personaje",
                    "lblNombrePersonaje",
                    "label_personaje",
                    "labelPersonaje",
                )
            )
        )

        self.lbl_imagen_personaje_actual = (
            self.buscar_label_por_nombres(
                (
                    "lbl_imagenpersonaje",
                    "lbl_foto_personaje",
                    "lbl_personaje_seleccionado",
                    "lblFotoPersonaje",
                    "lblImagenPersonaje",
                    "label_foto_personaje",
                    "labelFotoPersonaje",
                )
            )
        )

        if self.lbl_nombre_personaje_actual is None:
            print(
                "ADVERTENCIA: No se encontró lbl_nombrepersonaje."
            )
        else:
            self._geometria_nombre_personaje_base = QtCore.QRect(
                self.lbl_nombre_personaje_actual.geometry()
            )

            self.lbl_nombre_personaje_actual.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter
            )

            self.lbl_nombre_personaje_actual.setWordWrap(
                False
            )

            self.lbl_nombre_personaje_actual.setContentsMargins(
                34,
                8,
                34,
                8
            )

            self.lbl_nombre_personaje_actual.setStyleSheet(
                """
                QLabel {
                    color: #082B63;
                    background-color: transparent;
                    border: none;
                }
                """
            )

            # Crea el cuadro pixel art detrás del QLabel del nombre.
            padre_nombre = (
                self.lbl_nombre_personaje_actual.parentWidget()
                or self
            )

            self.marco_nombre_personaje = MarcoNombrePersonaje(
                padre_nombre
            )

            self.marco_nombre_personaje.setObjectName(
                "marco_nombre_personaje"
            )

            self.marco_nombre_personaje.setGeometry(
                self.lbl_nombre_personaje_actual.geometry()
            )

            self.marco_nombre_personaje.show()
            self.marco_nombre_personaje.stackUnder(
                self.lbl_nombre_personaje_actual
            )

        if self.lbl_imagen_personaje_actual is None:
            print(
                "ADVERTENCIA: No se encontró lbl_imagenpersonaje."
            )
        else:
            self.lbl_imagen_personaje_actual.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter
            )

            self.lbl_imagen_personaje_actual.setScaledContents(
                False
            )

            self.lbl_imagen_personaje_actual.setContentsMargins(
                0,
                0,
                0,
                0
            )

            self.lbl_imagen_personaje_actual.setStyleSheet(
                """
                QLabel {
                    color: #000000;
                    background: transparent;
                    border: none;
                }
                """
            )

        self.centrar_nombre_personaje()

    def centrar_nombre_personaje(self):
        """
        Centra el nombre sobre la tarjeta del personaje y coloca
        detrás un cuadro pixel art inspirado en la referencia.
        """

        etiqueta_nombre = self.lbl_nombre_personaje_actual
        etiqueta_imagen = self.lbl_imagen_personaje_actual

        if etiqueta_nombre is None:
            return

        etiqueta_nombre.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        geometria_base = (
            self._geometria_nombre_personaje_base
            or etiqueta_nombre.geometry()
        )

        escala_x = max(
            0.35,
            self.width() / 1920
        )

        escala_y = max(
            0.35,
            self.height() / 1080
        )

        # El cuadro será más ancho que el QLabel original para
        # que tenga la apariencia de la segunda imagen.
        ancho_base = max(
            380,
            geometria_base.width()
        )

        alto_base = max(
            92,
            geometria_base.height()
        )

        ancho_cuadro = max(
            230,
            round(ancho_base * escala_x)
        )

        alto_cuadro = max(
            62,
            round(alto_base * escala_y)
        )

        padre = etiqueta_nombre.parentWidget()

        if padre is None:
            padre = self

        # El centro horizontal se toma del QLabel de la imagen
        # para que el nombre quede exactamente centrado respecto
        # al personaje seleccionado.
        if (
            etiqueta_imagen is not None
            and etiqueta_imagen.parentWidget() is padre
        ):
            centro_x = etiqueta_imagen.geometry().center().x()
        else:
            centro_x = geometria_base.center().x()

        x = centro_x - ancho_cuadro // 2

        # Conserva la altura definida en Qt Designer.
        y = round(
            geometria_base.y() * escala_y
        )

        x = max(
            0,
            min(
                x,
                max(0, padre.width() - ancho_cuadro)
            )
        )

        y = max(
            0,
            min(
                y,
                max(0, padre.height() - alto_cuadro)
            )
        )

        geometria_cuadro = QtCore.QRect(
            x,
            y,
            ancho_cuadro,
            alto_cuadro
        )

        etiqueta_nombre.setGeometry(
            geometria_cuadro
        )

        if self.marco_nombre_personaje is not None:
            self.marco_nombre_personaje.setGeometry(
                geometria_cuadro
            )

            self.marco_nombre_personaje.show()
            self.marco_nombre_personaje.raise_()

        fuente = self.crear_fuente_nombre_personaje()
        etiqueta_nombre.setFont(fuente)

        etiqueta_nombre.show()
        etiqueta_nombre.raise_()

    def obtener_id_jugador(self):
        """
        Obtiene el ID del jugador de la sesión actual.

        Admite que la sesión llegue como diccionario, número
        entero u objeto con el atributo id_jugador.
        """

        if self.jugador is None:
            return None

        if isinstance(self.jugador, dict):
            return self.jugador.get("id_jugador")

        if isinstance(self.jugador, int):
            return self.jugador

        return getattr(
            self.jugador,
            "id_jugador",
            None
        )

    def actualizar_jugador_desde_bd(self):
        """
        Actualiza el diccionario de sesión con los datos más
        recientes del jugador, incluido el personaje guardado.
        """

        id_jugador = self.obtener_id_jugador()

        if id_jugador is None:
            return

        if not hasattr(
            self.db,
            "buscar_jugador_por_id"
        ):
            return

        try:
            jugador_bd = self.db.buscar_jugador_por_id(
                id_jugador
            )

            if not jugador_bd:
                return

            datos = dict(jugador_bd)

            if isinstance(self.jugador, dict):
                self.jugador.update(datos)
            else:
                for clave, valor in datos.items():
                    try:
                        setattr(
                            self.jugador,
                            clave,
                            valor
                        )
                    except Exception:
                        pass

        except Exception as error:
            print(
                "No se pudieron actualizar los datos "
                f"del jugador desde MySQL: {error}"
            )

    def obtener_personaje_sesion(self):
        """
        Obtiene el personaje guardado para el jugador y normaliza
        nombres antiguos. Funciona con diccionarios y objetos.
        """

        if isinstance(self.jugador, dict):
            valor_personaje = self.jugador.get("personaje")
        else:
            valor_personaje = getattr(
                self.jugador,
                "personaje",
                None
            )

        personaje = str(
            valor_personaje or ""
        ).strip().lower()

        equivalencias = {
            "cerdito": "cerdo",
            "jugador": "cerdo",
            "banano": "gato",
            "patito": "pato",
        }

        return equivalencias.get(
            personaje,
            personaje
        )

    def mostrar_personaje_usuario(self):
        """
        Muestra en el cuadro el nombre del personaje guardado en
        MySQL y reproduce su animación dentro del menú.
        """

        if (
            self.lbl_nombre_personaje_actual is None
            or self.lbl_imagen_personaje_actual is None
        ):
            return

        personaje = self.obtener_personaje_sesion()

        nombres_visibles = {
            "cerdo": "CERDO",
            "gato": "GATO",
            "pato": "PATO",
        }

        if not personaje:
            self.timer_animacion_personaje.stop()
            self.frames_personaje_menu = []
            self.personaje_animado_actual = None
            self.pixmap_personaje_original = None

            self.lbl_nombre_personaje_actual.setText(
                "SIN PERSONAJE"
            )

            self.lbl_imagen_personaje_actual.clear()
            self.centrar_nombre_personaje()
            return

        # Para personajes conocidos usa su nombre definido. Si en
        # el futuro agregas otro personaje, mostrará automáticamente
        # el valor guardado en la base de datos en mayúsculas.
        nombre_visible = nombres_visibles.get(
            personaje,
            personaje.replace("_", " ").upper()
        )

        self.lbl_nombre_personaje_actual.setText(
            nombre_visible
        )

        self.centrar_nombre_personaje()

        if (
            personaje != self.personaje_animado_actual
            or not self.frames_personaje_menu
        ):
            self.timer_animacion_personaje.stop()

            self.frames_personaje_menu = (
                self.cargar_frames_personaje_menu(
                    personaje
                )
            )

            self.personaje_animado_actual = personaje
            self.indice_frame_personaje = 0

        if not self.frames_personaje_menu:
            self.pixmap_personaje_original = None
            self.lbl_imagen_personaje_actual.clear()
            self.lbl_imagen_personaje_actual.setText(
                "IMAGEN NO ENCONTRADA"
            )

            print(
                "No se encontraron frames para:",
                personaje
            )

            if self.marco_nombre_personaje is not None:
                self.marco_nombre_personaje.raise_()

            self.lbl_nombre_personaje_actual.raise_()
            self.lbl_imagen_personaje_actual.raise_()
            return

        self.lbl_imagen_personaje_actual.setText("")

        self.pixmap_personaje_original = (
            self.frames_personaje_menu[
                self.indice_frame_personaje
            ]
        )

        self.actualizar_imagen_personaje()

        if len(self.frames_personaje_menu) > 1:
            self.timer_animacion_personaje.start()
        else:
            self.timer_animacion_personaje.stop()

        if self.marco_nombre_personaje is not None:
            self.marco_nombre_personaje.raise_()

        self.lbl_nombre_personaje_actual.raise_()
        self.lbl_imagen_personaje_actual.raise_()

    def obtener_configuracion_frames_personaje(
        self,
        personaje
    ):
        """
        Devuelve las carpetas y los frames en el orden
        correcto para cada personaje.
        """

        configuraciones = {
            "cerdo": {
                "carpetas": (
                    "cerdo",
                    "cerdito",
                    "jugador",
                ),
                "frames": (
                    ("jugador_caminar1.png",),
                    ("jugador_caminar2.png",),
                    ("jugador_caminar3.png",),
                    ("jugador_caminar4.png",),
                ),
            },

            "gato": {
                "carpetas": (
                    "gato",
                    "banano",
                ),
                "frames": (
                    ("gato_caminar2.png",),
                    ("gato_caminar3.png",),
                    ("gato_caminar4.png",),
                    ("gato_caminar5.png",),
                    ("gato_caminar6.png",),
                    ("gato_caminar7.png",),
                    ("gato_caminar8.png",),
                ),
            },

            "pato": {
                "carpetas": (
                    "pato",
                    "patito",
                ),
                "frames": (
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
                ),
            },
        }

        return configuraciones.get(
            personaje
        )

    def obtener_raices_personajes_menu(self):
        return (
            self.proyecto_dir
            / "assets"
            / "personajes",

            self.proyecto_dir
            / "ASSETS"
            / "PERSONAJES",

            self.proyecto_dir
            / "juego"
            / "assets"
            / "personajes",

            self.proyecto_dir
            / "EXPO-DISEÑOS"
            / "DISEÑOS"
            / "PERSONAJES",
        )

    def buscar_frame_personaje_menu(
        self,
        nombres_carpetas,
        nombres_archivo
    ):
        """
        Busca un frame de animación en todas las ubicaciones
        compatibles con el proyecto.
        """

        for raiz in self.obtener_raices_personajes_menu():
            if not raiz.exists():
                continue

            for nombre_carpeta in nombres_carpetas:
                carpeta = raiz / nombre_carpeta

                if not carpeta.exists():
                    continue

                for nombre_archivo in nombres_archivo:
                    ruta = carpeta / nombre_archivo

                    if ruta.exists():
                        return ruta

                for nombre_archivo in nombres_archivo:
                    encontrados = list(
                        carpeta.rglob(
                            nombre_archivo
                        )
                    )

                    if encontrados:
                        return encontrados[0]

        return None

    def cargar_frames_personaje_menu(
        self,
        personaje
    ):
        """
        Carga todos los frames del personaje como QPixmap.
        """

        configuracion = (
            self.obtener_configuracion_frames_personaje(
                personaje
            )
        )

        if configuracion is None:
            return []

        frames_cargados = []

        for opciones_archivo in configuracion["frames"]:
            ruta_frame = self.buscar_frame_personaje_menu(
                configuracion["carpetas"],
                opciones_archivo
            )

            if ruta_frame is None:
                print(
                    "No se encontró uno de los frames de",
                    personaje,
                    opciones_archivo
                )
                continue

            pixmap = QtGui.QPixmap(
                str(ruta_frame)
            )

            if not pixmap.isNull():
                # Elimina márgenes transparentes desiguales.
                # Así todos los personajes quedan centrados.
                pixmap_centrado = recortar_pixmap_transparente(
                    pixmap,
                    margen=2,
                )

                frames_cargados.append(
                    pixmap_centrado
                )

        return frames_cargados

    def actualizar_animacion_personaje(self):
        """
        Avanza al siguiente frame del personaje.
        """

        if not self.frames_personaje_menu:
            self.timer_animacion_personaje.stop()
            return

        self.indice_frame_personaje += 1

        if (
            self.indice_frame_personaje
            >= len(self.frames_personaje_menu)
        ):
            self.indice_frame_personaje = 0

        self.pixmap_personaje_original = (
            self.frames_personaje_menu[
                self.indice_frame_personaje
            ]
        )

        self.actualizar_imagen_personaje()

    def actualizar_imagen_personaje(self):
        """
        Escala el frame sin deformarlo y centra el contenido
        visible de CERDO, GATO y PATO dentro del QLabel.
        """

        etiqueta = self.lbl_imagen_personaje_actual

        if etiqueta is None:
            return

        if self.pixmap_personaje_original is None:
            etiqueta.clear()
            return

        ancho = etiqueta.width()
        alto = etiqueta.height()

        if ancho <= 0 or alto <= 0:
            return

        pixmap_centrado = recortar_pixmap_transparente(
            self.pixmap_personaje_original,
            margen=2,
        )

        margen_horizontal = max(
            8,
            round(ancho * 0.04),
        )

        margen_vertical = max(
            8,
            round(alto * 0.04),
        )

        pixmap_escalado = pixmap_centrado.scaled(
            max(1, ancho - margen_horizontal * 2),
            max(1, alto - margen_vertical * 2),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.FastTransformation,
        )

        etiqueta.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        etiqueta.setScaledContents(False)
        etiqueta.setContentsMargins(0, 0, 0, 0)
        etiqueta.setPixmap(pixmap_escalado)

    def corregir_rutas_stylesheet(
        self,
        ruta_botones
    ):
        ruta_absoluta = (
            ruta_botones
            .resolve()
            .as_posix()
        )

        controles = [
            self,
            *self.findChildren(
                QtWidgets.QWidget
            ),
        ]

        for control in controles:
            estilo_original = (
                control.styleSheet()
            )

            if not estilo_original:
                continue

            estilo_corregido = estilo_original

            estilo_corregido = (
                estilo_corregido.replace(
                    'url("../Botones/',
                    f'url("{ruta_absoluta}/'
                )
            )

            estilo_corregido = (
                estilo_corregido.replace(
                    "url('../Botones/",
                    f"url('{ruta_absoluta}/"
                )
            )

            estilo_corregido = (
                estilo_corregido.replace(
                    "url(../Botones/",
                    f"url({ruta_absoluta}/"
                )
            )

            if (
                estilo_corregido
                != estilo_original
            ):
                control.setStyleSheet(
                    estilo_corregido
                )

    def configurar_botones(self):
        for boton in self.botones_menu:
            boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape
                    .PointingHandCursor
                )
            )

    def actualizar_hover_botones(self):
        """
        Actualiza las posiciones originales
        utilizadas por las animaciones hover.
        """

        for efecto in getattr(
            self,
            "efectos_hover",
            []
        ):
            efecto.actualizar_geometria_base()

    def conectar_eventos(self):
        self.btnJugar.clicked.connect(
            self.abrir_lecciones
        )

        self.btnAjustes.clicked.connect(
            self.abrir_ajustes
        )

        self.btnPerfil.clicked.connect(
            self.abrir_perfil
        )

        self.btnCerrarSesion.clicked.connect(
            self.cerrar_sesion
        )

        self.btn_personaje.clicked.connect(
            self.abrir_personajes
        )

    def abrir_personajes(self):
        """
        Abre Personajes.py conservando los datos
        del jugador que inició sesión.
        """

        try:

            from Personajes import Personajes


            Personajes.jugador_pendiente = (
                self.jugador
            )

            self.transicion_personajes = (
                FormTransicion(
                    self,
                    Personajes
                )
            )

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error al abrir personajes",
                "No se pudo abrir la ventana "
                "de personajes."
                f"\n\nDetalles:\n{error}",
                "error"
            )

    def abrir_perfil(self):
        """
        Abre Perfil.py con la información del jugador actual.
        Evita crear más de una ventana de perfil.
        """

        if (
            self.form_perfil is not None
            and self.form_perfil.isVisible()
        ):
            self.form_perfil.raise_()
            self.form_perfil.activateWindow()
            return

        try:
            # Importación local para evitar importaciones circulares.
            from Perfil import PerfilWindow

            id_jugador = self.obtener_id_jugador()

            if id_jugador is None:
                raise ValueError(
                    "No se encontró el id_jugador del "
                    "usuario que inició sesión."
                )

            self.form_perfil = PerfilWindow(
                id_jugador=id_jugador,
                formulario_anterior=self,
            )

            self.form_perfil.setAttribute(
                QtCore.Qt.WidgetAttribute.WA_DeleteOnClose,
                True,
            )

            self.form_perfil.destroyed.connect(
                self._limpiar_form_perfil
            )

            self.transicion_perfil = FormTransicion(
                self,
                self.form_perfil,
            )

        except Exception as error:
            # Limpia referencias si la apertura falló.
            self.form_perfil = None
            self.transicion_perfil = None

            Alertas.mostrar(
                self,
                "Error al abrir perfil",
                "No se pudo abrir la ventana de perfil."
                f"\n\nDetalles:\n{error}",
                "error",
            )

    def _limpiar_form_perfil(self, *_args):
        """
        Limpia las referencias cuando Perfil se cierra.
        """

        self.form_perfil = None
        self.transicion_perfil = None

    def abrir_ajustes(self):
        """
        Abre Ajustes desde el menú del jugador.
        """

        # Si ya está abierta, solamente se lleva
        # al frente.
        if (
            self.form_ajustes is not None
            and self.form_ajustes.isVisible()
        ):
            self.form_ajustes.raise_()
            self.form_ajustes.activateWindow()
            return

        try:
            self.form_ajustes = Ajustes(
                ventana_anterior=self,
                jugador=self.jugador,
                desde_juego=False,
            )

            self.form_ajustes.setAttribute(
                QtCore.Qt.WidgetAttribute
                .WA_DeleteOnClose,
                True
            )

            self.form_ajustes.destroyed.connect(
                self._limpiar_form_ajustes
            )

            self.transicion_ajustes = (
                FormTransicion(
                    self,
                    self.form_ajustes
                )
            )

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error al abrir ajustes",
                "No se pudo abrir la ventana "
                "de ajustes."
                f"\n\nDetalles:\n{error}",
                "error"
            )

    def _limpiar_form_ajustes(self):
        """
        Limpia las referencias para poder abrir
        nuevamente la ventana de Ajustes.
        """

        self.form_ajustes = None
        self.transicion_ajustes = None

    def abrir_lecciones(self):
        try:
            from Lecciones import Lecciones

            try:
                self.ventana_lecciones = Lecciones(
                    jugador=self.jugador,
                    ventana_anterior=self,
                    tipo_usuario="jugador"
                )

            except TypeError:
                try:
                    self.ventana_lecciones = Lecciones(
                        self.jugador,
                        self
                    )

                except TypeError:
                    try:
                        self.ventana_lecciones = (
                            Lecciones(
                                self.jugador
                            )
                        )

                    except TypeError:
                        self.ventana_lecciones = (
                            Lecciones()
                        )

            self.transicion_lecciones = (
                FormTransicion(
                    self,
                    self.ventana_lecciones
                )
            )

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error al abrir lecciones",
                "No se pudo abrir la ventana "
                "de lecciones."
                f"\n\nDetalles:\n{error}",
                "error"
            )

    def cerrar_sesion(self):
        respuesta = Alertas.confirmar(
            self,
            "Cerrar sesión",
            "¿Seguro que deseas cerrar sesión?",
            tipo="error",
            texto_confirmar="SÍ, CERRAR",
            texto_cancelar="CANCELAR"
        )

        if not respuesta:
            return

        try:
            from Login import LoginWindow

            app = (
                QtWidgets.QApplication.instance()
            )

            if hasattr(
                app,
                "historial_forms"
            ):
                app.historial_forms.clear()

            self.ventana_login = (
                LoginWindow()
            )

            app.ventana_login = (
                self.ventana_login
            )

            self.ventana_login.resize(
                1020,
                720
            )

            self.ventana_login.showNormal()

            self.close()

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error al cerrar sesión",
                "No se pudo abrir el Login:"
                f"\n{error}",
                "error"
            )

    def actualizar_tarjeta_personaje(self):
        # Recupera los datos más recientes y vuelve a mostrar
        # el nombre y la imagen del personaje.
        self.actualizar_jugador_desde_bd()
        self.mostrar_personaje_usuario()

    def showEvent(self, event):
        super().showEvent(event)

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_tarjeta_personaje
        )

    def hideEvent(self, event):
        if hasattr(
            self,
            "timer_animacion_personaje"
        ):
            self.timer_animacion_personaje.stop()

        super().hideEvent(event)

    def resizeEvent(self, event):
        # Ajustar el fondo.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        if hasattr(self, "MenuJugador"):
            self.MenuJugador.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )

            self.MenuJugador.raise_()

        if hasattr(self, "btn_personaje"):
            self.btn_personaje.show()
            self.btn_personaje.raise_()

        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        if hasattr(
            self,
            "logo_reutilizable"
        ):
            self.logo_reutilizable.actualizar()

        if hasattr(
            self,
            "botones_responsivos"
        ):
            self.botones_responsivos.ajustar()

        if hasattr(
            self,
            "pixmap_personaje_original"
        ):
            self.actualizar_imagen_personaje()

        self.centrar_nombre_personaje()

        if self.marco_nombre_personaje is not None:
            self.marco_nombre_personaje.show()
            self.marco_nombre_personaje.raise_()

        if self.lbl_nombre_personaje_actual is not None:
            self.lbl_nombre_personaje_actual.raise_()

        if self.lbl_imagen_personaje_actual is not None:
            self.lbl_imagen_personaje_actual.raise_()

        if hasattr(self, "efectos_hover"):
            QtCore.QTimer.singleShot(
                0,
                self.actualizar_hover_botones
            )

        super().resizeEvent(event)