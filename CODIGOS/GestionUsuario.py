from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui
from Alertas import Alertas
from Transicion import FormTransicion, FormAnterior
from AjusteResponsive import BotonesResponsivos


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

        # Mantiene el fondo detrás del frame y los botones.
        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class GestionUsuario(QtWidgets.QWidget):
    def __init__(self, ventana_anterior=None):
        super().__init__()

        self.ventana_anterior = ventana_anterior

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "Gestion-Usuario.ui"
        )

        ruta_imagen = (
            PROYECTO_DIR
            / "assets"
            / "DISEÑOS"
            / "Gestion-Usuarios.png"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        # Carga el diseño.
        uic.loadUi(str(ruta_ui), self)

        # Resolución original utilizada en Designer.
        self.resize(1920, 1080)

        # Permite que la ventana se adapte a otras resoluciones.
        self.setMinimumSize(0, 0)
        self.setMaximumSize(
            16777215,
            16777215
        )

        # Crea el fondo.
        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        # Ajusta automáticamente los cuatro botones.
        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=[
                self.btn_editar,
                self.btn_eliminar,
                self.btn_visualizar,
                self.btn_volver,
            ],
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.conectar_eventos()

    def conectar_eventos(self):
        self.btn_visualizar.clicked.connect(
            self.abrir_visualizar_usuario
        )

        self.btn_eliminar.clicked.connect(
            self.abrir_eliminar_usuario
        )

        self.btn_editar.clicked.connect(
            self.abrir_editar_usuario
        )

        self.btn_volver.clicked.connect(
            self.volver_menu_administrador
        )

    def abrir_visualizar_usuario(self):
        try:
            from VisualizarUsuario import VisualizarUsuario

            FormTransicion(
                self,
                VisualizarUsuario
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir Visualizar Usuarios.\n\nDetalles:\n{e}",
                "error"
            )

    def abrir_eliminar_usuario(self):
        try:
            from EliminarUsuario import EliminarUsuario

            FormTransicion(
                self,
                EliminarUsuario
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir Eliminar Usuario.\n\nDetalles:\n{e}",
                "error"
            )

    def abrir_editar_usuario(self):
        try:
            from EditarUsuario import EditarUsuario

            FormTransicion(
                self,
                EditarUsuario
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir Editar Usuario.\n\nDetalles:\n{e}",
                "error"
            )

    def volver_menu_administrador(self):
        try:
            app = QtWidgets.QApplication.instance()

            if (
                hasattr(app, "historial_forms")
                and len(app.historial_forms) > 0
            ):
                FormAnterior(self)
                return

            if self.ventana_anterior is not None:
                FormTransicion(
                    self,
                    self.ventana_anterior,
                    guardar_actual=False
                )
                return

            from MenuAdministrador import MenuAdministrador

            FormTransicion(
                self,
                MenuAdministrador,
                guardar_actual=False
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo volver al Menú Administrador.\n\nDetalles:\n{e}",
                "error"
            )

    def resizeEvent(self, event):
        # Ajusta el fondo.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        # El frame contiene los cuatro botones.
        # También debe ocupar toda la ventana.
        if hasattr(self, "GestionUsuario"):
            self.GestionUsuario.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )

            self.GestionUsuario.raise_()

        # Fuerza el ajuste después de redimensionar el frame.
        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        super().resizeEvent(event)