from pathlib import Path
import re
import unicodedata

from PyQt6 import QtCore, QtGui, QtWidgets, uic

from ConexionBD import ConexionBD
from quitar_barra import quitar
from AjusteResponsive import BotonesResponsivos

try:
    from Alertas import Alertas
except ImportError:
    Alertas = None

try:
    from Transicion import FormTransicion
except ImportError:
    FormTransicion = None


# ==========================================================
# RUTAS PRINCIPALES
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
PROYECTO_DIR = BASE_DIR.parent

RUTA_UI = (
    PROYECTO_DIR
    / "EXPO-DISEÑOS"
    / "DESIGNER"
    / "Perfil.ui"
)

RUTA_FUENTE_NORMAL = (
    PROYECTO_DIR
    / "assets"
    / "FUENTES"
    / "PixelOperator.ttf"
)

RUTA_FUENTE_BOLD = (
    PROYECTO_DIR
    / "assets"
    / "FUENTES"
    / "PixelOperator-Bold.ttf"
)

# El proyecto tiene 4 niveles y una prueba final.
TOTAL_NIVELES = 5

# Configuración de las vidas del jugador.
MAX_VIDAS = 5
MINUTOS_RECUPERACION_VIDAS = 5
# Consulta vidas y progreso cada 2 segundos mientras el perfil esté visible.
INTERVALO_ACTUALIZACION_PERFIL_MS = 2000


# ==========================================================
# FONDO RESPONSIVO
# ==========================================================

class FondoImagen(QtWidgets.QLabel):
    def __init__(
        self,
        contenedor: QtWidgets.QWidget,
        ruta_imagen: Path
    ):
        super().__init__(contenedor)

        self.contenedor = contenedor
        self.ruta_imagen = Path(ruta_imagen)

        self.pixmap_original = QtGui.QPixmap(
            str(self.ruta_imagen)
        )

        if self.pixmap_original.isNull():
            raise FileNotFoundError(
                "No se pudo cargar el fondo:\n"
                f"{self.ruta_imagen}"
            )

        self.setObjectName("fondo_perfil")

        self.setScaledContents(True)

        self.setGeometry(
            self.contenedor.rect()
        )

        self.setPixmap(
            self.pixmap_original
        )

        # Evita que el fondo bloquee los botones.
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

        self.lower()

    def actualizar_tamano(self):
        self.setGeometry(
            self.contenedor.rect()
        )

        self.lower()



# ==========================================================
# ELEMENTOS RESPONSIVOS
# ==========================================================

class ElementosResponsivos(QtCore.QObject):
    """
    Escala posición, tamaño y fuente de los controles tomando
    como referencia el diseño original de 1920 x 1080.

    Los botones se excluyen de esta clase porque se ajustan con
    BotonesResponsivos, evitando que dos clases cambien al mismo
    tiempo la geometría del mismo botón.
    """

    def __init__(
        self,
        ventana: QtWidgets.QWidget,
        elementos: list[QtWidgets.QWidget],
        ancho_base: int = 1920,
        alto_base: int = 1080,
        escalar_fuentes: bool = True,
    ):
        super().__init__(ventana)

        self.ventana = ventana
        self.ancho_base = ancho_base
        self.alto_base = alto_base
        self.escalar_fuentes = escalar_fuentes

        self.elementos = [
            elemento
            for elemento in elementos
            if elemento is not None
        ]

        self.geometrias_originales = {
            elemento: QtCore.QRect(elemento.geometry())
            for elemento in self.elementos
        }

        self.fuentes_originales = {}

        for elemento in self.elementos:
            fuente = QtGui.QFont(elemento.font())
            tamano = fuente.pointSizeF()

            self.fuentes_originales[elemento] = (
                fuente,
                tamano
            )

    def ajustar(self):
        if self.ventana.width() <= 0 or self.ventana.height() <= 0:
            return

        escala_x = self.ventana.width() / self.ancho_base
        escala_y = self.ventana.height() / self.alto_base
        escala_fuente = min(escala_x, escala_y)

        for elemento in self.elementos:
            if elemento not in self.geometrias_originales:
                continue

            original = self.geometrias_originales[elemento]

            elemento.setGeometry(
                round(original.x() * escala_x),
                round(original.y() * escala_y),
                max(1, round(original.width() * escala_x)),
                max(1, round(original.height() * escala_y)),
            )

            if not self.escalar_fuentes:
                continue

            fuente_original, tamano_original = (
                self.fuentes_originales[elemento]
            )

            # pointSizeF() puede devolver -1 cuando el widget usa
            # un tamaño definido en píxeles o heredado.
            if tamano_original <= 0:
                continue

            fuente_escalada = QtGui.QFont(fuente_original)
            fuente_escalada.setPointSizeF(
                max(6.0, tamano_original * escala_fuente)
            )

            elemento.setFont(fuente_escalada)


# ==========================================================
# EFECTO HOVER DEL BOTÓN VOLVER
# ==========================================================

