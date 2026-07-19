from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui, QtCore
from Alertas import Alertas
from quitar_barra import quitar
from Transicion import FormTransicion
from AjusteResponsive import BotonesResponsivos
from LogoReutilizable import LogoReutilizable
from Ajustes import Ajustes


class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.ruta_imagen = ruta_imagen
        self.pixmap_original = QtGui.QPixmap(
            str(self.ruta_imagen)
        )

        self.setScaledContents(True)
        self.setGeometry(
            0,
            0,
            ventana.width(),
            ventana.height()
        )
        self.setPixmap(self.pixmap_original)

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class EfectoHoverBoton(QtCore.QObject):
    """
    Agranda ligeramente un botón y aumenta su sombra
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

        # Se actualizará después de que BotonesResponsivos
        # coloque el botón en su posición correcta.
        self.geometria_normal = QtCore.QRect(
            boton.geometry()
        )

        # Animación para agrandar o restaurar el botón.
        self.animacion_geometria = QtCore.QPropertyAnimation(
            boton,
            b"geometry",
            self
        )
        self.animacion_geometria.setDuration(
            self.duracion
        )
        self.animacion_geometria.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        # Sombra del botón.
        self.sombra = QtWidgets.QGraphicsDropShadowEffect(
            boton
        )
        self.sombra.setColor(
            QtGui.QColor(0, 0, 0, 180)
        )
        self.sombra.setBlurRadius(10)
        self.sombra.setOffset(0, 3)

        boton.setGraphicsEffect(self.sombra)

        # Animación de la sombra.
        self.animacion_sombra = QtCore.QPropertyAnimation(
            self.sombra,
            b"blurRadius",
            self
        )
        self.animacion_sombra.setDuration(
            self.duracion
        )
        self.animacion_sombra.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        boton.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )

        boton.installEventFilter(self)

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
            rectangulo.x() - diferencia_ancho // 2,
            rectangulo.y() - diferencia_alto // 2,
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
        Se ejecuta después de redimensionar la ventana para
        conservar la nueva posición responsiva del botón.
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

                # Guarda la posición actual establecida
                # por BotonesResponsivos.
                self.geometria_normal = QtCore.QRect(
                    self.boton.geometry()
                )

                # Evita que el botón agrandado quede detrás
                # de los demás.
                self.boton.raise_()

                self.animar_geometria(
                    self.obtener_geometria_grande()
                )
                self.animar_sombra(28)

            elif evento.type() == QtCore.QEvent.Type.Leave:
                self.cursor_encima = False

                self.animar_geometria(
                    self.geometria_normal
                )
                self.animar_sombra(10)

        return super().eventFilter(
            objeto,
            evento
        )


class MenuAdministrador(QtWidgets.QWidget):
    def __init__(self, admin=None):
        super().__init__()
        quitar(self)
        self.admin = admin

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = (
                PROYECTO_DIR
                / "EXPO-DISEÑOS"
                / "DESIGNER"
                / "Menu-Administrador.ui"
        )

        ruta_imagen = (
                PROYECTO_DIR
                / "assets"
                / "DISEÑOS"
                / "Menu-Administrador.png"
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
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        if not ruta_botones.exists():
            raise FileNotFoundError(
                f"No se encontró la carpeta de botones:\n{ruta_botones}"
            )

        if not ruta_logo.exists():
            raise FileNotFoundError(
                f"No se encontró el logo:\n{ruta_logo}"
            )

        uic.loadUi(str(ruta_ui), self)

        # Conserva las referencias para evitar que las ventanas
        # sean eliminadas por Python.
        self.form_ajustes = None
        self.transicion_ajustes = None

        self.btnAjustes.clicked.connect(
            self.abrir_ajustes
        )

        # Conserva los StyleSheet de Designer y corrige sus rutas.
        self.corregir_rutas_stylesheet(ruta_botones)

        # Resolución original del diseño.
        self.resize(1920, 1080)

        # Permite cambiar libremente el tamaño de la ventana.
        self.setMinimumSize(0, 0)
        self.setMaximumSize(
            16777215,
            16777215
        )

        # Fondo adaptable.
        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        self.logo_reutilizable = LogoReutilizable(
            self,
            ruta_logo
        )

        self.lbl_logo.raise_()

        # Hace responsivos todos los botones del menú.
        # Lista reutilizable de botones del menú.
        self.botones_menu = [
            self.btnAjustes,
            self.btnCerrarSesion,
            self.btnGestionUsuarios,
            self.btnJugar,
            self.btnPerfil,
        ]

        # Hace responsivos todos los botones del menú.
        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=self.botones_menu,
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        # Efecto al pasar el cursor sobre los botones.
        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor=1.035,
                duracion=120,
                parent=self
            )
            for boton in self.botones_menu
        ]

        # Espera a que Qt termine de colocar los botones
        # antes de guardar sus posiciones iniciales.
        QtCore.QTimer.singleShot(
            0,
            self.actualizar_hover_botones
        )

        self.conectar_eventos()

    def conectar_eventos(self):
        if hasattr(self, "btnGestionUsuarios"):
            self.btnGestionUsuarios.clicked.connect(self.abrir_gestionar_usuarios)
        else:
            Alertas.mostrar(
                self,
                "Botón no encontrado",
                "No existe un botón llamado btnGestionUsuarios en el archivo .ui.",
                "error"
            )

        self.btnJugar.clicked.connect(
            self.abrir_lecciones
        )

        self.btnCerrarSesion.clicked.connect(
            self.cerrar_sesion
        )

        # Cuando tengas las ventanas de ajustes y perfil,
        # puedes conectar aquí sus eventos.
        #
        # self.btnAjustes.clicked.connect(self.abrir_ajustes)
        # self.btnPerfil.clicked.connect(self.abrir_perfil)

    def abrir_gestionar_usuarios(self):
        try:
            from GestionUsuario import GestionUsuario

            FormTransicion(
                self,
                GestionUsuario
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir Gestión de Usuarios.\n\nDetalles:\n{e}",
                "error"
            )

    def abrir_lecciones(self):
        try:
            from Lecciones import Lecciones

            try:
                ventana_lecciones = Lecciones(
                    self.admin
                )
            except TypeError:
                ventana_lecciones = Lecciones()

            FormTransicion(
                self,
                ventana_lecciones
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir Lecciones.\n\nDetalles:\n{e}",
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

            app = QtWidgets.QApplication.instance()

            # Limpia el historial para evitar que el usuario
            # pueda regresar al menú después de cerrar sesión.
            if hasattr(app, "historial_forms"):
                app.historial_forms.clear()

            self.ventana_login = LoginWindow()
            app.ventana_login = self.ventana_login

            # El Login se abre en tamaño normal.
            self.ventana_login.resize(1020, 720)
            self.ventana_login.showNormal()

            self.close()

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error al cerrar sesión",
                f"No se pudo abrir el Login:\n{e}",
                "error"
            )

    def actualizar_hover_botones(self):
        """
        Actualiza las posiciones originales utilizadas
        por las animaciones hover.
        """

        for efecto in getattr(
            self,
            "efectos_hover",
            []
        ):
            efecto.actualizar_geometria_base()

    def resizeEvent(self, event):
        # Ajusta el fondo a la ventana.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )
            self.fondo.lower()

        # El QFrame contiene todos los botones y también
        # debe ocupar toda la ventana.
        if hasattr(self, "MenuAdministrador"):
            self.MenuAdministrador.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )
            self.MenuAdministrador.raise_()

        # Mantiene el logo encima del fondo y del QFrame.
        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        if hasattr(self, "logo_reutilizable"):
            self.logo_reutilizable.actualizar()

        # Actualiza los botones después de cambiar
        # el tamaño del QFrame.
        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        if hasattr(self, "efectos_hover"):
            QtCore.QTimer.singleShot(
                0,
                self.actualizar_hover_botones
            )

        super().resizeEvent(event)

    def corregir_rutas_stylesheet(self, ruta_botones):
        """
        Conserva los StyleSheet creados en Qt Designer,
        pero transforma ../Botones/ en una ruta absoluta.
        """

        ruta_absoluta = ruta_botones.resolve().as_posix()

        botones = [
            self.btnAjustes,
            self.btnCerrarSesion,
            self.btnGestionUsuarios,
            self.btnJugar,
            self.btnPerfil,
        ]

        for boton in botones:
            estilo = boton.styleSheet()

            if not estilo:
                continue

            estilo_corregido = estilo.replace(
                'url("../Botones/',
                f'url("{ruta_absoluta}/'
            )

            boton.setStyleSheet(estilo_corregido)

    def abrir_ajustes(self):
        """
        Abre el formulario de Ajustes desde el menú administrador.
        """

        # Si la ventana ya está abierta, solamente la coloca al frente.
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
                jugador=getattr(self, "jugador", None),
                desde_juego=False,
            )

            # Permite liberar correctamente la ventana al cerrarla.
            self.form_ajustes.setAttribute(
                QtCore.Qt.WidgetAttribute.WA_DeleteOnClose,
                True,
            )

            self.form_ajustes.destroyed.connect(
                self._limpiar_form_ajustes
            )

            # Se guarda la transición para evitar que Python
            # la elimine antes de terminar.
            self.transicion_ajustes = FormTransicion(
                self,
                self.form_ajustes,
            )

        except Exception as error:
            print(
                "[MENU ADMIN] No se pudo abrir Ajustes:",
                error,
            )

            # Apertura normal si la transición falla.
            if self.form_ajustes is not None:
                self.hide()
                self.form_ajustes.showMaximized()
                self.form_ajustes.raise_()
                self.form_ajustes.activateWindow()

    def _limpiar_form_ajustes(self):
        """
        Limpia la referencia para poder abrir Ajustes nuevamente.
        """

        self.form_ajustes = None
        self.transicion_ajustes = None