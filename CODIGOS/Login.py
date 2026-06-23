import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui

from MenuUsuario import MenuUsuario


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


class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Login.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "LoginNuevo.png"

        try:
            if not ruta_ui.exists():
                raise FileNotFoundError(f"No se encontró Login.ui en:\n{ruta_ui}")

            if not ruta_imagen.exists():
                raise FileNotFoundError(f"No se encontró la imagen del login en:\n{ruta_imagen}")

            # Cargar diseño del login
            uic.loadUi(str(ruta_ui), self)

            self.resize(1020, 720)

            # Fondo del login
            self.fondo = FondoImagen(self, ruta_imagen)

            # Mostrar / ocultar contraseña
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.btnMostrarContrasena.setCheckable(True)
            self.btnMostrarContrasena.clicked.connect(self.mostrar_ocultar_contrasena)

            # Botón para abrir el menú de usuario
            self.btn_Iniciar.clicked.connect(self.abrir_menu_usuario)

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error de Sistema",
                f"No se pudo cargar la interfaz o el fondo.\n\nDetalles:\n{str(e)}"
            )
            sys.exit(1)

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())

        super().resizeEvent(event)

    def mostrar_ocultar_contrasena(self, checked):
        if checked:
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def abrir_menu_usuario(self):
        self.menu_usuario = MenuUsuario()
        self.menu_usuario.showMaximized()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.show()
    sys.exit(app.exec())