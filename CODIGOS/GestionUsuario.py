from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui

from VisualizarUsuario import VisualizarUsuario
from EliminarUsuario import EliminarUsuario
from EditarUsuario import EditarUsuario


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


class GestionUsuario(QtWidgets.QWidget):
    def __init__(self, ventana_anterior=None):
        super().__init__()

        # Aquí se guarda el Menú Administrador
        self.ventana_anterior = ventana_anterior
        self.ventana_visualizar = None
        self.ventana_eliminar = None
        self.ventana_editar = None

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Gestion-Usuario.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Gestion-Usuarios.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        uic.loadUi(str(ruta_ui), self)

        self.resize(1920, 1080)

        self.fondo = FondoImagen(self, ruta_imagen)

        self.conectar_eventos()

    def conectar_eventos(self):
        # Botón Visualizar Usuarios
        self.btn_visualizar.clicked.connect(self.abrir_visualizar_usuario)

        # Botón Eliminar Usuarios
        self.btn_eliminar.clicked.connect(self.abrir_eliminar_usuario)

        # Botón Editar Usuarios
        self.btn_editar.clicked.connect(self.abrir_editar_usuario)

        # Botón Volver al Menú Administrador
        if hasattr(self, "btn_volver"):
            self.btn_volver.clicked.connect(self.volver_menu_administrador)

        if hasattr(self, "btn_Volver"):
            self.btn_Volver.clicked.connect(self.volver_menu_administrador)

    def abrir_visualizar_usuario(self):
        self.ventana_visualizar = VisualizarUsuario(self)
        self.ventana_visualizar.show()
        self.hide()

    def abrir_eliminar_usuario(self):
        self.ventana_eliminar = EliminarUsuario(self)
        self.ventana_eliminar.show()
        self.hide()

    def abrir_editar_usuario(self):
        self.ventana_editar = EditarUsuario(self)
        self.ventana_editar.show()
        self.hide()

    def volver_menu_administrador(self):
        if self.ventana_anterior is not None:
            self.ventana_anterior.show()
            self.close()
        else:
            self.close()

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        super().resizeEvent(event)