from __future__ import annotations

import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic

from AjusteResponsive import BotonesResponsivos
from quitar_barra import quitar
from Transicion import FormTransicion
from juego.sistemas.audio import gestor_audio


# =============================================================
# RESOLUCIÓN BASE DEL DISEÑO
# =============================================================

ANCHO_BASE = 1920
ALTO_BASE = 1080


# =============================================================
# FUNCIONES PARA ENCONTRAR ARCHIVOS
# =============================================================

def encontrar_raiz_proyecto(
    archivo_actual: Path,
) -> Path:
    """
    Encuentra la carpeta PROYECTO_EDUCORE buscando las
    carpetas juego y assets.
    """

    carpeta_actual = archivo_actual.resolve().parent

    posibles_carpetas = (
        carpeta_actual,
        *carpeta_actual.parents,
    )

    for carpeta in posibles_carpetas:
        if (
            (carpeta / "juego").is_dir()
            and (carpeta / "assets").is_dir()
        ):
            return carpeta

    return carpeta_actual


def primer_archivo_existente(
    rutas: list[Path],
) -> Path | None:
    for ruta in rutas:
        if ruta.is_file():
            return ruta

    return None


def buscar_imagen(
    nombre_base: str,
    carpetas: list[Path],
) -> Path | None:
    """
    Busca una imagen por su nombre sin depender de que
    la extensión sea png, jpg, jpeg o webp.
    """

    extensiones = (
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
    )

    # Primero intenta las rutas directas.
    for carpeta in carpetas:
        for extension in extensiones:
            ruta = carpeta / f"{nombre_base}{extension}"

            if ruta.is_file():
                return ruta

    # Búsqueda de respaldo sin distinguir mayúsculas.
    for carpeta in carpetas:
        if not carpeta.is_dir():
            continue

        try:
            for archivo in carpeta.iterdir():
                if not archivo.is_file():
                    continue

                if (
                    archivo.stem.lower() == nombre_base.lower()
                    and archivo.suffix.lower() in extensiones
                ):
                    return archivo

        except (OSError, PermissionError):
            continue

    return None


def buscar_archivo_recursivamente(
    nombre_archivo: str,
    carpetas: list[Path],
) -> Path | None:
    carpetas_ignoradas = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
    }

    for carpeta in carpetas:
        if not carpeta.is_dir():
            continue

        try:
            for archivo in carpeta.rglob(nombre_archivo):
                if any(
                    parte in carpetas_ignoradas
                    for parte in archivo.parts
                ):
                    continue

                if archivo.is_file():
                    return archivo

        except (OSError, PermissionError):
            continue

    return None


# =============================================================
# FONDO RESPONSIVO
# =============================================================

class FondoImagen(QtWidgets.QLabel):
    def __init__(
        self,
        ventana: QtWidgets.QWidget,
        ruta_imagen: Path,
    ):
        super().__init__(ventana)

        self.pixmap_original = QtGui.QPixmap(
            str(ruta_imagen)
        )

        if self.pixmap_original.isNull():
            raise FileNotFoundError(
                "No se pudo cargar el fondo:\n"
                f"{ruta_imagen}"
            )

        self.setScaledContents(True)

        self.setGeometry(
            0,
            0,
            ventana.width(),
            ventana.height(),
        )

        self.setPixmap(
            self.pixmap_original
        )

        self.lower()

    def actualizar_tamano(
        self,
        ancho: int,
        alto: int,
    ):
        self.setGeometry(
            0,
            0,
            ancho,
            alto,
        )


# =============================================================
# FORMULARIO DE AJUSTES
# =============================================================

