import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from quitar_barra import quitar
from Transicion import FormTransicion
from AjusteResponsive import BotonesResponsivos, ElementosResponsivos

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

ANCHO_BASE = 1366
ALTO_BASE = 768

VELOCIDAD_ANIMACION = 120  # Milisegundos entre cada frame


# ==========================================================
# FONDO RESPONSIVO
# ==========================================================

class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.pixmap_original = QtGui.QPixmap(
            str(ruta_imagen)
        )

        if self.pixmap_original.isNull():
            raise FileNotFoundError(
                f"No se pudo cargar el fondo:\n{ruta_imagen}"
            )

        self.setPixmap(self.pixmap_original)
        self.setScaledContents(True)

        self.setGeometry(
            0,
            0,
            ventana.width(),
            ventana.height()
        )

        # El fondo no debe bloquear los clics.
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


# ==========================================================
# CREAR UNA VERSIÓN APAGADA DEL PERSONAJE
# ==========================================================

def crear_pixmap_apagado(pixmap):
    """
    Convierte el personaje a escala de grises y reduce
    su opacidad, conservando el fondo transparente.
    """

    imagen = pixmap.toImage().convertToFormat(
        QtGui.QImage.Format.Format_ARGB32
    )

    for y in range(imagen.height()):
        for x in range(imagen.width()):
            color = imagen.pixelColor(x, y)

            if color.alpha() == 0:
                continue

            gris = round(
                color.red() * 0.299
                + color.green() * 0.587
                + color.blue() * 0.114
            )

            # Oscurecer un poco el personaje.
            gris = round(gris * 0.55)

            color_apagado = QtGui.QColor(
                gris,
                gris,
                gris,
                round(color.alpha() * 0.75)
            )

            imagen.setPixelColor(
                x,
                y,
                color_apagado
            )

    return QtGui.QPixmap.fromImage(imagen)


# ==========================================================
# PERSONAJE PEQUEÑO SELECCIONABLE
# ==========================================================

class TarjetaPersonaje(QtWidgets.QLabel):
    seleccionado = QtCore.pyqtSignal(str)

    def __init__(
            self,
            nombre,
            pixmap_personaje,
            parent=None
    ):
        super().__init__(parent)

        self.nombre = nombre

        # Imagen original.
        self.pixmap_original = pixmap_personaje

        # Imagen apagada.
        self.pixmap_apagado = crear_pixmap_apagado(
            pixmap_personaje
        )

        self.esta_seleccionado = False

        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )

        self.setStyleSheet(
            """
            QLabel {
                background: transparent;
                border: none;
            }
            """
        )

        # Inicialmente aparece apagado.
        self.marcar_seleccionado(False)

    def marcar_seleccionado(self, seleccionado):
        self.esta_seleccionado = seleccionado
        self.actualizar_imagen()

    def actualizar_imagen(self):
        if self.width() <= 0 or self.height() <= 0:
            return

        if self.esta_seleccionado:
            pixmap = self.pixmap_original
        else:
            pixmap = self.pixmap_apagado

        ancho_disponible = max(
            1,
            self.width() - 18
        )

        alto_disponible = max(
            1,
            self.height() - 18
        )

        pixmap_escalado = pixmap.scaled(
            ancho_disponible,
            alto_disponible,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.FastTransformation
        )

        self.setPixmap(pixmap_escalado)

    def mousePressEvent(self, evento):
        if (
                evento.button()
                == QtCore.Qt.MouseButton.LeftButton
        ):
            self.seleccionado.emit(self.nombre)

        super().mousePressEvent(evento)

    def resizeEvent(self, evento):
        self.actualizar_imagen()
        super().resizeEvent(evento)


# ==========================================================
# EFECTO HOVER PARA VOLVER Y CONFIRMAR
# ==========================================================

