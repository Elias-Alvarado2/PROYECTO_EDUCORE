import sys
from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui, QtCore

from Alertas import Alertas
from Transicion import FormTransicion, FormAnterior
from AjusteResponsive import BotonesResponsivos
from quitar_barra import quitar
from LogoReutilizable import LogoReutilizable


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

        self.setPixmap(
            self.pixmap_original
        )

        # Mantiene el fondo detrás del frame
        # y de todos los controles.
        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class EfectoHoverBoton(QtCore.QObject):
    """
    Agranda suavemente el botón al pasar el cursor.

    No utiliza QGraphicsDropShadowEffect porque los botones
    de los lenguajes ya utilizan QGraphicsColorizeEffect
    para mostrarse en escala de grises.
    """

    def __init__(
        self,
        boton,
        factor=1.04,
        duracion=120,
        parent=None
    ):
        super().__init__(
            parent if parent is not None else boton
        )

        self.boton = boton
        self.factor = factor
        self.duracion = duracion
        self.cursor_encima = False

        # Guarda la posición y el tamaño normales.
        self.geometria_normal = QtCore.QRect(
            boton.geometry()
        )

        # Animación del tamaño y posición.
        self.animacion = QtCore.QPropertyAnimation(
            boton,
            b"geometry",
            self
        )

        self.animacion.setDuration(
            self.duracion
        )

        self.animacion.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        self.boton.installEventFilter(
            self
        )

    def obtener_geometria_grande(self):
        """
        Calcula una geometría más grande manteniendo
        el botón centrado.
        """

        rectangulo = self.geometria_normal

        ancho_nuevo = round(
            rectangulo.width() * self.factor
        )

        alto_nuevo = round(
            rectangulo.height() * self.factor
        )

        diferencia_ancho = (
            ancho_nuevo - rectangulo.width()
        )

        diferencia_alto = (
            alto_nuevo - rectangulo.height()
        )

        return QtCore.QRect(
            rectangulo.x() - diferencia_ancho // 2,
            rectangulo.y() - diferencia_alto // 2,
            ancho_nuevo,
            alto_nuevo
        )

    def animar_hacia(self, geometria_destino):
        """
        Ejecuta la animación desde el tamaño actual
        hasta la geometría indicada.
        """

        self.animacion.stop()

        self.animacion.setStartValue(
            self.boton.geometry()
        )

        self.animacion.setEndValue(
            geometria_destino
        )

        self.animacion.start()

    def preparar_ajuste_responsivo(self):
        """
        Detiene la animación antes de que
        BotonesResponsivos cambie la geometría.
        """

        self.animacion.stop()

        if self.cursor_encima:
            self.boton.setGeometry(
                self.geometria_normal
            )

    def actualizar_geometria_base(self):
        """
        Guarda la posición y tamaño establecidos
        por BotonesResponsivos.
        """

        self.animacion.stop()

        self.geometria_normal = QtCore.QRect(
            self.boton.geometry()
        )

        if (
            self.cursor_encima
            and self.boton.isEnabled()
        ):
            self.boton.setGeometry(
                self.obtener_geometria_grande()
            )

    def restaurar_inmediatamente(self):
        """
        Devuelve el botón a su tamaño normal sin animación.
        Se utiliza cuando el botón queda deshabilitado.
        """

        self.cursor_encima = False
        self.animacion.stop()

        self.boton.setGeometry(
            self.geometria_normal
        )

    def eventFilter(self, objeto, evento):
        if objeto is self.boton:

            if (
                evento.type()
                == QtCore.QEvent.Type.Enter
                and self.boton.isEnabled()
            ):
                self.cursor_encima = True

                # Coloca el botón por encima de los demás.
                self.boton.raise_()

                self.animar_hacia(
                    self.obtener_geometria_grande()
                )

            elif (
                evento.type()
                == QtCore.QEvent.Type.Leave
            ):
                if self.cursor_encima:
                    self.cursor_encima = False

                    self.animar_hacia(
                        self.geometria_normal
                    )

            elif (
                evento.type()
                == QtCore.QEvent.Type.EnabledChange
            ):
                if not self.boton.isEnabled():
                    self.restaurar_inmediatamente()

        return super().eventFilter(
            objeto,
            evento
        )


