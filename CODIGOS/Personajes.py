import sys
from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui


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

        self.setPixmap(self.pixmap_original)

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class Personajes(QtWidgets.QWidget):
    def __init__(self, jugador=None):
        super().__init__()

        self.jugador = jugador

        # PROYECTO_EDUCORE/CODIGOS
        base_dir = Path(__file__).resolve().parent

        # PROYECTO_EDUCORE
        proyecto_dir = base_dir.parent

        # Formulario creado en Qt Designer.
        ruta_ui = (
            proyecto_dir
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "Personaje.ui"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el formulario:\n{ruta_ui}"
            )

        uic.loadUi(str(ruta_ui), self)

        # Imagen completa usada como fondo del formulario.
        ruta_fondo = (
            proyecto_dir
            / "assets"
            / "DISEÑOS"
            / "Personaje.png"
        )

        if not ruta_fondo.exists():
            raise FileNotFoundError(
                f"No se encontró el fondo del formulario:\n{ruta_fondo}"
            )

        self.fondo = FondoImagen(
            self,
            ruta_fondo
        )

        # Asegura nuevamente que permanezca detrás.
        self.fondo.lower()

        self.setWindowTitle("Selección de personajes")

    def resizeEvent(self, evento):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

        super().resizeEvent(evento)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = Personajes()
    ventana.showMaximized()

    sys.exit(app.exec())