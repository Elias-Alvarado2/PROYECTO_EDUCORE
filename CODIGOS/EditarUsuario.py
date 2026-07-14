import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from Alertas import Alertas
from ConexionBD import ConexionBD
from Transicion import FormTransicion, FormAnterior
from AjusteResponsive import ElementosResponsivos
from quitar_barra import quitar

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
        quitar(self)

        self.ventana_anterior = ventana_anterior

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = (PROYECTO_DIR/ "EXPO-DISEÑOS"/ "DESIGNER"/ "Editar-Usuarios.ui"
        )

        ruta_imagen = (PROYECTO_DIR/ "assets"/ "DISEÑOS"/ "Editar_Usuarios.png"
        )

        ruta_botones = (
                PROYECTO_DIR
                / "EXPO-DISEÑOS"
                / "Botones"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        if not ruta_botones.exists():
            raise FileNotFoundError(
                f"No se encontró la carpeta de botones:\n{ruta_botones}"
            )

        # Cargar el formulario de Designer.
        uic.loadUi(str(ruta_ui), self)

        # Corrige las rutas ../Botones/ de los StyleSheet.
        self.corregir_rutas_stylesheet(ruta_botones)

        ruta_fuente = (
                PROYECTO_DIR
                / "assets"
                / "FUENTES"
                / "PixelOperator.ttf"
        )

        self.cargar_fuente_personalizada(ruta_fuente)

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

        self.configurar_botones()
        self.configurar_campos()
        self.conectar_eventos()

    def corregir_rutas_stylesheet(self, ruta_botones):
        """
        Conserva los StyleSheet creados en Qt Designer,
        cambiando ../Botones/ por la ruta absoluta.
        """

        ruta_absoluta = ruta_botones.resolve().as_posix()

        controles = [
            self,
            *self.findChildren(QtWidgets.QWidget),
        ]

        for control in controles:
            estilo_original = control.styleSheet()

            if not estilo_original:
                continue

            estilo_corregido = estilo_original

            # url("../Botones/...")
            estilo_corregido = estilo_corregido.replace(
                'url("../Botones/',
                f'url("{ruta_absoluta}/'
            )

            # url('../Botones/...')
            estilo_corregido = estilo_corregido.replace(
                "url('../Botones/",
                f"url('{ruta_absoluta}/"
            )

            # url(../Botones/...)
            estilo_corregido = estilo_corregido.replace(
                "url(../Botones/",
                f"url({ruta_absoluta}/"
            )

            if estilo_corregido != estilo_original:
                control.setStyleSheet(estilo_corregido)

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )
            self.fondo.lower()

        if hasattr(self, "elementos_responsivos"):
            self.elementos_responsivos.ajustar()

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

        # No mostrar ninguna opción al abrir la ventana.
        self.cmb_estado.setCurrentIndex(-1)
        self.cmb_estado.setEnabled(False)

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
        # Oculta el estado anterior mientras busca el nuevo ID.
        self.cmb_estado.setCurrentIndex(-1)
        self.cmb_estado.setEnabled(False)

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
            Alertas.mostrar(
                self,
                "Error de base de datos",
                str(e),
                "error"
            )

    def buscar_usuario(self):
        id_jugador = self.txt_idjugador.text().strip()

        if id_jugador == "":
            self.jugador_actual = None
            self.ultimo_id_buscado = ""
            self.limpiar_datos_usuario()

            Alertas.mostrar(
                self,
                "ID vacío",
                "Debes ingresar el ID del jugador.",
                "advertencia"
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

                Alertas.mostrar(
                    self,
                    "Usuario no encontrado",
                    f"No existe un jugador con ID {id_jugador}.",
                    "advertencia"
                )
                return

            self.jugador_actual = jugador
            self.ultimo_id_buscado = id_jugador

            self.mostrar_datos_usuario(jugador)

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error de base de datos",
                str(e),
                "error"
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

        estado = str(jugador["estado"]).strip()

        index_estado = self.cmb_estado.findText(
            estado,
            QtCore.Qt.MatchFlag.MatchFixedString
        )

        if index_estado >= 0:
            self.cmb_estado.setCurrentIndex(index_estado)
        else:
            self.cmb_estado.setCurrentIndex(-1)

        # Habilitar únicamente cuando el usuario existe.
        self.cmb_estado.setEnabled(True)

    def limpiar_datos_usuario(self):
        self.txt_nombreusuario.clear()
        self.txt_correo.clear()
        self.txt_contrasena.clear()
        self.txt_personaje.clear()
        self.txt_vidas.clear()
        self.txt_fecharegistro.clear()

        # No mostrar Activo ni Inactivo.
        self.cmb_estado.setCurrentIndex(-1)
        self.cmb_estado.setEnabled(False)

    def validar_campos(self):
        id_jugador = self.txt_idjugador.text().strip()
        nombre = self.txt_nombreusuario.text().strip()
        correo = self.txt_correo.text().strip()
        contrasena = self.txt_contrasena.text().strip()
        personaje = self.txt_personaje.text().strip()
        vidas = self.txt_vidas.text().strip()
        estado = self.cmb_estado.currentText().strip()

        if id_jugador == "":
            Alertas.mostrar(
                self,
                "ID vacío",
                "Debes ingresar el ID del jugador.",
                "advertencia"
            )
            return None

        if nombre == "":
            Alertas.mostrar(
                self,
                "Nombre vacío",
                "El nombre del usuario no puede estar vacío.",
                "advertencia"
            )
            return None

        if correo == "":
            Alertas.mostrar(
                self,
                "Correo vacío",
                "El correo no puede estar vacío.",
                "advertencia"
            )
            return None

        if contrasena == "":
            Alertas.mostrar(
                self,
                "Contraseña vacía",
                "La contraseña no puede estar vacía.",
                "advertencia"
            )
            return None

        if contrasena == "":
            Alertas.mostrar(
                self,
                "Contraseña vacía",
                "La contraseña no puede estar vacía.",
                "advertencia"
            )
            return None

        if personaje == "":
            Alertas.mostrar(
                self,
                "Personaje vacío",
                "El personaje no puede estar vacío.",
                "advertencia"
            )
            return None

        if vidas == "":
            Alertas.mostrar(
                self,
                "Vidas vacías",
                "Las vidas no pueden estar vacías.",
                "advertencia"
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

        respuesta = Alertas.confirmar(
            self,
            "Confirmar cambios",
            f"¿Seguro que deseas actualizar este jugador?\n\n"
            f"ID: {datos['id_jugador']}\n"
            f"Nombre: {datos['nombre']}\n"
            f"Correo: {datos['correo']}",
            tipo="error",
            texto_confirmar="SÍ, ACTUALIZAR",
            texto_cancelar="CANCELAR"
        )

        if not respuesta:
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
                Alertas.mostrar(
                    self,
                    "Usuario actualizado",
                    "Los datos del jugador fueron "
                    "actualizados correctamente.",
                    "informacion"
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
                Alertas.mostrar(
                    self,
                    "Sin cambios",
                    "No se realizaron cambios "
                    "en el jugador.",
                    "informacion"
                )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error de base de datos",
                str(e),
                "error"
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
            Alertas.mostrar(
                self,
                "Error",
                "No se pudo abrir Gestión de Usuarios."
                f"\n\nDetalles:\n{e}",
                "error"
            )

    def cargar_fuente_personalizada(self, ruta_fuente):
        if not ruta_fuente.exists():
            print(f"No se encontró la fuente:\n{ruta_fuente}")
            return

        id_fuente = QtGui.QFontDatabase.addApplicationFont(
            str(ruta_fuente)
        )

        if id_fuente == -1:
            print("No se pudo cargar la fuente PixelOperator.")
            return

        familias = QtGui.QFontDatabase.applicationFontFamilies(
            id_fuente
        )

        if not familias:
            print("La fuente no contiene una familia válida.")
            return

        nombre_fuente = familias[0]

        # Fuente para el campo donde se escribe el ID.
        fuente_id = QtGui.QFont(
            nombre_fuente,
            22
        )
        fuente_id.setBold(False)

        # Fuente para los datos del jugador.
        fuente_datos = QtGui.QFont(
            nombre_fuente,
            20
        )
        fuente_datos.setBold(False)

        # Fuente para el ComboBox.
        fuente_combo = QtGui.QFont(
            nombre_fuente,
            20
        )
        fuente_combo.setBold(False)

        self.txt_idjugador.setFont(fuente_id)

        campos_datos = [
            self.txt_nombreusuario,
            self.txt_correo,
            self.txt_contrasena,
            self.txt_personaje,
            self.txt_vidas,
            self.txt_fecharegistro,
        ]

        for campo in campos_datos:
            campo.setFont(fuente_datos)

        self.cmb_estado.setFont(fuente_combo)

        # También cambia la fuente de las opciones desplegables.
        self.cmb_estado.view().setFont(fuente_combo)

    def configurar_botones(self):
        botones = [
            self.btn_confirmarcambios,
            self.btn_volver,
        ]

        for boton in botones:
            boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.PointingHandCursor
                )
            )

            # No usar setStyleSheet aquí.
            # Se mantiene la imagen configurada en Designer.


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = EditarUsuario()

    ventana.showMaximized()

    sys.exit(app.exec())