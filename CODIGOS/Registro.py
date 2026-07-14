import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic

from Alertas import Alertas
from ConexionBD import ConexionBD


class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.ruta_imagen = ruta_imagen
        self.pixmap_original = QtGui.QPixmap(str(self.ruta_imagen))

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
        self.setGeometry(0, 0, ancho, alto)


class RegistroWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = (PROYECTO_DIR/ "EXPO-DISEÑOS"/ "DESIGNER"/ "Registro.ui")

        ruta_imagen = (PROYECTO_DIR/ "assets"/ "DISEÑOS"/ "Registro.jpeg")

        try:
            if not ruta_ui.exists():
                raise FileNotFoundError(
                    f"No se encontró Registro.ui en:\n{ruta_ui}"
                )

            if not ruta_imagen.exists():
                raise FileNotFoundError(
                    f"No se encontró la imagen del registro en:\n"
                    f"{ruta_imagen}"
                )

            # Cargar el formulario de Qt Designer
            uic.loadUi(str(ruta_ui), self)

            self.resize(1020, 720)

            # =================================================
            # CORREGIR EL COMPORTAMIENTO DE LA TECLA ENTER
            # =================================================

            # El botón de volver al login nunca debe ejecutarse
            # automáticamente al presionar Enter.
            self.btn_Iniciar.setAutoDefault(False)
            self.btn_Iniciar.setDefault(False)
            self.btn_Iniciar.setFocusPolicy(
                QtCore.Qt.FocusPolicy.NoFocus
            )

            # El botón del ojo tampoco debe activarse con Enter.
            self.btnMostrarContrasena.setAutoDefault(False)
            self.btnMostrarContrasena.setDefault(False)
            self.btnMostrarContrasena.setFocusPolicy(
                QtCore.Qt.FocusPolicy.NoFocus
            )

            # El botón Registrar será el botón predeterminado.
            # Por eso, al presionar Enter, se ejecutará
            # registrar_usuario().
            self.btnRegistrarUsuario.setAutoDefault(True)
            self.btnRegistrarUsuario.setDefault(True)

            # El cursor comienza en el campo de usuario.
            self.txtUsuario.setFocus()

            # =================================================
            # FONDO DE LA VENTANA
            # =================================================

            self.setObjectName("RegistroWindow")

            self.setStyleSheet(f"""
                #RegistroWindow {{
                    border-image:
                        url("{ruta_imagen.as_posix()}")
                        0 0 0 0
                        stretch stretch;
                }}
            """)

            # Conexión con la base de datos
            self.db = ConexionBD()

            # =================================================
            # CONTRASEÑA
            # =================================================

            self.txtContrasena.setEchoMode(
                QtWidgets.QLineEdit.EchoMode.Password
            )

            self.btnMostrarContrasena.setCheckable(True)

            self.btnMostrarContrasena.clicked.connect(
                self.mostrar_ocultar_contrasena
            )

            # =================================================
            # BOTONES
            # =================================================

            self.btnRegistrarUsuario.clicked.connect(
                self.registrar_usuario
            )

            self.btn_Iniciar.clicked.connect(
                self.volver_login
            )

            # No es necesario conectar returnPressed de cada
            # campo porque btnRegistrarUsuario es el botón
            # predeterminado del QDialog.

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error de Sistema",
                "No se pudo cargar la ventana de registro."
                f"\n\nDetalles:\n{str(e)}",
                "error"
            )
            sys.exit(1)

    def mostrar_ocultar_contrasena(self, checked):
        if checked:
            self.txtContrasena.setEchoMode(
                QtWidgets.QLineEdit.EchoMode.Normal
            )
        else:
            self.txtContrasena.setEchoMode(
                QtWidgets.QLineEdit.EchoMode.Password
            )

    def registrar_usuario(self):
        nombre = self.txtUsuario.text().strip()
        correo = self.txtCorreo.text().strip()
        contrasena = self.txtContrasena.text().strip()

        # Si presiona Enter sin llenar los campos,
        # aparecerá esta alerta.
        if nombre == "" or correo == "" or contrasena == "":
            Alertas.mostrar(
                self,
                "Campos vacíos",
                "Debes llenar usuario, correo electrónico "
                "y contraseña.",
                "advertencia"
            )

            # Colocar el cursor en el primer campo vacío
            if nombre == "":
                self.txtUsuario.setFocus()
            elif correo == "":
                self.txtCorreo.setFocus()
            else:
                self.txtContrasena.setFocus()

            return

        if "@" not in correo or "." not in correo:
            Alertas.mostrar(
                self,
                "Correo inválido",
                "Debes ingresar un correo electrónico válido.",
                "advertencia"
            )

            self.txtCorreo.setFocus()
            self.txtCorreo.selectAll()
            return

        if len(contrasena) < 4:
            Alertas.mostrar(
                self,
                "Contraseña débil",
                "La contraseña debe tener al menos "
                "4 caracteres.",
                "advertencia"
            )

            self.txtContrasena.setFocus()
            self.txtContrasena.selectAll()
            return

        try:
            registrado = self.db.registrar_jugador(
                nombre,
                correo,
                contrasena
            )

            if registrado:
                Alertas.mostrar(
                    self,
                    "Registro exitoso",
                    "Tu cuenta fue creada correctamente."
                    "\n\nAhora puedes iniciar sesión.",
                    "exito"
                )

                self.volver_login()

            else:
                Alertas.mostrar(
                    self,
                    "Usuario existente",
                    "Ya existe un jugador con ese usuario "
                    "o correo electrónico.\n\n"
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
        try:
            from Login import LoginWindow

            self.login = LoginWindow()

            # Mantener una referencia para evitar que Python
            # elimine la ventana.
            app = QtWidgets.QApplication.instance()

            if app is not None:
                app.login = self.login

            self.login.show()
            self.close()

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                "No se pudo volver al inicio de sesión."
                f"\n\nDetalles:\n{str(e)}",
                "error"
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = RegistroWindow()
    ventana.show()

    sys.exit(app.exec())