class EfectoHoverBoton(QtCore.QObject):
    """
    Agrega crecimiento, elevación, presión y sombra suave.

    Se aplicará únicamente a los botones Volver y Confirmar.
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

        self.geometria_normal = QtCore.QRect(
            self.boton.geometry()
        )

        parent_boton = self.boton.parentWidget()

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

        self.efecto_desenfoque = QtWidgets.QGraphicsBlurEffect(
            self.capa_sombra
        )

        self.efecto_desenfoque.setBlurRadius(11)

        self.capa_sombra.setGraphicsEffect(
            self.efecto_desenfoque
        )

        self.actualizar_estilo_sombra()

        self.capa_sombra.setGeometry(
            self.obtener_geometria_sombra_normal()
        )

        self.capa_sombra.show()
        self.capa_sombra.stackUnder(self.boton)

        self.animacion_boton = QtCore.QPropertyAnimation(
            self.boton,
            b"geometry",
            self
        )

        self.animacion_sombra = QtCore.QPropertyAnimation(
            self.capa_sombra,
            b"geometry",
            self
        )

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

        self.boton.installEventFilter(self)
        self.actualizar_estado_habilitado()

    def actualizar_estilo_sombra(self):
        opacidad = 135 if self.boton.isEnabled() else 55

        radio = max(
            6,
            round(self.geometria_normal.height() * 0.06)
        )

        self.capa_sombra.setStyleSheet(
            f"""
            QFrame {{
                background-color: rgba(0, 0, 0, {opacidad});
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

        return QtCore.QRect(
            centro.x() - ancho_nuevo // 2,
            centro.y() - alto_nuevo // 2 - elevacion,
            ancho_nuevo,
            alto_nuevo
        )

    def crear_geometria_sombra(
            self,
            geometria_boton,
            desplazamiento_y,
            reduccion=4
    ):
        reduccion_real = max(1, reduccion)

        sombra = geometria_boton.adjusted(
            reduccion_real,
            reduccion_real,
            -reduccion_real,
            -reduccion_real
        )

        sombra.translate(0, desplazamiento_y)
        return sombra

    def obtener_geometria_sombra_normal(self):
        return self.crear_geometria_sombra(
            self.geometria_normal,
            desplazamiento_y=5,
            reduccion=4
        )

    def colocar_capas_correctamente(self):
        self.capa_sombra.raise_()
        self.boton.raise_()
        self.capa_sombra.stackUnder(self.boton)

    def ejecutar_animacion(
            self,
            geometria_boton,
            geometria_sombra,
            desenfoque,
            duracion,
            curva
    ):
        self.grupo_animacion.stop()

        self.animacion_boton.setDuration(duracion)
        self.animacion_boton.setEasingCurve(curva)
        self.animacion_boton.setStartValue(
            self.boton.geometry()
        )
        self.animacion_boton.setEndValue(
            geometria_boton
        )

        self.animacion_sombra.setDuration(duracion)
        self.animacion_sombra.setEasingCurve(curva)
        self.animacion_sombra.setStartValue(
            self.capa_sombra.geometry()
        )
        self.animacion_sombra.setEndValue(
            geometria_sombra
        )

        self.animacion_desenfoque.setDuration(duracion)
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
        posicion_cursor = self.boton.mapFromGlobal(
            QtGui.QCursor.pos()
        )

        cursor_dentro = self.boton.rect().contains(
            posicion_cursor
        )

        if cursor_dentro and self.boton.isEnabled():
            self.mostrar_hover()
        else:
            self.mostrar_normal()

    def restaurar_inmediatamente(self):
        self.grupo_animacion.stop()

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
        cursor = (
            QtCore.Qt.CursorShape.PointingHandCursor
            if self.boton.isEnabled()
            else QtCore.Qt.CursorShape.ArrowCursor
        )

        self.boton.setCursor(
            QtGui.QCursor(cursor)
        )

        self.actualizar_estilo_sombra()
        self.restaurar_inmediatamente()

    def preparar_ajuste_responsivo(self):
        self.grupo_animacion.stop()

        self.boton.setGeometry(
            self.geometria_normal
        )

        self.capa_sombra.setGeometry(
            self.obtener_geometria_sombra_normal()
        )

    def actualizar_geometria_base(self):
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
                    and evento.button()
                    == QtCore.Qt.MouseButton.LeftButton
            ):
                self.mostrar_presionado()

            elif (
                    tipo_evento
                    == QtCore.QEvent.Type.MouseButtonRelease
                    and evento.button()
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

        return super().eventFilter(objeto, evento)


# ==========================================================
# FORMULARIO PRINCIPAL
# ==========================================================

class Personajes(QtWidgets.QWidget):
    """
    Esta variable permite conservar el jugador cuando
    FormTransicion abre la clase sin parámetros.
    """

    jugador_pendiente = None

    def __init__(self, jugador=None):
        super().__init__()
        quitar(self)
        if jugador is None:
            jugador = Personajes.jugador_pendiente

        Personajes.jugador_pendiente = None

        self.jugador = jugador

        self.personaje_actual = None
        self.indice_frame = 0

        self.transicion = None
        self.clase_menu_destino = None

        # --------------------------------------------------
        # RUTAS PRINCIPALES
        # --------------------------------------------------

        # Carpeta PROYECTO_EDUCORE/CODIGOS
        base_dir = Path(__file__).resolve().parent

        # Carpeta PROYECTO_EDUCORE
        proyecto_dir = base_dir.parent

        self.proyecto_dir = proyecto_dir

        ruta_ui = (
                proyecto_dir
                / "EXPO-DISEÑOS"
                / "DESIGNER"
                / "Personaje.ui"
        )

        ruta_fondo = (
                proyecto_dir
                / "assets"
                / "DISEÑOS"
                / "Personaje.png"
        )

        ruta_logo = (
                proyecto_dir
                / "EXPO-DISEÑOS"
                / "Logo"
                / "logo_confondo.png"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el formulario:\n{ruta_ui}"
            )

        if not ruta_fondo.exists():
            raise FileNotFoundError(
                f"No se encontró el fondo:\n{ruta_fondo}"
            )

        if not ruta_logo.exists():
            raise FileNotFoundError(
                f"No se encontró el logo:\n{ruta_logo}"
            )

        # Cargar el archivo de Qt Designer.
        uic.loadUi(str(ruta_ui), self)

        self.setWindowTitle(
            "Selección de personajes"
        )

        # Se toma como resolución base el tamaño REAL guardado
        # dentro de Personaje.ui. Así no se obliga al formulario
        # a usar 1366x768 ni 1920x1080 si fue diseñado con otra
        # resolución.
        self.ancho_base_ui = max(1, self.width())
        self.alto_base_ui = max(1, self.height())

        self.setMinimumSize(
            900,
            506
        )

        self.setMaximumSize(
            16777215,
            16777215
        )

        # Fondo completo.
        self.fondo = FondoImagen(
            self,
            ruta_fondo
        )

        # Cargar directamente el logo con una ruta absoluta.
        # Esto evita que el pixmap configurado en Qt Designer
        # deje de aparecer al ejecutar el programa desde otra
        # carpeta.
        self.pixmap_logo_original = QtGui.QPixmap(
            str(ruta_logo)
        )

        if self.pixmap_logo_original.isNull():
            raise FileNotFoundError(
                f"No se pudo cargar el logo:\n{ruta_logo}"
            )

        if not hasattr(self, "lbl_logo"):
            raise AttributeError(
                "No se encontró lbl_logo en Personaje.ui."
            )

        self.lbl_logo.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.lbl_logo.setScaledContents(False)
        self.actualizar_logo()
        self.lbl_logo.raise_()

        # --------------------------------------------------
        # CONFIGURACIÓN DE LOS PERSONAJES
        # --------------------------------------------------
        #
        # La estructura recomendada es:
        #
        # PROYECTO_EDUCORE/
        # └── assets/
        #     └── personajes/
        #         ├── cerdo/
        #         ├── gato/
        #         └── pato/
        #
        # El código también busca en otras carpetas comunes.
        # --------------------------------------------------

        self.raices_personajes = [
            proyecto_dir
            / "assets"
            / "personajes",

            proyecto_dir
            / "ASSETS"
            / "PERSONAJES",

            proyecto_dir
            / "juego"
            / "assets"
            / "personajes",

            proyecto_dir
            / "EXPO-DISEÑOS"
            / "DISEÑOS"
            / "PERSONAJES",
        ]

        self.config_personajes = {
            # CERDO:
            # jugador_caminar1.png hasta jugador_caminar4.png
            "cerdo": {
                "carpetas": (
                    "cerdo",
                    "cerdito",
                    "jugador",
                ),

                "frames": [
                    (
                        "jugador_caminar1.png",
                    ),
                    (
                        "jugador_caminar2.png",
                    ),
                    (
                        "jugador_caminar3.png",
                    ),
                    (
                        "jugador_caminar4.png",
                    ),
                ],
            },

            # GATO/BANANO:
            # La animación comienza en gato_caminar2.png
            # y termina en gato_caminar8.png.
            "gato": {
                "carpetas": (
                    "gato",
                    "banano",
                ),

                "frames": [
                    (
                        "gato_caminar2.png",
                    ),
                    (
                        "gato_caminar3.png",
                    ),
                    (
                        "gato_caminar4.png",
                    ),
                    (
                        "gato_caminar5.png",
                    ),
                    (
                        "gato_caminar6.png",
                    ),
                    (
                        "gato_caminar7.png",
                    ),
                    (
                        "gato_caminar8.png",
                    ),
                ],
            },

            # PATO:
            # Pato_Caminar1.png hasta Pato_Caminar5.png
            "pato": {
                "carpetas": (
                    "pato",
                    "patito",
                ),

                "frames": [
                    (
                        "Pato_Caminar1.png",
                        "pato_caminar1.png",
                    ),
                    (
                        "Pato_Caminar2.png",
                        "pato_caminar2.png",
                    ),
                    (
                        "Pato_Caminar3.png",
                        "pato_caminar3.png",
                    ),
                    (
                        "Pato_Caminar4.png",
                        "pato_caminar4.png",
                    ),
                    (
                        "Pato_Caminar5.png",
                        "pato_caminar5.png",
                    ),
                ],
            },
        }

        # Cargar todos los frames.
        self.frames_personajes = (
            self.cargar_todos_los_personajes()
        )

        # --------------------------------------------------
        # CUADRO GRANDE
        # --------------------------------------------------

        self.vista_personaje = QtWidgets.QLabel(
            self
        )

        self.vista_personaje.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.vista_personaje.setStyleSheet(
            """
            QLabel {
                background: transparent;
                border: none;
            }
            """
        )

        # --------------------------------------------------
        # TARJETAS PEQUEÑAS
        # --------------------------------------------------

        self.tarjetas = {}

        for nombre in (
                "cerdo",
                "gato",
                "pato"
        ):
            primer_frame = (
                self.frames_personajes[nombre][0]
            )

            tarjeta = TarjetaPersonaje(
                nombre,
                primer_frame,
                self
            )

            tarjeta.seleccionado.connect(
                self.seleccionar_personaje
            )

            self.tarjetas[nombre] = tarjeta

        # --------------------------------------------------
        # TEMPORIZADOR DE LA ANIMACIÓN
        # --------------------------------------------------

        self.timer_animacion = QtCore.QTimer(
            self
        )

        self.timer_animacion.setInterval(
            VELOCIDAD_ANIMACION
        )

        self.timer_animacion.timeout.connect(
            self.actualizar_animacion
        )

        # --------------------------------------------------
        # BOTONES, ELEMENTOS RESPONSIVOS Y EVENTOS
        # --------------------------------------------------

        self.configurar_botones_interfaz()

        self.botones_interactivos = [
            boton
            for boton in (
                getattr(self, "btn_confirmar", None),
                getattr(self, "btn_personaje1", None),
                getattr(self, "btn_personaje2", None),
                getattr(self, "btn_personaje3", None),
                getattr(self, "btn_volver", None),
            )
            if boton is not None
        ]

        # Las tarjetas se colocan exactamente sobre la zona de
        # cada botón creada en Qt Designer. De esta forma ya no
        # dependen de coordenadas manuales que se desalinean.
        self.preparar_elementos_dinamicos()

        # Se crean grupos separados para la ventana principal y
        # para el QFrame Personaje. Esto es importante porque las
        # coordenadas de un control dentro de un QFrame son
        # relativas al QFrame, no a toda la ventana.
        self.configurar_responsividad()

        # El hover se aplica únicamente a Volver y Confirmar.
        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor_hover=1.045,
                factor_presionado=1.018,
                elevacion=3,
                parent=self
            )
            for boton in (
                getattr(self, "btn_volver", None),
                getattr(self, "btn_confirmar", None),
            )
            if boton is not None
        ]

        # Colocar todos los objetos.
        self.actualizar_responsividad()
        self.actualizar_capas()

        # Estado inicial:
        # todos apagados y cuadro grande vacío.
        self.vista_personaje.clear()

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_interfaz
        )

    # ======================================================
    # BUSCAR Y CARGAR SPRITES
    # ======================================================

    def buscar_frame(
            self,
            nombres_carpetas,
            nombres_archivo
    ):
        for raiz in self.raices_personajes:
            if not raiz.exists():
                continue

            for nombre_carpeta in nombres_carpetas:
                carpeta = raiz / nombre_carpeta

                if not carpeta.exists():
                    continue

                # Primero busca directamente.
                for nombre_archivo in nombres_archivo:
                    ruta = carpeta / nombre_archivo

                    if ruta.exists():
                        return ruta

                # Después busca dentro de subcarpetas.
                for nombre_archivo in nombres_archivo:
                    encontrados = list(
                        carpeta.rglob(nombre_archivo)
                    )

                    if encontrados:
                        return encontrados[0]

        return None

    def cargar_todos_los_personajes(self):
        personajes_cargados = {}

        for nombre, configuracion in (
                self.config_personajes.items()
        ):
            frames_cargados = []

            for opciones_nombre in configuracion["frames"]:
                ruta_frame = self.buscar_frame(
                    configuracion["carpetas"],
                    opciones_nombre
                )

                if ruta_frame is None:
                    nombres = "\n".join(
                        f"• {archivo}"
                        for archivo in opciones_nombre
                    )

                    carpetas = "\n".join(
                        f"• {carpeta}"
                        for carpeta
                        in configuracion["carpetas"]
                    )

                    raise FileNotFoundError(
                        f"No se encontró un frame de "
                        f"'{nombre}'.\n\n"
                        f"Carpetas buscadas:\n"
                        f"{carpetas}\n\n"
                        f"Nombres buscados:\n"
                        f"{nombres}"
                    )

                pixmap = QtGui.QPixmap(
                    str(ruta_frame)
                )

                if pixmap.isNull():
                    raise FileNotFoundError(
                        f"No se pudo abrir este frame:\n"
                        f"{ruta_frame}"
                    )

                frames_cargados.append(pixmap)

            personajes_cargados[nombre] = (
                frames_cargados
            )

        return personajes_cargados

    # ======================================================
    # CONFIGURACIÓN DE BOTONES DEL FORMULARIO
    # ======================================================

    def configurar_botones_interfaz(self):
        nombres_volver = (
            "btn_volver",
            "btnVolver",
            "btn_Volver",
            "botonVolver"
        )

        self.btn_volver = None

        for nombre in nombres_volver:
            boton = self.findChild(
                QtWidgets.QPushButton,
                nombre
            )

            if boton is not None:
                self.btn_volver = boton
                break

        if self.btn_volver is None:
            raise AttributeError(
                "No se encontró el botón Volver en Personaje.ui. "
                "Usa el objectName btn_volver."
            )

        self.btn_confirmar = self.findChild(
            QtWidgets.QPushButton,
            "btn_confirmar"
        )

        if self.btn_confirmar is None:
            raise AttributeError(
                "No se encontró el botón Confirmar en Personaje.ui. "
                "Usa el objectName btn_confirmar."
            )

        self.btn_personaje1 = self.findChild(
            QtWidgets.QPushButton,
            "btn_personaje1"
        )

        self.btn_personaje2 = self.findChild(
            QtWidgets.QPushButton,
            "btn_personaje2"
        )

        self.btn_personaje3 = self.findChild(
            QtWidgets.QPushButton,
            "btn_personaje3"
        )

        for boton in (
                self.btn_volver,
                self.btn_confirmar,
                self.btn_personaje1,
                self.btn_personaje2,
                self.btn_personaje3,
        ):
            if boton is not None:
                boton.setCursor(
                    QtGui.QCursor(
                        QtCore.Qt.CursorShape.PointingHandCursor
                    )
                )

        self.btn_volver.clicked.connect(
            self.volver_menu_usuario
        )

        # Los botones transparentes del .ui también permiten
        # seleccionar cada personaje. Las tarjetas continúan
        # siendo seleccionables directamente.
        if self.btn_personaje1 is not None:
            self.btn_personaje1.clicked.connect(
                lambda: self.seleccionar_personaje("cerdo")
            )

        if self.btn_personaje2 is not None:
            self.btn_personaje2.clicked.connect(
                lambda: self.seleccionar_personaje("gato")
            )

        if self.btn_personaje3 is not None:
            self.btn_personaje3.clicked.connect(
                lambda: self.seleccionar_personaje("pato")
            )

    def preparar_elementos_dinamicos(self):
        """
        Coloca el cuadro grande y las tarjetas en el mismo
        contenedor que los controles diseñados en Qt Designer.
        """

        contenedor_principal = getattr(
            self,
            "Personaje",
            self
        )

        if not isinstance(
                contenedor_principal,
                QtWidgets.QWidget
        ):
            contenedor_principal = self

        # Primero intenta usar un QLabel de Qt Designer como
        # referencia para el cuadro grande. Si no existe, usa la
        # posición original de la clase anterior.
        nombres_vista = (
            "lbl_vista_personaje",
            "lbl_personaje_grande",
            "lbl_personaje_seleccionado",
            "lbl_preview_personaje",
            "lbl_preview",
        )

        etiqueta_referencia = None

        for nombre_objeto in nombres_vista:
            etiqueta_referencia = self.findChild(
                QtWidgets.QLabel,
                nombre_objeto
            )

            if etiqueta_referencia is not None:
                break

        if etiqueta_referencia is not None:
            padre_vista = etiqueta_referencia.parentWidget()
            self.vista_personaje.setParent(padre_vista)
            self.vista_personaje.setGeometry(
                etiqueta_referencia.geometry()
            )
            etiqueta_referencia.hide()
        else:
            self.vista_personaje.setParent(
                contenedor_principal
            )

            punto_vista = contenedor_principal.mapFrom(
                self,
                QtCore.QPoint(527, 171)
            )

            self.vista_personaje.setGeometry(
                punto_vista.x(),
                punto_vista.y(),
                312,
                245
            )

        configuracion_tarjetas = (
            ("cerdo", self.btn_personaje1),
            ("gato", self.btn_personaje2),
            ("pato", self.btn_personaje3),
        )

        posiciones_respaldo = {
            "cerdo": QtCore.QRect(432, 458, 111, 142),
            "gato": QtCore.QRect(558, 458, 111, 142),
            "pato": QtCore.QRect(684, 458, 111, 142),
        }

        for nombre, boton in configuracion_tarjetas:
            tarjeta = self.tarjetas[nombre]

            if boton is not None:
                padre = boton.parentWidget()
                tarjeta.setParent(padre)
                tarjeta.setGeometry(boton.geometry())
                tarjeta.stackUnder(boton)
            else:
                tarjeta.setParent(contenedor_principal)

                rectangulo = posiciones_respaldo[nombre]
                punto = contenedor_principal.mapFrom(
                    self,
                    rectangulo.topLeft()
                )

                tarjeta.setGeometry(
                    punto.x(),
                    punto.y(),
                    rectangulo.width(),
                    rectangulo.height()
                )

            tarjeta.show()

    def _elementos_directos(self, padre):
        return padre.findChildren(
            QtWidgets.QWidget,
            options=(
                QtCore.Qt.FindChildOption.FindDirectChildrenOnly
            )
        )

    def _crear_grupo_responsivo(
            self,
            padre,
            ancho_base,
            alto_base,
            excluir=None
    ):
        """
        Crea un BotonesResponsivos para los botones y un
        ElementosResponsivos para los demás controles que sean
        hijos directos del mismo padre.
        """

        excluir = set(excluir or [])

        elementos = [
            elemento
            for elemento in self._elementos_directos(padre)
            if elemento not in excluir
               and not elemento.objectName().startswith("sombra_")
        ]

        botones = [
            elemento
            for elemento in elementos
            if isinstance(
                elemento,
                QtWidgets.QAbstractButton
            )
        ]

        otros_elementos = [
            elemento
            for elemento in elementos
            if not isinstance(
                elemento,
                QtWidgets.QAbstractButton
            )
        ]

        if botones:
            self.grupos_botones_responsivos.append(
                BotonesResponsivos(
                    ventana=padre,
                    botones=botones,
                    ancho_base=max(1, ancho_base),
                    alto_base=max(1, alto_base),
                    escalar_iconos=True,
                    escalar_fuentes=False,
                )
            )

        if otros_elementos:
            self.grupos_elementos_responsivos.append(
                ElementosResponsivos(
                    ventana=padre,
                    elementos=otros_elementos,
                    ancho_base=max(1, ancho_base),
                    alto_base=max(1, alto_base),
                    escalar_iconos=True,
                    escalar_fuentes=False,
                )
            )

    def configurar_responsividad(self):
        """
        Configura la responsividad respetando la jerarquía real
        de widgets del archivo Personaje.ui.
        """

        self.grupos_botones_responsivos = []
        self.grupos_elementos_responsivos = []

        contenedor = getattr(
            self,
            "Personaje",
            None
        )

        # Primero se escalan los controles que son hijos directos
        # de la ventana. El fondo se excluye porque siempre ocupa
        # el tamaño completo.
        self._crear_grupo_responsivo(
            padre=self,
            ancho_base=self.ancho_base_ui,
            alto_base=self.alto_base_ui,
            excluir=(self.fondo,)
        )

        # Después se escalan los controles internos del QFrame
        # usando el tamaño original del propio QFrame.
        if (
                isinstance(contenedor, QtWidgets.QWidget)
                and contenedor is not self
        ):
            self.ancho_base_contenedor = max(
                1,
                contenedor.width()
            )
            self.alto_base_contenedor = max(
                1,
                contenedor.height()
            )

            self._crear_grupo_responsivo(
                padre=contenedor,
                ancho_base=self.ancho_base_contenedor,
                alto_base=self.alto_base_contenedor
            )

    def actualizar_responsividad(self):
        """
        Ejecuta los ajustes en el orden correcto: primero la
        ventana y luego los elementos internos del QFrame.
        """

        if not hasattr(self, "tarjetas"):
            return

        for grupo in getattr(
                self,
                "grupos_elementos_responsivos",
                []
        ):
            if grupo.ventana is self:
                grupo.ajustar()

        for grupo in getattr(
                self,
                "grupos_botones_responsivos",
                []
        ):
            if grupo.ventana is self:
                grupo.ajustar()

        for grupo in getattr(
                self,
                "grupos_elementos_responsivos",
                []
        ):
            if grupo.ventana is not self:
                grupo.ajustar()

        for grupo in getattr(
                self,
                "grupos_botones_responsivos",
                []
        ):
            if grupo.ventana is not self:
                grupo.ajustar()

        for tarjeta in self.tarjetas.values():
            tarjeta.actualizar_imagen()

        self.mostrar_frame_actual()
        self.actualizar_logo()

    def actualizar_logo(self):
        if not hasattr(self, "lbl_logo"):
            return

        if not hasattr(self, "pixmap_logo_original"):
            return

        if self.lbl_logo.width() <= 0 or self.lbl_logo.height() <= 0:
            return

        pixmap = self.pixmap_logo_original.scaled(
            max(1, self.lbl_logo.width()),
            max(1, self.lbl_logo.height()),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )

        self.lbl_logo.setPixmap(pixmap)

    def preparar_hover_para_resize(self):
        for efecto in getattr(
                self,
                "efectos_hover",
                []
        ):
            efecto.preparar_ajuste_responsivo()

    def actualizar_hover_botones(self):
        for efecto in getattr(
                self,
                "efectos_hover",
                []
        ):
            efecto.actualizar_geometria_base()

    def actualizar_interfaz(self):
        if hasattr(self, "efectos_hover"):
            self.preparar_hover_para_resize()

        self.actualizar_responsividad()
        self.actualizar_capas()

        if hasattr(self, "efectos_hover"):
            QtCore.QTimer.singleShot(
                0,
                self.actualizar_hover_botones
            )

    def volver_menu_usuario(self):
        self.timer_animacion.stop()

        # Import local para evitar importación circular.
        from MenuUsuario import MenuUsuario

        jugador_actual = self.jugador

        # FormTransicion abre una clase sin parámetros.
        # Esta clase auxiliar conserva el jugador actual.
        class MenuUsuarioDestino(MenuUsuario):
            def __init__(self):
                super().__init__(
                    jugador=jugador_actual
                )

        self.clase_menu_destino = (
            MenuUsuarioDestino
        )

        self.transicion = FormTransicion(
            self,
            self.clase_menu_destino
        )

    # ======================================================
    # SELECCIÓN DE PERSONAJES
    # ======================================================

    def seleccionar_personaje(self, nombre):
        if nombre not in self.frames_personajes:
            return

        self.personaje_actual = nombre
        self.indice_frame = 0

        # El seleccionado recupera el color.
        # Los demás vuelven a estar apagados.
        for nombre_tarjeta, tarjeta in (
                self.tarjetas.items()
        ):
            tarjeta.marcar_seleccionado(
                nombre_tarjeta == nombre
            )

        self.timer_animacion.stop()

        # Mostrar inmediatamente el primer frame.
        self.mostrar_frame_actual()

        # Comenzar la animación.
        if (
                len(self.frames_personajes[nombre])
                > 1
        ):
            self.timer_animacion.start()

        print(
            f"Personaje seleccionado: {nombre}"
        )

    # ======================================================
    # ANIMACIÓN DEL CUADRO GRANDE
    # ======================================================

    def actualizar_animacion(self):
        if self.personaje_actual is None:
            return

        frames = self.frames_personajes[
            self.personaje_actual
        ]

        if not frames:
            return

        self.indice_frame += 1

        if self.indice_frame >= len(frames):
            self.indice_frame = 0

        self.mostrar_frame_actual()

    def mostrar_frame_actual(self):
        if self.personaje_actual is None:
            self.vista_personaje.clear()
            return

        frames = self.frames_personajes[
            self.personaje_actual
        ]

        if not frames:
            self.vista_personaje.clear()
            return

        pixmap = frames[self.indice_frame]

        ancho_disponible = max(
            1,
            self.vista_personaje.width() - 30
        )

        alto_disponible = max(
            1,
            self.vista_personaje.height() - 20
        )

        pixmap_escalado = pixmap.scaled(
            ancho_disponible,
            alto_disponible,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.FastTransformation
        )

        self.vista_personaje.setPixmap(
            pixmap_escalado
        )

    # ======================================================
    # ACTUALIZACIÓN DE CAPAS
    # ======================================================

    def actualizar_capas(self):
        if hasattr(self, "fondo"):
            self.fondo.lower()

        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        if hasattr(self, "vista_personaje"):
            self.vista_personaje.raise_()

        for tarjeta in getattr(self, "tarjetas", {}).values():
            tarjeta.raise_()

        for boton in getattr(self, "botones_interactivos", []):
            boton.raise_()

        for efecto in getattr(self, "efectos_hover", []):
            efecto.colocar_capas_correctamente()

    # ======================================================
    # EVENTOS DEL FORMULARIO
    # ======================================================

    def resizeEvent(self, evento):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        if hasattr(self, "efectos_hover"):
            self.preparar_hover_para_resize()

        self.actualizar_responsividad()

        self.actualizar_logo()

        self.actualizar_capas()

        if hasattr(self, "efectos_hover"):
            QtCore.QTimer.singleShot(
                0,
                self.actualizar_hover_botones
            )

        super().resizeEvent(evento)

    def hideEvent(self, evento):
        if hasattr(self, "timer_animacion"):
            self.timer_animacion.stop()

        super().hideEvent(evento)

    def showEvent(self, evento):
        super().showEvent(evento)

        if (
                hasattr(self, "timer_animacion")
                and self.personaje_actual is not None
        ):
            self.timer_animacion.start()

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_interfaz
        )

        QtCore.QTimer.singleShot(
            100,
            self.actualizar_interfaz
        )


# ==========================================================
# EJECUTAR PERSONAJES.PY DIRECTAMENTE
# ==========================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = Personajes()
    ventana.showMaximized()

    sys.exit(app.exec())