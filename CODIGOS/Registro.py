import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui
from Alertas import Alertas
from ConexionBD import ConexionBD

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

class RegistroWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Registro.ui"

        # CAMBIA ESTE NOMBRE SI TU IMAGEN SE LLAMA DIFERENTE
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Registro.jpeg"

        try:
            if not ruta_ui.exists():
                raise FileNotFoundError(f"No se encontró Registro.ui en:\n{ruta_ui}")

            if not ruta_imagen.exists():
                raise FileNotFoundError(f"No se encontró la imagen del registro en:\n{ruta_imagen}")

            uic.loadUi(str(ruta_ui), self)

            self.resize(1020, 720)

            # Fondo de la ventana
            self.setObjectName("RegistroWindow")

            self.setStyleSheet(f"""
                #RegistroWindow {{
                    border-image: url("{ruta_imagen.as_posix()}") 0 0 0 0 stretch stretch;
                }}
            """)

            self.db = ConexionBD()

            # Ocultar contraseña
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

            # Mostrar / ocultar contraseña
            self.btnMostrarContrasena.setCheckable(True)
            self.btnMostrarContrasena.clicked.connect(self.mostrar_ocultar_contrasena)

            # Botón naranja: registrar usuario
            self.btnRegistrarUsuario.clicked.connect(self.registrar_usuario)

            # Botón verde: volver al login
            self.btn_Iniciar.clicked.connect(self.volver_login)

            # Enter para registrar
            self.txtContrasena.returnPressed.connect(self.registrar_usuario)
            self.txtUsuario.returnPressed.connect(self.registrar_usuario)
            self.txtCorreo.returnPressed.connect(self.registrar_usuario)

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error de Sistema",
                f"No se pudo cargar la ventana de registro.\n\nDetalles:\n{str(e)}",
                "error"
            )
            sys.exit(1)

    def mostrar_ocultar_contrasena(self, checked):
        if checked:
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def registrar_usuario(self):
        nombre = self.txtUsuario.text().strip()
        correo = self.txtCorreo.text().strip()
        contrasena = self.txtContrasena.text().strip()

        if nombre == "" or correo == "" or contrasena == "":
            Alertas.mostrar(
                self,
                "Campos vacíos",
                "Debes llenar usuario, correo electrónico y contraseña.",
                "advertencia"
            )
            return

        if "@" not in correo or "." not in correo:
            Alertas.mostrar(
                self,
                "Correo inválido",
                "Debes ingresar un correo electrónico válido.",
                "advertencia"
            )
            self.txtCorreo.setFocus()
            return

        if len(contrasena) < 4:
            Alertas.mostrar(
                self,
                "Contraseña débil",
                "La contraseña debe tener al menos 4 caracteres.",
                "advertencia"
            )
            self.txtContrasena.setFocus()
            return

        try:
            registrado = self.db.registrar_jugador(nombre, correo, contrasena)

            if registrado:
                Alertas.mostrar(
                    self,
                    "Registro exitoso",
                    "Tu cuenta fue creada correctamente.\n\nAhora puedes iniciar sesión.",
                    "exito"
                )

                self.volver_login()

            else:
                Alertas.mostrar(
                    self,
                    "Usuario existente",
                    "Ya existe un jugador con ese usuario o correo electrónico.\n\n"
                    "Intenta con otros datos o inicia sesión.",
                    "advertencia"
                )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error de base de datos",
                str(e),
                "error"
            )

    def volver_login(self):
        from Login import LoginWindow

        self.login = LoginWindow()
        self.login.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = RegistroWindow()
    ventana.show()
    sys.exit(app.exec())