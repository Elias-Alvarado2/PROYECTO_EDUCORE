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

        # Coloca el fondo detrás del frame y los botones.
        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class NivelesC(QtWidgets.QWidget):
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
            / "NivelesC.ui"
        )

        ruta_imagen = (
            PROYECTO_DIR
            / "assets"
            / "DISEÑOS"
            / "Niveles-C.png"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        # Carga la interfaz de Qt Designer.
        uic.loadUi(str(ruta_ui), self)

        # Resolución original utilizada en Designer.
        self.resize(1920, 1080)

        # Permite reducir o aumentar libremente la ventana.
        self.setMinimumSize(0, 0)
        self.setMaximumSize(
            16777215,
            16777215
        )

        # Fondo de pantalla.
        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        # Ajusta automáticamente los botones.
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
        # Ajusta el fondo a toda la ventana.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        # El QFrame del Designer también debe ocupar
        # todo el espacio disponible.
        if hasattr(self, "NivelesC"):
            self.NivelesC.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )

            self.NivelesC.raise_()

        # Fuerza el ajuste después de cambiar el tamaño del frame.
        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = NivelesC()
    ventana.showMaximized()

    sys.exit(app.exec())