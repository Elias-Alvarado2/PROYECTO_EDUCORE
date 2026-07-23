import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic

from AjusteResponsive import BotonesResponsivos
from CofreDiploma import CofreDiplomaMixin
from ConexionBD import ConexionBD
from Transicion import FormAnterior, FormTransicion
from ValidarVidas import validar_vidas_disponibles
from quitar_barra import quitar


class FondoImagen(QtWidgets.QLabel):
    """QLabel usado como fondo responsivo de la ventana."""

    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.ruta_imagen = Path(ruta_imagen)
        self.pixmap_original = QtGui.QPixmap(
            str(self.ruta_imagen)
        )

        if self.pixmap_original.isNull():
            raise FileNotFoundError(
                "No se pudo cargar la imagen de fondo:\n"
                f"{self.ruta_imagen}"
            )

        # Evita que el fondo bloquee los clics de los botones.
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True,
        )
        self.setScaledContents(True)
        self.setGeometry(
            0,
            0,
            ventana.width(),
            ventana.height(),
        )
        self.setPixmap(self.pixmap_original)
        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto,
        )
        self.lower()


class PintorImagenBoton(QtCore.QObject):
    """
    Dibuja una imagen directamente sobre un QPushButton.

    Recorta una sola vez los márgenes transparentes de cada archivo y guarda
    el resultado en caché. Así todos los niveles se ven del mismo tamaño sin
    agregar una pausa cada vez que se actualiza el progreso.
    """

    _cache_pixmaps = {}

    def __init__(self, boton):
        super().__init__(boton)

        self.boton = boton
        self.pixmap = QtGui.QPixmap()

        boton.installEventFilter(self)

    def establecer_imagen(self, ruta_imagen):
        ruta_imagen = Path(ruta_imagen).resolve()
        clave_cache = ruta_imagen.as_posix().casefold()

        pixmap_recortado = self._cache_pixmaps.get(
            clave_cache
        )

        if pixmap_recortado is None:
            pixmap_original = QtGui.QPixmap(
                str(ruta_imagen)
            )

            if pixmap_original.isNull():
                raise FileNotFoundError(
                    "No se pudo cargar la imagen del botón:\n"
                    f"{ruta_imagen}"
                )

            pixmap_recortado = self.recortar_transparencia(
                pixmap_original
            )
            self._cache_pixmaps[clave_cache] = pixmap_recortado

        self.pixmap = pixmap_recortado
        self.boton.update()

    @staticmethod
    def recortar_transparencia(pixmap):
        """
        Elimina el espacio transparente exterior del PNG.

        Primero utiliza createAlphaMask(), QBitmap y QRegion, que ejecutan
        el cálculo internamente en Qt y son mucho más rápidos que recorrer
        cada píxel desde MySQL. El recorrido manual queda solamente como
        respaldo de compatibilidad.
        """
        if pixmap.isNull():
            return pixmap

        imagen = pixmap.toImage().convertToFormat(
            QtGui.QImage.Format.Format_ARGB32
        )

        try:
            mascara_alpha = imagen.createAlphaMask()
            mapa_bits = QtGui.QBitmap.fromImage(
                mascara_alpha
            )
            region_visible = QtGui.QRegion(
                mapa_bits
            )
            rectangulo_visible = (
                region_visible.boundingRect()
            )

            if not rectangulo_visible.isEmpty():
                return QtGui.QPixmap.fromImage(
                    imagen.copy(
                        rectangulo_visible
                    )
                )

        except Exception:
            # Algunas instalaciones antiguas de Qt pueden no aceptar
            # directamente QRegion(QBitmap). En ese caso se usa respaldo.
            pass

        ancho = imagen.width()
        alto = imagen.height()

        izquierda = ancho
        derecha = -1
        arriba = alto
        abajo = -1

        for y in range(alto):
            for x in range(ancho):
                if QtGui.qAlpha(
                    imagen.pixel(x, y)
                ) > 0:
                    izquierda = min(
                        izquierda,
                        x,
                    )
                    derecha = max(
                        derecha,
                        x,
                    )
                    arriba = min(
                        arriba,
                        y,
                    )
                    abajo = max(
                        abajo,
                        y,
                    )

        if derecha < izquierda or abajo < arriba:
            return pixmap

        rectangulo_visible = QtCore.QRect(
            izquierda,
            arriba,
            derecha - izquierda + 1,
            abajo - arriba + 1,
        )

        return QtGui.QPixmap.fromImage(
            imagen.copy(
                rectangulo_visible
            )
        )

    def eventFilter(self, objeto, evento):
        if (
            objeto is self.boton
            and evento.type() == QtCore.QEvent.Type.Paint
            and not self.pixmap.isNull()
        ):
            pintor = QtGui.QPainter(self.boton)

            # Mantiene los píxeles definidos, sin suavizar la imagen.
            pintor.setRenderHint(
                QtGui.QPainter.RenderHint.SmoothPixmapTransform,
                False,
            )

            pintor.drawPixmap(
                self.boton.rect(),
                self.pixmap,
                self.pixmap.rect(),
            )
            pintor.end()
            return True

        return super().eventFilter(
            objeto,
            evento,
        )


