from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui

from GestionUsuario import GestionUsuario


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


class MenuAdministrador(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Menu-Administrador.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Menu-Administrador.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        uic.loadUi(str(ruta_ui), self)

        self.resize(1920, 1080)

        self.fondo = FondoImagen(self, ruta_imagen)

        self.conectar_eventos()

    def conectar_eventos(self):
        # Botón Gestionar Usuarios
        if hasattr(self, "btnGestionUsuarios"):
            self.btnGestionUsuarios.clicked.connect(self.abrir_gestionar_usuarios)

        if hasattr(self, "btn_gestionusuarios"):
            self.btn_gestionusuarios.clicked.connect(self.abrir_gestionar_usuarios)

        if hasattr(self, "btn_gestion_usuarios"):
            self.btn_gestion_usuarios.clicked.connect(self.abrir_gestionar_usuarios)

    def abrir_gestionar_usuarios(self):
        self.ventana_gestionar = GestionUsuario(self)
        self.ventana_gestionar.show()

        # Oculta el menú administrador
        self.hide()

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        super().resizeEvent(event)