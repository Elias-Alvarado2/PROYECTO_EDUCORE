from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui, QtCore

from Alertas import Alertas
from AjusteResponsive import BotonesResponsivos
from Transicion import FormTransicion
from quitar_barra import quitar


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


class MenuUsuario(QtWidgets.QWidget):
    def __init__(self, jugador=None):
        super().__init__()

        quitar(self)

        self.jugador = jugador

        self.ventana_lecciones = None
        self.ventana_login = None

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
                "No se encontró la carpeta de botones:"
                f"\n{ruta_botones}"
            )

        uic.loadUi(
            str(ruta_ui),
            self
        )

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

        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=[
                self.btnAjustes,
                self.btnCerrarSesion,
                self.btnJugar,
                self.btnPerfil,
            ],
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.configurar_botones()
        self.conectar_eventos()

    def corregir_rutas_stylesheet(self, ruta_botones):
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
            estilo_original = control.styleSheet()

            if not estilo_original:
                continue

            estilo_corregido = estilo_original

            estilo_corregido = estilo_corregido.replace(
                'url("../Botones/',
                f'url("{ruta_absoluta}/'
            )

            estilo_corregido = estilo_corregido.replace(
                "url('../Botones/",
                f"url('{ruta_absoluta}/"
            )

            estilo_corregido = estilo_corregido.replace(
                "url(../Botones/",
                f"url({ruta_absoluta}/"
            )

            if estilo_corregido != estilo_original:
                control.setStyleSheet(
                    estilo_corregido
                )

    def configurar_botones(self):
        botones = [
            self.btnAjustes,
            self.btnCerrarSesion,
            self.btnJugar,
            self.btnPerfil,
        ]

        for boton in botones:
            boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.PointingHandCursor
                )
            )

    def conectar_eventos(self):
        self.btnJugar.clicked.connect(
            self.abrir_lecciones
        )

        self.btnCerrarSesion.clicked.connect(
            self.cerrar_sesion
        )

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
                        self.ventana_lecciones = Lecciones(
                            self.jugador
                        )

                    except TypeError:
                        self.ventana_lecciones = Lecciones()

            FormTransicion(
                self,
                self.ventana_lecciones
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error al abrir lecciones",
                f"No se pudo abrir la ventana de lecciones.\n\nDetalles:\n{e}",
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

            if hasattr(app, "historial_forms"):
                app.historial_forms.clear()

            self.ventana_login = LoginWindow()

            app.ventana_login = self.ventana_login

            self.ventana_login.resize(
                1020,
                720
            )

            self.ventana_login.showNormal()
            self.close()

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error al cerrar sesión",
                f"No se pudo abrir el Login:\n{e}",
                "error"
            )

    def resizeEvent(self, event):
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

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        super().resizeEvent(event)