class EfectoHoverBoton(QtCore.QObject):
    """
    Agranda ligeramente el botón y aumenta su sombra al pasar el cursor.

    El efecto usa como base la geometría final calculada por
    BotonesResponsivos y por la función que iguala los tamaños.
    """

    def __init__(
        self,
        boton,
        factor=1.035,
        duracion=120,
        parent=None,
    ):
        super().__init__(
            parent if parent is not None else boton
        )

        self.boton = boton
        self.factor = factor
        self.duracion = duracion
        self.cursor_encima = False
        self.geometria_normal = QtCore.QRect(
            boton.geometry()
        )

        self.animacion_geometria = QtCore.QPropertyAnimation(
            boton,
            b"geometry",
            self,
        )
        self.animacion_geometria.setDuration(
            self.duracion
        )
        self.animacion_geometria.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        self.sombra = QtWidgets.QGraphicsDropShadowEffect(
            boton
        )
        self.sombra.setColor(
            QtGui.QColor(0, 0, 0, 180)
        )
        self.sombra.setBlurRadius(10)
        self.sombra.setOffset(0, 3)

        boton.setGraphicsEffect(
            self.sombra
        )

        self.animacion_sombra = QtCore.QPropertyAnimation(
            self.sombra,
            b"blurRadius",
            self,
        )
        self.animacion_sombra.setDuration(
            self.duracion
        )
        self.animacion_sombra.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        boton.installEventFilter(
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
            rectangulo.x() - diferencia_ancho // 2,
            rectangulo.y() - diferencia_alto // 2,
            ancho_nuevo,
            alto_nuevo,
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

    def restaurar_sin_animacion(self):
        self.animacion_geometria.stop()
        self.animacion_sombra.stop()

        self.cursor_encima = False
        self.boton.setGeometry(
            self.geometria_normal
        )
        self.sombra.setBlurRadius(10)

    def establecer_geometria_base(self, geometria):
        self.animacion_geometria.stop()
        self.animacion_sombra.stop()

        self.cursor_encima = False
        self.geometria_normal = QtCore.QRect(
            geometria
        )
        self.boton.setGeometry(
            self.geometria_normal
        )
        self.sombra.setBlurRadius(10)

    def actualizar_geometria_base(self):
        self.establecer_geometria_base(
            self.boton.geometry()
        )

    def eventFilter(self, objeto, evento):
        if objeto is self.boton:
            tipo_evento = evento.type()

            if (
                tipo_evento == QtCore.QEvent.Type.Enter
                and self.boton.isEnabled()
            ):
                self.cursor_encima = True
                self.geometria_normal = QtCore.QRect(
                    self.boton.geometry()
                )

                self.boton.raise_()
                self.animar_geometria(
                    self.obtener_geometria_grande()
                )
                self.animar_sombra(28)

            elif tipo_evento == QtCore.QEvent.Type.Leave:
                if self.cursor_encima:
                    self.cursor_encima = False
                    self.animar_geometria(
                        self.geometria_normal
                    )
                    self.animar_sombra(10)

            elif tipo_evento == QtCore.QEvent.Type.EnabledChange:
                if not self.boton.isEnabled():
                    self.restaurar_sin_animacion()

        return super().eventFilter(
            objeto,
            evento,
        )


class SenalesCargaProgreso(QtCore.QObject):
    """Señales enviadas desde la tarea que consulta la base de datos."""

    terminado = QtCore.pyqtSignal(object)
    error = QtCore.pyqtSignal(str)


class TareaCargaProgreso(QtCore.QRunnable):
    """
    Consulta progreso_jugador en un hilo del QThreadPool.

    La tarea no modifica widgets. Únicamente obtiene un diccionario y lo
    entrega a la ventana principal mediante una señal.
    """

    def __init__(
        self,
        id_jugador,
        lenguaje,
    ):
        super().__init__()

        self.id_jugador = int(id_jugador)
        self.lenguaje = str(lenguaje)
        self.senales = SenalesCargaProgreso()

        self.setAutoDelete(
            True
        )

    @QtCore.pyqtSlot()
    def run(self):
        try:
            progreso = self.consultar_progreso()
            self.senales.terminado.emit(
                progreso
            )

        except Exception as error:
            self.senales.error.emit(
                str(error)
            )

    def consultar_progreso(self):
        base_datos = ConexionBD()

        # Primera opción: utiliza el método compartido con Perfil.
        if hasattr(
            base_datos,
            "obtener_progreso_perfil",
        ):
            try:
                registros = (
                    base_datos.obtener_progreso_perfil(
                        self.id_jugador
                    )
                    or []
                )

                for registro in registros:
                    lenguaje_registro = str(
                        registro.get("lenguaje")
                        or ""
                    ).strip().casefold()

                    if (
                        lenguaje_registro
                        == self.lenguaje.casefold()
                    ):
                        return dict(
                            registro
                        )

            except Exception:
                # Si ese método falla, se intenta la consulta directa.
                pass

        conexion = None
        cursor = None

        try:
            conexion = base_datos.conectar()

            if conexion is None:
                return {}

            cursor = conexion.cursor(
                dictionary=True
            )
            cursor.execute(
                """
                SELECT
                    pj.leccion_actual,
                    pj.lecciones_completadas,
                    pj.porcentaje_avance,
                    pj.prueba_desbloqueada,
                    pj.prueba_completada
                FROM progreso_jugador AS pj
                INNER JOIN lenguaje AS l
                    ON l.id_lenguaje = pj.id_lenguaje
                WHERE pj.id_jugador = %s
                  AND LOWER(TRIM(l.nombre)) = LOWER(%s)
                ORDER BY pj.ultima_actualizacion DESC
                LIMIT 1;
                """,
                (
                    self.id_jugador,
                    self.lenguaje,
                ),
            )

            return (
                cursor.fetchone()
                or {}
            )

        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

            if conexion is not None:
                try:
                    conexion.close()
                except Exception:
                    pass


class NivelesMySQL(CofreDiplomaMixin, QtWidgets.QWidget):
    """Menú de MySQL con desbloqueo progresivo de niveles."""

    LENGUAJE = "mysql"
    TOTAL_NIVELES = 5

    IMAGEN_NIVEL_BLOQUEADO = "Bloqueado"
    IMAGEN_PRUEBA_DESBLOQUEADA = "boton_prueba"
    IMAGEN_PRUEBA_BLOQUEADA = "PruebaBloqueada"

    EXTENSIONES_IMAGEN = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
    }

    def __init__(
        self,
        jugador=None,
        ventana_anterior=None,
    ):
        super().__init__()

        quitar(self)

        self.jugador = jugador
        self.ventana_anterior = ventana_anterior
        self.nivel_en_ejecucion = False
        self.menu_estaba_maximizado = True

        # Evita ejecutar varias actualizaciones iguales en el mismo ciclo.
        self._actualizacion_programada = False
        self._debe_cargar_progreso = False

        # La consulta de progreso se ejecuta fuera del hilo de la interfaz.
        # De esta manera NivelesMySQL termina de construirse rápidamente y
        # FormTransicion puede comenzar apenas se hace clic.
        self._carga_progreso_en_curso = False
        self._recarga_progreso_pendiente = False
        self._tarea_carga_progreso = None
        self._progreso_actual = {}
        self._envio_diploma_en_curso = False
        self._tarea_envio_diploma = None

        self.base_dir = Path(__file__).resolve().parent
        self.proyecto_dir = self.base_dir.parent

        self.ruta_ui = (
            self.proyecto_dir
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "NivelesMySQL.ui"
        )

        self.ruta_imagen_fondo = (
            self.proyecto_dir
            / "assets"
            / "DISEÑOS"
            / "Niveles-MySQL.png"
        )

        self.ruta_botones = (
            self.proyecto_dir
            / "EXPO-DISEÑOS"
            / "Botones"
        )

        self.validar_rutas_principales()

        uic.loadUi(
            str(self.ruta_ui),
            self,
        )
        self.inicializar_cofre_diploma()

        self.corregir_rutas_stylesheet(
            self.ruta_botones
        )

        self.resize(
            1920,
            1080,
        )
        self.setMinimumSize(
            0,
            0,
        )
        self.setMaximumSize(
            16777215,
            16777215,
        )

        self.fondo = FondoImagen(
            self,
            self.ruta_imagen_fondo,
        )

        self.botones_por_nivel = {
            1: self.btnNivel1,
            2: self.btnNivel2,
            3: self.btnNivel3,
            4: self.btnNivel4,
            5: self.btnNivel5,
        }

        # Todos los botones de nivel usan el tamaño de btnNivel1.
        self.igualar_tamano_botones_nivel()

        self.botones_niveles = [
            *self.botones_por_nivel.values(),
            self.btnComenzar,
        ]

        # Se crea solamente cuando se necesita aplicar la primera imagen.
        # Esto reduce el trabajo realizado antes de FormTransicion.
        self.indice_imagenes_botones = None

        # Mantiene vivos los filtros que dibujan cada imagen.
        self.pintores_imagen_botones = {}

        self.botones_hover = [
            self.btnVolver,
            self.btnDiploma,
            *self.botones_niveles,
        ]

        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=self.botones_hover,
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor=1.035,
                duracion=120,
                parent=self,
            )
            for boton in self.botones_hover
        ]

        self.efectos_hover_por_boton = {
            efecto.boton: efecto
            for efecto in self.efectos_hover
        }

        self.configurar_botones()
        self.conectar_eventos()
        self.poner_controles_al_frente()

        # Estado seguro mientras la consulta asíncrona todavía no termina.
        # Las imágenes definidas en Designer permanecen visibles.
        self.preparar_estado_temporal()

    # ========================================================
    # ACTUALIZACIÓN COORDINADA DE LA INTERFAZ
    # ========================================================

    def programar_actualizacion_interfaz(
        self,
        cargar_progreso=False,
    ):
        """
        Agrupa en una sola ejecución los ajustes responsivos, el tamaño
        uniforme, la carga de progreso y la actualización del hover.

        QTimer.singleShot(0, ...) no añade un delay visible; solamente evita
        que varias operaciones de Qt se ejecuten en un orden conflictivo.
        """
        self._debe_cargar_progreso = (
            self._debe_cargar_progreso
            or bool(cargar_progreso)
        )

        if self._actualizacion_programada:
            return

        self._actualizacion_programada = True

        QtCore.QTimer.singleShot(
            0,
            self._ejecutar_actualizacion_interfaz,
        )

    def _ejecutar_actualizacion_interfaz(self):
        self._actualizacion_programada = False

        cargar_progreso = self._debe_cargar_progreso
        self._debe_cargar_progreso = False

        self.restaurar_hover_botones()

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        self.igualar_tamano_botones_nivel()

        if (
            cargar_progreso
            and not self.nivel_en_ejecucion
        ):
            self.cargar_estado_niveles()

        self.poner_controles_al_frente()
        self.actualizar_hover_botones()

    # ========================================================
    # RUTAS, TAMAÑOS E IMÁGENES
    # ========================================================

    def validar_rutas_principales(self):
        if not self.ruta_ui.exists():
            raise FileNotFoundError(
                "No se encontró el archivo UI:\n"
                f"{self.ruta_ui}"
            )

        if not self.ruta_imagen_fondo.exists():
            raise FileNotFoundError(
                "No se encontró la imagen de fondo:\n"
                f"{self.ruta_imagen_fondo}"
            )

        if not self.ruta_botones.exists():
            raise FileNotFoundError(
                "No se encontró la carpeta de botones:\n"
                f"{self.ruta_botones}"
            )

    def igualar_tamano_botones_nivel(self):
        """
        Iguala btnNivel2...btnNivel5 al tamaño actual de btnNivel1.

        Conserva el centro de cada botón para no modificar su distribución.
        La prueba final mantiene su tamaño horizontal independiente.
        """
        if not hasattr(self, "botones_por_nivel"):
            return

        boton_referencia = self.botones_por_nivel.get(1)

        if boton_referencia is None:
            return

        ancho_uniforme = boton_referencia.width()
        alto_uniforme = boton_referencia.height()

        if ancho_uniforme <= 0 or alto_uniforme <= 0:
            return

        for numero_nivel, boton in self.botones_por_nivel.items():
            if numero_nivel == 1:
                continue

            geometria = boton.geometry()
            centro_x = (
                geometria.x()
                + geometria.width() // 2
            )
            centro_y = (
                geometria.y()
                + geometria.height() // 2
            )

            nueva_x = (
                centro_x
                - ancho_uniforme // 2
            )
            nueva_y = (
                centro_y
                - alto_uniforme // 2
            )

            boton.setMinimumSize(
                0,
                0,
            )
            boton.setMaximumSize(
                16777215,
                16777215,
            )
            boton.setGeometry(
                nueva_x,
                nueva_y,
                ancho_uniforme,
                alto_uniforme,
            )

        for boton in self.botones_por_nivel.values():
            boton.update()

    def crear_indice_imagenes_botones(self):
        """
        Guarda una ruta por cada nombre de imagen, sin importar mayúsculas,
        minúsculas o extensión. También revisa las subcarpetas de Botones.
        """
        indice = {}

        for archivo in self.ruta_botones.rglob("*"):
            if not archivo.is_file():
                continue

            if archivo.suffix.lower() not in self.EXTENSIONES_IMAGEN:
                continue

            clave = archivo.stem.strip().casefold()

            # Los archivos de MySQL utilizan nombres específicos:
            # boton1...boton5, BotonDes_1...BotonDes_5,
            # Bloqueado, boton_prueba y PruebaBloqueada.
            indice.setdefault(
                clave,
                archivo.resolve(),
            )

        return indice

    def obtener_ruta_imagen_boton(self, nombre_imagen):
        # El índice se construye de forma perezosa para que __init__ no
        # recorra la carpeta antes de que FormTransicion pueda comenzar.
        if self.indice_imagenes_botones is None:
            self.indice_imagenes_botones = (
                self.crear_indice_imagenes_botones()
            )

        clave = str(
            nombre_imagen
        ).strip().casefold()

        ruta = self.indice_imagenes_botones.get(
            clave
        )

        if ruta is None:
            nombres_disponibles = sorted(
                archivo.stem
                for archivo
                in self.indice_imagenes_botones.values()
            )

            raise FileNotFoundError(
                "No se encontró la imagen del botón "
                f"'{nombre_imagen}' dentro de:\n"
                f"{self.ruta_botones}\n\n"
                "Imágenes detectadas:\n"
                + "\n".join(nombres_disponibles)
            )

        return ruta

    def aplicar_imagen_boton(
        self,
        boton,
        nombre_imagen,
    ):
        """
        Recorta los márgenes transparentes y ocupa todo el QPushButton.
        """
        ruta_imagen = self.obtener_ruta_imagen_boton(
            nombre_imagen
        )

        boton.setText("")
        boton.setIcon(
            QtGui.QIcon()
        )
        boton.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }

            QPushButton:hover,
            QPushButton:pressed,
            QPushButton:disabled {
                background: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
            """
        )

        pintor = self.pintores_imagen_botones.get(
            boton
        )

        if pintor is None:
            pintor = PintorImagenBoton(
                boton
            )
            self.pintores_imagen_botones[boton] = pintor

        pintor.establecer_imagen(
            ruta_imagen
        )

    def corregir_rutas_stylesheet(self, ruta_botones):
        ruta_absoluta = (
            ruta_botones.resolve().as_posix()
        )

        controles = [
            self,
            *self.findChildren(QtWidgets.QWidget),
        ]

        for control in controles:
            estilo_original = control.styleSheet()

            if not estilo_original:
                continue

            estilo_corregido = estilo_original
            estilo_corregido = estilo_corregido.replace(
                'url("../Botones/',
                f'url("{ruta_absoluta}/',
            )
            estilo_corregido = estilo_corregido.replace(
                "url('../Botones/",
                f"url('{ruta_absoluta}/",
            )
            estilo_corregido = estilo_corregido.replace(
                "url(../Botones/",
                f"url({ruta_absoluta}/",
            )

            if estilo_corregido != estilo_original:
                control.setStyleSheet(
                    estilo_corregido
                )

    def poner_controles_al_frente(self):
        if hasattr(self, "fondo"):
            self.fondo.lower()

        nombres = (
            "btnVolver",
            "btnNivel1",
            "btnNivel2",
            "btnNivel3",
            "btnNivel4",
            "btnNivel5",
            "btnComenzar",
            "btnDiploma",
        )

        for nombre in nombres:
            control = getattr(
                self,
                nombre,
                None,
            )

            if control is not None:
                control.raise_()

    # ========================================================
    # PROGRESO Y ESTADO DE LOS BOTONES
    # ========================================================

    def es_sesion_administrador(self):
        if not isinstance(
            self.jugador,
            dict,
        ):
            return False

        rol = str(
            self.jugador.get(
                "rol",
                "",
            )
        ).strip().casefold()

        return (
            rol == "administrador"
            or self.jugador.get("id_admin") is not None
        )

    def obtener_id_jugador(self):
        if isinstance(
            self.jugador,
            dict,
        ):
            valor = self.jugador.get(
                "id_jugador"
            )
        elif (
            isinstance(self.jugador, int)
            and not isinstance(self.jugador, bool)
        ):
            valor = self.jugador
        else:
            valor = None

        try:
            return (
                int(valor)
                if valor is not None
                else None
            )
        except (TypeError, ValueError):
            return None

    def consultar_progreso_mysql(self):
        id_jugador = self.obtener_id_jugador()

        if id_jugador is None:
            return {}

        base_datos = ConexionBD()

        if hasattr(
            base_datos,
            "obtener_progreso_perfil",
        ):
            try:
                registros = (
                    base_datos.obtener_progreso_perfil(
                        id_jugador
                    )
                    or []
                )

                for registro in registros:
                    lenguaje = str(
                        registro.get("lenguaje")
                        or ""
                    ).strip().casefold()

                    if lenguaje == self.LENGUAJE.casefold():
                        return dict(
                            registro
                        )

            except Exception as error:
                print(
                    "[NIVELES MYSQL] No se pudo consultar "
                    "el progreso con obtener_progreso_perfil():",
                    error,
                )

        conexion = None
        cursor = None

        try:
            conexion = base_datos.conectar()

            if conexion is None:
                return {}

            cursor = conexion.cursor(
                dictionary=True
            )
            cursor.execute(
                """
                SELECT
                    pj.leccion_actual,
                    pj.lecciones_completadas,
                    pj.porcentaje_avance,
                    pj.prueba_desbloqueada,
                    pj.prueba_completada
                FROM progreso_jugador AS pj
                INNER JOIN lenguaje AS l
                    ON l.id_lenguaje = pj.id_lenguaje
                WHERE pj.id_jugador = %s
                  AND LOWER(TRIM(l.nombre)) = LOWER(%s)
                ORDER BY pj.ultima_actualizacion DESC
                LIMIT 1;
                """,
                (
                    id_jugador,
                    self.LENGUAJE,
                ),
            )

            return (
                cursor.fetchone()
                or {}
            )

        except Exception as error:
            print(
                "[NIVELES MYSQL] No se pudo consultar "
                "el progreso:",
                error,
            )
            return {}

        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

            if conexion is not None:
                try:
                    conexion.close()
                except Exception:
                    pass

    def calcular_niveles_completados(self, progreso):
        progreso = progreso if isinstance(progreso, dict) else {}

        try:
            porcentaje = float(
                progreso.get("porcentaje_avance") or 0
            )
        except (TypeError, ValueError):
            porcentaje = 0

        try:
            lecciones = int(
                progreso.get("lecciones_completadas") or 0
            )
        except (TypeError, ValueError):
            lecciones = 0

        try:
            prueba_completada = bool(
                int(progreso.get("prueba_completada") or 0)
            )
        except (TypeError, ValueError):
            prueba_completada = False

        if prueba_completada:
            return self.TOTAL_NIVELES

        porcentaje = max(0, min(porcentaje, 100))
        lecciones = max(0, lecciones)
        umbrales_por_nivel = (3, 7, 9, 13, 16)

        # lecciones_completadas guarda el orden de la última lección.
        # Se compara contra el final real de cada nivel; nunca se interpreta
        # directamente como una cantidad de niveles terminados.
        niveles_por_lecciones = sum(
            lecciones >= umbral
            for umbral in umbrales_por_nivel
        )
        niveles_por_porcentaje = int(porcentaje // 20)

        # El menor de ambos valores repara porcentajes antiguos inflados sin
        # borrar el progreso ni afectar una prueba final ya completada.
        return min(
            niveles_por_porcentaje,
            niveles_por_lecciones,
            self.TOTAL_NIVELES,
        )

    @staticmethod
    def nombre_imagen_nivel_completado(numero_nivel):
        return f"boton{numero_nivel}"

    @staticmethod
    def nombre_imagen_nivel_desbloqueado(numero_nivel):
        return f"BotonDes_{numero_nivel}"

    def preparar_estado_temporal(self):
        """
        Mantiene la ventana lista para aparecer durante la transición.

        No consulta la base de datos ni recorta imágenes. Los botones de
        Designer siguen visibles, pero permanecen deshabilitados hasta que
        llega el progreso real.
        """
        self.btnVolver.setEnabled(
            True
        )
        self.btnVolver.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )
        self._progreso_actual = {}
        self.actualizar_estado_boton_diploma()

        for boton in self.botones_niveles:
            boton.setEnabled(
                False
            )
            boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.ArrowCursor
                )
            )

    def cargar_estado_niveles(self):
        """
        Inicia la carga del progreso sin bloquear la interfaz.

        La transición puede comenzar inmediatamente porque la consulta a
        MySQL se ejecuta en QThreadPool.
        """
        if self.nivel_en_ejecucion:
            self._recarga_progreso_pendiente = True
            return

        if self.es_sesion_administrador():
            self.aplicar_estado_niveles(
                {}
            )
            return

        id_jugador = self.obtener_id_jugador()

        if id_jugador is None:
            self.aplicar_estado_niveles(
                {}
            )
            return

        if self._carga_progreso_en_curso:
            self._recarga_progreso_pendiente = True
            return

        self._carga_progreso_en_curso = True
        self._recarga_progreso_pendiente = False

        tarea = TareaCargaProgreso(
            id_jugador=id_jugador,
            lenguaje=self.LENGUAJE,
        )
        tarea.senales.terminado.connect(
            self._al_recibir_progreso
        )
        tarea.senales.error.connect(
            self._al_fallar_carga_progreso
        )

        # Mantiene una referencia mientras la tarea está ejecutándose.
        self._tarea_carga_progreso = tarea

        QtCore.QThreadPool.globalInstance().start(
            tarea
        )

    @QtCore.pyqtSlot(object)
    def _al_recibir_progreso(self, progreso):
        self._carga_progreso_en_curso = False
        self._tarea_carga_progreso = None

        if not self.nivel_en_ejecucion:
            self.aplicar_estado_niveles(
                progreso or {}
            )

        if self._recarga_progreso_pendiente:
            self._recarga_progreso_pendiente = False
            self.cargar_estado_niveles()

    @QtCore.pyqtSlot(str)
    def _al_fallar_carga_progreso(self, detalle):
        self._carga_progreso_en_curso = False
        self._tarea_carga_progreso = None

        print(
            "[NIVELES MYSQL] No se pudo cargar el progreso "
            "en segundo plano:",
            detalle,
        )

        # Mantiene habilitado al menos el primer nivel si no fue posible
        # consultar la base de datos.
        if not self.nivel_en_ejecucion:
            self.aplicar_estado_niveles(
                {}
            )

        if self._recarga_progreso_pendiente:
            self._recarga_progreso_pendiente = False
            self.cargar_estado_niveles()

    def aplicar_estado_niveles(self, progreso):
        """
        Aplica imágenes y habilitación usando un progreso ya obtenido.

        Este método se ejecuta en el hilo principal porque modifica widgets,
        pero ya no realiza consultas lentas a la base de datos.
        """
        if self.nivel_en_ejecucion:
            return

        try:
            self._progreso_actual = dict(progreso or {})

            if self.es_sesion_administrador():
                for numero_nivel, boton in self.botones_por_nivel.items():
                    self.aplicar_imagen_boton(
                        boton,
                        self.nombre_imagen_nivel_desbloqueado(
                            numero_nivel
                        ),
                    )
                    self.habilitar_boton(
                        boton,
                        True,
                    )

                self.aplicar_imagen_boton(
                    self.btnComenzar,
                    self.IMAGEN_PRUEBA_DESBLOQUEADA,
                )
                self.habilitar_boton(
                    self.btnComenzar,
                    True,
                )
                self.actualizar_estado_boton_diploma()
                self.poner_controles_al_frente()
                self.actualizar_hover_botones()
                return

            niveles_completados = (
                self.calcular_niveles_completados(
                    progreso
                )
            )

            for numero_nivel, boton in self.botones_por_nivel.items():
                if numero_nivel <= niveles_completados:
                    nombre_imagen = (
                        self.nombre_imagen_nivel_completado(
                            numero_nivel
                        )
                    )
                    habilitado = True

                elif numero_nivel == niveles_completados + 1:
                    nombre_imagen = (
                        self.nombre_imagen_nivel_desbloqueado(
                            numero_nivel
                        )
                    )
                    habilitado = True

                else:
                    nombre_imagen = (
                        self.IMAGEN_NIVEL_BLOQUEADO
                    )
                    habilitado = False

                self.aplicar_imagen_boton(
                    boton,
                    nombre_imagen,
                )
                self.habilitar_boton(
                    boton,
                    habilitado,
                )

            prueba_desbloqueada = (
                niveles_completados
                >= self.TOTAL_NIVELES
                or bool(
                    progreso.get(
                        "prueba_desbloqueada"
                    )
                    or False
                )
                or bool(
                    progreso.get(
                        "prueba_completada"
                    )
                    or False
                )
            )

            imagen_prueba = (
                self.IMAGEN_PRUEBA_DESBLOQUEADA
                if prueba_desbloqueada
                else self.IMAGEN_PRUEBA_BLOQUEADA
            )

            self.aplicar_imagen_boton(
                self.btnComenzar,
                imagen_prueba,
            )
            self.habilitar_boton(
                self.btnComenzar,
                prueba_desbloqueada,
            )
            self.actualizar_estado_boton_diploma()

            self.poner_controles_al_frente()
            self.actualizar_hover_botones()

        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al cargar los botones",
                (
                    "No se pudieron cargar las imágenes "
                    "de los niveles de MySQL.\n\n"
                    f"Detalles:\n{error}"
                ),
            )

    def habilitar_boton(
        self,
        boton,
        habilitado,
    ):
        habilitado = bool(
            habilitado
        )
        boton.setEnabled(
            habilitado
        )

        cursor = (
            QtCore.Qt.CursorShape.PointingHandCursor
            if habilitado
            else QtCore.Qt.CursorShape.ArrowCursor
        )

        boton.setCursor(
            QtGui.QCursor(
                cursor
            )
        )

    # ========================================================
    # CONEXIÓN DE BOTONES
    # ========================================================

    def conectar_eventos(self):
        self.btnVolver.clicked.connect(
            self.volver_form_anterior
        )
        self.btnNivel1.clicked.connect(
            self.abrir_nivel_1
        )
        self.btnNivel2.clicked.connect(
            self.abrir_nivel_2
        )
        self.btnNivel3.clicked.connect(
            self.abrir_nivel_3
        )
        self.btnNivel4.clicked.connect(
            self.abrir_nivel_4
        )
        self.btnNivel5.clicked.connect(
            self.abrir_nivel_5
        )
        self.btnComenzar.clicked.connect(
            self.abrir_prueba_final
        )

    # ========================================================
    # SESIÓN Y APERTURA DE NIVELES
    # ========================================================

    def obtener_sesion_juego(self):
        if isinstance(
            self.jugador,
            dict,
        ):
            sesion = dict(
                self.jugador
            )

            if (
                str(
                    sesion.get(
                        "rol",
                        "",
                    )
                ).lower()
                == "administrador"
                or sesion.get("id_admin") is not None
            ):
                sesion["rol"] = "administrador"
                sesion["id_jugador"] = None
                sesion["personaje"] = (
                    sesion.get("personaje")
                    or "cerdo"
                )
                sesion["vidas_infinitas"] = True
                return sesion

            if sesion.get("id_jugador") is not None:
                sesion["rol"] = "jugador"
                sesion["vidas_infinitas"] = False
                return sesion

        if (
            isinstance(self.jugador, int)
            and not isinstance(self.jugador, bool)
        ):
            return {
                "rol": "jugador",
                "id_jugador": self.jugador,
                "id_admin": None,
                "vidas_infinitas": False,
            }

        raise ValueError(
            "No se recibió una sesión válida desde el login."
        )

    def abrir_nivel_1(self):
        self.abrir_nivel_mysql(1)

    def abrir_nivel_2(self):
        self.abrir_nivel_mysql(2)

    def abrir_nivel_3(self):
        self.abrir_nivel_mysql(3)

    def abrir_nivel_4(self):
        self.abrir_nivel_mysql(4)

    def abrir_nivel_5(self):
        self.abrir_nivel_mysql(5)

    def abrir_prueba_final(self):
        self.abrir_nivel_mysql(6)

    def abrir_nivel_mysql(self, numero_nivel):
        if self.nivel_en_ejecucion:
            return

        sesion = self.obtener_sesion_juego()

        if not validar_vidas_disponibles(
            self,
            sesion,
        ):
            return

        self.nivel_en_ejecucion = True
        error_nivel = None

        try:
            from main import abrir_nivel as ejecutar_nivel

            self.menu_estaba_maximizado = self.isMaximized()
            self.cambiar_estado_botones(
                False
            )

            # Mantener la seleccion visible evita mostrar el escritorio
            # mientras la pantalla de carga y Pygame toman el primer plano.
            QtWidgets.QApplication.processEvents()

            ejecutar_nivel(
                sesion=sesion,
                lenguaje=self.LENGUAJE,
                numero_nivel=numero_nivel,
                usar_pantalla_carga=True,
            )

        except Exception as error:
            error_nivel = error

        finally:
            # Mientras vuelve a mostrarse, showEvent todavía detecta que
            # Pygame sigue activo y no duplica la consulta a la base de datos.
            self.mostrar_menu_niveles()
            self.nivel_en_ejecucion = False
            self.cambiar_estado_botones(
                True
            )

        if error_nivel is not None:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al abrir el nivel",
                (
                    "No se pudo abrir el nivel "
                    f"{numero_nivel} de MySQL."
                    f"\n\nDetalles:\n{error_nivel}"
                ),
            )

    def cambiar_estado_botones(self, habilitados):
        if not habilitados:
            self.restaurar_hover_botones()
            self.btnVolver.setEnabled(
                False
            )

            for boton in self.botones_niveles:
                boton.setEnabled(
                    False
                )

            self.btnDiploma.setEnabled(False)
            return

        self.btnVolver.setEnabled(
            True
        )
        self.btnVolver.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )

        self.cargar_estado_niveles()
        self.programar_actualizacion_interfaz(
            cargar_progreso=False
        )

    def mostrar_menu_niveles(self):
        if self.menu_estaba_maximizado:
            self.showMaximized()
        else:
            self.show()

        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height(),
            )

        self.poner_controles_al_frente()
        self.raise_()
        self.activateWindow()
        QtWidgets.QApplication.processEvents()

    # ========================================================
    # VOLVER AL FORMULARIO ANTERIOR
    # ========================================================

    def volver_form_anterior(self):
        if self.nivel_en_ejecucion:
            return

        try:
            app = QtWidgets.QApplication.instance()

            if (
                hasattr(
                    app,
                    "historial_forms",
                )
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
                    guardar_actual=False,
                )
                return

            from Lecciones import Lecciones

            try:
                ventana_lecciones = Lecciones(
                    jugador=self.jugador,
                    ventana_anterior=self,
                )
            except TypeError:
                ventana_lecciones = Lecciones(
                    self.jugador
                )

            FormTransicion(
                self,
                ventana_lecciones,
                guardar_actual=False,
            )

        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al regresar",
                (
                    "No se pudo regresar al formulario anterior."
                    f"\n\nDetalles:\n{error}"
                ),
            )

    # ========================================================
    # EVENTOS DE LA VENTANA Y HOVER
    # ========================================================

    def showEvent(self, event):
        super().showEvent(event)

        # La transición ya puede pintar su primer cuadro. La consulta de
        # progreso iniciada aquí se ejecuta en segundo plano.
        self.programar_actualizacion_interfaz(
            cargar_progreso=not self.nivel_en_ejecucion
        )

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height(),
            )

        if hasattr(self, "efectos_hover"):
            self.restaurar_hover_botones()

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        if hasattr(self, "botones_por_nivel"):
            self.igualar_tamano_botones_nivel()

        self.poner_controles_al_frente()

        if hasattr(self, "efectos_hover"):
            self.actualizar_hover_botones()

        super().resizeEvent(
            event
        )

    def restaurar_hover_botones(self):
        for efecto in getattr(
            self,
            "efectos_hover",
            [],
        ):
            efecto.restaurar_sin_animacion()

    def actualizar_hover_botones(self):
        for efecto in getattr(
            self,
            "efectos_hover",
            [],
        ):
            efecto.establecer_geometria_base(
                efecto.boton.geometry()
            )

    def configurar_botones(self):
        for boton in self.botones_hover:
            boton.setFocusPolicy(
                QtCore.Qt.FocusPolicy.NoFocus
            )

        self.btnVolver.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )

        for boton in self.botones_niveles:
            boton.setText("")


if __name__ == "__main__":
    app = QtWidgets.QApplication(
        sys.argv
    )

    # ID 2 utilizado solamente para probar este archivo.
    ventana = NivelesMySQL(
        jugador=2
    )
    ventana.showMaximized()

    sys.exit(
        app.exec()
    )