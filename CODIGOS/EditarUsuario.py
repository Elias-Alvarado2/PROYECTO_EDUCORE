import sys
from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui, QtCore

from ConexionBD import ConexionBD
from Transicion import FormTransicion, FormAnterior
from AjusteResponsive import ElementosResponsivos


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

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class EditarUsuario(QtWidgets.QWidget):
    def __init__(self, ventana_anterior=None):
        super().__init__()

        self.ventana_anterior = ventana_anterior

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "Editar-Usuarios.ui"
        )

        ruta_imagen = (
            PROYECTO_DIR
            / "assets"
            / "DISEÑOS"
            / "Editar_Usuarios.png"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        # Cargar el formulario de Designer.
        uic.loadUi(str(ruta_ui), self)

        # Resolución original del diseño.
        self.resize(1920, 1080)

        # Permite adaptar la ventana a otras resoluciones.
        self.setMinimumSize(0, 0)
        self.setMaximumSize(
            16777215,
            16777215
        )

        # Fondo adaptable.
        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        # Ajuste automático del frame, botones, campos y ComboBox.
        self.elementos_responsivos = ElementosResponsivos(
            ventana=self,
            elementos=[
                # Frame principal
                self.Editar_Usuarios,

                # Botones
                self.btn_confirmarcambios,
                self.btn_volver,

                # Campos
                self.txt_idjugador,
                self.txt_nombreusuario,
                self.txt_correo,
                self.txt_contrasena,
                self.txt_personaje,
                self.txt_vidas,
                self.txt_fecharegistro,

                # ComboBox
                self.cmb_estado,
            ],
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.db = ConexionBD()

        self.jugador_actual = None
        self.ultimo_id_buscado = ""

        self.timer_busqueda_id = QtCore.QTimer(self)
        self.timer_busqueda_id.setSingleShot(True)
        self.timer_busqueda_id.timeout.connect(
            self.buscar_usuario_automatico
        )

        self.configurar_campos()
        self.conectar_eventos()

    def resizeEvent(self, event):
        # Solo el fondo se controla aquí.
        # Los demás elementos los controla ElementosResponsivos.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )
            self.fondo.lower()

        super().resizeEvent(event)

    def configurar_campos(self):
        self.txt_idjugador.setValidator(
            QtGui.QIntValidator(1, 999999)
        )

        self.txt_vidas.setValidator(
            QtGui.QIntValidator(0, 999)
        )

        self.txt_fecharegistro.setReadOnly(True)

        self.cmb_estado.clear()
        self.cmb_estado.addItems([
            "Activo",
            "Inactivo"
        ])

    def conectar_eventos(self):
        self.txt_idjugador.textChanged.connect(
            self.iniciar_busqueda_automatica
        )

        self.txt_idjugador.returnPressed.connect(
            self.buscar_usuario
        )

        self.btn_confirmarcambios.clicked.connect(
            self.confirmar_cambios
        )

        self.btn_volver.clicked.connect(
            self.volver_gestion_usuario
        )

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
            jugador = self.db.buscar_jugador_por_id(
                id_jugador
            )

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
            jugador = self.db.buscar_jugador_por_id(
                id_jugador
            )

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
        self.txt_nombreusuario.setText(
            str(jugador["nombre"])
        )

        self.txt_correo.setText(
            str(jugador["correo"])
        )

        self.txt_contrasena.setText(
            str(jugador["contrasena"])
        )

        self.txt_personaje.setText(
            str(jugador["personaje"])
        )

        self.txt_vidas.setText(
            str(jugador["vidas"])
        )

        self.txt_fecharegistro.setText(
            str(jugador["fecha_registro"])
        )

        estado = str(jugador["estado"])

        index_estado = self.cmb_estado.findText(
            estado
        )

        if index_estado >= 0:
            self.cmb_estado.setCurrentIndex(
                index_estado
            )
        else:
            self.cmb_estado.setCurrentIndex(0)

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
            "estado": estado,
        }

    def confirmar_cambios(self):
        datos = self.validar_campos()

        if datos is None:
            return

        if self.jugador_actual is None:
            self.buscar_usuario()

            if self.jugador_actual is None:
                return

        if (
            str(self.jugador_actual["id_jugador"])
            != str(datos["id_jugador"])
        ):
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
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No
        )

        if (
            respuesta
            != QtWidgets.QMessageBox.StandardButton.Yes
        ):
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
                    "Los datos del jugador fueron "
                    "actualizados correctamente."
                )

                jugador_actualizado = (
                    self.db.buscar_jugador_por_id(
                        datos["id_jugador"]
                    )
                )

                if jugador_actualizado:
                    self.jugador_actual = (
                        jugador_actualizado
                    )

                    self.ultimo_id_buscado = str(
                        jugador_actualizado[
                            "id_jugador"
                        ]
                    )

                    self.mostrar_datos_usuario(
                        jugador_actualizado
                    )

            else:
                QtWidgets.QMessageBox.information(
                    self,
                    "Sin cambios",
                    "No se realizaron cambios "
                    "en el jugador."
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
                "No se pudo abrir Gestión de Usuarios."
                f"\n\nDetalles:\n{e}"
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = EditarUsuario()

    ventana.showMaximized()

    sys.exit(app.exec())