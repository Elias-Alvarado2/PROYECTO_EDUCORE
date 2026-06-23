import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic


class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Carpeta donde está este archivo Login.py
        BASE_DIR = Path(__file__).resolve().parent

        # Carpeta principal del proyecto: PROYECTO_EDUCORE
        PROYECTO_DIR = BASE_DIR.parent

        # RUTA CORRECTA DEL ARCHIVO .ui
        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Login.ui"

        # RUTA CORRECTA DE LA IMAGEN DE FONDO
        nombre_imagen = "LoginNuevo.png"
        ruta_imagen = PROYECTO_DIR / "assets" / "diseños" / nombre_imagen

        # Mostrar rutas en consola para comprobar
        print("Buscando UI en:", ruta_ui)
        print("Buscando imagen en:", ruta_imagen)

        try:
            # Verificar que exista el archivo Login.ui
            if not ruta_ui.exists():
                raise FileNotFoundError(f"No se encontró el archivo Login.ui en:\n{ruta_ui}")

            # Verificar que exista la imagen
            if not ruta_imagen.exists():
                raise FileNotFoundError(f"No se encontró la imagen de fondo en:\n{ruta_imagen}")

            # Cargar interfaz hecha en Qt Designer
            uic.loadUi(str(ruta_ui), self)

            # Tamaño de la ventana
            self.resize(1020, 720)

            # Aplicar fondo
            ruta_css = ruta_imagen.as_posix()

            self.setStyleSheet(f"""
                QDialog {{
                    border-image: url("{ruta_css}") 0 0 0 0 stretch stretch;
                }}
            """)

            # Verificar que existan los objetos del Designer
            if not hasattr(self, "txtContrasena"):
                raise AttributeError("No existe un QLineEdit llamado txtContrasena en Login.ui")

            if not hasattr(self, "btnMostrarContrasena"):
                raise AttributeError("No existe un botón llamado btnMostrarContrasena en Login.ui")

            # La contraseña empieza oculta
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

            # El botón funciona como interruptor
            self.btnMostrarContrasena.setCheckable(True)

            # Conectar botón para mostrar/ocultar contraseña
            self.btnMostrarContrasena.clicked.connect(self.mostrar_ocultar_contrasena)

            # Aquí puedes conectar tu botón de iniciar sesión
            # self.btnIngresar.clicked.connect(self.funcion_login)

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error de Sistema",
                f"No se pudo cargar la interfaz o el fondo.\n\nDetalles:\n{str(e)}"
            )
            sys.exit(1)

    def mostrar_ocultar_contrasena(self, checked):
        if checked:
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def funcion_login(self):
        print("¡El botón de login funciona!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.show()
    sys.exit(app.exec())