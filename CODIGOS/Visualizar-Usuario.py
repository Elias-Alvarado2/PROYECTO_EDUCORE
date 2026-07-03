from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui


class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.ruta_imagen = ruta_imagen
        self.pixmap_original = QtGui.QPixmap(str(self.ruta_imagen))

        self.setScaledContents(True)
        self.setGeometry(0, 0, ventana.width(), ventana.height())
        self.setPixmap(self.pixmap_original)

        # Mandar la imagen al fondo
        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(0, 0, ancho, alto)


class VisualizarUsuario(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Carpeta CODIGOS
        BASE_DIR = Path(__file__).resolve().parent

        # Carpeta PROYECTO_EDUCORE
        PROYECTO_DIR = BASE_DIR.parent

        # Ruta del archivo .ui del menú
        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Visualizar-Usuarios.ui"
        
        # Ruta de la imagen del menú
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Visualizar-Usuarios.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        # Cargar diseño del menú
        uic.loadUi(str(ruta_ui), self)

        # Tamaño del menú
        self.resize(1920, 1080)

        # Crear fondo usando la clase FondoImagen
        self.fondo = FondoImagen(self, ruta_imagen)

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())

        super().resizeEvent(event)