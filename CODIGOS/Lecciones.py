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

        if self.pixmap_original.isNull():
            raise FileNotFoundError(
                f"No se pudo cargar el fondo:\n{ruta_imagen}"
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
    Agrega una animación suave de crecimiento,
    elevación, presión y sombra.

    La sombra se dibuja como un rectángulo desenfocado
    detrás del botón. No copia la imagen del botón.
    """

    def __init__(
        self,
        boton,
        factor_hover=1.045,
        factor_presionado=1.018,
        elevacion=3,
        parent=None
    ):
        super().__init__(
            parent if parent is not None else boton
        )

        self.boton = boton
        self.factor_hover = factor_hover
        self.factor_presionado = factor_presionado
        self.elevacion = elevacion

        self.cursor_encima = False
        self.presionado = False

        self.geometria_normal = QtCore.QRect(
            self.boton.geometry()
        )

        parent_boton = self.boton.parentWidget()

        # Rectángulo independiente que produce la sombra.
        # No contiene ninguna copia de la imagen del botón.
        self.capa_sombra = QtWidgets.QFrame(
            parent_boton
        )

        self.capa_sombra.setObjectName(
            f"sombra_{self.boton.objectName()}"
        )

        self.capa_sombra.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

        self.capa_sombra.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_StyledBackground,
            True
        )

        self.capa_sombra.setFocusPolicy(
            QtCore.Qt.FocusPolicy.NoFocus
        )

        # Efecto de desenfoque para suavizar la sombra.
        self.efecto_desenfoque = QtWidgets.QGraphicsBlurEffect(
            self.capa_sombra
        )

        self.efecto_desenfoque.setBlurRadius(
            11
        )

        self.capa_sombra.setGraphicsEffect(
            self.efecto_desenfoque
        )

        self.actualizar_estilo_sombra()

        self.capa_sombra.setGeometry(
            self.obtener_geometria_sombra_normal()
        )

        self.capa_sombra.show()
        self.capa_sombra.stackUnder(
            self.boton
        )

        # Animación de la geometría del botón.
        self.animacion_boton = QtCore.QPropertyAnimation(
            self.boton,
            b"geometry",
            self
        )

        # Animación de la geometría de la sombra.
        self.animacion_sombra = QtCore.QPropertyAnimation(
            self.capa_sombra,
            b"geometry",
            self
        )

        # Animación del desenfoque.
        self.animacion_desenfoque = QtCore.QPropertyAnimation(
            self.efecto_desenfoque,
            b"blurRadius",
            self
        )

        self.grupo_animacion = QtCore.QParallelAnimationGroup(
            self
        )

        self.grupo_animacion.addAnimation(
            self.animacion_boton
        )

        self.grupo_animacion.addAnimation(
            self.animacion_sombra
        )

        self.grupo_animacion.addAnimation(
            self.animacion_desenfoque
        )

        self.boton.installEventFilter(
            self
        )

        self.actualizar_estado_habilitado()

    def actualizar_estilo_sombra(self):
        """
        Cambia la intensidad de la sombra según
        el estado habilitado del botón.
        """

        if self.boton.isEnabled():
            opacidad = 135
        else:
            opacidad = 55

        radio = max(
            6,
            round(self.geometria_normal.height() * 0.06)
        )

        self.capa_sombra.setStyleSheet(
            f"""
            QFrame {{
                background-color: rgba(
                    0,
                    0,
                    0,
                    {opacidad}
                );

                border: none;
                border-radius: {radio}px;
            }}
            """
        )

    def crear_geometria_boton(
        self,
        factor,
        elevacion=0
    ):
        """
        Agranda el botón conservando su centro.
        """

        rectangulo = self.geometria_normal

        ancho_nuevo = max(
            1,
            round(rectangulo.width() * factor)
        )

        alto_nuevo = max(
            1,
            round(rectangulo.height() * factor)
        )

        centro = rectangulo.center()

        x_nuevo = (
            centro.x()
            - ancho_nuevo // 2
        )

        y_nuevo = (
            centro.y()
            - alto_nuevo // 2
            - elevacion
        )

        return QtCore.QRect(
            x_nuevo,
            y_nuevo,
            ancho_nuevo,
            alto_nuevo
        )

    def crear_geometria_sombra(
        self,
        geometria_boton,
        desplazamiento_y,
        reduccion=4
    ):
        """
        Crea una sombra ligeramente más pequeña que
        el botón y desplazada hacia abajo.
        """

        reduccion_real = max(
            1,
            reduccion
        )

        sombra = geometria_boton.adjusted(
            reduccion_real,
            reduccion_real,
            -reduccion_real,
            -reduccion_real
        )

        sombra.translate(
            0,
            desplazamiento_y
        )

        return sombra

    def obtener_geometria_sombra_normal(self):
        return self.crear_geometria_sombra(
            self.geometria_normal,
            desplazamiento_y=5,
            reduccion=4
        )

    def colocar_capas_correctamente(self):
        """
        Mantiene la sombra detrás de su botón.
        """

        self.capa_sombra.raise_()
        self.boton.raise_()

        self.capa_sombra.stackUnder(
            self.boton
        )

    def ejecutar_animacion(
        self,
        geometria_boton,
        geometria_sombra,
        desenfoque,
        duracion,
        curva
    ):
        self.grupo_animacion.stop()

        self.animacion_boton.setDuration(
            duracion
        )

        self.animacion_boton.setEasingCurve(
            curva
        )

        self.animacion_boton.setStartValue(
            self.boton.geometry()
        )

        self.animacion_boton.setEndValue(
            geometria_boton
        )

        self.animacion_sombra.setDuration(
            duracion
        )

        self.animacion_sombra.setEasingCurve(
            curva
        )

        self.animacion_sombra.setStartValue(
            self.capa_sombra.geometry()
        )

        self.animacion_sombra.setEndValue(
            geometria_sombra
        )

        self.animacion_desenfoque.setDuration(
            duracion
        )

        self.animacion_desenfoque.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        self.animacion_desenfoque.setStartValue(
            self.efecto_desenfoque.blurRadius()
        )

        self.animacion_desenfoque.setEndValue(
            desenfoque
        )

        self.colocar_capas_correctamente()

        self.grupo_animacion.start()

    def mostrar_hover(self):
        if not self.boton.isEnabled():
            return

        self.cursor_encima = True
        self.presionado = False

        geometria_hover = self.crear_geometria_boton(
            factor=self.factor_hover,
            elevacion=self.elevacion
        )

        geometria_sombra = self.crear_geometria_sombra(
            geometria_hover,
            desplazamiento_y=8,
            reduccion=4
        )

        self.ejecutar_animacion(
            geometria_boton=geometria_hover,
            geometria_sombra=geometria_sombra,
            desenfoque=19,
            duracion=165,
            curva=QtCore.QEasingCurve.Type.OutCubic
        )

    def mostrar_presionado(self):
        if not self.boton.isEnabled():
            return

        self.presionado = True

        geometria_presionada = self.crear_geometria_boton(
            factor=self.factor_presionado,
            elevacion=0
        )

        geometria_sombra = self.crear_geometria_sombra(
            geometria_presionada,
            desplazamiento_y=3,
            reduccion=4
        )

        self.ejecutar_animacion(
            geometria_boton=geometria_presionada,
            geometria_sombra=geometria_sombra,
            desenfoque=8,
            duracion=75,
            curva=QtCore.QEasingCurve.Type.OutCubic
        )

    def mostrar_normal(self):
        self.cursor_encima = False
        self.presionado = False

        self.ejecutar_animacion(
            geometria_boton=self.geometria_normal,
            geometria_sombra=(
                self.obtener_geometria_sombra_normal()
            ),
            desenfoque=11,
            duracion=140,
            curva=QtCore.QEasingCurve.Type.OutCubic
        )

    def restaurar_despues_de_presionar(self):
        self.presionado = False

        posicion_cursor = self.boton.mapFromGlobal(
            QtGui.QCursor.pos()
        )

        cursor_dentro = self.boton.rect().contains(
            posicion_cursor
        )

        if (
            cursor_dentro
            and self.boton.isEnabled()
        ):
            self.mostrar_hover()
        else:
            self.mostrar_normal()

    def restaurar_inmediatamente(self):
        self.grupo_animacion.stop()

        self.cursor_encima = False
        self.presionado = False

        self.boton.setGeometry(
            self.geometria_normal
        )

        self.capa_sombra.setGeometry(
            self.obtener_geometria_sombra_normal()
        )

        self.efecto_desenfoque.setBlurRadius(
            11 if self.boton.isEnabled() else 7
        )

        self.colocar_capas_correctamente()

    def actualizar_estado_habilitado(self):
        if self.boton.isEnabled():
            self.boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.PointingHandCursor
                )
            )
        else:
            self.boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.ArrowCursor
                )
            )

        self.actualizar_estilo_sombra()
        self.restaurar_inmediatamente()

    def preparar_ajuste_responsivo(self):
        """
        Restaura los controles antes de ejecutar
        BotonesResponsivos.
        """

        self.grupo_animacion.stop()

        self.boton.setGeometry(
            self.geometria_normal
        )

        self.capa_sombra.setGeometry(
            self.obtener_geometria_sombra_normal()
        )

    def actualizar_geometria_base(self):
        """
        Guarda la nueva geometría asignada por
        BotonesResponsivos.
        """

        self.grupo_animacion.stop()

        self.geometria_normal = QtCore.QRect(
            self.boton.geometry()
        )

        self.actualizar_estilo_sombra()

        self.capa_sombra.setGeometry(
            self.obtener_geometria_sombra_normal()
        )

        self.efecto_desenfoque.setBlurRadius(
            11 if self.boton.isEnabled() else 7
        )

        self.colocar_capas_correctamente()

    def eventFilter(self, objeto, evento):
        if objeto is self.boton:
            tipo_evento = evento.type()

            if tipo_evento == QtCore.QEvent.Type.Enter:
                self.mostrar_hover()

            elif tipo_evento == QtCore.QEvent.Type.Leave:
                self.mostrar_normal()

            elif (
                tipo_evento
                == QtCore.QEvent.Type.MouseButtonPress
            ):
                if (
                    evento.button()
                    == QtCore.Qt.MouseButton.LeftButton
                ):
                    self.mostrar_presionado()

            elif (
                tipo_evento
                == QtCore.QEvent.Type.MouseButtonRelease
            ):
                if (
                    evento.button()
                    == QtCore.Qt.MouseButton.LeftButton
                ):
                    self.restaurar_despues_de_presionar()

            elif (
                tipo_evento
                == QtCore.QEvent.Type.EnabledChange
            ):
                self.actualizar_estado_habilitado()

            elif tipo_evento == QtCore.QEvent.Type.Show:
                self.capa_sombra.show()

                QtCore.QTimer.singleShot(
                    0,
                    self.actualizar_geometria_base
                )

            elif tipo_evento == QtCore.QEvent.Type.Hide:
                self.capa_sombra.hide()

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

        uic.loadUi(
            str(ruta_ui),
            self
        )

        self.resize(
            1920,
            1080
        )

        self.setMinimumSize(
            0,
            0
        )

        self.setMaximumSize(
            16777215,
            16777215
        )

        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        self.logo_reutilizable = LogoReutilizable(
            self,
            ruta_logo
        )

        self.lbl_logo.raise_()

        self.botones_lenguaje = [
            self.btnPython,
            self.btnJava,
            self.btnC,
            self.btnMySQL,
        ]

        self.botones_interactivos = [
            self.btnPython,
            self.btnJava,
            self.btnC,
            self.btnMySQL,
            self.btnComenzar,
            self.btn_volver,
        ]

        # Conserva permanentemente un efecto gris
        # para cada botón de lenguaje.
        self.efectos_grises = {}

        self.crear_efectos_grises()

        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=self.botones_interactivos,
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.configurar_botones()

        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor_hover=1.045,
                factor_presionado=1.018,
                elevacion=3,
                parent=self
            )
            for boton in self.botones_interactivos
        ]

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_interfaz
        )

        self.conectar_eventos()

    def crear_efectos_grises(self):
        """
        Crea una sola vez el efecto gris de cada lenguaje.

        Los efectos no se eliminan ni se reemplazan al hacer
        clic, evitando cierres nativos de Qt.
        """

        for boton in self.botones_lenguaje:
            efecto_gris = QtWidgets.QGraphicsColorizeEffect(
                boton
            )

            efecto_gris.setColor(
                QtGui.QColor(
                    115,
                    115,
                    115
                )
            )

            efecto_gris.setStrength(
                1.0
            )

            # El efecto queda colocado una sola vez.
            boton.setGraphicsEffect(
                efecto_gris
            )

            self.efectos_grises[boton] = (
                efecto_gris
            )

    def configurar_botones(self):
        for boton in self.botones_interactivos:
            boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.PointingHandCursor
                )
            )

        for boton in self.botones_lenguaje:
            self.aplicar_escala_grises(
                boton,
                activar=True
            )

        self.btnComenzar.setEnabled(
            False
        )

    def actualizar_hover_botones(self):
        for efecto in getattr(
            self,
            "efectos_hover",
            []
        ):
            efecto.actualizar_geometria_base()

    def preparar_hover_para_resize(self):
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

        # Coloca todos los lenguajes en gris.
        for boton in self.botones_lenguaje:
            self.aplicar_escala_grises(
                boton,
                activar=True
            )

        # Recupera los colores del lenguaje seleccionado.
        boton_seleccionado = botones.get(
            lenguaje
        )

        if boton_seleccionado is not None:
            self.aplicar_escala_grises(
                boton_seleccionado,
                activar=False
            )

        # Habilita Comenzar aventura.
        self.btnComenzar.setEnabled(
            True
        )

        self.btnComenzar.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )

    def limpiar_estilos_lenguajes(self):
        for boton in self.botones_lenguaje:
            self.aplicar_escala_grises(
                boton,
                activar=True
            )

    def aplicar_escala_grises(
            self,
            boton,
            activar=True
    ):
        """
        Activa o desactiva el efecto gris existente.

        No elimina ni reemplaza efectos gráficos,
        evitando que Qt se cierre al hacer clic.
        """

        efecto_gris = self.efectos_grises.get(
            boton
        )

        if efecto_gris is None:
            return

        efecto_gris.setStrength(
            1.0
        )

        efecto_gris.setEnabled(
            activar
        )

        boton.update()

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
                    "El lenguaje seleccionado no es válido.",
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
                    "No se pudo abrir la ventana de niveles."
                    f"\n\nDetalles:\n{error}"
                ),
                "error"
            )

    def crear_ventana_niveles(
        self,
        clase_niveles
    ):
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

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error",
                (
                    "No se pudo volver a la pantalla anterior."
                    f"\n\nDetalles:\n{error}"
                ),
                "error"
            )

    def es_administrador(self):
        if self.jugador is None:
            return False

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

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        if hasattr(self, "Lecciones"):
            self.Lecciones.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )

            self.Lecciones.raise_()

        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        if hasattr(self, "logo_reutilizable"):
            self.logo_reutilizable.actualizar()

        if hasattr(self, "efectos_hover"):
            self.preparar_hover_para_resize()

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        if hasattr(self, "efectos_hover"):
            QtCore.QTimer.singleShot(
                0,
                self.actualizar_hover_botones
            )

        super().resizeEvent(
            event
        )

    def showEvent(self, event):
        super().showEvent(
            event
        )

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_interfaz
        )

        QtCore.QTimer.singleShot(
            100,
            self.actualizar_interfaz
        )

    def actualizar_interfaz(self):
        if hasattr(self, "efectos_hover"):
            self.preparar_hover_para_resize()

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        if hasattr(self, "efectos_hover"):
            self.actualizar_hover_botones()

        if hasattr(self, "lbl_logo"):
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