class EfectoHoverBoton(QtCore.QObject):
    """
    Agranda suavemente el botón y aumenta su sombra cuando
    el cursor pasa sobre él.
    """

    def __init__(
        self,
        boton: QtWidgets.QPushButton,
        factor: float = 1.04,
        duracion: int = 120,
        parent=None,
    ):
        super().__init__(parent if parent is not None else boton)

        self.boton = boton
        self.factor = factor
        self.duracion = duracion
        self.cursor_encima = False

        self.geometria_normal = QtCore.QRect(
            self.boton.geometry()
        )

        self.animacion_geometria = QtCore.QPropertyAnimation(
            self.boton,
            b"geometry",
            self,
        )
        self.animacion_geometria.setDuration(self.duracion)
        self.animacion_geometria.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        self.sombra = QtWidgets.QGraphicsDropShadowEffect(
            self.boton
        )
        self.sombra.setColor(QtGui.QColor(0, 0, 0, 170))
        self.sombra.setBlurRadius(10)
        self.sombra.setOffset(0, 3)
        self.boton.setGraphicsEffect(self.sombra)

        self.animacion_sombra = QtCore.QPropertyAnimation(
            self.sombra,
            b"blurRadius",
            self,
        )
        self.animacion_sombra.setDuration(self.duracion)
        self.animacion_sombra.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        self.boton.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )
        self.boton.installEventFilter(self)

    def obtener_geometria_grande(self):
        rectangulo = self.geometria_normal

        ancho_nuevo = round(rectangulo.width() * self.factor)
        alto_nuevo = round(rectangulo.height() * self.factor)

        diferencia_ancho = ancho_nuevo - rectangulo.width()
        diferencia_alto = alto_nuevo - rectangulo.height()

        return QtCore.QRect(
            rectangulo.x() - diferencia_ancho // 2,
            rectangulo.y() - diferencia_alto // 2,
            ancho_nuevo,
            alto_nuevo,
        )

    def animar_geometria(self, destino):
        self.animacion_geometria.stop()
        self.animacion_geometria.setStartValue(
            self.boton.geometry()
        )
        self.animacion_geometria.setEndValue(destino)
        self.animacion_geometria.start()

    def animar_sombra(self, radio):
        self.animacion_sombra.stop()
        self.animacion_sombra.setStartValue(
            self.sombra.blurRadius()
        )
        self.animacion_sombra.setEndValue(radio)
        self.animacion_sombra.start()

    def actualizar_geometria_base(self):
        """
        Guarda la posición y tamaño asignados por
        BotonesResponsivos.
        """

        self.animacion_geometria.stop()

        if not self.cursor_encima:
            self.geometria_normal = QtCore.QRect(
                self.boton.geometry()
            )

    def restaurar_inmediatamente(self):
        self.cursor_encima = False
        self.animacion_geometria.stop()
        self.animacion_sombra.stop()
        self.boton.setGeometry(self.geometria_normal)
        self.sombra.setBlurRadius(10)

    def eventFilter(self, objeto, evento):
        if objeto is self.boton:
            if (
                evento.type() == QtCore.QEvent.Type.Enter
                and self.boton.isEnabled()
            ):
                self.cursor_encima = True
                self.geometria_normal = QtCore.QRect(
                    self.boton.geometry()
                )
                self.boton.raise_()
                self.animar_geometria(
                    self.obtener_geometria_grande()
                )
                self.animar_sombra(28)

            elif evento.type() == QtCore.QEvent.Type.Leave:
                if self.cursor_encima:
                    self.cursor_encima = False
                    self.animar_geometria(
                        self.geometria_normal
                    )
                    self.animar_sombra(10)

            elif evento.type() == QtCore.QEvent.Type.EnabledChange:
                if not self.boton.isEnabled():
                    self.restaurar_inmediatamente()

        return super().eventFilter(objeto, evento)


# ==========================================================
# VENTANA DE PERFIL
# ==========================================================

