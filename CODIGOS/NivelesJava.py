import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui

from Transicion import FormTransicion, FormAnterior

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


class NivelesJava(QtWidgets.QWidget):
    def __init__(self, jugador=None, ventana_anterior=None):
        super().__init__()

        self.jugador = jugador
        self.ventana_anterior = ventana_anterior

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "NivelesJava.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Niveles-Java.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        uic.loadUi(str(ruta_ui), self)

        self.resize(1920, 1080)

        self.fondo = FondoImagen(self, ruta_imagen)

        self.conectar_eventos()
    
    def conectar_eventos(self):
        self.btnVolver.clicked.connect(self.volver_form_anterior)

    def volver_form_anterior(self):
        try:
            app = QtWidgets.QApplication.instance()

            if hasattr(app, "historial_forms") and len(app.historial_forms) > 0:
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
                ventana_lecciones = Lecciones(self.jugador)
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
                f"No se pudo regresar al formulario anterior.\n\nDetalles:\n{e}"
            )

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = NivelesJava()
    ventana.showMaximized()
    sys.exit(app.exec())