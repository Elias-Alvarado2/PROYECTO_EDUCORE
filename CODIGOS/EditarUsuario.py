import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui, QtCore

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


class EditarUsuario(QtWidgets.QWidget):
    def __init__(self, ventana_anterior=None):
        super().__init__()

        self.ventana_anterior = ventana_anterior

        self.ANCHO_BASE = 1920
        self.ALTO_BASE = 1080

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Editar-Usuarios.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Editar_Usuarios.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        uic.loadUi(str(ruta_ui), self)

        self.resize(1920, 1080)

        self.fondo = FondoImagen(self, ruta_imagen)

        self.db = ConexionBD()

        self.jugador_actual = None
        self.ultimo_id_buscado = ""

        self.timer_busqueda_id = QtCore.QTimer(self)
        self.timer_busqueda_id.setSingleShot(True)
        self.timer_busqueda_id.timeout.connect(self.buscar_usuario_automatico)

        self.configurar_campos()
        self.conectar_eventos()

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        super().resizeEvent(event)

    def configurar_campos(self):
        self.txt_idjugador.setValidator(QtGui.QIntValidator(1, 999999))
        self.txt_vidas.setValidator(QtGui.QIntValidator(0, 999))
        self.txt_fecharegistro.setReadOnly(True)

        self.cmb_estado.clear()
        self.cmb_estado.addItems(["Activo", "Inactivo"])

    def conectar_eventos(self):
        self.txt_idjugador.textChanged.connect(self.iniciar_busqueda_automatica)
        self.txt_idjugador.returnPressed.connect(self.buscar_usuario)
        self.btn_confirmarcambios.clicked.connect(self.confirmar_cambios)

        if hasattr(self, "btn_volver"):
            self.btn_volver.clicked.connect(self.volver_gestion_usuario)

        if hasattr(self, "btn_Volver"):
            self.btn_Volver.clicked.connect(self.volver_gestion_usuario)

    def iniciar_busqueda_automatica(self):
        self.timer_busqueda_id.start(500)

    def buscar_usuario_automatico(self):
        id_jugador = self.txt_idjugador.text().strip()

        if id_jugador == "":
            self.jugador_actual = None
            self.ultimo_id_buscado = ""
            self.limpiar_datos_usuario()
            return

        if id_jugador == self.ultimo_id_buscado:
            return

        try:
            jugador = self.db.buscar_jugador_por_id(id_jugador)

            if jugador is None:
                self.jugador_actual = None
                self.ultimo_id_buscado = id_jugador
                self.limpiar_datos_usuario()
                return

            self.jugador_actual = jugador
            self.ultimo_id_buscado = id_jugador
            self.mostrar_datos_usuario(jugador)

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error de base de datos",
                str(e)
            )

    def buscar_usuario(self):
        id_jugador = self.txt_idjugador.text().strip()

        if id_jugador == "":
            self.jugador_actual = None
            self.ultimo_id_buscado = ""
            self.limpiar_datos_usuario()

            QtWidgets.QMessageBox.warning(
                self,
                "ID vacío",
                "Debes ingresar el ID del jugador."
            )
            return

        try:
            jugador = self.db.buscar_jugador_por_id(id_jugador)

            if jugador is None:
                self.jugador_actual = None
                self.ultimo_id_buscado = id_jugador
                self.limpiar_datos_usuario()

                QtWidgets.QMessageBox.warning(
                    self,
                    "Usuario no encontrado",
                    f"No existe un jugador con ID {id_jugador}."
                )
                return

            self.jugador_actual = jugador
            self.ultimo_id_buscado = id_jugador
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
        self.txt_contrasena.setText(str(jugador["contrasena"]))
        self.txt_personaje.setText(str(jugador["personaje"]))
        self.txt_vidas.setText(str(jugador["vidas"]))
        self.txt_fecharegistro.setText(str(jugador["fecha_registro"]))

        estado = str(jugador["estado"])

        index_estado = self.cmb_estado.findText(estado)

        if index_estado >= 0:
            self.cmb_estado.setCurrentIndex(index_estado)
        else:
            self.cmb_estado.setCurrentIndex(0)

        self.posicionar_elementos()

    def limpiar_datos_usuario(self):
        self.txt_nombreusuario.clear()
        self.txt_correo.clear()
        self.txt_contrasena.clear()
        self.txt_personaje.clear()
        self.txt_vidas.clear()
        self.txt_fecharegistro.clear()

        if self.cmb_estado.count() > 0:
            self.cmb_estado.setCurrentIndex(0)

    def validar_campos(self):
        id_jugador = self.txt_idjugador.text().strip()
        nombre = self.txt_nombreusuario.text().strip()
        correo = self.txt_correo.text().strip()
        contrasena = self.txt_contrasena.text().strip()
        personaje = self.txt_personaje.text().strip()
        vidas = self.txt_vidas.text().strip()
        estado = self.cmb_estado.currentText().strip()

        if id_jugador == "":
            QtWidgets.QMessageBox.warning(
                self,
                "ID vacío",
                "Debes ingresar el ID del jugador."
            )
            return None

        if nombre == "":
            QtWidgets.QMessageBox.warning(
                self,
                "Nombre vacío",
                "El nombre del usuario no puede estar vacío."
            )
            return None

        if correo == "":
            QtWidgets.QMessageBox.warning(
                self,
                "Correo vacío",
                "El correo no puede estar vacío."
            )
            return None

        if contrasena == "":
            QtWidgets.QMessageBox.warning(
                self,
                "Contraseña vacía",
                "La contraseña no puede estar vacía."
            )
            return None

        if personaje == "":
            QtWidgets.QMessageBox.warning(
                self,
                "Personaje vacío",
                "El personaje no puede estar vacío."
            )
            return None

        if vidas == "":
            QtWidgets.QMessageBox.warning(
                self,
                "Vidas vacías",
                "Las vidas no pueden estar vacías."
            )
            return None

        return {
            "id_jugador": id_jugador,
            "nombre": nombre,
            "correo": correo,
            "contrasena": contrasena,
            "personaje": personaje,
            "vidas": int(vidas),
            "estado": estado
        }

    def confirmar_cambios(self):
        datos = self.validar_campos()

        if datos is None:
            return

        if self.jugador_actual is None:
            self.buscar_usuario()

            if self.jugador_actual is None:
                return

        if str(self.jugador_actual["id_jugador"]) != str(datos["id_jugador"]):
            self.buscar_usuario()

            if self.jugador_actual is None:
                return

        respuesta = QtWidgets.QMessageBox.question(
            self,
            "Confirmar cambios",
            f"¿Seguro que deseas actualizar este jugador?\n\n"
            f"ID: {datos['id_jugador']}\n"
            f"Nombre: {datos['nombre']}\n"
            f"Correo: {datos['correo']}",
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No
        )

        if respuesta != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        try:
            actualizado = self.db.actualizar_jugador(
                datos["id_jugador"],
                datos["nombre"],
                datos["correo"],
                datos["contrasena"],
                datos["personaje"],
                datos["vidas"],
                datos["estado"]
            )

            if actualizado:
                QtWidgets.QMessageBox.information(
                    self,
                    "Usuario actualizado",
                    "Los datos del jugador fueron actualizados correctamente."
                )

                jugador_actualizado = self.db.buscar_jugador_por_id(datos["id_jugador"])

                if jugador_actualizado:
                    self.jugador_actual = jugador_actualizado
                    self.ultimo_id_buscado = str(jugador_actualizado["id_jugador"])
                    self.mostrar_datos_usuario(jugador_actualizado)

            else:
                QtWidgets.QMessageBox.information(
                    self,
                    "Sin cambios",
                    "No se realizaron cambios en el jugador."
                )

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error de base de datos",
                str(e)
            )

    def volver_gestion_usuario(self):
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
                "Error",
                f"No se pudo abrir Gestión de Usuarios.\n\nDetalles:\n{e}"
            )

    def posicionar_elementos(self):
        escala_x = self.width() / self.ANCHO_BASE
        escala_y = self.height() / self.ALTO_BASE

        if hasattr(self, "Editar_Usuarios"):
            self.Editar_Usuarios.setGeometry(0, 0, self.width(), self.height())
            self.Editar_Usuarios.raise_()

        x_izquierda = 355
        x_derecha = 1025

        ancho_campo = 555
        alto_campo = 60

        y_id = 436
        y_nombre = 550
        y_correo = 660
        y_contrasena = 775

        y_personaje = 436
        y_vidas = 550
        y_fecha = 660
        y_estado = 773

        self.txt_idjugador.setGeometry(
            int(x_izquierda * escala_x),
            int(y_id * escala_y),
            int(ancho_campo * escala_x),
            int(alto_campo * escala_y)
        )

        self.txt_nombreusuario.setGeometry(
            int(x_izquierda * escala_x),
            int(y_nombre * escala_y),
            int(ancho_campo * escala_x),
            int(alto_campo * escala_y)
        )

        self.txt_correo.setGeometry(
            int(x_izquierda * escala_x),
            int(y_correo * escala_y),
            int(ancho_campo * escala_x),
            int(alto_campo * escala_y)
        )

        self.txt_contrasena.setGeometry(
            int(x_izquierda * escala_x),
            int(y_contrasena * escala_y),
            int(ancho_campo * escala_x),
            int(alto_campo * escala_y)
        )

        self.txt_personaje.setGeometry(
            int(x_derecha * escala_x),
            int(y_personaje * escala_y),
            int(ancho_campo * escala_x),
            int(alto_campo * escala_y)
        )

        self.txt_vidas.setGeometry(
            int(x_derecha * escala_x),
            int(y_vidas * escala_y),
            int(ancho_campo * escala_x),
            int(alto_campo * escala_y)
        )

        self.txt_fecharegistro.setGeometry(
            int(x_derecha * escala_x),
            int(y_fecha * escala_y),
            int(ancho_campo * escala_x),
            int(alto_campo * escala_y)
        )

        self.cmb_estado.setGeometry(
            int(x_derecha * escala_x),
            int(y_estado * escala_y),
            int(ancho_campo * escala_x),
            int(alto_campo * escala_y)
        )

        self.btn_confirmarcambios.setGeometry(
            int(720 * escala_x),
            int(885 * escala_y),
            int(480 * escala_x),
            int(70 * escala_y)
        )

        if hasattr(self, "btn_volver"):
            self.btn_volver.setGeometry(
                int(58 * escala_x),
                int(51 * escala_y),
                int(205 * escala_x),
                int(70 * escala_y)
            )
            self.btn_volver.raise_()

        if hasattr(self, "btn_Volver"):
            self.btn_Volver.setGeometry(
                int(65 * escala_x),
                int(70 * escala_y),
                int(205 * escala_x),
                int(70 * escala_y)
            )
            self.btn_Volver.raise_()

        campos = [
            self.txt_idjugador,
            self.txt_nombreusuario,
            self.txt_correo,
            self.txt_contrasena,
            self.txt_personaje,
            self.txt_vidas,
            self.txt_fecharegistro,
            self.cmb_estado,
            self.btn_confirmarcambios
        ]

        for campo in campos:
            campo.raise_()

    def showEvent(self, event):
        super().showEvent(event)

        QtCore.QTimer.singleShot(0, self.posicionar_elementos)
        QtCore.QTimer.singleShot(100, self.posicionar_elementos)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = EditarUsuario()
    ventana.show()

    sys.exit(app.exec())