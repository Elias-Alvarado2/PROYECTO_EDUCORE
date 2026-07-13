import sys
from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui
from quitar_barra import quitar
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

        # Coloca el fondo detrás de los botones.
        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class NivelesJava(QtWidgets.QWidget):
    def __init__(self,jugador=None,ventana_anterior=None):
        super().__init__()
        quitar(self)
        self.jugador = jugador
        self.ventana_anterior = ventana_anterior

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "NivelesJava.ui"
        )

        ruta_imagen = (
            PROYECTO_DIR
            / "assets"
            / "DISEÑOS"
            / "Niveles-Java.png"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        # Carga el formulario creado en Qt Designer.
        uic.loadUi(str(ruta_ui), self)

        # Resolución base utilizada en Qt Designer.
        self.resize(1920, 1080)

        # Permite que la ventana cambie libremente de tamaño.
        self.setMinimumSize(0, 0)

        self.setMaximumSize(
            16777215,
            16777215
        )

        # Crea el fondo de pantalla.
        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        # Ajusta automáticamente los botones tomando como
        # referencia la resolución de 1920 x 1080.
        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=[
                self.btnVolver,
                self.btnNivel1,
                self.btnNivel2,
                self.btnNivel3,
                self.btnNivel4,
                self.btnNivel5,
                self.btnComenzar,
            ],
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.conectar_eventos()

    def conectar_eventos(self):
        self.btnVolver.clicked.connect(
            self.volver_form_anterior
        )

    def volver_form_anterior(self):
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

            from Lecciones import Lecciones

            try:
                ventana_lecciones = Lecciones(
                    self.jugador
                )

            except TypeError:
                ventana_lecciones = Lecciones()

            FormTransicion(
                self,
                ventana_lecciones,
                guardar_actual=False
            )

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al regresar",
                "No se pudo regresar al formulario anterior."
                f"\n\nDetalles:\n{e}"
            )

    def resizeEvent(self, event):
        # Ajusta únicamente el fondo.
        # Los botones son ajustados por BotonesResponsivos.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = NivelesJava()

    ventana.showMaximized()

    sys.exit(app.exec())