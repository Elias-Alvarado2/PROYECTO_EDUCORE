from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui, QtCore

from Alertas import Alertas
from AjusteResponsive import BotonesResponsivos
from Transicion import FormTransicion
from quitar_barra import quitar
from LogoReutilizable import LogoReutilizable
from Ajustes import Ajustes


# ==========================================================
# FONDO RESPONSIVO
# ==========================================================

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


# ==========================================================
# EFECTO HOVER PARA LOS BOTONES
# ==========================================================

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

        # Animación para agrandar/reducir el botón.
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

        # Animación de la sombra.
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


# ==========================================================
# MENÚ PRINCIPAL DEL JUGADOR
# ==========================================================

class MenuUsuario(QtWidgets.QWidget):
    def __init__(self, jugador=None):
        super().__init__()

        quitar(self)

        self.jugador = jugador

        # Ventanas y transiciones.
        self.ventana_lecciones = None
        self.ventana_login = None

        self.form_ajustes = None
        self.transicion_ajustes = None

        self.transicion_personajes = None

        # --------------------------------------------------
        # RUTAS
        # --------------------------------------------------

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

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

        # --------------------------------------------------
        # COMPROBAR RUTAS
        # --------------------------------------------------

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

        # --------------------------------------------------
        # CARGAR FORMULARIO
        # --------------------------------------------------

        uic.loadUi(
            str(ruta_ui),
            self
        )

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

        # --------------------------------------------------
        # FONDO
        # --------------------------------------------------

        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        # --------------------------------------------------
        # LOGO
        # --------------------------------------------------

        self.logo_reutilizable = (
            LogoReutilizable(
                self,
                ruta_logo
            )
        )

        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        # --------------------------------------------------
        # BOTONES RESPONSIVOS
        # --------------------------------------------------

        self.botones_menu = [
            self.btnJugar,
            self.btnAjustes,
            self.btnPerfil,
            self.btnCerrarSesion,

            # Botón para abrir Personajes.py.
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

        # --------------------------------------------------
        # EFECTOS HOVER
        # --------------------------------------------------

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

        # --------------------------------------------------
        # EVENTOS
        # --------------------------------------------------

        self.conectar_eventos()

    # ======================================================
    # CORREGIR RUTAS DEL STYLESHEET
    # ======================================================

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

    # ======================================================
    # CONFIGURAR BOTONES
    # ======================================================

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

    # ======================================================
    # CONECTAR BOTONES
    # ======================================================

    def conectar_eventos(self):
        self.btnJugar.clicked.connect(
            self.abrir_lecciones
        )

        self.btnAjustes.clicked.connect(
            self.abrir_ajustes
        )

        self.btnCerrarSesion.clicked.connect(
            self.cerrar_sesion
        )

        self.btn_personaje.clicked.connect(
            self.abrir_personajes
        )

    # ======================================================
    # ABRIR PERSONAJES
    # ======================================================

    def abrir_personajes(self):
        """
        Abre Personajes.py conservando los datos
        del jugador que inició sesión.
        """

        try:
            # Importación local para evitar
            # importaciones circulares.
            from Personajes import Personajes

            # La clase Personajes recuperará este jugador
            # cuando FormTransicion cree la ventana.
            Personajes.jugador_pendiente = (
                self.jugador
            )

            # FormTransicion recibe la clase Personajes.
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

    # ======================================================
    # ABRIR AJUSTES
    # ======================================================

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

            # Libera la ventana cuando se cierre.
            self.form_ajustes.setAttribute(
                QtCore.Qt.WidgetAttribute
                .WA_DeleteOnClose,
                True
            )

            self.form_ajustes.destroyed.connect(
                self._limpiar_form_ajustes
            )

            # Guardar la transición evita que Python
            # la elimine antes de terminar.
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

    # ======================================================
    # ABRIR LECCIONES
    # ======================================================

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

            # Guardamos la transición dentro de la
            # instancia para evitar que se elimine.
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

    # ======================================================
    # CERRAR SESIÓN
    # ======================================================

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

    # ======================================================
    # REDIMENSIONAR VENTANA
    # ======================================================

    def resizeEvent(self, event):
        # Ajustar el fondo.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        # Ajustar el frame principal.
        if hasattr(self, "MenuJugador"):
            self.MenuJugador.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )

            self.MenuJugador.raise_()

        # Asegurar que el botón de personajes
        # permanezca visible.
        if hasattr(self, "btn_personaje"):
            self.btn_personaje.show()
            self.btn_personaje.raise_()

        # Mantener el logo sobre el fondo.
        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        if hasattr(
            self,
            "logo_reutilizable"
        ):
            self.logo_reutilizable.actualizar()

        # Escalar botones.
        if hasattr(
            self,
            "botones_responsivos"
        ):
            self.botones_responsivos.ajustar()

        # Actualizar la geometría usada por
        # las animaciones hover.
        if hasattr(self, "efectos_hover"):
            QtCore.QTimer.singleShot(
                0,
                self.actualizar_hover_botones
            )

        super().resizeEvent(event)