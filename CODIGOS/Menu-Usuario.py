import sys
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QLineEdit


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Login(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Cargar diseño Login.ui
        ruta_login = os.path.join(BASE_DIR, "Login.ui")
        uic.loadUi(ruta_login, self)

        # La contraseña empieza oculta
        self.txtContrasena.setEchoMode(QLineEdit.EchoMode.Password)

        # Hacer que el botón del ojo funcione como activado/desactivado
        self.btnMostrarContrasena.setCheckable(True)

        # Botón para mostrar/ocultar contraseña
        self.btnMostrarContrasena.clicked.connect(self.mostrar_ocultar_contrasena)

        # Botón para pasar al Menu-Jugador
        self.btn_Iniciar.clicked.connect(self.abrir_menu_jugador)

    def mostrar_ocultar_contrasena(self, checked):
        if checked:
            self.txtContrasena.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.txtContrasena.setEchoMode(QLineEdit.EchoMode.Password)

    def abrir_menu_jugador(self):
        self.menu_jugador = MenuJugador()
        self.menu_jugador.show()
        self.close()


class MenuJugador(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Cargar diseño Menu-Jugador.ui
        ruta_menu = os.path.join(BASE_DIR, "Menu-Jugador.ui")
        uic.loadUi(ruta_menu, self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = Login()
    ventana.show()

    sys.exit(app.exec())