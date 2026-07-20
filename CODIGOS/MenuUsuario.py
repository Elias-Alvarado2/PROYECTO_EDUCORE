from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui, QtCore

from Alertas import Alertas
from AjusteResponsive import BotonesResponsivos
from Transicion import FormTransicion
from quitar_barra import quitar
from LogoReutilizable import LogoReutilizable
from Ajustes import Ajustes
from ConexionBD import ConexionBD

VELOCIDAD_ANIMACION_PERSONAJE = 130

class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.ruta_imagen = ruta_imagen

        self.pixmap_original = QtGui.QPixmap(
            str(self.ruta_imagen)
        )

        if self.pixmap_original.isNull():
            raise FileNotFoundError(
                f"No se pudo cargar el fondo:\n"
                f"{self.ruta_imagen}"
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

        # Evita que el fondo bloquee clics.
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
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
    Agranda ligeramente el botón y aumenta su sombra
    cuando el cursor pasa sobre él.
    """

    def __init__(
        self,
        boton,
        factor=1.035,
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

        self.geometria_normal = QtCore.QRect(
            self.boton.geometry()
        )

        self.animacion_geometria = (
            QtCore.QPropertyAnimation(
                self.boton,
                b"geometry",
                self
            )
        )

        self.animacion_geometria.setDuration(
            self.duracion
        )

        self.animacion_geometria.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        # Sombra del botón.
        self.sombra = (
            QtWidgets.QGraphicsDropShadowEffect(
                self.boton
            )
        )

        self.sombra.setColor(
            QtGui.QColor(0, 0, 0, 170)
        )

        self.sombra.setBlurRadius(10)
        self.sombra.setOffset(0, 3)

        self.boton.setGraphicsEffect(
            self.sombra
        )

        self.animacion_sombra = (
            QtCore.QPropertyAnimation(
                self.sombra,
                b"blurRadius",
                self
            )
        )

        self.animacion_sombra.setDuration(
            self.duracion
        )

        self.animacion_sombra.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        self.boton.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )

        self.boton.installEventFilter(
            self
        )

    def obtener_geometria_grande(self):
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
            rectangulo.x()
            - diferencia_ancho // 2,

            rectangulo.y()
            - diferencia_alto // 2,

            ancho_nuevo,
            alto_nuevo
        )

    def animar_geometria(self, destino):
        self.animacion_geometria.stop()

        self.animacion_geometria.setStartValue(
            self.boton.geometry()
        )

        self.animacion_geometria.setEndValue(
            destino
        )

        self.animacion_geometria.start()

    def animar_sombra(self, radio):
        self.animacion_sombra.stop()

        self.animacion_sombra.setStartValue(
            self.sombra.blurRadius()
        )

        self.animacion_sombra.setEndValue(
            radio
        )

        self.animacion_sombra.start()

    def actualizar_geometria_base(self):
        """
        Guarda la posición asignada por
        BotonesResponsivos.
        """

        self.animacion_geometria.stop()

        self.geometria_normal = QtCore.QRect(
            self.boton.geometry()
        )

        if self.cursor_encima:
            self.boton.setGeometry(
                self.obtener_geometria_grande()
            )

    def eventFilter(self, objeto, evento):
        if objeto is self.boton:

            if (
                evento.type()
                == QtCore.QEvent.Type.Enter
                and self.boton.isEnabled()
            ):
                self.cursor_encima = True

                self.boton.raise_()

                self.animar_geometria(
                    self.obtener_geometria_grande()
                )

                self.animar_sombra(28)

            elif (
                evento.type()
                == QtCore.QEvent.Type.Leave
            ):
                self.cursor_encima = False

                self.animar_geometria(
                    self.geometria_normal
                )

                self.animar_sombra(10)

        return super().eventFilter(
            objeto,
            evento
        )

class MenuUsuario(QtWidgets.QWidget):
    def __init__(self, jugador=None):
        super().__init__()

        quitar(self)

        self.jugador = jugador or {}
        self.db = ConexionBD()

        # Ventanas y transiciones.
        self.ventana_lecciones = None
        self.ventana_login = None

        self.form_ajustes = None
        self.transicion_ajustes = None

        self.transicion_personajes = None

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        # Rutas y referencias utilizadas para mostrar el
        # personaje seleccionado por el usuario.
        self.base_dir = BASE_DIR
        self.proyecto_dir = PROYECTO_DIR
        self.pixmap_personaje_original = None
        self.lbl_nombre_personaje_actual = None
        self.lbl_imagen_personaje_actual = None

        # Animación del personaje en el menú.
        self.frames_personaje_menu = []
        self.indice_frame_personaje = 0
        self.personaje_animado_actual = None

        self.timer_animacion_personaje = QtCore.QTimer(
            self
        )
        self.timer_animacion_personaje.setInterval(
            VELOCIDAD_ANIMACION_PERSONAJE
        )
        self.timer_animacion_personaje.timeout.connect(
            self.actualizar_animacion_personaje
        )

        ruta_ui = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "Menu-Jugador.ui"
        )

        ruta_imagen = (
            PROYECTO_DIR
            / "assets"
            / "DISEÑOS"
            / "Menu-Usuario.png"
        )

        ruta_logo = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "Logo"
            / "logo_confondo.png"
        )

        ruta_botones = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "Botones"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n"
                f"{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n"
                f"{ruta_imagen}"
            )

        if not ruta_botones.exists():
            raise FileNotFoundError(
                "No se encontró la carpeta de botones:"
                f"\n{ruta_botones}"
            )

        if not ruta_logo.exists():
            raise FileNotFoundError(
                f"No se encontró el logo:\n"
                f"{ruta_logo}"
            )

        uic.loadUi(
            str(ruta_ui),
            self
        )

        # Recupera nuevamente el jugador para asegurar que
        # el personaje mostrado sea el guardado en MySQL.
        self.actualizar_jugador_desde_bd()

        # Configura los QLabel donde aparecerán el nombre
        # y la imagen del personaje guardado.
        self.configurar_vista_personaje()
        self.mostrar_personaje_usuario()

        # Corregir las rutas relativas de Qt Designer.
        self.corregir_rutas_stylesheet(
            ruta_botones
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

        self.logo_reutilizable = (
            LogoReutilizable(
                self,
                ruta_logo
            )
        )

        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        self.botones_menu = [
            self.btnJugar,
            self.btnAjustes,
            self.btnPerfil,
            self.btnCerrarSesion,

            self.btn_personaje,
        ]

        self.botones_responsivos = (
            BotonesResponsivos(
                ventana=self,
                botones=self.botones_menu,
                ancho_base=1920,
                alto_base=1080,
                escalar_iconos=True,
                escalar_fuentes=False,
            )
        )

        self.configurar_botones()

        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor=1.035,
                duracion=120,
                parent=self
            )
            for boton in self.botones_menu
        ]

        # Espera a que BotonesResponsivos coloque
        # correctamente los botones.
        QtCore.QTimer.singleShot(
            0,
            self.actualizar_hover_botones
        )

        self.conectar_eventos()

        # Ejecuta otra actualización cuando todos los widgets
        # ya tengan su tamaño y posición definitivos.
        QtCore.QTimer.singleShot(
            0,
            self.actualizar_tarjeta_personaje
        )


    # ======================================================
    # INFORMACIÓN DEL PERSONAJE SELECCIONADO
    # ======================================================

    def buscar_label_por_nombres(self, nombres):
        """
        Busca un QLabel usando varios objectName posibles.
        """

        for nombre in nombres:
            etiqueta = self.findChild(
                QtWidgets.QLabel,
                nombre
            )

            if etiqueta is not None:
                return etiqueta

        return None

    def configurar_vista_personaje(self):
        """
        Localiza y configura los QLabel creados en Qt Designer.

        ObjectName usados en tu formulario:
            lbl_nombrepersonaje
            lbl_imagenpersonaje
        """

        self.lbl_nombre_personaje_actual = (
            self.buscar_label_por_nombres(
                (
                    "lbl_nombrepersonaje",
                    "lbl_personaje",
                    "lbl_nombre_personaje",
                    "lblNombrePersonaje",
                    "label_personaje",
                    "labelPersonaje",
                )
            )
        )

        self.lbl_imagen_personaje_actual = (
            self.buscar_label_por_nombres(
                (
                    "lbl_imagenpersonaje",
                    "lbl_foto_personaje",
                    "lbl_personaje_seleccionado",
                    "lblFotoPersonaje",
                    "lblImagenPersonaje",
                    "label_foto_personaje",
                    "labelFotoPersonaje",
                )
            )
        )

        if self.lbl_nombre_personaje_actual is None:
            print(
                "ADVERTENCIA: No se encontró lbl_nombrepersonaje."
            )
        else:
            self.lbl_nombre_personaje_actual.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter
            )

            self.lbl_nombre_personaje_actual.setWordWrap(
                False
            )

            self.lbl_nombre_personaje_actual.setStyleSheet(
                """
                QLabel {
                    color: #000000;
                    background: transparent;
                    border: none;
                    font-size: 28px;
                    font-weight: 900;
                }
                """
            )

        if self.lbl_imagen_personaje_actual is None:
            print(
                "ADVERTENCIA: No se encontró lbl_imagenpersonaje."
            )
        else:
            self.lbl_imagen_personaje_actual.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter
            )

            self.lbl_imagen_personaje_actual.setScaledContents(
                False
            )

            self.lbl_imagen_personaje_actual.setStyleSheet(
                """
                QLabel {
                    color: #000000;
                    background: transparent;
                    border: none;
                }
                """
            )

        self.centrar_nombre_personaje()

    def centrar_nombre_personaje(self):
        """
        Hace que la etiqueta del nombre tenga el mismo ancho
        y centro horizontal que la etiqueta de la imagen.
        """

        etiqueta_nombre = self.lbl_nombre_personaje_actual
        etiqueta_imagen = self.lbl_imagen_personaje_actual

        if (
            etiqueta_nombre is None
            or etiqueta_imagen is None
        ):
            return

        etiqueta_nombre.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # Cuando ambos QLabel pertenecen al mismo contenedor,
        # el nombre se alinea exactamente con la imagen.
        if (
            etiqueta_nombre.parentWidget()
            is etiqueta_imagen.parentWidget()
        ):
            geometria_nombre = etiqueta_nombre.geometry()
            geometria_imagen = etiqueta_imagen.geometry()

            etiqueta_nombre.setGeometry(
                geometria_imagen.x(),
                geometria_nombre.y(),
                geometria_imagen.width(),
                max(50, geometria_nombre.height())
            )

        # Ajusta el tamaño de fuente según el tamaño del label.
        fuente = etiqueta_nombre.font()
        fuente.setBold(True)

        tamano = max(
            18,
            min(
                30,
                round(
                    etiqueta_nombre.height() * 0.46
                )
            )
        )

        fuente.setPointSize(tamano)
        etiqueta_nombre.setFont(fuente)

    def obtener_id_jugador(self):
        """Obtiene el ID del jugador de la sesión actual."""

        if isinstance(self.jugador, dict):
            return self.jugador.get("id_jugador")

        return getattr(
            self.jugador,
            "id_jugador",
            None
        )

    def actualizar_jugador_desde_bd(self):
        """
        Actualiza el diccionario de sesión con los datos más
        recientes del jugador, incluido el personaje guardado.
        """

        id_jugador = self.obtener_id_jugador()

        if id_jugador is None:
            return

        if not hasattr(
            self.db,
            "buscar_jugador_por_id"
        ):
            return

        try:
            jugador_bd = self.db.buscar_jugador_por_id(
                id_jugador
            )

            if not jugador_bd:
                return

            datos = dict(jugador_bd)

            if isinstance(self.jugador, dict):
                self.jugador.update(datos)
            else:
                for clave, valor in datos.items():
                    try:
                        setattr(
                            self.jugador,
                            clave,
                            valor
                        )
                    except Exception:
                        pass

        except Exception as error:
            print(
                "No se pudieron actualizar los datos "
                f"del jugador desde MySQL: {error}"
            )

    def obtener_personaje_sesion(self):
        """
        Obtiene el personaje del diccionario del jugador
        y normaliza nombres antiguos.
        """

        if not hasattr(self.jugador, "get"):
            return ""

        personaje = str(
            self.jugador.get("personaje") or ""
        ).strip().lower()

        equivalencias = {
            "cerdito": "cerdo",
            "jugador": "cerdo",
            "banano": "gato",
            "patito": "pato",
        }

        return equivalencias.get(
            personaje,
            personaje
        )

    def mostrar_personaje_usuario(self):
        """
        Muestra el nombre y reproduce la animación del personaje
        seleccionado por el usuario.
        """

        if (
            self.lbl_nombre_personaje_actual is None
            or self.lbl_imagen_personaje_actual is None
        ):
            return

        personaje = self.obtener_personaje_sesion()

        nombres_visibles = {
            "cerdo": "CERDO",
            "gato": "GATO",
            "pato": "PATO",
        }

        if personaje not in nombres_visibles:
            self.timer_animacion_personaje.stop()
            self.frames_personaje_menu = []
            self.personaje_animado_actual = None
            self.pixmap_personaje_original = None

            self.lbl_nombre_personaje_actual.setText(
                "SIN PERSONAJE"
            )
            self.lbl_imagen_personaje_actual.clear()
            return

        self.lbl_nombre_personaje_actual.setText(
            nombres_visibles[personaje]
        )

        self.centrar_nombre_personaje()

        # Solo vuelve a cargar los archivos cuando cambia
        # el personaje de la sesión.
        if (
            personaje != self.personaje_animado_actual
            or not self.frames_personaje_menu
        ):
            self.timer_animacion_personaje.stop()

            self.frames_personaje_menu = (
                self.cargar_frames_personaje_menu(
                    personaje
                )
            )

            self.personaje_animado_actual = personaje
            self.indice_frame_personaje = 0

        if not self.frames_personaje_menu:
            self.pixmap_personaje_original = None
            self.lbl_imagen_personaje_actual.clear()
            self.lbl_imagen_personaje_actual.setText(
                "IMAGEN NO ENCONTRADA"
            )

            print(
                "No se encontraron frames para:",
                personaje
            )
            return

        self.lbl_imagen_personaje_actual.setText("")

        self.pixmap_personaje_original = (
            self.frames_personaje_menu[
                self.indice_frame_personaje
            ]
        )

        self.actualizar_imagen_personaje()

        if len(self.frames_personaje_menu) > 1:
            self.timer_animacion_personaje.start()
        else:
            self.timer_animacion_personaje.stop()

        self.lbl_nombre_personaje_actual.raise_()
        self.lbl_imagen_personaje_actual.raise_()

    def obtener_configuracion_frames_personaje(
        self,
        personaje
    ):
        """
        Devuelve las carpetas y los frames en el orden
        correcto para cada personaje.
        """

        configuraciones = {
            "cerdo": {
                "carpetas": (
                    "cerdo",
                    "cerdito",
                    "jugador",
                ),
                "frames": (
                    ("jugador_caminar1.png",),
                    ("jugador_caminar2.png",),
                    ("jugador_caminar3.png",),
                    ("jugador_caminar4.png",),
                ),
            },

            "gato": {
                "carpetas": (
                    "gato",
                    "banano",
                ),
                "frames": (
                    ("gato_caminar2.png",),
                    ("gato_caminar3.png",),
                    ("gato_caminar4.png",),
                    ("gato_caminar5.png",),
                    ("gato_caminar6.png",),
                    ("gato_caminar7.png",),
                    ("gato_caminar8.png",),
                ),
            },

            "pato": {
                "carpetas": (
                    "pato",
                    "patito",
                ),
                "frames": (
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
                ),
            },
        }

        return configuraciones.get(
            personaje
        )

    def obtener_raices_personajes_menu(self):
        return (
            self.proyecto_dir
            / "assets"
            / "personajes",

            self.proyecto_dir
            / "ASSETS"
            / "PERSONAJES",

            self.proyecto_dir
            / "juego"
            / "assets"
            / "personajes",

            self.proyecto_dir
            / "EXPO-DISEÑOS"
            / "DISEÑOS"
            / "PERSONAJES",
        )

    def buscar_frame_personaje_menu(
        self,
        nombres_carpetas,
        nombres_archivo
    ):
        """
        Busca un frame de animación en todas las ubicaciones
        compatibles con el proyecto.
        """

        for raiz in self.obtener_raices_personajes_menu():
            if not raiz.exists():
                continue

            for nombre_carpeta in nombres_carpetas:
                carpeta = raiz / nombre_carpeta

                if not carpeta.exists():
                    continue

                for nombre_archivo in nombres_archivo:
                    ruta = carpeta / nombre_archivo

                    if ruta.exists():
                        return ruta

                for nombre_archivo in nombres_archivo:
                    encontrados = list(
                        carpeta.rglob(
                            nombre_archivo
                        )
                    )

                    if encontrados:
                        return encontrados[0]

        return None

    def cargar_frames_personaje_menu(
        self,
        personaje
    ):
        """
        Carga todos los frames del personaje como QPixmap.
        """

        configuracion = (
            self.obtener_configuracion_frames_personaje(
                personaje
            )
        )

        if configuracion is None:
            return []

        frames_cargados = []

        for opciones_archivo in configuracion["frames"]:
            ruta_frame = self.buscar_frame_personaje_menu(
                configuracion["carpetas"],
                opciones_archivo
            )

            if ruta_frame is None:
                print(
                    "No se encontró uno de los frames de",
                    personaje,
                    opciones_archivo
                )
                continue

            pixmap = QtGui.QPixmap(
                str(ruta_frame)
            )

            if not pixmap.isNull():
                frames_cargados.append(
                    pixmap
                )

        return frames_cargados

    def actualizar_animacion_personaje(self):
        """
        Avanza al siguiente frame del personaje.
        """

        if not self.frames_personaje_menu:
            self.timer_animacion_personaje.stop()
            return

        self.indice_frame_personaje += 1

        if (
            self.indice_frame_personaje
            >= len(self.frames_personaje_menu)
        ):
            self.indice_frame_personaje = 0

        self.pixmap_personaje_original = (
            self.frames_personaje_menu[
                self.indice_frame_personaje
            ]
        )

        self.actualizar_imagen_personaje()

    def actualizar_imagen_personaje(self):
        """
        Escala el frame actual sin deformarlo y lo mantiene
        centrado dentro de lbl_imagenpersonaje.
        """

        if self.lbl_imagen_personaje_actual is None:
            return

        if self.pixmap_personaje_original is None:
            return

        ancho = self.lbl_imagen_personaje_actual.width()
        alto = self.lbl_imagen_personaje_actual.height()

        if ancho <= 0 or alto <= 0:
            return

        pixmap_escalado = (
            self.pixmap_personaje_original.scaled(
                max(1, ancho - 12),
                max(1, alto - 12),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.FastTransformation
            )
        )

        self.lbl_imagen_personaje_actual.setPixmap(
            pixmap_escalado
        )

    def corregir_rutas_stylesheet(
        self,
        ruta_botones
    ):
        ruta_absoluta = (
            ruta_botones
            .resolve()
            .as_posix()
        )

        controles = [
            self,
            *self.findChildren(
                QtWidgets.QWidget
            ),
        ]

        for control in controles:
            estilo_original = (
                control.styleSheet()
            )

            if not estilo_original:
                continue

            estilo_corregido = estilo_original

            estilo_corregido = (
                estilo_corregido.replace(
                    'url("../Botones/',
                    f'url("{ruta_absoluta}/'
                )
            )

            estilo_corregido = (
                estilo_corregido.replace(
                    "url('../Botones/",
                    f"url('{ruta_absoluta}/"
                )
            )

            estilo_corregido = (
                estilo_corregido.replace(
                    "url(../Botones/",
                    f"url({ruta_absoluta}/"
                )
            )

            if (
                estilo_corregido
                != estilo_original
            ):
                control.setStyleSheet(
                    estilo_corregido
                )

    def configurar_botones(self):
        for boton in self.botones_menu:
            boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape
                    .PointingHandCursor
                )
            )

    def actualizar_hover_botones(self):
        """
        Actualiza las posiciones originales
        utilizadas por las animaciones hover.
        """

        for efecto in getattr(
            self,
            "efectos_hover",
            []
        ):
            efecto.actualizar_geometria_base()

    def conectar_eventos(self):
        self.btnJugar.clicked.connect(
            self.abrir_lecciones
        )

        self.btnAjustes.clicked.connect(
            self.abrir_ajustes
        )

        self.btnCerrarSesion.clicked.connect(
            self.cerrar_sesion
        )

        self.btn_personaje.clicked.connect(
            self.abrir_personajes
        )

    def abrir_personajes(self):
        """
        Abre Personajes.py conservando los datos
        del jugador que inició sesión.
        """

        try:

            from Personajes import Personajes


            Personajes.jugador_pendiente = (
                self.jugador
            )

            self.transicion_personajes = (
                FormTransicion(
                    self,
                    Personajes
                )
            )

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error al abrir personajes",
                "No se pudo abrir la ventana "
                "de personajes."
                f"\n\nDetalles:\n{error}",
                "error"
            )

    def abrir_ajustes(self):
        """
        Abre Ajustes desde el menú del jugador.
        """

        # Si ya está abierta, solamente se lleva
        # al frente.
        if (
            self.form_ajustes is not None
            and self.form_ajustes.isVisible()
        ):
            self.form_ajustes.raise_()
            self.form_ajustes.activateWindow()
            return

        try:
            self.form_ajustes = Ajustes(
                ventana_anterior=self,
                jugador=self.jugador,
                desde_juego=False,
            )

            self.form_ajustes.setAttribute(
                QtCore.Qt.WidgetAttribute
                .WA_DeleteOnClose,
                True
            )

            self.form_ajustes.destroyed.connect(
                self._limpiar_form_ajustes
            )

            self.transicion_ajustes = (
                FormTransicion(
                    self,
                    self.form_ajustes
                )
            )

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error al abrir ajustes",
                "No se pudo abrir la ventana "
                "de ajustes."
                f"\n\nDetalles:\n{error}",
                "error"
            )

    def _limpiar_form_ajustes(self):
        """
        Limpia las referencias para poder abrir
        nuevamente la ventana de Ajustes.
        """

        self.form_ajustes = None
        self.transicion_ajustes = None

    def abrir_lecciones(self):
        try:
            from Lecciones import Lecciones

            try:
                self.ventana_lecciones = Lecciones(
                    jugador=self.jugador,
                    ventana_anterior=self,
                    tipo_usuario="jugador"
                )

            except TypeError:
                try:
                    self.ventana_lecciones = Lecciones(
                        self.jugador,
                        self
                    )

                except TypeError:
                    try:
                        self.ventana_lecciones = (
                            Lecciones(
                                self.jugador
                            )
                        )

                    except TypeError:
                        self.ventana_lecciones = (
                            Lecciones()
                        )

            self.transicion_lecciones = (
                FormTransicion(
                    self,
                    self.ventana_lecciones
                )
            )

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error al abrir lecciones",
                "No se pudo abrir la ventana "
                "de lecciones."
                f"\n\nDetalles:\n{error}",
                "error"
            )

    def cerrar_sesion(self):
        respuesta = Alertas.confirmar(
            self,
            "Cerrar sesión",
            "¿Seguro que deseas cerrar sesión?",
            tipo="error",
            texto_confirmar="SÍ, CERRAR",
            texto_cancelar="CANCELAR"
        )

        if not respuesta:
            return

        try:
            from Login import LoginWindow

            app = (
                QtWidgets.QApplication.instance()
            )

            if hasattr(
                app,
                "historial_forms"
            ):
                app.historial_forms.clear()

            self.ventana_login = (
                LoginWindow()
            )

            app.ventana_login = (
                self.ventana_login
            )

            self.ventana_login.resize(
                1020,
                720
            )

            self.ventana_login.showNormal()

            self.close()

        except Exception as error:
            Alertas.mostrar(
                self,
                "Error al cerrar sesión",
                "No se pudo abrir el Login:"
                f"\n{error}",
                "error"
            )

    def actualizar_tarjeta_personaje(self):
        # Recupera los datos más recientes y vuelve a mostrar
        # el nombre y la imagen del personaje.
        self.actualizar_jugador_desde_bd()
        self.mostrar_personaje_usuario()

    def showEvent(self, event):
        super().showEvent(event)

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_tarjeta_personaje
        )

    def hideEvent(self, event):
        if hasattr(
            self,
            "timer_animacion_personaje"
        ):
            self.timer_animacion_personaje.stop()

        super().hideEvent(event)

    def resizeEvent(self, event):
        # Ajustar el fondo.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )

            self.fondo.lower()

        if hasattr(self, "MenuJugador"):
            self.MenuJugador.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )

            self.MenuJugador.raise_()

        if hasattr(self, "btn_personaje"):
            self.btn_personaje.show()
            self.btn_personaje.raise_()

        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        if hasattr(
            self,
            "logo_reutilizable"
        ):
            self.logo_reutilizable.actualizar()

        if hasattr(
            self,
            "botones_responsivos"
        ):
            self.botones_responsivos.ajustar()

        if hasattr(
            self,
            "pixmap_personaje_original"
        ):
            self.actualizar_imagen_personaje()

        self.centrar_nombre_personaje()

        if self.lbl_nombre_personaje_actual is not None:
            self.lbl_nombre_personaje_actual.raise_()

        if self.lbl_imagen_personaje_actual is not None:
            self.lbl_imagen_personaje_actual.raise_()

        if hasattr(self, "efectos_hover"):
            QtCore.QTimer.singleShot(
                0,
                self.actualizar_hover_botones
            )

        super().resizeEvent(event)