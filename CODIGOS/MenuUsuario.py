from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui
from Alertas import Alertas

class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.ruta_imagen = ruta_imagen
        self.pixmap_original = QtGui.QPixmap(str(self.ruta_imagen))

        self.setScaledContents(True)
        self.setGeometry(0, 0, ventana.width(), ventana.height())
        self.setPixmap(self.pixmap_original)

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(0, 0, ancho, alto)


class MenuUsuario(QtWidgets.QWidget):
    def __init__(self, jugador=None):
        super().__init__()

        self.jugador = jugador

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Menu-Jugador.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Menu-Usuario.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        uic.loadUi(str(ruta_ui), self)

        self.resize(1920, 1080)

        self.fondo = FondoImagen(self, ruta_imagen)

        self.conectar_eventos()

    def conectar_eventos(self):
        if hasattr(self, "btnJugar"):
            self.btnJugar.clicked.connect(self.abrir_lecciones)

        if hasattr(self, "btnCerrarSesion"):
            self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)

        if hasattr(self, "btn_CerrarSesion"):
            self.btn_CerrarSesion.clicked.connect(self.cerrar_sesion)

        if hasattr(self, "btn_cerrarsesion"):
            self.btn_cerrarsesion.clicked.connect(self.cerrar_sesion)

    def abrir_lecciones(self):
        try:
            from Lecciones import Lecciones

            try:
                self.ventana_lecciones = Lecciones(self.jugador)
            except TypeError:
                self.ventana_lecciones = Lecciones()

            self.ventana_lecciones.showMaximized()
            self.close()

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
            texto_confirmar="SÍ, ELIMINAR",
            texto_cancelar="CANCELAR"
        )

        if not respuesta:
            return

        try:
            from Login import LoginWindow

            self.ventana_login = LoginWindow()
            self.ventana_login.show()
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
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        super().resizeEvent(event)