class Lecciones(QtWidgets.QWidget):
    def __init__(
        self,
        jugador=None,
        ventana_anterior=None
    ):
        super().__init__()

        quitar(self)

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

        ruta_logo = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "Logo"
            / "logo_confondo.png"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        if not ruta_logo.exists():
            raise FileNotFoundError(
                f"No se encontró el logo:\n{ruta_logo}"
            )

        # Carga el formulario creado en Qt Designer.
        uic.loadUi(
            str(ruta_ui),
            self
        )

        # Resolución base del diseño.
        self.resize(
            1920,
            1080
        )

        # Permite maximizar y adaptar la ventana.
        self.setMinimumSize(
            0,
            0
        )

        self.setMaximumSize(
            16777215,
            16777215
        )

        # Fondo adaptable.
        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        # Logo adaptable.
        self.logo_reutilizable = LogoReutilizable(
            self,
            ruta_logo
        )

        self.lbl_logo.raise_()

        # Botones de selección de lenguaje.
        self.botones_lenguaje = [
            self.btnPython,
            self.btnJava,
            self.btnC,
            self.btnMySQL,
        ]

        # Todos los botones que tendrán efecto hover.
        self.botones_interactivos = [
            self.btnPython,
            self.btnJava,
            self.btnC,
            self.btnMySQL,
            self.btnComenzar,
            self.btn_volver,
        ]

        # Hace responsivos todos los botones.
        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=self.botones_interactivos,
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.configurar_botones()

        # Crea el efecto hover para todos los botones.
        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor=1.04,
                duracion=120,
                parent=self
            )
            for boton in self.botones_interactivos
        ]

        # Espera a que Qt termine de colocar los controles
        # antes de guardar sus posiciones originales.
        QtCore.QTimer.singleShot(
            0,
            self.actualizar_hover_botones
        )

        self.conectar_eventos()

    def configurar_botones(self):
        """
        Configura el cursor, la escala de grises inicial
        y el estado del botón Comenzar.
        """

        for boton in self.botones_interactivos:
            boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.PointingHandCursor
                )
            )

        # Todos los lenguajes comienzan en gris.
        for boton in self.botones_lenguaje:
            self.aplicar_escala_grises(
                boton,
                activar=True
            )

        # No se puede comenzar hasta seleccionar
        # un lenguaje.
        self.btnComenzar.setEnabled(
            False
        )

    def actualizar_hover_botones(self):
        """
        Actualiza las posiciones normales utilizadas
        por las animaciones.
        """

        for efecto in getattr(
            self,
            "efectos_hover",
            []
        ):
            efecto.actualizar_geometria_base()

    def preparar_hover_para_resize(self):
        """
        Restaura temporalmente los botones antes
        de aplicar el ajuste responsivo.
        """

        for efecto in getattr(
            self,
            "efectos_hover",
            []
        ):
            efecto.preparar_ajuste_responsivo()

    def conectar_eventos(self):
        self.btnPython.clicked.connect(
            lambda: self.seleccionar_lenguaje(
                "Python"
            )
        )

        self.btnJava.clicked.connect(
            lambda: self.seleccionar_lenguaje(
                "Java"
            )
        )

        self.btnC.clicked.connect(
            lambda: self.seleccionar_lenguaje(
                "C"
            )
        )

        self.btnMySQL.clicked.connect(
            lambda: self.seleccionar_lenguaje(
                "MySQL"
            )
        )

        self.btnComenzar.clicked.connect(
            self.comenzar_aventura
        )

        self.btn_volver.clicked.connect(
            self.volver_pantalla_anterior
        )

    def seleccionar_lenguaje(self, lenguaje):
        self.lenguaje_seleccionado = lenguaje

        botones = {
            "Python": self.btnPython,
            "Java": self.btnJava,
            "C": self.btnC,
            "MySQL": self.btnMySQL,
        }

        # Coloca nuevamente todos los botones en gris.
        self.limpiar_estilos_lenguajes()

        # Recupera el color del lenguaje seleccionado.
        boton_seleccionado = botones.get(
            lenguaje
        )

        if boton_seleccionado is not None:
            self.aplicar_escala_grises(
                boton_seleccionado,
                activar=False
            )

        # Habilita el botón Comenzar.
        self.btnComenzar.setEnabled(
            True
        )

    def limpiar_estilos_lenguajes(self):
        """
        Coloca todos los botones de lenguajes
        nuevamente en escala de grises.
        """

        for boton in self.botones_lenguaje:
            self.aplicar_escala_grises(
                boton,
                activar=True
            )

    def comenzar_aventura(self):
        if self.lenguaje_seleccionado is None:
            Alertas.mostrar(
                self,
                "Selecciona un lenguaje",
                (
                    "Debes seleccionar un lenguaje antes "
                    "de comenzar la aventura."
                ),
                "advertencia"
            )
            return

        try:
            if self.lenguaje_seleccionado == "Python":
                from NivelesPython import NivelesPython

                self.ventana_niveles = (
                    self.crear_ventana_niveles(
                        NivelesPython
                    )
                )

            elif self.lenguaje_seleccionado == "Java":
                from NivelesJava import NivelesJava

                self.ventana_niveles = (
                    self.crear_ventana_niveles(
                        NivelesJava
                    )
                )

            elif self.lenguaje_seleccionado == "C":
                from NivelesC import NivelesC

                self.ventana_niveles = (
                    self.crear_ventana_niveles(
                        NivelesC
                    )
                )

            elif self.lenguaje_seleccionado == "MySQL":
                from NivelesMySQL import NivelesMySQL

                self.ventana_niveles = (
                    self.crear_ventana_niveles(
                        NivelesMySQL
                    )
                )

            else:
                Alertas.mostrar(
                    self,
                    "Lenguaje no válido",
                    (
                        "El lenguaje seleccionado "
                        "no es válido."
                    ),
                    "advertencia"
                )
                return

            FormTransicion(
                self,
                self.ventana_niveles
            )

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error al abrir niveles",
                (
                    "No se pudo abrir la ventana "
                    "de niveles."
                    f"\n\nDetalles:\n{error}"
                ),
                "error"
            )

    def crear_ventana_niveles(
        self,
        clase_niveles
    ):
        """
        Intenta crear la ventana enviando el jugador
        y esta ventana como ventana anterior.
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

            # Primero utiliza el historial universal.
            if (
                hasattr(app, "historial_forms")
                and len(app.historial_forms) > 0
            ):
                FormAnterior(
                    self
                )
                return

            # Si se recibió una ventana anterior,
            # regresa directamente a ella.
            if self.ventana_anterior is not None:
                FormTransicion(
                    self,
                    self.ventana_anterior,
                    guardar_actual=False
                )
                return

            # Si no existe historial ni ventana anterior,
            # determina el menú correspondiente.
            if self.es_administrador():
                from MenuAdministrador import MenuAdministrador

                try:
                    self.ventana_menu = MenuAdministrador(
                        self.jugador
                    )

                except TypeError:
                    self.ventana_menu = (
                        MenuAdministrador()
                    )

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

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error",
                (
                    "No se pudo volver a la pantalla "
                    "anterior."
                    f"\n\nDetalles:\n{error}"
                ),
                "error"
            )

    def es_administrador(self):
        """
        Determina si la información recibida
        corresponde a un administrador.
        """

        if self.jugador is None:
            return False

        # Cuando los datos vienen como diccionario.
        if isinstance(
            self.jugador,
            dict
        ):
            rol = str(
                self.jugador.get(
                    "rol",
                    ""
                )
            ).lower()

            if rol == "administrador":
                return True

            if "id_admin" in self.jugador:
                return True

            if (
                "usuario" in self.jugador
                and "id_jugador" not in self.jugador
            ):
                return True

            return False

        # Cuando los datos vienen como objeto.
        if hasattr(
            self.jugador,
            "id_admin"
        ):
            return True

        if (
            hasattr(
                self.jugador,
                "usuario"
            )
            and not hasattr(
                self.jugador,
                "id_jugador"
            )
        ):
            return True

        return False

    def volver_menu_administrador(self):
        """
        Método conservado por compatibilidad con otras
        partes del proyecto que puedan llamarlo.
        """

        try:
            app = QtWidgets.QApplication.instance()

            if (
                hasattr(app, "historial_forms")
                and len(app.historial_forms) > 0
            ):
                FormAnterior(
                    self
                )
                return

            if self.ventana_anterior is not None:
                FormTransicion(
                    self,
                    self.ventana_anterior,
                    guardar_actual=False
                )
                return

            from MenuAdministrador import MenuAdministrador

            try:
                self.ventana_menu = MenuAdministrador(
                    self.jugador
                )

            except TypeError:
                self.ventana_menu = MenuAdministrador()

            FormTransicion(
                self,
                self.ventana_menu,
                guardar_actual=False
            )

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error",
                (
                    "No se pudo volver al Menú "
                    "Administrador."
                    f"\n\nDetalles:\n{error}"
                ),
                "error"
            )

    def aplicar_escala_grises(
        self,
        boton,
        activar=True
    ):
        """
        Coloca el botón en escala de grises o recupera
        sus colores originales.
        """

        if activar:
            efecto_gris = (
                QtWidgets.QGraphicsColorizeEffect(
                    boton
                )
            )

            efecto_gris.setColor(
                QtGui.QColor(
                    115,
                    115,
                    115
                )
            )

            # 1.0 significa completamente gris.
            efecto_gris.setStrength(
                1.0
            )

            boton.setGraphicsEffect(
                efecto_gris
            )

        else:
            # Quita el efecto y recupera
            # la imagen con sus colores.
            boton.setGraphicsEffect(
                None
            )

    def resizeEvent(self, event):
        """
        Ajusta el fondo, frame, logo, botones responsivos
        y geometrías utilizadas por el efecto hover.
        """

        # Ajusta el fondo.
        if hasattr(
            self,
            "fondo"
        ):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        # El frame principal ocupa toda la ventana.
        if hasattr(
            self,
            "Lecciones"
        ):
            self.Lecciones.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )

            self.Lecciones.raise_()

        # Mantiene el logo por encima del fondo y el frame.
        if hasattr(
            self,
            "lbl_logo"
        ):
            self.lbl_logo.raise_()

        if hasattr(
            self,
            "logo_reutilizable"
        ):
            self.logo_reutilizable.actualizar()

        # Restaura temporalmente los botones antes
        # de aplicar las nuevas posiciones responsivas.
        if hasattr(
            self,
            "efectos_hover"
        ):
            self.preparar_hover_para_resize()

        # Ajusta los botones a la resolución actual.
        if hasattr(
            self,
            "botones_responsivos"
        ):
            self.botones_responsivos.ajustar()

        # Guarda las nuevas posiciones normales.
        if hasattr(
            self,
            "efectos_hover"
        ):
            self.actualizar_hover_botones()

        super().resizeEvent(
            event
        )

    def showEvent(self, event):
        """
        Actualiza la interfaz cuando se muestra
        la ventana.
        """

        super().showEvent(
            event
        )

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_interfaz
        )

    def actualizar_interfaz(self):
        """
        Realiza un ajuste final después de que
        la ventana termina de mostrarse.
        """

        if hasattr(
            self,
            "efectos_hover"
        ):
            self.preparar_hover_para_resize()

        if hasattr(
            self,
            "botones_responsivos"
        ):
            self.botones_responsivos.ajustar()

        if hasattr(
            self,
            "efectos_hover"
        ):
            self.actualizar_hover_botones()

        if hasattr(
            self,
            "lbl_logo"
        ):
            self.lbl_logo.raise_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(
        sys.argv
    )

    ventana = Lecciones()

    ventana.showMaximized()

    sys.exit(
        app.exec()
    )