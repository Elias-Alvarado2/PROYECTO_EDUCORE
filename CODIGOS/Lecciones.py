import sys
from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui, QtCore

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

        # Mantiene el fondo detrás del frame y de los botones.
        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class Lecciones(QtWidgets.QWidget):
    def __init__(
        self,
        jugador=None,
        ventana_anterior=None
    ):
        super().__init__()

        self.jugador = jugador
        self.ventana_anterior = ventana_anterior

        self.lenguaje_seleccionado = None
        self.ventana_niveles = None
        self.ventana_menu = None

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "Lecciones.ui"
        )

        ruta_imagen = (
            PROYECTO_DIR
            / "assets"
            / "DISEÑOS"
            / "Lecciones.png"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        # Carga el formulario de Qt Designer.
        uic.loadUi(
            str(ruta_ui),
            self
        )

        # Resolución utilizada para diseñar el formulario.
        self.resize(
            1920,
            1080
        )

        # Permite que pueda ajustarse a resoluciones menores o mayores.
        self.setMinimumSize(
            0,
            0
        )

        self.setMaximumSize(
            16777215,
            16777215
        )

        # Crea el fondo adaptable.
        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        # Hace responsivos todos los botones.
        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=[
                self.btnPython,
                self.btnJava,
                self.btnC,
                self.btnMySQL,
                self.btnComenzar,
                self.btn_volver,
            ],
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.configurar_botones()
        self.conectar_eventos()

    def configurar_botones(self):
        botones_lenguaje = [
            self.btnPython,
            self.btnJava,
            self.btnC,
            self.btnMySQL,
        ]

        for boton in botones_lenguaje:
            boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.PointingHandCursor
                )
            )

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

        self.btnComenzar.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )

        # El botón comienza desactivado hasta elegir un lenguaje.
        self.btnComenzar.setEnabled(False)

    def conectar_eventos(self):
        self.btnPython.clicked.connect(
            lambda: self.seleccionar_lenguaje("Python")
        )

        self.btnJava.clicked.connect(
            lambda: self.seleccionar_lenguaje("Java")
        )

        self.btnC.clicked.connect(
            lambda: self.seleccionar_lenguaje("C")
        )

        self.btnMySQL.clicked.connect(
            lambda: self.seleccionar_lenguaje("MySQL")
        )

        self.btnComenzar.clicked.connect(
            self.comenzar_aventura
        )

        self.btn_volver.clicked.connect(
            self.volver_pantalla_anterior
        )

    def seleccionar_lenguaje(self, lenguaje):
        self.lenguaje_seleccionado = lenguaje

        # Habilita el botón Comenzar.
        self.btnComenzar.setEnabled(True)

        # Limpia la selección anterior.
        self.limpiar_estilos_lenguajes()

        boton = None

        if lenguaje == "Python":
            boton = self.btnPython

        elif lenguaje == "Java":
            boton = self.btnJava

        elif lenguaje == "C":
            boton = self.btnC

        elif lenguaje == "MySQL":
            boton = self.btnMySQL

        if boton is not None:
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
        botones_lenguaje = [
            self.btnPython,
            self.btnJava,
            self.btnC,
            self.btnMySQL,
        ]

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
                "Debes seleccionar un lenguaje antes "
                "de comenzar la aventura."
            )
            return

        try:
            if self.lenguaje_seleccionado == "Python":
                from NivelesPython import NivelesPython

                self.ventana_niveles = self.crear_ventana_niveles(
                    NivelesPython
                )

            elif self.lenguaje_seleccionado == "Java":
                from NivelesJava import NivelesJava

                self.ventana_niveles = self.crear_ventana_niveles(
                    NivelesJava
                )

            elif self.lenguaje_seleccionado == "C":
                from NivelesC import NivelesC

                self.ventana_niveles = self.crear_ventana_niveles(
                    NivelesC
                )

            elif self.lenguaje_seleccionado == "MySQL":
                from NivelesMySQL import NivelesMySQL

                self.ventana_niveles = self.crear_ventana_niveles(
                    NivelesMySQL
                )

            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Lenguaje no válido",
                    "El lenguaje seleccionado no es válido."
                )
                return

            FormTransicion(
                self,
                self.ventana_niveles
            )

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al abrir niveles",
                "No se pudo abrir la ventana de niveles."
                f"\n\nDetalles:\n{e}"
            )

    def crear_ventana_niveles(self, clase_niveles):
        """
        Intenta crear la ventana enviando el jugador y esta
        ventana como anterior. Si la clase no recibe esos
        argumentos, prueba con formas más simples.
        """

        try:
            return clase_niveles(
                jugador=self.jugador,
                ventana_anterior=self
            )

        except TypeError:
            try:
                return clase_niveles(
                    self.jugador
                )

            except TypeError:
                return clase_niveles()

    def volver_pantalla_anterior(self):
        try:
            app = QtWidgets.QApplication.instance()

            # Primero intenta utilizar el historial universal.
            if (
                hasattr(app, "historial_forms")
                and len(app.historial_forms) > 0
            ):
                FormAnterior(self)
                return

            # Si se entregó una ventana anterior explícitamente,
            # regresa a ella.
            if self.ventana_anterior is not None:
                FormTransicion(
                    self,
                    self.ventana_anterior,
                    guardar_actual=False
                )
                return

            # Si no existe historial ni ventana anterior,
            # determina si debe volver al menú de administrador
            # o al menú de usuario.
            if self.es_administrador():
                from MenuAdministrador import MenuAdministrador

                try:
                    self.ventana_menu = MenuAdministrador(
                        self.jugador
                    )

                except TypeError:
                    self.ventana_menu = MenuAdministrador()

            else:
                from MenuUsuario import MenuUsuario

                try:
                    self.ventana_menu = MenuUsuario(
                        self.jugador
                    )

                except TypeError:
                    self.ventana_menu = MenuUsuario()

            FormTransicion(
                self,
                self.ventana_menu,
                guardar_actual=False
            )

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                "No se pudo volver a la pantalla anterior."
                f"\n\nDetalles:\n{e}"
            )

    def es_administrador(self):
        """
        Intenta determinar si la información recibida pertenece
        a un administrador.
        """

        if self.jugador is None:
            return False

        # Cuando los datos vienen en forma de diccionario.
        if isinstance(self.jugador, dict):
            if "id_admin" in self.jugador:
                return True

            if (
                "usuario" in self.jugador
                and "id_jugador" not in self.jugador
            ):
                return True

            return False

        # Cuando los datos vienen en forma de objeto.
        if hasattr(self.jugador, "id_admin"):
            return True

        if (
            hasattr(self.jugador, "usuario")
            and not hasattr(self.jugador, "id_jugador")
        ):
            return True

        return False

    def resizeEvent(self, event):
        # Ajusta el fondo al tamaño actual de la ventana.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        # El frame principal también ocupa toda la ventana.
        if hasattr(self, "Lecciones"):
            self.Lecciones.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )

            self.Lecciones.raise_()

        # Ajusta nuevamente los botones después de cambiar
        # el tamaño del frame.
        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = Lecciones()

    ventana.showMaximized()

    sys.exit(app.exec())