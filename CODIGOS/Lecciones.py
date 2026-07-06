import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui, QtCore


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


class Lecciones(QtWidgets.QWidget):
    def __init__(self, jugador=None):
        super().__init__()

        self.jugador = jugador
        self.lenguaje_seleccionado = None

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Lecciones.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Lecciones.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        uic.loadUi(str(ruta_ui), self)

        self.resize(1920, 1080)

        self.fondo = FondoImagen(self, ruta_imagen)

        self.configurar_botones()
        self.conectar_eventos()

    def configurar_botones(self):
        botones_lenguaje = [self.btnPython, self.btnJava, self.btnC, self.btnMySQL]

        for boton in botones_lenguaje:
            boton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            boton.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }

                QPushButton:hover {
                    border: 3px solid #0B73D9;
                    border-radius: 8px;
                    background-color: rgba(11, 115, 217, 25);
                }
            """)

        self.btnComenzar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnComenzar.setEnabled(False)

    def conectar_eventos(self):
        self.btnPython.clicked.connect(lambda: self.seleccionar_lenguaje("Python"))
        self.btnJava.clicked.connect(lambda: self.seleccionar_lenguaje("Java"))
        self.btnC.clicked.connect(lambda: self.seleccionar_lenguaje("C"))
        self.btnMySQL.clicked.connect(lambda: self.seleccionar_lenguaje("MySQL"))

        self.btnComenzar.clicked.connect(self.comenzar_aventura)

    def seleccionar_lenguaje(self, lenguaje):
        self.lenguaje_seleccionado = lenguaje
        self.btnComenzar.setEnabled(True)

        self.limpiar_estilos_lenguajes()

        if lenguaje == "Python":
            boton = self.btnPython
        elif lenguaje == "Java":
            boton = self.btnJava
        elif lenguaje == "C":
            boton = self.btnC
        elif lenguaje == "MySQL":
            boton = self.btnMySQL
        else:
            boton = None

        if boton:
            boton.setStyleSheet("""
                QPushButton {
                    background-color: rgba(11, 115, 217, 45);
                    border: 4px solid #0B73D9;
                    border-radius: 8px;
                }

                QPushButton:hover {
                    background-color: rgba(11, 115, 217, 55);
                    border: 4px solid #0B73D9;
                    border-radius: 8px;
                }
            """)

    def limpiar_estilos_lenguajes(self):
        botones_lenguaje = [self.btnPython, self.btnJava, self.btnC, self.btnMySQL]

        for boton in botones_lenguaje:
            boton.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }

                QPushButton:hover {
                    border: 3px solid #0B73D9;
                    border-radius: 8px;
                    background-color: rgba(11, 115, 217, 25);
                }
            """)

    def comenzar_aventura(self):
        if self.lenguaje_seleccionado is None:
            QtWidgets.QMessageBox.warning(
                self,
                "Selecciona un lenguaje",
                "Debes seleccionar un lenguaje antes de comenzar la aventura."
            )
            return

        try:
            if self.lenguaje_seleccionado == "Python":
                from NivelesPython import NivelesPython

                try:
                    self.ventana_niveles = NivelesPython(self.jugador)
                except TypeError:
                    self.ventana_niveles = NivelesPython()

            elif self.lenguaje_seleccionado == "Java":
                from NivelesJava import NivelesJava

                try:
                    self.ventana_niveles = NivelesJava(self.jugador)
                except TypeError:
                    self.ventana_niveles = NivelesJava()

            elif self.lenguaje_seleccionado == "CSharp":
                from NivelesC import NivelesCSharp

                try:
                    self.ventana_niveles = NivelesCSharp(self.jugador)
                except TypeError:
                    self.ventana_niveles = NivelesCSharp()

            elif self.lenguaje_seleccionado == "MySQL":
                from NivelesMySQL import NivelesMySQL

                try:
                    self.ventana_niveles = NivelesMySQL(self.jugador)
                except TypeError:
                    self.ventana_niveles = NivelesMySQL()

            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Lenguaje no válido",
                    "El lenguaje seleccionado no es válido."
                )
                return

            self.ventana_niveles.showMaximized()
            self.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al abrir niveles",
                f"No se pudo abrir la ventana de niveles.\n\nDetalles:\n{e}"
            )

    def volver_menu_usuario(self):
        try:
            from MenuUsuario import MenuUsuario

            try:
                self.ventana_menu = MenuUsuario(self.jugador)
            except TypeError:
                self.ventana_menu = MenuUsuario()

            self.ventana_menu.showMaximized()
            self.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"No se pudo volver al menú de usuario.\n\nDetalles:\n{e}"
            )

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Lecciones()
    ventana.show()
    sys.exit(app.exec())