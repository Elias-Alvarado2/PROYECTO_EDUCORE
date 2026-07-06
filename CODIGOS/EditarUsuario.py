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


class EditarUsuario(QtWidgets.QWidget):
    def __init__(self, ventana_anterior=None):
        super().__init__()

        # Guarda la ventana anterior, en este caso Gestión Usuarios
        self.ventana_anterior = ventana_anterior
        self.ventana_gestion_usuarios = None

        # Carpeta CODIGOS
        BASE_DIR = Path(__file__).resolve().parent

        # Carpeta PROYECTO_EDUCORE
        PROYECTO_DIR = BASE_DIR.parent

        # Ruta del archivo .ui del menú
        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Editar-Usuarios.ui"

        # Ruta de la imagen del menú
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Editar_Usuarios.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontro el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontro la imagen:\n{ruta_imagen}")

        # Cargar diseño del menú
        uic.loadUi(str(ruta_ui), self)

        # Tamaño del menú
        self.resize(1920, 1080)

        # Crear fondo usando la clase FondoImagen
        self.fondo = FondoImagen(self, ruta_imagen)

        # Conectar botón volver
        self.conectar_eventos()

    def conectar_eventos(self):
        # Botón volver
        if hasattr(self, "btn_volver"):
            self.btn_volver.clicked.connect(self.volver_gestion_usuarios)

        if hasattr(self, "btn_Volver"):
            self.btn_Volver.clicked.connect(self.volver_gestion_usuarios)

    def volver_gestion_usuarios(self):
        # Si EditarUsuario fue abierto desde Gestión Usuarios,
        # vuelve a mostrar esa misma ventana.
        if self.ventana_anterior is not None:
            self.ventana_anterior.show()
            self.close()
            return

        # Si ejecutaste este archivo directamente,
        # intenta abrir Gestión Usuarios desde su clase.
        try:
            from GestionUsuario import GestionUsuario

            self.ventana_gestion_usuarios = GestionUsuario()
            self.ventana_gestion_usuarios.show()
            self.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al volver",
                f"No se pudo abrir Gestión Usuarios:\n{e}"
            )

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        super().resizeEvent(event)