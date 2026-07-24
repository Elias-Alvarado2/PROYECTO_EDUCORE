import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic

from Alertas import Alertas
from ConexionBD import ConexionBD
from Transicion import FormTransicion


class TrabajadorRegistro(QtCore.QObject):
    completado = QtCore.pyqtSignal(object)
    error = QtCore.pyqtSignal(str)

    def __init__(self, nombre, correo, contrasena):
        super().__init__()

        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    @QtCore.pyqtSlot()
    def ejecutar(self):
        try:
            db = ConexionBD()

            registrado = db.registrar_jugador(
                self.nombre,
                self.correo,
                self.contrasena
            )

            if not registrado:
                self.completado.emit(None)
                return

            jugador = db.validar_jugador(
                self.correo,
                self.contrasena
            )

            if jugador is None:
                raise ValueError(
                    "La cuenta fue registrada, pero no se pudieron "
                    "recuperar los datos del jugador."
                )

            self.completado.emit(jugador)

        except Exception as error:
            self.error.emit(str(error))


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

        self.setPixmap(
            self.pixmap_original
        )

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class RegistroWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        base_dir = Path(__file__).resolve().parent
        proyecto_dir = base_dir.parent

        ruta_ui = (
            proyecto_dir
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "Registro.ui"
        )

        ruta_imagen = (
            proyecto_dir
            / "assets"
            / "DISEÑOS"
            / "Registro.jpeg"
        )

        self.hilo_registro = None
        self.trabajador_registro = None
        self.menu_usuario = None
        self.transicion_menu_usuario = None
        self.login = None
        self.texto_boton_registro = ""
        self.transicion_en_curso = False

        try:
            if not ruta_ui.exists():
                raise FileNotFoundError(
                    f"No se encontró Registro.ui en:\n"
                    f"{ruta_ui}"
                )

            if not ruta_imagen.exists():
                raise FileNotFoundError(
                    "No se encontró la imagen del registro en:\n"
                    f"{ruta_imagen}"
                )

            uic.loadUi(
                str(ruta_ui),
                self
            )

            self.resize(
                1020,
                720
            )

            self.btn_Iniciar.setAutoDefault(False)
            self.btn_Iniciar.setDefault(False)

            self.btn_Iniciar.setFocusPolicy(
                QtCore.Qt.FocusPolicy.NoFocus
            )

            self.btnMostrarContrasena.setAutoDefault(False)
            self.btnMostrarContrasena.setDefault(False)

            self.btnMostrarContrasena.setFocusPolicy(
                QtCore.Qt.FocusPolicy.NoFocus
            )

            self.btnRegistrarUsuario.setAutoDefault(True)
            self.btnRegistrarUsuario.setDefault(True)

            self.texto_boton_registro = (
                self.btnRegistrarUsuario.text()
            )

            self.txtUsuario.setFocus()

            self.setObjectName(
                "RegistroWindow"
            )

            self.setStyleSheet(
                f"""
                #RegistroWindow {{
                    border-image:
                        url("{ruta_imagen.as_posix()}")
                        0 0 0 0
                        stretch stretch;
                }}
                """
            )

            self.txtContrasena.setEchoMode(
                QtWidgets.QLineEdit.EchoMode.Password
            )

            self.btnMostrarContrasena.setCheckable(
                True
            )

            self.btnMostrarContrasena.clicked.connect(
                self.mostrar_ocultar_contrasena
            )

            self.btnRegistrarUsuario.clicked.connect(
                self.registrar_usuario
            )

            self.btn_Iniciar.clicked.connect(
                self.volver_login
            )

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error de Sistema",
                "No se pudo cargar la ventana de registro."
                f"\n\nDetalles:\n{error}",
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
        if self.transicion_en_curso:
            return

        if (
            self.hilo_registro is not None
            and self.hilo_registro.isRunning()
        ):
            return

        nombre = self.txtUsuario.text().strip()
        correo = self.txtCorreo.text().strip()
        contrasena = self.txtContrasena.text().strip()

        if nombre == "" or correo == "" or contrasena == "":
            Alertas.mostrar(
                self,
                "Campos vacíos",
                "Debes llenar usuario, correo electrónico "
                "y contraseña.",
                "advertencia"
            )

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

        self.bloquear_formulario()

        self.hilo_registro = QtCore.QThread(
            self
        )

        self.trabajador_registro = TrabajadorRegistro(
            nombre,
            correo,
            contrasena
        )

        self.trabajador_registro.moveToThread(
            self.hilo_registro
        )

        self.hilo_registro.started.connect(
            self.trabajador_registro.ejecutar
        )

        self.trabajador_registro.completado.connect(
            self.registro_completado
        )

        self.trabajador_registro.error.connect(
            self.registro_fallido
        )

        self.trabajador_registro.completado.connect(
            self.hilo_registro.quit
        )

        self.trabajador_registro.error.connect(
            self.hilo_registro.quit
        )

        self.hilo_registro.finished.connect(
            self.trabajador_registro.deleteLater
        )

        self.hilo_registro.finished.connect(
            self.limpiar_hilo_registro
        )

        self.hilo_registro.start()

    def bloquear_formulario(self):
        self.btnRegistrarUsuario.setEnabled(False)
        self.btn_Iniciar.setEnabled(False)
        self.btnMostrarContrasena.setEnabled(False)

        self.txtUsuario.setEnabled(False)
        self.txtCorreo.setEnabled(False)
        self.txtContrasena.setEnabled(False)

        self.btnRegistrarUsuario.setText(
            "Registrando..."
        )

        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CursorShape.WaitCursor
        )

    def desbloquear_formulario(self):
        self.btnRegistrarUsuario.setEnabled(True)
        self.btn_Iniciar.setEnabled(True)
        self.btnMostrarContrasena.setEnabled(True)

        self.txtUsuario.setEnabled(True)
        self.txtCorreo.setEnabled(True)
        self.txtContrasena.setEnabled(True)

        self.btnRegistrarUsuario.setText(
            self.texto_boton_registro
        )

        self.restaurar_cursor()

    def restaurar_cursor(self):
        if QtWidgets.QApplication.overrideCursor() is not None:
            QtWidgets.QApplication.restoreOverrideCursor()

    def registro_completado(self, jugador):
        self.restaurar_cursor()

        if jugador is None:
            self.desbloquear_formulario()

            Alertas.mostrar(
                self,
                "Usuario existente",
                "Ya existe un jugador con ese usuario "
                "o correo electrónico.\n\n"
                "Intenta con otros datos o inicia sesión.",
                "advertencia"
            )

            return

        self.btnRegistrarUsuario.setText(
            self.texto_boton_registro
        )

        Alertas.mostrar(
            self,
            "Registro exitoso",
            "Tu cuenta fue creada correctamente."
            "\n\nBienvenido a EduCore.",
            "exito",
            "ACEPTAR"
        )

        self.transicion_en_curso = True

        QtCore.QTimer.singleShot(
            0,
            lambda jugador_actual=jugador:
            self.abrir_menu_usuario(jugador_actual)
        )

    def registro_fallido(self, mensaje):
        self.desbloquear_formulario()

        Alertas.mostrar(
            self,
            "Error de base de datos",
            mensaje,
            "error"
        )

    def limpiar_hilo_registro(self):
        hilo = self.hilo_registro

        self.hilo_registro = None
        self.trabajador_registro = None

        if hilo is not None:
            hilo.deleteLater()

    def abrir_menu_usuario(self, jugador):
        try:
            from MenuUsuario import MenuUsuario

            class MenuUsuarioRegistro(MenuUsuario):
                def actualizar_jugador_desde_bd(self):
                    return None

            self.menu_usuario = MenuUsuarioRegistro(
                jugador=jugador
            )

            self.menu_usuario.setAttribute(
                QtCore.Qt.WidgetAttribute.WA_DeleteOnClose,
                True
            )

            self.menu_usuario.destroyed.connect(
                self.limpiar_menu_usuario
            )

            app = QtWidgets.QApplication.instance()

            if app is not None:
                app.menu_usuario = self.menu_usuario

            try:
                self.transicion_menu_usuario = FormTransicion(
                    self,
                    self.menu_usuario,
                    guardar_actual=False
                )

            except TypeError:
                self.transicion_menu_usuario = FormTransicion(
                    self,
                    self.menu_usuario
                )

        except Exception as error:
            self.transicion_en_curso = False
            self.menu_usuario = None
            self.transicion_menu_usuario = None

            self.desbloquear_formulario()

            Alertas.mostrar(
                self,
                "Error",
                "La cuenta fue creada correctamente, pero "
                "no se pudo abrir el menú de usuario."
                f"\n\nDetalles:\n{error}",
                "error"
            )

    def limpiar_menu_usuario(self, *_):
        self.menu_usuario = None
        self.transicion_menu_usuario = None
        self.transicion_en_curso = False

    def volver_login(self):
        if self.transicion_en_curso:
            return

        if (
            self.hilo_registro is not None
            and self.hilo_registro.isRunning()
        ):
            return

        try:
            from Login import LoginWindow

            self.login = LoginWindow()

            app = QtWidgets.QApplication.instance()

            if app is not None:
                app.login = self.login

            self.login.show()
            self.close()

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error",
                "No se pudo volver al inicio de sesión."
                f"\n\nDetalles:\n{error}",
                "error"
            )

    def closeEvent(self, event):
        if (
            self.hilo_registro is not None
            and self.hilo_registro.isRunning()
        ):
            event.ignore()
            return

        super().closeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = RegistroWindow()
    ventana.show()

    sys.exit(app.exec())