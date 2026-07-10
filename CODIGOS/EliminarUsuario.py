import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui

from ConexionBD import ConexionBD
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


class EliminarUsuario(QtWidgets.QWidget):
    def __init__(self, ventana_anterior=None):
        super().__init__()

        self.ventana_anterior = ventana_anterior
        self.ventana_gestion_usuarios = None

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Eliminar-Usuario.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Eliminar_Usuario.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        uic.loadUi(str(ruta_ui), self)

        self.resize(1920, 1080)

        self.fondo = FondoImagen(self, ruta_imagen)

        self.db = ConexionBD()
        self.jugador_actual = None

        self.configurar_campos()
        self.conectar_eventos()

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        super().resizeEvent(event)

    def configurar_campos(self):
        self.txt_idjugador.setValidator(QtGui.QIntValidator(1, 999999))

        self.txt_nombreusuario.setReadOnly(True)
        self.txt_correo.setReadOnly(True)
        self.txt_personaje.setReadOnly(True)
        self.txt_vidas.setReadOnly(True)
        self.txt_fecharegistro.setReadOnly(True)
        self.txt_estado.setReadOnly(True)

    def conectar_eventos(self):
        self.txt_idjugador.returnPressed.connect(self.buscar_usuario)
        self.txt_idjugador.editingFinished.connect(self.buscar_usuario)

        self.btn_eliminarusuario.clicked.connect(self.eliminar_usuario)

        if hasattr(self, "btn_cancelar"):
            self.btn_cancelar.clicked.connect(self.limpiar_campos)

        if hasattr(self, "btn_volver"):
            self.btn_volver.clicked.connect(self.volver_gestion_usuarios)

        if hasattr(self, "btn_Volver"):
            self.btn_Volver.clicked.connect(self.volver_gestion_usuarios)

    def volver_gestion_usuarios(self):
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

            from GestionUsuario import GestionUsuario

            FormTransicion(
                self,
                GestionUsuario,
                guardar_actual=False
            )

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al volver",
                f"No se pudo abrir Gestión Usuarios:\n{e}"
            )

    def buscar_usuario(self):
        id_jugador = self.txt_idjugador.text().strip()

        if id_jugador == "":
            self.jugador_actual = None
            self.limpiar_datos_usuario()
            return

        try:
            jugador = self.db.buscar_jugador_por_id(id_jugador)

            if jugador is None:
                self.jugador_actual = None
                self.limpiar_datos_usuario()

                QtWidgets.QMessageBox.warning(
                    self,
                    "Usuario no encontrado",
                    f"No existe un jugador con ID {id_jugador}."
                )
                return

            self.jugador_actual = jugador
            self.mostrar_datos_usuario(jugador)

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error de base de datos",
                str(e)
            )

    def mostrar_datos_usuario(self, jugador):
        self.txt_nombreusuario.setText(str(jugador["nombre"]))
        self.txt_correo.setText(str(jugador["correo"]))
        self.txt_personaje.setText(str(jugador["personaje"]))
        self.txt_vidas.setText(str(jugador["vidas"]))
        self.txt_fecharegistro.setText(str(jugador["fecha_registro"]))
        self.txt_estado.setText(str(jugador["estado"]))

    def limpiar_datos_usuario(self):
        self.txt_nombreusuario.clear()
        self.txt_correo.clear()
        self.txt_personaje.clear()
        self.txt_vidas.clear()
        self.txt_fecharegistro.clear()
        self.txt_estado.clear()

    def limpiar_campos(self):
        self.txt_idjugador.clear()
        self.limpiar_datos_usuario()
        self.jugador_actual = None
        self.txt_idjugador.setFocus()

    def eliminar_usuario(self):
        id_jugador = self.txt_idjugador.text().strip()

        if id_jugador == "":
            QtWidgets.QMessageBox.warning(
                self,
                "ID vacío",
                "Debes ingresar el ID del jugador que deseas eliminar."
            )
            return

        if self.jugador_actual is None:
            self.buscar_usuario()

            if self.jugador_actual is None:
                return

        respuesta = QtWidgets.QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Seguro que deseas eliminar este jugador?\n\n"
            f"ID: {self.jugador_actual['id_jugador']}\n"
            f"Nombre: {self.jugador_actual['nombre']}\n"
            f"Correo: {self.jugador_actual['correo']}\n\n"
            f"Esta acción también eliminará sus datos relacionados.",
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No
        )

        if respuesta != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        try:
            eliminado = self.db.eliminar_jugador(id_jugador)

            if eliminado:
                QtWidgets.QMessageBox.information(
                    self,
                    "Usuario eliminado",
                    "El jugador fue eliminado correctamente."
                )

                self.limpiar_campos()

            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "No se pudo eliminar",
                    "No se encontró el jugador o no se pudo eliminar."
                )

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error de base de datos",
                str(e)
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = EliminarUsuario()
    ventana.show()

    sys.exit(app.exec())