class PerfilWindow(QtWidgets.QWidget):
    def __init__(
        self,
        id_jugador: int,
        formulario_anterior=None
    ):
        super().__init__()

        quitar(self)

        self.ANCHO_BASE = 1920
        self.ALTO_BASE = 1080
        self._pantalla_completa_aplicada = False

        # Instancia para realizar las consultas.
        self.base_datos = ConexionBD()

        self.id_jugador = id_jugador
        self.formulario_anterior = formulario_anterior

        self.pixmap_personaje_original = None
        self.transicion_volver = None

        # Evita ejecutar dos consultas simultáneas si una actualización
        # tarda más de lo esperado.
        self._actualizacion_en_curso = False

        # Mantiene vivas las animaciones de las barras de progreso.
        self.animaciones_progreso = {}

        if not RUTA_UI.exists():
            raise FileNotFoundError(
                "No se encontró el formulario Perfil.ui:\n"
                f"{RUTA_UI}"
            )

        uic.loadUi(
            str(RUTA_UI),
            self
        )

        # Carga PixelOperator y la aplica a todos los controles
        # antes de guardar las geometrías y fuentes responsivas.
        self.cargar_y_aplicar_fuentes()

        self.setMinimumSize(0, 0)
        self.setMaximumSize(
            16777215,
            16777215
        )

        self.resize(
            1920,
            1080
        )

        if hasattr(self, "Perfil"):
            self.contenedor_principal = self.Perfil
        else:
            self.contenedor_principal = self

        ruta_fondo = self.buscar_fondo_perfil()

        self.fondo = FondoImagen(
            self.contenedor_principal,
            ruta_fondo
        )

        self.subir_controles_sobre_fondo()
        self.configurar_formulario()
        self.configurar_responsividad()
        self.configurar_actualizacion_tiempo_real()

        QtCore.QTimer.singleShot(
            0,
            self.cargar_toda_la_informacion
        )

        QtCore.QTimer.singleShot(
            0,
            self.mostrar_pantalla_completa
        )

    # ======================================================
    # FUENTES PIXELOPERATOR
    # ======================================================

    @staticmethod
    def registrar_fuente(ruta_fuente: Path):
        """
        Registra una fuente TTF y devuelve su familia interna.
        """

        ruta_fuente = Path(ruta_fuente)

        if not ruta_fuente.exists():
            print(
                "No se encontró la fuente:\n"
                f"{ruta_fuente}"
            )
            return None

        id_fuente = QtGui.QFontDatabase.addApplicationFont(
            str(ruta_fuente)
        )

        if id_fuente == -1:
            print(
                "No se pudo registrar la fuente:\n"
                f"{ruta_fuente}"
            )
            return None

        familias = QtGui.QFontDatabase.applicationFontFamilies(
            id_fuente
        )

        if not familias:
            print(
                "La fuente no devolvió una familia válida:\n"
                f"{ruta_fuente}"
            )
            return None

        return familias[0]

    @staticmethod
    def quitar_font_family_stylesheet(control):
        """
        Elimina solamente font-family del stylesheet para evitar
        que Qt Designer sobrescriba PixelOperator.
        """

        estilo = control.styleSheet()

        if not estilo:
            return

        estilo_corregido = re.sub(
            r"font-family\s*:\s*[^;}{]+;?",
            "",
            estilo,
            flags=re.IGNORECASE,
        )

        if estilo_corregido != estilo:
            control.setStyleSheet(estilo_corregido)

    def aplicar_fuente_a_control(
        self,
        control: QtWidgets.QWidget,
        usar_bold: bool = False,
    ):
        """
        Cambia únicamente la familia y el peso. Conserva el
        tamaño definido en Qt Designer.
        """

        self.quitar_font_family_stylesheet(control)

        fuente = QtGui.QFont(control.font())

        if usar_bold and self.familia_pixel_bold:
            fuente.setFamily(self.familia_pixel_bold)
            fuente.setBold(True)
        else:
            fuente.setFamily(self.familia_pixel_normal)

            # Conserva la negrita original del Designer.
            if fuente.bold():
                fuente.setBold(True)

        control.setFont(fuente)

    def obtener_labels_responsivos(self):
        """
        Obtiene todos los QLabel creados en Qt Designer.
        Su posición y tamaño originales se toman directamente
        del archivo Perfil.ui.
        """

        labels = []

        for label in self.contenedor_principal.findChildren(
                QtWidgets.QLabel
        ):
            # No incluir el fondo creado desde Python.
            if label is self.fondo:
                continue

            # Ignorar labels internos sin nombre.
            if not label.objectName():
                continue

            labels.append(label)

        return labels

    def cargar_y_aplicar_fuentes(self):
        """
        Aplica PixelOperator a labels, botones, barras, tabla,
        encabezados y demás controles del perfil.
        """

        self.familia_pixel_normal = self.registrar_fuente(
            RUTA_FUENTE_NORMAL
        )

        self.familia_pixel_bold = self.registrar_fuente(
            RUTA_FUENTE_BOLD
        )

        if not self.familia_pixel_normal:
            # El formulario continúa funcionando aunque falte
            # la fuente; solamente conservará la fuente del UI.
            return

        controles = [
            self,
            *self.findChildren(QtWidgets.QWidget),
        ]

        for control in controles:
            fuente_actual = control.font()

            usar_bold = (
                fuente_actual.bold()
                or isinstance(control, QtWidgets.QPushButton)
                or isinstance(control, QtWidgets.QHeaderView)
            )

            self.aplicar_fuente_a_control(
                control,
                usar_bold=usar_bold,
            )

        # Refuerzo para los controles cuyo texto se pinta mediante
        # componentes internos de Qt.
        if hasattr(self, "dgv_perfil"):
            fuente_tabla = QtGui.QFont(
                self.dgv_perfil.font()
            )
            fuente_tabla.setFamily(
                self.familia_pixel_normal
            )
            fuente_tabla.setBold(False)
            self.dgv_perfil.setFont(fuente_tabla)

            fuente_encabezado = QtGui.QFont(
                self.dgv_perfil.horizontalHeader().font()
            )
            fuente_encabezado.setFamily(
                self.familia_pixel_bold
                or self.familia_pixel_normal
            )
            fuente_encabezado.setBold(True)

            self.dgv_perfil.horizontalHeader().setFont(
                fuente_encabezado
            )
            self.dgv_perfil.verticalHeader().setFont(
                fuente_encabezado
            )

        for nombre_barra in (
            "pb_python",
            "pb_java",
            "pb_mysql",
        ):
            barra = getattr(self, nombre_barra, None)

            if barra is not None:
                fuente_barra = QtGui.QFont(barra.font())
                fuente_barra.setFamily(
                    self.familia_pixel_bold
                    or self.familia_pixel_normal
                )
                fuente_barra.setBold(True)
                barra.setFont(fuente_barra)

        # Labels dinámicos y botón Volver con la variante Bold.
        for nombre_control in (
            "lbl_personaje",
            "lbl_usuario",
            "lbl_vidas",
            "btn_volver",
        ):
            control = getattr(self, nombre_control, None)

            if control is not None:
                self.aplicar_fuente_a_control(
                    control,
                    usar_bold=True,
                )

        print(
            "Fuente del perfil cargada:",
            self.familia_pixel_normal
        )

    # ======================================================
    # CONFIGURAR RESPONSIVIDAD
    # ======================================================

    def configurar_responsividad(self):
        # ======================================================
        # BOTÓN VOLVER
        # ======================================================

        self.botones_perfil = []

        if hasattr(self, "btn_volver"):
            self.botones_perfil.append(
                self.btn_volver
            )

        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=self.botones_perfil,
            ancho_base=self.ANCHO_BASE,
            alto_base=self.ALTO_BASE,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        # ======================================================
        # LABELS DEL DESIGNER
        # ======================================================

        self.labels_perfil = (
            self.obtener_labels_responsivos()
        )

        self.labels_responsivos = ElementosResponsivos(
            ventana=self.contenedor_principal,
            elementos=self.labels_perfil,
            ancho_base=self.ANCHO_BASE,
            alto_base=self.ALTO_BASE,
            escalar_fuentes=True,
        )

        # ======================================================
        # RESTO DE ELEMENTOS
        # ======================================================

        elementos = self.obtener_elementos_responsivos()

        self.elementos_responsivos = ElementosResponsivos(
            ventana=self.contenedor_principal,
            elementos=elementos,
            ancho_base=self.ANCHO_BASE,
            alto_base=self.ALTO_BASE,
            escalar_fuentes=True,
        )

        # ======================================================
        # HOVER
        # ======================================================

        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor=1.04,
                duracion=120,
                parent=self,
            )
            for boton in self.botones_perfil
        ]

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_interfaz_responsiva,
        )

    def obtener_elementos_responsivos(self):
        """
        Devuelve únicamente los controles creados por el archivo
        .ui. Se omiten los widgets internos de QTableWidget y el
        fondo para evitar deformaciones.
        """

        elementos = []
        excluidos = {
            self.contenedor_principal,
            self.fondo,
        }

        # La tabla se posiciona y escala de forma manual en
        # ajustar_tabla_responsiva(), para tener control exacto
        # sobre su ubicación, columnas, filas y fuente.
        if hasattr(self, "dgv_perfil"):
            excluidos.add(self.dgv_perfil)

        for boton in getattr(self, "botones_perfil", []):
            excluidos.add(boton)

        for elemento in self.contenedor_principal.findChildren(
                QtWidgets.QWidget
        ):
            if elemento in excluidos:
                continue

            # Los QLabel se ajustan mediante labels_responsivos.
            if isinstance(elemento, QtWidgets.QLabel):
                continue

            nombre = elemento.objectName() or ""

            if nombre.startswith("qt_"):
                continue

            if not nombre:
                continue

            elementos.append(elemento)

        return elementos

    def actualizar_hover_botones(self):
        for efecto in getattr(self, "efectos_hover", []):
            efecto.actualizar_geometria_base()

    def actualizar_interfaz_responsiva(self):
        if hasattr(self, "labels_responsivos"):
            self.labels_responsivos.ajustar()

        if hasattr(self, "elementos_responsivos"):
            self.elementos_responsivos.ajustar()

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        self.actualizar_imagen_personaje()
        self.ajustar_tabla_responsiva()
        self.subir_controles_sobre_fondo()
        self.actualizar_hover_botones()

    def ajustar_tabla_responsiva(self):
        """
        Ajusta la tabla exactamente al espacio disponible dentro
        del cuadro dibujado en el fondo del perfil.
        """

        if not hasattr(self, "dgv_perfil"):
            return

        escala_x = self.width() / self.ANCHO_BASE
        escala_y = self.height() / self.ALTO_BASE
        escala_fuente = min(escala_x, escala_y)

        # ======================================================
        # POSICIÓN EXACTA DENTRO DEL CUADRO
        # ======================================================
        # Valores calibrados para el fondo de 1920 x 1080.
        x_base = 242
        y_base = 620
        ancho_base = 1408
        alto_base = 325

        self.dgv_perfil.setGeometry(
            round(x_base * escala_x),
            round(y_base * escala_y),
            max(1, round(ancho_base * escala_x)),
            max(1, round(alto_base * escala_y)),
        )

        # Elimina el borde propio del QTableWidget.
        self.dgv_perfil.setFrameShape(
            QtWidgets.QFrame.Shape.NoFrame
        )

        self.dgv_perfil.setContentsMargins(0, 0, 0, 0)

        # Los encabezados ya están dibujados en el fondo.
        self.dgv_perfil.horizontalHeader().setVisible(False)
        self.dgv_perfil.verticalHeader().setVisible(False)

        self.dgv_perfil.setShowGrid(True)
        self.dgv_perfil.setWordWrap(False)
        self.dgv_perfil.setAlternatingRowColors(False)

        self.dgv_perfil.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.dgv_perfil.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.dgv_perfil.setTextElideMode(
            QtCore.Qt.TextElideMode.ElideRight
        )

        # Fondo transparente para conservar el diseño.
        self.dgv_perfil.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground,
            True
        )

        self.dgv_perfil.viewport().setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground,
            True
        )

        self.dgv_perfil.viewport().setAutoFillBackground(False)

        self.dgv_perfil.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                alternate-background-color: transparent;
                border: none;
                gridline-color: #6f604d;
                selection-background-color: rgba(243, 205, 169, 180);
                selection-color: #102b68;
            }

            QTableWidget::viewport {
                background-color: transparent;
                border: none;
            }

            QTableWidget::item {
                background-color: transparent;
                padding-left: 6px;
                padding-right: 6px;
                border: none;
                color: #102b68;
            }

            QTableWidget::item:selected {
                background-color: rgba(243, 205, 169, 180);
                color: #102b68;
            }

            /* Barra vertical completa */
            QScrollBar:vertical {
                background-color: transparent;
                width: 12px;
                margin: 0px;
                border: none;
            }

            /* Parte móvil azul */
            QScrollBar::handle:vertical {
                background-color: #102b68;
                min-height: 25px;
                border: none;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #173b86;
            }

            /* Fondo superior e inferior de la barra */
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background-color: transparent;
                border: none;
            }

            /* Quita los botones con flechas */
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background-color: transparent;
                border: none;
                height: 0px;
            }

            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                background: transparent;
                width: 0px;
                height: 0px;
            }

            /* Esquina que puede aparecer gris */
            QAbstractScrollArea::corner {
                background-color: transparent;
                border: none;
            }
        """)

        # ======================================================
        # MISMA FUENTE QUE LOS LABELS
        # ======================================================

        if hasattr(self, "lbl_usuario"):
            fuente_tabla = QtGui.QFont(
                self.lbl_usuario.font()
            )

        elif hasattr(self, "lbl_personaje"):
            fuente_tabla = QtGui.QFont(
                self.lbl_personaje.font()
            )

        else:
            fuente_tabla = QtGui.QFont(
                self.dgv_perfil.font()
            )

        # Tamaño independiente para que el texto siga cabiendo.
        tamano_fuente = max(
            9,
            round(14 * escala_fuente)
        )

        fuente_tabla.setPointSize(
            tamano_fuente
        )

        # Conserva el estilo de la fuente de los labels.
        fuente_tabla.setBold(
            self.lbl_usuario.font().bold()
            if hasattr(self, "lbl_usuario")
            else False
        )

        self.dgv_perfil.setFont(
            fuente_tabla
        )

        # ======================================================
        # ANCHO EXACTO DE LAS COLUMNAS
        # ======================================================

        encabezado_horizontal = (
            self.dgv_perfil.horizontalHeader()
        )

        encabezado_horizontal.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Fixed
        )

        ancho_util = self.dgv_perfil.viewport().width()

        if ancho_util <= 0:
            ancho_util = self.dgv_perfil.width()

        # FECHA, EVENTO, DETALLE, LENGUAJE.
        porcentajes = [
            0.135,  # FECHA
            0.210,  # EVENTO
            0.330,  # DETALLE
            0.180,  # LENGUAJE
        ]

        anchos_calculados = []

        for porcentaje in porcentajes:
            ancho_columna = round(
                ancho_util * porcentaje
            )

            anchos_calculados.append(
                ancho_columna
            )

        # La última columna utiliza exactamente el espacio restante.
        ancho_ultima_columna = max(
            1,
            ancho_util - sum(anchos_calculados)
        )

        anchos_calculados.append(
            ancho_ultima_columna
        )

        for columna, ancho_columna in enumerate(
                anchos_calculados
        ):
            self.dgv_perfil.setColumnWidth(
                columna,
                ancho_columna
            )

        # ======================================================
        # ALTURA DE LAS FILAS
        # ======================================================

        encabezado_vertical = (
            self.dgv_perfil.verticalHeader()
        )

        cantidad_filas = self.dgv_perfil.rowCount()

        # Cuando hay entre 6 y 10 registros, las filas ocupan todo
        # el alto disponible, evitando el espacio vacío inferior.
        if 6 <= cantidad_filas <= 10:
            encabezado_vertical.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeMode.Stretch
            )

        else:
            encabezado_vertical.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeMode.Fixed
            )

            alto_fila = max(
                25,
                round(34 * escala_y)
            )

            encabezado_vertical.setDefaultSectionSize(
                alto_fila
            )

            for fila in range(cantidad_filas):
                self.dgv_perfil.setRowHeight(
                    fila,
                    alto_fila
                )

        self.dgv_perfil.raise_()

    def mostrar_pantalla_completa(self):
        """
        Abre el perfil ocupando toda la pantalla. El control se
        realiza una sola vez para no interrumpir las transiciones.
        """

        if self._pantalla_completa_aplicada:
            return

        self._pantalla_completa_aplicada = True
        self.showFullScreen()


    # ======================================================
    # BUSCAR FONDO DEL PERFIL
    # ======================================================

    def buscar_fondo_perfil(self) -> Path:
        """
        Busca automáticamente el fondo del perfil dentro de
        assets/DISEÑOS.
        """

        carpetas = [
            PROYECTO_DIR / "assets" / "DISEÑOS",
            PROYECTO_DIR / "assets" / "Diseños",
            PROYECTO_DIR / "assets" / "diseños",
            PROYECTO_DIR / "assets" / "DISENOS",
            PROYECTO_DIR / "assets" / "disenos",
        ]

        nombres_posibles = [
            "Perfil.png",
            "Perfil-Jugador.png",
            "Perfil-Usuario.png",
            "PerfilJugador.png",
            "PerfilUsuario.png",
            "perfil.png",
        ]

        # Buscar primero por nombres exactos.
        for carpeta in carpetas:
            for nombre in nombres_posibles:
                ruta = carpeta / nombre

                if ruta.exists():
                    return ruta

        # Buscar cualquier PNG que contenga "perfil".
        for carpeta in carpetas:
            if not carpeta.exists():
                continue

            for ruta in carpeta.glob("*.png"):
                nombre_normalizado = (
                    self.normalizar_texto(
                        ruta.stem
                    )
                )

                if "perfil" in nombre_normalizado:
                    return ruta

        carpetas_texto = "\n".join(
            str(carpeta)
            for carpeta in carpetas
        )

        raise FileNotFoundError(
            "No se encontró la imagen de fondo del perfil.\n\n"
            "Se buscó en:\n"
            f"{carpetas_texto}\n\n"
            "Puedes agregar el nombre real del fondo dentro "
            "de la lista nombres_posibles."
        )

    # ======================================================
    # SUBIR CONTROLES
    # ======================================================

    def subir_controles_sobre_fondo(self):
        """
        Mantiene los controles del Designer encima
        del QLabel utilizado como fondo.
        """

        for objeto in self.contenedor_principal.children():
            if (
                isinstance(objeto, QtWidgets.QWidget)
                and objeto is not self.fondo
            ):
                objeto.raise_()

        self.fondo.lower()

    # ======================================================
    # CONFIGURACIÓN DEL FORMULARIO
    # ======================================================

    def configurar_formulario(self):
        # --------------------------------------------------
        # BOTÓN VOLVER
        # --------------------------------------------------

        if hasattr(self, "btn_volver"):
            self.btn_volver.clicked.connect(
                self.volver
            )

            self.btn_volver.setCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )

        # --------------------------------------------------
        # FOTO DEL PERSONAJE
        # --------------------------------------------------

        self.lbl_fotopersonaje.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.lbl_fotopersonaje.setScaledContents(
            False
        )

        # --------------------------------------------------
        # LABELS
        # --------------------------------------------------

        self.lbl_usuario.setText(
            ""
        )

        self.lbl_personaje.setText(
            ""
        )

        self.lbl_vidas.setText(
            "0"
        )

        # --------------------------------------------------
        # BARRAS DE PROGRESO
        # --------------------------------------------------

        barras = [
            self.pb_python,
            self.pb_java,
            self.pb_mysql,
        ]

        for barra in barras:
            barra.setRange(
                0,
                100
            )

            barra.setValue(
                0
            )

            barra.setFormat(
                "0%"
            )

            barra.setTextVisible(
                True
            )

        # --------------------------------------------------
        # TABLA
        # --------------------------------------------------

        self.dgv_perfil.setColumnCount(5)

        # Los títulos ya forman parte del fondo del diseño.
        # Se conservan internamente, pero no se muestran.
        self.dgv_perfil.setHorizontalHeaderLabels([
            "FECHA",
            "EVENTO",
            "DETALLE",
            "LENGUAJE",
            "ACCIÓN",
        ])

        self.dgv_perfil.horizontalHeader().setVisible(False)
        self.dgv_perfil.verticalHeader().setVisible(False)

        # Elimina las filas de ejemplo creadas en Qt Designer.
        self.dgv_perfil.clearContents()
        self.dgv_perfil.setRowCount(0)

        self.dgv_perfil.setEditTriggers(
            QtWidgets.QAbstractItemView
            .EditTrigger
            .NoEditTriggers
        )

        self.dgv_perfil.setSelectionBehavior(
            QtWidgets.QAbstractItemView
            .SelectionBehavior
            .SelectRows
        )

        self.dgv_perfil.setSelectionMode(
            QtWidgets.QAbstractItemView
            .SelectionMode
            .SingleSelection
        )

        self.dgv_perfil.setAlternatingRowColors(False)
        self.dgv_perfil.setWordWrap(False)

        self.dgv_perfil.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.dgv_perfil.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.ajustar_tabla_responsiva()

    # ======================================================
    # ACTUALIZACIÓN AUTOMÁTICA DE VIDAS Y PROGRESO
    # ======================================================

    def configurar_actualizacion_tiempo_real(self):
        """
        Consulta periódicamente las vidas y el progreso mientras
        el perfil permanece visible.

        De esta forma, si otro formulario completa una lección o
        modifica las vidas, el perfil refleja el cambio sin tener
        que cerrarse y abrirse otra vez.
        """

        self.timer_actualizar_perfil = QtCore.QTimer(self)
        self.timer_actualizar_perfil.setInterval(
            INTERVALO_ACTUALIZACION_PERFIL_MS
        )
        self.timer_actualizar_perfil.timeout.connect(
            self.actualizar_datos_en_tiempo_real
        )

    def actualizar_datos_en_tiempo_real(self):
        """Actualiza únicamente los datos que pueden cambiar."""

        if self._actualizacion_en_curso:
            return

        if not self.isVisible():
            return

        self._actualizacion_en_curso = True

        try:
            self.actualizar_vidas_perfil()
            self.actualizar_progreso_lenguajes()

        finally:
            self._actualizacion_en_curso = False

    # Se conserva este nombre por compatibilidad con cualquier
    # parte del proyecto que todavía lo llame directamente.
    def configurar_actualizacion_vidas(self):
        self.configurar_actualizacion_tiempo_real()

    def aplicar_recuperacion_vidas_si_corresponde(self) -> bool:
        """
        Recupera las cinco vidas cuando el jugador llegó a cero y
        ya transcurrió el tiempo configurado en la base de datos.

        Devuelve True cuando la consulta restauró las vidas.
        """

        conexion = None
        cursor = None

        try:
            conexion = self.obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute(
                f"""
                UPDATE jugador
                SET
                    vidas = %s,
                    fecha_recuperacion_vidas = NULL
                WHERE id_jugador = %s
                  AND vidas <= 0
                  AND fecha_recuperacion_vidas IS NOT NULL
                  AND DATE_ADD(
                        fecha_recuperacion_vidas,
                        INTERVAL {MINUTOS_RECUPERACION_VIDAS} MINUTE
                      ) <= NOW()
                """,
                (
                    MAX_VIDAS,
                    self.id_jugador,
                ),
            )

            vidas_restauradas = cursor.rowcount > 0
            conexion.commit()

            return vidas_restauradas

        except Exception as error:
            if conexion is not None:
                try:
                    conexion.rollback()
                except Exception:
                    pass

            print(
                "No se pudo comprobar la recuperación de vidas:",
                error
            )

            return False

        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

            if conexion is not None:
                try:
                    conexion.close()
                except Exception:
                    pass

    def actualizar_vidas_perfil(self):
        """
        Consulta las vidas actuales y actualiza lbl_vidas. Antes de
        leer el dato, comprueba si ya corresponde restaurarlas.
        """

        try:
            self.aplicar_recuperacion_vidas_si_corresponde()

            jugador = self.base_datos.obtener_datos_perfil(
                self.id_jugador
            )

            if jugador is None:
                return

            vidas = int(
                jugador.get("vidas") or 0
            )

            vidas = max(
                0,
                min(vidas, MAX_VIDAS)
            )

            texto_vidas = str(vidas)

            if self.lbl_vidas.text() != texto_vidas:
                self.lbl_vidas.setText(
                    texto_vidas
                )

        except Exception as error:
            print(
                "No se pudieron actualizar las vidas del perfil:",
                error
            )

    # ======================================================
    # CONEXIÓN
    # ======================================================

    def obtener_conexion(self):
        conexion_bd = ConexionBD()

        conexion = conexion_bd.conectar()

        if conexion is None:
            raise ConnectionError(
                "No se pudo conectar con la base de datos."
            )

        if hasattr(conexion, "is_connected"):
            if not conexion.is_connected():
                raise ConnectionError(
                    "La conexión con MySQL está cerrada."
                )

        return conexion

    # ======================================================
    # CARGAR TODO
    # ======================================================

    def cargar_toda_la_informacion(self):
        errores = []

        try:
            self.cargar_datos_jugador()

        except Exception as error:
            errores.append(
                "Datos del jugador:\n"
                f"{error}"
            )

        try:
            self.cargar_progreso_lenguajes()

        except Exception as error:
            errores.append(
                "Progreso de lenguajes:\n"
                f"{error}"
            )

        try:
            self.cargar_historial()

        except Exception as error:
            errores.append(
                "Historial:\n"
                f"{error}"
            )

        if errores:
            self.mostrar_error(
                "No se pudo cargar completamente el perfil:\n\n"
                + "\n\n".join(errores)
            )

    # ======================================================
    # MOSTRAR ERRORES
    # ======================================================

    def mostrar_error(self, mensaje: str):
        if Alertas is not None:
            try:
                Alertas.mostrar(
                    self,
                    "Error",
                    mensaje,
                    "error"
                )
                return

            except Exception:
                pass

        QtWidgets.QMessageBox.critical(
            self,
            "Error",
            mensaje
        )

    # ======================================================
    # COLUMNAS DE UNA TABLA
    # ======================================================

    def obtener_columnas_tabla(
        self,
        cursor,
        nombre_tabla: str
    ) -> set[str]:
        cursor.execute(
            f"SHOW COLUMNS FROM `{nombre_tabla}`"
        )

        resultados = cursor.fetchall()

        columnas = set()

        for registro in resultados:
            if isinstance(registro, dict):
                campo = (
                    registro.get("Field")
                    or registro.get("field")
                )
            else:
                campo = registro[0]

            if campo:
                columnas.add(
                    str(campo)
                )

        return columnas

    # ======================================================
    # ELEGIR PRIMERA COLUMNA EXISTENTE
    # ======================================================

    def primera_columna_existente(
        self,
        columnas: set[str],
        posibles: list[str]
    ):
        for columna in posibles:
            if columna in columnas:
                return columna

        return None

    # ======================================================
    # DATOS DEL JUGADOR
    # ======================================================

    def cargar_datos_jugador(self):
        # Antes de mostrar las vidas, comprueba si ya pasó el
        # tiempo necesario para recuperar las cinco.
        self.aplicar_recuperacion_vidas_si_corresponde()

        jugador = self.base_datos.obtener_datos_perfil(
            self.id_jugador
        )

        if jugador is None:
            raise ValueError(
                "No se encontró el jugador con id "
                f"{self.id_jugador}."
            )

        nombre = jugador.get("nombre") or "Sin nombre"
        personaje = jugador.get("personaje") or "pato"
        vidas = int(jugador.get("vidas") or 0)
        vidas = max(0, min(vidas, MAX_VIDAS))

        self.lbl_usuario.setText(
            str(nombre).upper()
        )

        self.lbl_personaje.setText(
            str(personaje)
            .replace("_", " ")
            .upper()
        )

        self.lbl_vidas.setText(
            str(vidas)
        )

        self.cargar_imagen_personaje(
            personaje
        )

    # ======================================================
    # NORMALIZAR TEXTO
    # ======================================================

    @staticmethod
    def normalizar_texto(texto: str) -> str:
        texto = str(texto).strip().lower()

        texto = unicodedata.normalize(
            "NFD",
            texto
        )

        texto = "".join(
            caracter
            for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )

        texto = texto.replace(
            " ",
            "_"
        )

        texto = texto.replace(
            "-",
            "_"
        )

        return texto

    # ======================================================
    # BUSCAR IMAGEN DEL PERSONAJE
    # ======================================================

    def buscar_imagen_personaje(
        self,
        personaje: str
    ):
        personaje_original = str(
            personaje
        ).strip()

        personaje_normalizado = (
            self.normalizar_texto(
                personaje_original
            )
        )

        # Si en la base de datos ya se guardó una ruta.
        posibles_rutas_directas = [
            Path(personaje_original),
            BASE_DIR / personaje_original,
            PROYECTO_DIR / personaje_original,
            PROYECTO_DIR / "assets" / personaje_original,
        ]

        for ruta in posibles_rutas_directas:
            if (
                ruta.exists()
                and ruta.is_file()
            ):
                return ruta

        carpetas_personajes = [
            PROYECTO_DIR / "assets" / "personajes",
            PROYECTO_DIR / "assets" / "PERSONAJES",
            PROYECTO_DIR / "assets" / "Personajes",

            PROYECTO_DIR
            / "juego"
            / "assets"
            / "personajes",

            BASE_DIR
            / "juego"
            / "assets"
            / "personajes",

            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "Personajes",
        ]

        mejores_resultados = []

        for carpeta in carpetas_personajes:
            if not carpeta.exists():
                continue

            try:
                imagenes = carpeta.rglob(
                    "*.png"
                )

                for ruta in imagenes:
                    nombre_archivo = (
                        self.normalizar_texto(
                            ruta.stem
                        )
                    )

                    nombre_carpeta = (
                        self.normalizar_texto(
                            ruta.parent.name
                        )
                    )

                    puntuacion = 0

                    if (
                        nombre_archivo
                        == personaje_normalizado
                    ):
                        puntuacion += 100

                    if (
                        nombre_carpeta
                        == personaje_normalizado
                    ):
                        puntuacion += 80

                    if nombre_archivo.startswith(
                        personaje_normalizado
                    ):
                        puntuacion += 60

                    if (
                        personaje_normalizado
                        in nombre_archivo
                    ):
                        puntuacion += 40

                    if (
                        personaje_normalizado
                        in nombre_carpeta
                    ):
                        puntuacion += 40

                    # Preferir la imagen quieta.
                    if "idle" in nombre_archivo:
                        puntuacion += 30

                    if "quieto" in nombre_archivo:
                        puntuacion += 30

                    if "caminar1" in nombre_archivo:
                        puntuacion += 10

                    if puntuacion > 0:
                        mejores_resultados.append(
                            (
                                puntuacion,
                                ruta
                            )
                        )

            except OSError:
                continue

        if not mejores_resultados:
            return None

        mejores_resultados.sort(
            key=lambda elemento: elemento[0],
            reverse=True
        )

        return mejores_resultados[0][1]

    # ======================================================
    # CARGAR FOTO DEL PERSONAJE
    # ======================================================

    def cargar_imagen_personaje(
        self,
        personaje: str
    ):
        ruta_imagen = self.buscar_imagen_personaje(
            personaje
        )

        if ruta_imagen is None:
            self.pixmap_personaje_original = None

            self.lbl_fotopersonaje.clear()

            self.lbl_fotopersonaje.setText(
                "Imagen\nno encontrada"
            )

            print(
                "No se encontró la imagen del personaje:",
                personaje
            )

            return

        pixmap = QtGui.QPixmap(
            str(ruta_imagen)
        )

        if pixmap.isNull():
            self.pixmap_personaje_original = None

            self.lbl_fotopersonaje.setText(
                "Error al cargar\nla imagen"
            )

            return

        self.pixmap_personaje_original = pixmap

        self.lbl_fotopersonaje.setToolTip(
            str(ruta_imagen)
        )

        self.actualizar_imagen_personaje()

    # ======================================================
    # ESCALAR FOTO DEL PERSONAJE
    # ======================================================

    def actualizar_imagen_personaje(self):
        if self.pixmap_personaje_original is None:
            return

        ancho = max(
            self.lbl_fotopersonaje.width() - 12,
            1
        )

        alto = max(
            self.lbl_fotopersonaje.height() - 12,
            1
        )

        pixmap_escalado = (
            self.pixmap_personaje_original.scaled(
                ancho,
                alto,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,

                # Conserva el estilo pixel art.
                QtCore.Qt.TransformationMode.FastTransformation
            )
        )

        self.lbl_fotopersonaje.setPixmap(
            pixmap_escalado
        )

    # ======================================================
    # OBTENER BARRA DE UN LENGUAJE
    # ======================================================

    def obtener_barra_lenguaje(
        self,
        lenguaje: str
    ):
        lenguaje = self.normalizar_texto(
            lenguaje
        )

        barras = {
            "python": self.pb_python,
            "java": self.pb_java,
            "mysql": self.pb_mysql,
        }

        return barras.get(
            lenguaje
        )

    # ======================================================
    # TOTAL DE LECCIONES POR LENGUAJE
    # ======================================================

    def obtener_totales_lecciones(
        self,
        cursor
    ) -> dict:
        try:
            columnas = self.obtener_columnas_tabla(
                cursor,
                "leccion"
            )

            if "id_lenguaje" not in columnas:
                return {}

            cursor.execute("""
                SELECT
                    id_lenguaje,
                    COUNT(*) AS total
                FROM leccion
                GROUP BY id_lenguaje
            """)

            resultados = cursor.fetchall()

            return {
                int(registro["id_lenguaje"]):
                int(registro["total"] or 0)

                for registro in resultados
            }

        except Exception:
            return {}

    # ======================================================
    # PROGRESO DE LENGUAJES
    # ======================================================

    def animar_barra_progreso(
        self,
        barra: QtWidgets.QProgressBar,
        porcentaje: int,
    ):
        """Cambia el porcentaje con una animación corta y fluida."""

        porcentaje = max(0, min(int(porcentaje), 100))
        valor_actual = barra.value()

        if valor_actual == porcentaje:
            barra.setFormat(f"{porcentaje}%")
            return

        animacion_anterior = self.animaciones_progreso.get(barra)

        if animacion_anterior is not None:
            animacion_anterior.stop()

        animacion = QtCore.QPropertyAnimation(
            barra,
            b"value",
            self,
        )
        animacion.setDuration(350)
        animacion.setStartValue(valor_actual)
        animacion.setEndValue(porcentaje)
        animacion.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        animacion.valueChanged.connect(
            lambda valor, b=barra: b.setFormat(
                f"{int(valor)}%"
            )
        )

        animacion.finished.connect(
            lambda b=barra, p=porcentaje: b.setFormat(
                f"{p}%"
            )
        )

        self.animaciones_progreso[barra] = animacion
        animacion.start()

    def actualizar_progreso_lenguajes(self):
        """
        Vuelve a consultar el progreso sin reiniciar visualmente
        las barras, evitando que parpadeen cada pocos segundos.
        """

        try:
            self.cargar_progreso_lenguajes(animar=True)

        except Exception as error:
            print(
                "No se pudo actualizar el progreso del perfil:",
                error
            )

    def cargar_progreso_lenguajes(self, animar: bool = False):
        barras = {
            "python": self.pb_python,
            "java": self.pb_java,
            "mysql": self.pb_mysql,
        }

        for barra in barras.values():
            barra.setRange(0, 100)
            barra.setTextVisible(True)

        registros = (
            self.base_datos
            .obtener_progreso_perfil(
                self.id_jugador
            )
        )

        # Empieza en cero para que un lenguaje sin registro se
        # muestre correctamente, pero sin reiniciar la interfaz
        # antes de terminar la consulta.
        datos_progreso = {
            lenguaje: {
                "porcentaje": 0,
                "lecciones_completadas": 0,
            }
            for lenguaje in barras
        }

        for registro in registros:
            lenguaje = self.normalizar_texto(
                registro.get("lenguaje") or ""
            )

            if lenguaje not in barras:
                continue

            porcentaje = float(
                registro.get("porcentaje_avance")
                or 0
            )

            prueba_completada = bool(
                registro.get("prueba_completada")
                or False
            )

            if prueba_completada:
                porcentaje = 100

            porcentaje = max(
                0,
                min(round(porcentaje), 100)
            )

            lecciones_completadas = int(
                registro.get("lecciones_completadas")
                or 0
            )

            datos_progreso[lenguaje] = {
                "porcentaje": porcentaje,
                "lecciones_completadas": lecciones_completadas,
            }

        for lenguaje, barra in barras.items():
            datos = datos_progreso[lenguaje]
            porcentaje = datos["porcentaje"]
            lecciones_completadas = datos["lecciones_completadas"]

            if animar:
                self.animar_barra_progreso(
                    barra,
                    porcentaje,
                )
            else:
                barra.setValue(porcentaje)
                barra.setFormat(f"{porcentaje}%")

            barra.setToolTip(
                "Lecciones completadas: "
                f"{lecciones_completadas}"
            )

    # ======================================================
    # CARGAR HISTORIAL
    # ======================================================

    def cargar_historial(self):
        registros = (
            self.base_datos
            .obtener_historial_perfil(
                self.id_jugador
            )
        )

        self.dgv_perfil.setSortingEnabled(
            False
        )

        self.dgv_perfil.clearContents()

        self.dgv_perfil.setRowCount(
            len(registros)
        )

        for fila, registro in enumerate(registros):
            fecha = registro.get("fecha")

            if hasattr(fecha, "strftime"):
                fecha = fecha.strftime(
                    "%d/%m/%Y %H:%M"
                )

            valores = [
                fecha or "",
                registro.get("evento") or "",
                registro.get("detalle") or "",
                registro.get("lenguaje") or "",
                registro.get("accion") or "",
            ]

            for columna, valor in enumerate(valores):
                item = QtWidgets.QTableWidgetItem(
                    str(valor)
                )

                if columna in (0, 3, 4):
                    item.setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignCenter
                    )

                else:
                    item.setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignVCenter
                        | QtCore.Qt.AlignmentFlag.AlignLeft
                    )

                self.dgv_perfil.setItem(
                    fila,
                    columna,
                    item
                )

        # Mantiene una altura uniforme y una fuente legible.
        QtCore.QTimer.singleShot(
            0,
            self.ajustar_tabla_responsiva
        )

        self.dgv_perfil.setSortingEnabled(
            True
        )

    # ======================================================
    # VOLVER
    # ======================================================

    def volver(self):
        if self.formulario_anterior is None:
            self.close()
            return

        if FormTransicion is not None:
            try:
                self.transicion_volver = (
                    FormTransicion(
                        self,
                        self.formulario_anterior
                    )
                )

                return

            except Exception as error:
                print(
                    "No se pudo utilizar la transición:",
                    error
                )

        self.formulario_anterior.show()
        self.formulario_anterior.raise_()
        self.formulario_anterior.activateWindow()

        self.close()

    # ======================================================
    # REDIMENSIONAR
    # ======================================================

    def resizeEvent(self, evento):
        if (
                hasattr(self, "Perfil")
                and self.Perfil is not self
        ):
            self.Perfil.setGeometry(
                0,
                0,
                self.width(),
                self.height(),
            )

        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano()
            self.fondo.lower()

        if hasattr(self, "labels_responsivos"):
            self.labels_responsivos.ajustar()

        if hasattr(self, "elementos_responsivos"):
            self.elementos_responsivos.ajustar()

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        self.actualizar_imagen_personaje()
        self.ajustar_tabla_responsiva()
        self.subir_controles_sobre_fondo()

        if hasattr(self, "efectos_hover"):
            QtCore.QTimer.singleShot(
                0,
                self.actualizar_hover_botones,
            )

        super().resizeEvent(evento)

    # ======================================================
    # MOSTRAR VENTANA
    # ======================================================

    def showEvent(self, evento):
        super().showEvent(evento)

        # Al entrar al perfil, consulta inmediatamente las vidas
        # y el progreso por si cambiaron en otro formulario.
        QtCore.QTimer.singleShot(
            0,
            self.actualizar_datos_en_tiempo_real,
        )

        if hasattr(self, "timer_actualizar_perfil"):
            self.timer_actualizar_perfil.start()

        QtCore.QTimer.singleShot(
            0,
            self.mostrar_pantalla_completa,
        )

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_vista,
        )

        QtCore.QTimer.singleShot(
            100,
            self.actualizar_vista,
        )

    def hideEvent(self, evento):
        if hasattr(self, "timer_actualizar_perfil"):
            self.timer_actualizar_perfil.stop()

        super().hideEvent(evento)

    def closeEvent(self, evento):
        if hasattr(self, "timer_actualizar_perfil"):
            self.timer_actualizar_perfil.stop()

        for animacion in getattr(
            self,
            "animaciones_progreso",
            {}
        ).values():
            animacion.stop()

        super().closeEvent(evento)

    def actualizar_vista(self):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano()

        self.actualizar_interfaz_responsiva()