import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui

from MenuUsuario import MenuUsuario
from ConexionBD import ConexionBD
from Registro import RegistroWindow


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

            uic.loadUi(str(ruta_ui), self)

            self.resize(1020, 720)

            self.fondo = FondoImagen(self, ruta_imagen)

            self.db = ConexionBD()

            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

            self.btnMostrarContrasena.setCheckable(True)
            self.btnMostrarContrasena.clicked.connect(self.mostrar_ocultar_contrasena)

            self.btn_Iniciar.clicked.connect(self.iniciar_sesion)

            self.btn_Registrarse.clicked.connect(self.abrir_registro)

            self.txtContrasena.returnPressed.connect(self.iniciar_sesion)

            if hasattr(self, "txtUsuario"):
                self.txtUsuario.returnPressed.connect(self.iniciar_sesion)

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

    def iniciar_sesion(self):
        usuario = self.txtUsuario.text().strip()
        contrasena = self.txtContrasena.text().strip()

        if usuario == "" or contrasena == "":
            QtWidgets.QMessageBox.warning(
                self,
                "Campos vacíos",
                "Debes ingresar tu usuario/correo y contraseña."
            )
            return

        try:
            jugador = self.db.validar_jugador(usuario, contrasena)

            if jugador:
                self.db.registrar_historial(
                    jugador["id_jugador"],
                    "Inicio de sesión",
                    f"El jugador {jugador['nombre']} inició sesión correctamente."
                )

                QtWidgets.QMessageBox.information(
                    self,
                    "Bienvenido",
                    f"Inicio de sesión correcto.\n\nBienvenido, {jugador['nombre']}."
                )

                self.abrir_menu_usuario(jugador)

            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Usuario no encontrado",
                    "El usuario o la contraseña son incorrectos.\n\n"
                    "Si no tienes una cuenta, debes registrarte antes de iniciar sesión."
                )

                self.txtContrasena.clear()
                self.txtContrasena.setFocus()

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error de base de datos",
                str(e)
            )

    def abrir_menu_usuario(self, jugador):
        try:
            self.menu_usuario = MenuUsuario(jugador)
        except TypeError:
            self.menu_usuario = MenuUsuario()

        self.menu_usuario.showMaximized()
        self.close()

    def abrir_registro(self):
        self.registro = RegistroWindow()
        self.registro.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.show()
    sys.exit(app.exec())