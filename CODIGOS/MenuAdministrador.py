from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui
from Alertas import Alertas
from quitar_barra import quitar
from Transicion import FormTransicion


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


class MenuAdministrador(QtWidgets.QWidget):
    def __init__(self, admin=None):
        super().__init__()
        quitar(self)
        self.admin = admin

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Menu-Administrador.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Menu-Administrador.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        uic.loadUi(str(ruta_ui), self)

        self.resize(1920, 1080)

        self.fondo = FondoImagen(self, ruta_imagen)

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

        if hasattr(self, "btnJugar"):
            self.btnJugar.clicked.connect(self.abrir_lecciones)

        if hasattr(self, "btnCerrarSesion"):
            self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)

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
                ventana_lecciones = Lecciones(self.admin)
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
            texto_confirmar="SÍ, ELIMINAR",
            texto_cancelar="CANCELAR"
        )

        if not respuesta:
            return

        try:
            from Login import LoginWindow

            app = QtWidgets.QApplication.instance()

            # Limpia el historial para que no regrese por accidente a Registro u otro form
            if hasattr(app, "historial_forms"):
                app.historial_forms.clear()

            self.ventana_login = LoginWindow()

            app.ventana_login = self.ventana_login

            # Login en tamaño normal, sin transición y sin pantalla completa
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

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        super().resizeEvent(event)