class Ajustes(QtWidgets.QWidget):
    def __init__(
        self,
        ventana_anterior: QtWidgets.QWidget | None = None,
        jugador=None,
        desde_juego: bool = False,
    ):
        super().__init__()

        quitar(self)

        self.ventana_anterior = ventana_anterior
        self.jugador = jugador
        self.desde_juego = bool(desde_juego)

        self._transicion_regreso = None
        self._volviendo = False
        self._maximizado_inicial = False

        # Pixmaps originales de los labels.
        self._pixmaps_labels = {}

        # Geometrías originales para hacer responsivos
        # sliders y labels.
        self._geometrias_base = {}

        # Valores de respaldo.
        self._ultimo_volumen_sonido = 100
        self._ultimo_volumen_efectos = 100

        # Estado local de efectos. Se utiliza aunque
        # gestor_audio todavía no tenga métodos separados.
        self._volumen_efectos = 100
        self._efectos_silenciados = False

        # -----------------------------------------------------
        # Localizar carpetas
        # -----------------------------------------------------

        archivo_actual = Path(__file__).resolve()

        self.carpeta_actual = archivo_actual.parent

        self.proyecto_dir = encontrar_raiz_proyecto(
            archivo_actual
        )

        # En tu proyecto EXPO-DISEÑOS está dentro de
        # PROYECTO_EDUCORE.
        posibles_expo = [
            self.proyecto_dir
            / "EXPO-DISEÑOS",

            self.proyecto_dir.parent
            / "EXPO-DISEÑOS",
        ]

        self.expo_dir = next(
            (
                ruta
                for ruta in posibles_expo
                if ruta.is_dir()
            ),
            self.proyecto_dir / "EXPO-DISEÑOS",
        )

        print(
            "[AJUSTES] Proyecto:",
            self.proyecto_dir,
        )

        print(
            "[AJUSTES] EXPO-DISEÑOS:",
            self.expo_dir,
        )

        # -----------------------------------------------------
        # Localizar Ajustes.ui
        # -----------------------------------------------------

        posibles_rutas_ui = [
            self.expo_dir
            / "DESIGNER"
            / "Ajustes.ui",

            self.carpeta_actual
            / "Ajustes.ui",

            self.proyecto_dir
            / "Ajustes.ui",

            self.proyecto_dir
            / "interfaces"
            / "Ajustes.ui",

            self.proyecto_dir
            / "ui"
            / "Ajustes.ui",
        ]

        ruta_ui = primer_archivo_existente(
            posibles_rutas_ui
        )

        if ruta_ui is None:
            ruta_ui = buscar_archivo_recursivamente(
                "Ajustes.ui",
                [
                    self.proyecto_dir,
                    self.expo_dir,
                ],
            )

        if ruta_ui is None:
            raise FileNotFoundError(
                "No se encontró Ajustes.ui.\n\n"
                "La ubicación esperada es:\n"
                f"{self.expo_dir / 'DESIGNER' / 'Ajustes.ui'}"
            )

        print(
            "[AJUSTES] UI:",
            ruta_ui,
        )

        # -----------------------------------------------------
        # Cargar el formulario
        # -----------------------------------------------------

        uic.loadUi(
            str(ruta_ui),
            self,
        )

        self.setWindowTitle(
            "Ajustes - EduCore"
        )

        self.resize(
            ANCHO_BASE,
            ALTO_BASE,
        )

        self.setMinimumSize(
            0,
            0,
        )

        self.setMaximumSize(
            16777215,
            16777215,
        )

        if self.desde_juego:
            self.setWindowFlag(
                QtCore.Qt.WindowType.WindowStaysOnTopHint,
                True,
            )

        # -----------------------------------------------------
        # Obtener controles del formulario
        # -----------------------------------------------------

        self.frame_ajustes = self.findChild(
            QtWidgets.QFrame,
            "Ajustes",
        )

        self.btn_muteefectos = self.findChild(
            QtWidgets.QPushButton,
            "btn_muteefectos",
        )

        self.btn_silenciar = self.findChild(
            QtWidgets.QPushButton,
            "btn_silenciar",
        )

        self.hsz_efectos = self.findChild(
            QtWidgets.QSlider,
            "hsz_efectos",
        )

        self.hzs_sonido = self.findChild(
            QtWidgets.QSlider,
            "hzs_sonido",
        )

        self.label = self.findChild(
            QtWidgets.QLabel,
            "label",
        )

        self.lbl_efectos = self.findChild(
            QtWidgets.QLabel,
            "lbl_efectos",
        )

        self.lbl_logo = self.findChild(
            QtWidgets.QLabel,
            "lbl_logo",
        )

        self.lbl_sonidogeneral = self.findChild(
            QtWidgets.QLabel,
            "lbl_sonidogeneral",
        )

        self.pushButton = self.findChild(
            QtWidgets.QPushButton,
            "pushButton",
        )

        controles_obligatorios = {
            "QFrame Ajustes": self.frame_ajustes,
            "btn_muteefectos": self.btn_muteefectos,
            "btn_silenciar": self.btn_silenciar,
            "hsz_efectos": self.hsz_efectos,
            "hzs_sonido": self.hzs_sonido,
            "label": self.label,
            "lbl_efectos": self.lbl_efectos,
            "lbl_logo": self.lbl_logo,
            "lbl_sonidogeneral": self.lbl_sonidogeneral,
            "pushButton": self.pushButton,
        }

        controles_faltantes = [
            nombre
            for nombre, control
            in controles_obligatorios.items()
            if control is None
        ]

        if controles_faltantes:
            raise AttributeError(
                "Faltan estos controles en Ajustes.ui:\n\n"
                + "\n".join(controles_faltantes)
            )

        # -----------------------------------------------------
        # Configurar frame principal
        # -----------------------------------------------------

        self.frame_ajustes.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        # Conserva el stylesheet que ya tenía el formulario.
        estilo_frame = self.frame_ajustes.styleSheet()

        self.frame_ajustes.setStyleSheet(
            estilo_frame
            + """
            QFrame#Ajustes {
                background-color: transparent;
                border: none;
            }
            """
        )

        # -----------------------------------------------------
        # Fondo de Ajustes
        # -----------------------------------------------------

        ruta_fondo = buscar_imagen(
            "Ajustes",
            [
                self.proyecto_dir
                / "assets"
                / "DISEÑOS",

                self.proyecto_dir
                / "assets"
                / "diseños",

                self.expo_dir,

                self.carpeta_actual,
            ],
        )

        if ruta_fondo is None:
            raise FileNotFoundError(
                "No se encontró la imagen de fondo Ajustes.\n\n"
                "Colócala en:\n"
                f"{self.proyecto_dir / 'assets' / 'DISEÑOS'}"
            )

        self.fondo = FondoImagen(
            self,
            ruta_fondo,
        )

        # -----------------------------------------------------
        # Rutas de imágenes indicadas
        # -----------------------------------------------------

        carpeta_logo = (
            self.expo_dir
            / "Logo"
        )

        carpeta_botones = (
            self.expo_dir
            / "Botones"
            / "otros"
        )

        ruta_logo = buscar_imagen(
            "logo_confondo",
            [carpeta_logo],
        )

        ruta_titulo_sonido = buscar_imagen(
            "titulo_sonido",
            [carpeta_logo],
        )

        ruta_titulo_efectos = buscar_imagen(
            "titulo_efectos",
            [carpeta_logo],
        )

        self.ruta_boton_mute = buscar_imagen(
            "boton_mute",
            [carpeta_botones],
        )

        self.ruta_boton_sonido = buscar_imagen(
            "boton_sonido",
            [carpeta_botones],
        )

        imagenes_faltantes = []

        if ruta_logo is None:
            imagenes_faltantes.append(
                str(carpeta_logo / "logo_confondo.png")
            )

        if ruta_titulo_sonido is None:
            imagenes_faltantes.append(
                str(carpeta_logo / "titulo_sonido.png")
            )

        if ruta_titulo_efectos is None:
            imagenes_faltantes.append(
                str(carpeta_logo / "titulo_efectos.png")
            )

        if self.ruta_boton_mute is None:
            imagenes_faltantes.append(
                str(carpeta_botones / "boton_mute.png")
            )

        if self.ruta_boton_sonido is None:
            imagenes_faltantes.append(
                str(carpeta_botones / "boton_sonido.png")
            )

        if imagenes_faltantes:
            raise FileNotFoundError(
                "No se encontraron estas imágenes:\n\n"
                + "\n".join(imagenes_faltantes)
            )

        # -----------------------------------------------------
        # Cargar pixmaps de los labels
        # -----------------------------------------------------

        self._registrar_pixmap_label(
            self.lbl_logo,
            ruta_logo,
        )

        self._registrar_pixmap_label(
            self.lbl_sonidogeneral,
            ruta_titulo_sonido,
        )

        self._registrar_pixmap_label(
            self.lbl_efectos,
            ruta_titulo_efectos,
        )

        # -----------------------------------------------------
        # Preparar iconos de sonido
        # -----------------------------------------------------

        self.icono_mute = QtGui.QIcon(
            str(self.ruta_boton_mute)
        )

        self.icono_sonido = QtGui.QIcon(
            str(self.ruta_boton_sonido)
        )

        self._configurar_boton_audio(
            self.btn_silenciar
        )

        self._configurar_boton_audio(
            self.btn_muteefectos
        )

        # -----------------------------------------------------
        # Guardar posiciones originales
        # -----------------------------------------------------

        self._guardar_geometrias_base()

        # -----------------------------------------------------
        # Botones responsivos
        # -----------------------------------------------------

        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=[
                self.btn_silenciar,
                self.btn_muteefectos,
                self.pushButton,
            ],
            ancho_base=ANCHO_BASE,
            alto_base=ALTO_BASE,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        # -----------------------------------------------------
        # Configurar sliders y eventos
        # -----------------------------------------------------

        self._configurar_controles()
        self._conectar_eventos()

        try:
            gestor_audio.recargar()

        except Exception as error:
            print(
                "[AJUSTES] No se pudo recargar el audio:",
                error,
            )

        self.actualizar_controles_audio()
        self._actualizar_interfaz()

        # Garantiza apertura maximizada.
        QtCore.QTimer.singleShot(
            0,
            self._mostrar_maximizado,
        )

    # =========================================================
    # CONFIGURAR BOTÓN DE AUDIO
    # =========================================================

    def _configurar_boton_audio(
        self,
        boton: QtWidgets.QPushButton,
    ):
        boton.setText("")

        boton.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )

        boton.setFlat(True)

        # Quita cualquier border-image antiguo para que el
        # icono dinámico pueda visualizarse.
        boton.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }

            QPushButton:hover {
                background-color: transparent;
                border: none;
            }

            QPushButton:pressed {
                background-color: transparent;
                border: none;
            }
            """
        )

    # =========================================================
    # REGISTRAR PIXMAP DE UN LABEL
    # =========================================================

    def _registrar_pixmap_label(
        self,
        label: QtWidgets.QLabel,
        ruta_imagen: Path,
    ):
        pixmap = QtGui.QPixmap(
            str(ruta_imagen)
        )

        if pixmap.isNull():
            raise RuntimeError(
                "No se pudo cargar la imagen:\n"
                f"{ruta_imagen}"
            )

        self._pixmaps_labels[label] = pixmap

        label.setText("")

        label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        label.setScaledContents(False)

        label.setStyleSheet(
            f"""
            QLabel#{label.objectName()} {{
                background-color: transparent;
                border: none;
            }}
            """
        )

    # =========================================================
    # GUARDAR GEOMETRÍAS BASE
    # =========================================================

    def _guardar_geometrias_base(self):
        controles = [
            self.hzs_sonido,
            self.hsz_efectos,
            self.label,
            self.lbl_logo,
            self.lbl_sonidogeneral,
            self.lbl_efectos,
        ]

        for control in controles:
            self._geometrias_base[control] = QtCore.QRect(
                control.geometry()
            )

    # =========================================================
    # CONFIGURAR CONTROLES
    # =========================================================

    def _configurar_controles(self):
        for slider in (
            self.hzs_sonido,
            self.hsz_efectos,
        ):
            slider.setOrientation(
                QtCore.Qt.Orientation.Horizontal
            )

            slider.setRange(
                0,
                100,
            )

            slider.setSingleStep(1)
            slider.setPageStep(5)
            slider.setTracking(True)

            slider.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.PointingHandCursor
                )
            )

        self.label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.pushButton.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )

    # =========================================================
    # CONECTAR EVENTOS
    # =========================================================

    def _conectar_eventos(self):
        self.hzs_sonido.valueChanged.connect(
            self.cambiar_volumen_sonido
        )

        self.hsz_efectos.valueChanged.connect(
            self.cambiar_volumen_efectos
        )

        self.btn_silenciar.clicked.connect(
            self.cambiar_silencio_sonido
        )

        self.btn_muteefectos.clicked.connect(
            self.cambiar_silencio_efectos
        )

        self.pushButton.clicked.connect(
            self.volver
        )

        if hasattr(
            gestor_audio,
            "volumen_cambiado",
        ):
            gestor_audio.volumen_cambiado.connect(
                self.actualizar_controles_audio
            )

        if hasattr(
            gestor_audio,
            "silencio_cambiado",
        ):
            gestor_audio.silencio_cambiado.connect(
                self.actualizar_controles_audio
            )

        if hasattr(
            gestor_audio,
            "volumen_efectos_cambiado",
        ):
            gestor_audio.volumen_efectos_cambiado.connect(
                self.actualizar_controles_audio
            )

        if hasattr(
            gestor_audio,
            "silencio_efectos_cambiado",
        ):
            gestor_audio.silencio_efectos_cambiado.connect(
                self.actualizar_controles_audio
            )

    # =========================================================
    # CAMBIAR VOLUMEN GENERAL
    # =========================================================

    def cambiar_volumen_sonido(
        self,
        valor: int,
    ):
        valor = max(
            0,
            min(100, int(valor)),
        )

        if valor > 0:
            self._ultimo_volumen_sonido = valor

            # Mover el slider por encima de cero reactiva
            # el sonido cuando estaba silenciado.
            if bool(
                getattr(
                    gestor_audio,
                    "silenciado",
                    False,
                )
            ):
                gestor_audio.alternar_silencio()

        gestor_audio.establecer_volumen(
            valor
        )

        self.label.setText(
            f"{valor}%"
        )

        self._actualizar_iconos_audio()

    # =========================================================
    # BOTÓN SILENCIAR SONIDO GENERAL
    # =========================================================

    def cambiar_silencio_sonido(
        self,
        _checked: bool = False,
    ):
        porcentaje = self.hzs_sonido.value()

        esta_silenciado = bool(
            getattr(
                gestor_audio,
                "silenciado",
                False,
            )
        )

        # Si está en cero, restaura el último volumen.
        if porcentaje <= 0:
            volumen_restaurado = max(
                1,
                self._ultimo_volumen_sonido,
            )

            if esta_silenciado:
                gestor_audio.alternar_silencio()

            gestor_audio.establecer_volumen(
                volumen_restaurado
            )

            bloqueador = QtCore.QSignalBlocker(
                self.hzs_sonido
            )

            self.hzs_sonido.setValue(
                volumen_restaurado
            )

            del bloqueador

            self.label.setText(
                f"{volumen_restaurado}%"
            )

        else:
            gestor_audio.alternar_silencio()

        self.actualizar_controles_audio()

    # =========================================================
    # CAMBIAR VOLUMEN DE EFECTOS
    # =========================================================

    def cambiar_volumen_efectos(
        self,
        valor: int,
    ):
        valor = max(
            0,
            min(100, int(valor)),
        )

        self._volumen_efectos = valor

        if valor > 0:
            self._ultimo_volumen_efectos = valor

            if self._efectos_silenciados:
                self._efectos_silenciados = False
                self._alternar_silencio_efectos_gestor()

        self._establecer_volumen_efectos_gestor(
            valor
        )

        self._actualizar_iconos_audio()

    # =========================================================
    # BOTÓN SILENCIAR EFECTOS
    # =========================================================

    def cambiar_silencio_efectos(
        self,
        _checked: bool = False,
    ):
        porcentaje = self.hsz_efectos.value()

        if porcentaje <= 0:
            volumen_restaurado = max(
                1,
                self._ultimo_volumen_efectos,
            )

            self._efectos_silenciados = False
            self._volumen_efectos = volumen_restaurado

            bloqueador = QtCore.QSignalBlocker(
                self.hsz_efectos
            )

            self.hsz_efectos.setValue(
                volumen_restaurado
            )

            del bloqueador

            self._establecer_volumen_efectos_gestor(
                volumen_restaurado
            )

        else:
            self._efectos_silenciados = (
                not self._efectos_silenciados
            )

            self._alternar_silencio_efectos_gestor()

        self._actualizar_iconos_audio()

    # =========================================================
    # COMPATIBILIDAD CON GESTOR DE EFECTOS
    # =========================================================

    def _establecer_volumen_efectos_gestor(
        self,
        valor: int,
    ):
        """
        Utiliza el método de efectos si ya existe en
        gestor_audio. Si todavía no existe, la interfaz
        sigue funcionando sin producir errores.
        """

        nombres_metodos = (
            "establecer_volumen_efectos",
            "set_volumen_efectos",
            "cambiar_volumen_efectos",
        )

        for nombre in nombres_metodos:
            metodo = getattr(
                gestor_audio,
                nombre,
                None,
            )

            if callable(metodo):
                try:
                    metodo(valor)
                except Exception as error:
                    print(
                        "[AJUSTES] Error al cambiar "
                        "el volumen de efectos:",
                        error,
                    )

                return

    def _alternar_silencio_efectos_gestor(self):
        nombres_metodos = (
            "alternar_silencio_efectos",
            "alternar_mute_efectos",
            "silenciar_efectos",
        )

        for nombre in nombres_metodos:
            metodo = getattr(
                gestor_audio,
                nombre,
                None,
            )

            if callable(metodo):
                try:
                    metodo()
                except Exception as error:
                    print(
                        "[AJUSTES] Error al silenciar "
                        "los efectos:",
                        error,
                    )

                return

    # =========================================================
    # ACTUALIZAR CONTROLES DE AUDIO
    # =========================================================

    def actualizar_controles_audio(
        self,
        *_args,
    ):
        porcentaje = int(
            getattr(
                gestor_audio,
                "porcentaje_actual",
                self.hzs_sonido.value(),
            )
        )

        porcentaje = max(
            0,
            min(100, porcentaje),
        )

        if porcentaje > 0:
            self._ultimo_volumen_sonido = porcentaje

        bloqueador = QtCore.QSignalBlocker(
            self.hzs_sonido
        )

        self.hzs_sonido.setValue(
            porcentaje
        )

        del bloqueador

        self.label.setText(
            f"{porcentaje}%"
        )

        esta_silenciado = bool(
            getattr(
                gestor_audio,
                "silenciado",
                False,
            )
        )

        if esta_silenciado or porcentaje <= 0:
            self.btn_silenciar.setToolTip(
                "Activar sonido"
            )

            self.btn_silenciar.setAccessibleName(
                "Activar sonido"
            )

        else:
            self.btn_silenciar.setToolTip(
                "Silenciar sonido"
            )

            self.btn_silenciar.setAccessibleName(
                "Silenciar sonido"
            )

        porcentaje_efectos = int(
            getattr(
                gestor_audio,
                "porcentaje_efectos_actual",
                self.hsz_efectos.value(),
            )
        )

        porcentaje_efectos = max(
            0,
            min(100, porcentaje_efectos),
        )

        self._volumen_efectos = int(
            getattr(
                gestor_audio,
                "volumen_efectos",
                porcentaje_efectos,
            )
        )

        self._efectos_silenciados = bool(
            getattr(
                gestor_audio,
                "efectos_silenciados",
                porcentaje_efectos <= 0,
            )
        )

        ultimo_volumen_efectos = int(
            getattr(
                gestor_audio,
                "ultimo_volumen_efectos",
                self._volumen_efectos,
            )
        )

        if ultimo_volumen_efectos > 0:
            self._ultimo_volumen_efectos = ultimo_volumen_efectos

        bloqueador_efectos = QtCore.QSignalBlocker(
            self.hsz_efectos
        )

        self.hsz_efectos.setValue(
            porcentaje_efectos
        )

        del bloqueador_efectos

        if self._efectos_silenciados or porcentaje_efectos <= 0:
            texto_efectos = "Activar efectos"
        else:
            texto_efectos = "Silenciar efectos"

        self.btn_muteefectos.setToolTip(texto_efectos)
        self.btn_muteefectos.setAccessibleName(texto_efectos)

        self._actualizar_iconos_audio()

    # =========================================================
    # CAMBIAR IMÁGENES MUTE/SONIDO
    # =========================================================

    def _actualizar_iconos_audio(self):
        volumen_sonido = self.hzs_sonido.value()

        sonido_silenciado = bool(
            getattr(
                gestor_audio,
                "silenciado",
                False,
            )
        )

        # Sonido general.
        if (
            volumen_sonido <= 0
            or sonido_silenciado
        ):
            self.btn_silenciar.setIcon(
                self.icono_mute
            )
        else:
            self.btn_silenciar.setIcon(
                self.icono_sonido
            )

        # Efectos.
        if (
            self.hsz_efectos.value() <= 0
            or self._efectos_silenciados
        ):
            self.btn_muteefectos.setIcon(
                self.icono_mute
            )
        else:
            self.btn_muteefectos.setIcon(
                self.icono_sonido
            )

        self._ajustar_tamano_iconos()

    # =========================================================
    # AJUSTAR TAMAÑO DE ICONOS
    # =========================================================

    def _ajustar_tamano_iconos(self):
        for boton in (
            self.btn_silenciar,
            self.btn_muteefectos,
        ):
            ancho = max(
                1,
                boton.width(),
            )

            alto = max(
                1,
                boton.height(),
            )

            boton.setIconSize(
                QtCore.QSize(
                    ancho,
                    alto,
                )
            )

    # =========================================================
    # AJUSTAR PIXMAPS DE LABELS
    # =========================================================

    def _actualizar_pixmaps_labels(self):
        for label, pixmap_original in (
            self._pixmaps_labels.items()
        ):
            if (
                label.width() <= 0
                or label.height() <= 0
            ):
                continue

            pixmap_escalado = pixmap_original.scaled(
                label.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.FastTransformation,
            )

            label.setPixmap(
                pixmap_escalado
            )

            label.show()
            label.raise_()

    # =========================================================
    # AJUSTAR LABELS Y SLIDERS
    # =========================================================

    def _ajustar_controles_responsivos(self):
        if not self._geometrias_base:
            return

        escala_x = self.width() / ANCHO_BASE
        escala_y = self.height() / ALTO_BASE

        for control, geometria in (
            self._geometrias_base.items()
        ):
            control.setGeometry(
                round(
                    geometria.x() * escala_x
                ),
                round(
                    geometria.y() * escala_y
                ),
                max(
                    1,
                    round(
                        geometria.width() * escala_x
                    ),
                ),
                max(
                    1,
                    round(
                        geometria.height() * escala_y
                    ),
                ),
            )

    # =========================================================
    # ACTUALIZAR CAPAS
    # =========================================================

    def _actualizar_capas(self):
        if hasattr(self, "fondo"):
            self.fondo.lower()

        if self.frame_ajustes is not None:
            self.frame_ajustes.raise_()

        controles_superiores = [
            self.lbl_logo,
            self.lbl_sonidogeneral,
            self.lbl_efectos,
            self.label,
            self.hzs_sonido,
            self.hsz_efectos,
            self.btn_silenciar,
            self.btn_muteefectos,
            self.pushButton,
        ]

        for control in controles_superiores:
            if control is not None:
                control.show()
                control.raise_()

    # =========================================================
    # ACTUALIZAR TODA LA INTERFAZ
    # =========================================================

    def _actualizar_interfaz(self):
        self._ajustar_controles_responsivos()

        if hasattr(
            self,
            "botones_responsivos",
        ):
            self.botones_responsivos.ajustar()

        self._actualizar_pixmaps_labels()
        self._actualizar_iconos_audio()
        self._actualizar_capas()

    # =========================================================
    # MOSTRAR MAXIMIZADO
    # =========================================================

    def _mostrar_maximizado(self):
        if self._maximizado_inicial:
            return

        self._maximizado_inicial = True

        self.showMaximized()
        self.raise_()
        self.activateWindow()

        QtCore.QTimer.singleShot(
            0,
            self._actualizar_interfaz,
        )

    # =========================================================
    # VOLVER
    # =========================================================

    def volver(
        self,
        _checked: bool = False,
    ):
        if self.ventana_anterior is None:
            self._volviendo = True
            self.close()

            if self.desde_juego:
                aplicacion = (
                    QtWidgets.QApplication.instance()
                )

                if aplicacion is not None:
                    QtCore.QTimer.singleShot(
                        0,
                        aplicacion.quit,
                    )

            return

        self._volviendo = True

        try:
            self._transicion_regreso = FormTransicion(
                self,
                self.ventana_anterior,
                guardar_actual=False,
            )

        except TypeError:
            try:
                self._transicion_regreso = FormTransicion(
                    self,
                    self.ventana_anterior,
                )

            except Exception as error:
                self._volver_sin_transicion(
                    error
                )

        except Exception as error:
            self._volver_sin_transicion(
                error
            )

    def _volver_sin_transicion(
        self,
        error: Exception,
    ):
        print(
            "[AJUSTES] No se pudo ejecutar "
            "la transición:",
            error,
        )

        if self.ventana_anterior is not None:
            self.ventana_anterior.showMaximized()
            self.ventana_anterior.raise_()
            self.ventana_anterior.activateWindow()

        self.close()

    # =========================================================
    # EVENTO AL MOSTRAR
    # =========================================================

    def showEvent(
        self,
        event: QtGui.QShowEvent,
    ):
        super().showEvent(event)

        try:
            gestor_audio.recargar()

        except Exception as error:
            print(
                "[AJUSTES] No se pudo recargar el audio:",
                error,
            )

        self.actualizar_controles_audio()

        QtCore.QTimer.singleShot(
            0,
            self._actualizar_interfaz,
        )

    # =========================================================
    # EVENTO AL CAMBIAR TAMAÑO
    # =========================================================

    def resizeEvent(
        self,
        event: QtGui.QResizeEvent,
    ):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height(),
            )

            self.fondo.lower()

        if hasattr(
            self,
            "frame_ajustes",
        ) and self.frame_ajustes is not None:
            self.frame_ajustes.setGeometry(
                0,
                0,
                self.width(),
                self.height(),
            )

            self.frame_ajustes.raise_()

        if hasattr(
            self,
            "_geometrias_base",
        ):
            self._actualizar_interfaz()

        super().resizeEvent(event)

    # =========================================================
    # EVENTO AL CERRAR
    # =========================================================

    def closeEvent(
        self,
        event: QtGui.QCloseEvent,
    ):
        try:
            gestor_audio.guardar()

        except Exception as error:
            print(
                "[AJUSTES] No se pudo guardar el audio:",
                error,
            )

        if (
            self.ventana_anterior is not None
            and not self._volviendo
        ):
            self.ventana_anterior.showMaximized()
            self.ventana_anterior.raise_()
            self.ventana_anterior.activateWindow()

        event.accept()

        if self.desde_juego:
            aplicacion = (
                QtWidgets.QApplication.instance()
            )

            if aplicacion is not None:
                QtCore.QTimer.singleShot(
                    0,
                    aplicacion.quit,
                )


# =============================================================
# EJECUCIÓN INDEPENDIENTE
# =============================================================

if __name__ == "__main__":
    desde_juego = (
        "--desde-juego" in sys.argv
    )

    aplicacion = (
        QtWidgets.QApplication.instance()
    )

    if aplicacion is None:
        aplicacion = QtWidgets.QApplication(
            [sys.argv[0]]
        )

    aplicacion.setQuitOnLastWindowClosed(True)

    ventana = Ajustes(
        ventana_anterior=None,
        jugador=None,
        desde_juego=desde_juego,
    )

    ventana.showMaximized()
    ventana.raise_()
    ventana.activateWindow()

    sys.exit(
        aplicacion.exec()
    )