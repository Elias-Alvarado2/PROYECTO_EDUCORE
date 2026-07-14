import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui
from Alertas import Alertas
from ConexionBD import ConexionBD
from Registro import RegistroWindow
from pantalla_carga import PantallaCarga


PERSONAJE_ADMIN_PREDETERMINADO = "pato"


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
            Alertas.mostrar(
                self,
                "Error de Sistema",
                f"No se pudo cargar la interfaz o el fondo.\n\nDetalles:\n{str(e)}",
                "error"
            )
            sys.exit(1)

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

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
            Alertas.mostrar(
                self,
                "Campos vacíos",
                "Debes ingresar tu usuario y contraseña.",
                "advertencia"
            )
            return

        try:
            admin = self.db.validar_admin(usuario, contrasena)

            if admin:
                sesion_admin = dict(admin)
                sesion_admin["rol"] = "administrador"
                sesion_admin["id_jugador"] = None
                sesion_admin["personaje"] = PERSONAJE_ADMIN_PREDETERMINADO
                sesion_admin["vidas_infinitas"] = True

                Alertas.mostrar(
                    self,
                    "Bienvenido administrador",
                    f"Inicio de sesión correcto.\n\nBienvenido, {admin['nombre']}.",
                    "exito"
                )

                self.abrir_menu_admin(sesion_admin)
                return

            jugador = self.db.validar_jugador(usuario, contrasena)

            if jugador:
                sesion_jugador = dict(jugador)
                sesion_jugador["rol"] = "jugador"
                sesion_jugador["id_admin"] = None
                sesion_jugador["vidas_infinitas"] = False

                self.db.registrar_historial(
                    jugador["id_jugador"],  
                    "Inicio de sesión",
                    f"El jugador {jugador['nombre']} inició sesión correctamente."
                )

                Alertas.mostrar(
                    self,
                    "Bienvenido",
                    f"Inicio de sesión correcto.\n\nBienvenido, {jugador['nombre']}.",
                    "exito"
                )

                self.abrir_menu_usuario(sesion_jugador)
                return

            Alertas.mostrar(
                self,
                "Usuario no encontrado",
                "El usuario o la contraseña son incorrectos.\n\n"
                "Si no tienes una cuenta, debes registrarte antes de iniciar sesión.",
                "error"
            )

            self.txtContrasena.clear()
            self.txtContrasena.setFocus()

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error de base de datos",
                str(e),
                "error"
            )

    def abrir_menu_usuario(self, jugador):
        try:
            from MenuUsuario import MenuUsuario

            try:
                self.menu_usuario = MenuUsuario(jugador)
            except TypeError:
                self.menu_usuario = MenuUsuario()

            self.pantalla_carga = PantallaCarga(self.menu_usuario)

            app = QtWidgets.QApplication.instance()
            app.pantalla_carga = self.pantalla_carga
            app.menu_usuario = self.menu_usuario

            self.pantalla_carga.showMaximized()
            self.close()

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir el menú del jugador.\n\nDetalles:\n{e}",
                "error"
            )

    def abrir_menu_admin(self, admin):
        try:
            from MenuAdministrador import MenuAdministrador

            try:
                self.menu_admin = MenuAdministrador(admin)
            except TypeError:
                self.menu_admin = MenuAdministrador()

            self.pantalla_carga = PantallaCarga(self.menu_admin)

            app = QtWidgets.QApplication.instance()
            app.pantalla_carga = self.pantalla_carga
            app.menu_admin = self.menu_admin

            self.pantalla_carga.showMaximized()
            self.close()

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir el menú del administrador.\n\nDetalles:\n{e}",
                "error"
            )

    def abrir_registro(self):
        try:
            self.registro = RegistroWindow()

            app = QtWidgets.QApplication.instance()
            app.registro = self.registro

            self.registro.show()
            self.close()

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir el registro.\n\nDetalles:\n{e}",
                "error"
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = LoginWindow()
    ventana.show()

    sys.exit(app.exec())