import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic

from AjusteResponsive import BotonesResponsivos
from ConexionBD import ConexionBD
from Transicion import FormAnterior, FormTransicion
from ValidarVidas import validar_vidas_disponibles
from quitar_barra import quitar


class FondoImagen(QtWidgets.QLabel):
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
    Dibuja la imagen directamente sobre el QPushButton.

    Antes de dibujarla recorta los márgenes transparentes del PNG. Esto
    evita que una imagen se vea más pequeña aunque todos los QPushButton
    tengan exactamente el mismo ancho y alto.
    """

    def __init__(self, boton):
        super().__init__(boton)
        self.boton = boton
        self.pixmap = QtGui.QPixmap()
        boton.installEventFilter(self)

    def establecer_pixmap(self, pixmap):
        self.pixmap = self.recortar_transparencia(pixmap)
        self.boton.update()

    @staticmethod
    def recortar_transparencia(pixmap):
        if pixmap.isNull():
            return pixmap

        imagen = pixmap.toImage().convertToFormat(
            QtGui.QImage.Format.Format_ARGB32
        )

        ancho = imagen.width()
        alto = imagen.height()

        izquierda = ancho
        derecha = -1
        arriba = alto
        abajo = -1

        for y in range(alto):
            for x in range(ancho):
                if QtGui.qAlpha(imagen.pixel(x, y)) > 0:
                    if x < izquierda:
                        izquierda = x
                    if x > derecha:
                        derecha = x
                    if y < arriba:
                        arriba = y
                    if y > abajo:
                        abajo = y

        # Si no encontró píxeles visibles, conserva la imagen original.
        if derecha < izquierda or abajo < arriba:
            return pixmap

        rectangulo_visible = QtCore.QRect(
            izquierda,
            arriba,
            derecha - izquierda + 1,
            abajo - arriba + 1,
        )

        return QtGui.QPixmap.fromImage(
            imagen.copy(rectangulo_visible)
        )

    def eventFilter(self, objeto, event):
        if (
            objeto is self.boton
            and event.type() == QtCore.QEvent.Type.Paint
            and not self.pixmap.isNull()
        ):
            pintor = QtGui.QPainter(self.boton)

            # Se mantiene el aspecto pixel art, sin suavizado.
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

        return super().eventFilter(objeto, event)


class EfectoHoverBoton(QtCore.QObject):
    """
    Agranda ligeramente un botón y aumenta su sombra cuando el cursor
    pasa sobre él. Los botones deshabilitados no reciben la animación.
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

        # Se actualiza después de que BotonesResponsivos coloque
        # cada botón en su posición y tamaño correctos.
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
        """
        Restaura inmediatamente el botón cuando se deshabilita o cuando
        la ventana responsiva necesita recalcular su geometría.
        """
        self.animacion_geometria.stop()
        self.animacion_sombra.stop()

        self.cursor_encima = False
        self.boton.setGeometry(
            self.geometria_normal
        )
        self.sombra.setBlurRadius(10)

    def actualizar_geometria_base(self):
        """
        Guarda la nueva geometría responsiva para que el efecto hover
        siga funcionando después de redimensionar la ventana.
        """
        self.animacion_geometria.stop()

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

    def eventFilter(self, objeto, evento):
        if objeto is self.boton:
            tipo_evento = evento.type()

            if (
                tipo_evento == QtCore.QEvent.Type.Enter
                and self.boton.isEnabled()
            ):
                self.cursor_encima = True

                # Guarda la posición actual establecida por
                # BotonesResponsivos.
                self.geometria_normal = QtCore.QRect(
                    self.boton.geometry()
                )

                # Evita que el botón agrandado quede detrás
                # de los demás controles.
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


class NivelesMySQL(QtWidgets.QWidget):
    """Menú de niveles de MySQL con desbloqueo progresivo."""

    LENGUAJE = "mysql"
    TOTAL_NIVELES = 5

    # Nombres exactos de las imágenes mostradas por el usuario.
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

        # Evita abrir dos veces un nivel por doble clic.
        self.nivel_en_ejecucion = False

        # Guarda cómo estaba la ventana antes de entrar a Pygame.
        self.menu_estaba_maximizado = True

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

        # Conserva los StyleSheet de Designer y corrige las rutas
        # relativas que comienzan con ../Botones/.
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

        # Iguala el ancho y el alto de los cinco botones antes de crear
        # BotonesResponsivos. Así todos conservan exactamente el mismo
        # tamaño al maximizar o cambiar la resolución de la ventana.
        self.igualar_tamano_botones_nivel()

        self.botones_niveles = [
            *self.botones_por_nivel.values(),
            self.btnComenzar,
        ]

        # Crea un índice por nombre, sin importar mayúsculas ni extensión.
        # También busca dentro de subcarpetas de EXPO-DISEÑOS/Botones.
        self.indice_imagenes_botones = (
            self.crear_indice_imagenes_botones()
        )

        # Mantiene un pintor por botón. Los pintores recortan los márgenes
        # transparentes de cada PNG y ocupan todo el tamaño del QPushButton.
        self.pintores_imagen_botones = {}

        # Evita volver a recortar la misma imagen cada vez que se actualiza
        # el progreso. Esto elimina pausas innecesarias al mostrar el menú.
        self.cache_pixmaps_recortados = {}

        # Guarda qué botones deben estar habilitados según el progreso.
        self.habilitacion_por_progreso = {
            boton: False
            for boton in self.botones_niveles
        }

        self.botones_hover = [
            self.btnVolver,
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

        # Efecto hover del otro código: agranda suavemente el botón y
        # aumenta su sombra. Los botones bloqueados no se animan.
        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor=1.035,
                duracion=120,
                parent=self,
            )
            for boton in self.botones_hover
        ]

        self.configurar_botones()
        self.conectar_eventos()

        # Carga las imágenes correctas al abrir el formulario.
        self.cargar_estado_niveles()

        # Guarda las geometrías finales después de que Qt termine de
        # procesar el formulario. El valor 0 no agrega una espera visible.
        QtCore.QTimer.singleShot(
            0,
            self.actualizar_hover_botones,
        )

    # ========================================================
    # RUTAS E IMÁGENES
    # ========================================================

    def igualar_tamano_botones_nivel(self):
        """
        Hace que btnNivel1, btnNivel2, btnNivel3, btnNivel4 y btnNivel5
        tengan exactamente el mismo ancho y alto de btnNivel1.

        Se conserva el centro de cada botón para que las posiciones del
        formulario no cambien. La prueba final mantiene su tamaño propio.
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
            centro_x = geometria.x() + geometria.width() // 2
            centro_y = geometria.y() + geometria.height() // 2

            nueva_x = centro_x - ancho_uniforme // 2
            nueva_y = centro_y - alto_uniforme // 2

            boton.setMinimumSize(0, 0)
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

        # Obliga a repintar las imágenes después de cambiar geometrías.
        for boton in self.botones_por_nivel.values():
            boton.update()

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

    def crear_indice_imagenes_botones(self):
        """
        Registra todas las imágenes de la carpeta Botones usando su nombre
        sin extensión. Así funciona con .png, .jpg, .webp, etc.
        """
        indice = {}

        for archivo in self.ruta_botones.rglob("*"):
            if not archivo.is_file():
                continue

            if archivo.suffix.lower() not in self.EXTENSIONES_IMAGEN:
                continue

            clave = archivo.stem.strip().casefold()

            # Conserva la primera coincidencia encontrada.
            indice.setdefault(
                clave,
                archivo.resolve(),
            )

        return indice

    def obtener_ruta_imagen_boton(self, nombre_imagen):
        clave = str(nombre_imagen).strip().casefold()
        ruta = self.indice_imagenes_botones.get(clave)

        if ruta is None:
            nombres_disponibles = sorted(
                archivo.stem
                for archivo in self.indice_imagenes_botones.values()
            )

            raise FileNotFoundError(
                "No se encontró la imagen del botón "
                f"'{nombre_imagen}' dentro de:\n"
                f"{self.ruta_botones}\n\n"
                "Imágenes detectadas:\n"
                + "\n".join(nombres_disponibles)
            )

        return ruta

    def aplicar_imagen_boton(self, boton, nombre_imagen):
        """
        Coloca la imagen sin márgenes transparentes y la dibuja ocupando
        exactamente todo el ancho y alto del QPushButton.

        El recorte se guarda en caché para no repetir el recorrido de
        píxeles cada vez que se actualiza el progreso.
        """
        ruta_imagen = self.obtener_ruta_imagen_boton(
            nombre_imagen
        )

        clave_cache = str(ruta_imagen.resolve())

        pixmap_recortado = self.cache_pixmaps_recortados.get(
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

            pixmap_recortado = (
                PintorImagenBoton.recortar_transparencia(
                    pixmap_original
                )
            )
            self.cache_pixmaps_recortados[
                clave_cache
            ] = pixmap_recortado

        boton.setText("")
        boton.setIcon(QtGui.QIcon())
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

        pintor = self.pintores_imagen_botones.get(boton)

        if pintor is None:
            pintor = PintorImagenBoton(boton)
            self.pintores_imagen_botones[boton] = pintor

        # El pixmap ya está recortado; se asigna directamente para evitar
        # ejecutar nuevamente el recorte dentro del pintor.
        pintor.pixmap = pixmap_recortado
        boton.update()

    def corregir_rutas_stylesheet(self, ruta_botones):
        """
        Conserva los StyleSheet creados en Qt Designer,
        reemplazando ../Botones/ por la ruta absoluta.
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

    # ========================================================
    # PROGRESO Y ESTADO DE LOS BOTONES
    # ========================================================

    def es_sesion_administrador(self):
        if not isinstance(self.jugador, dict):
            return False

        rol = str(
            self.jugador.get("rol", "")
        ).strip().lower()

        return (
            rol == "administrador"
            or self.jugador.get("id_admin") is not None
        )

    def obtener_id_jugador(self):
        if isinstance(self.jugador, dict):
            valor = self.jugador.get("id_jugador")
        elif (
            isinstance(self.jugador, int)
            and not isinstance(self.jugador, bool)
        ):
            valor = self.jugador
        else:
            valor = None

        try:
            return int(valor) if valor is not None else None
        except (TypeError, ValueError):
            return None

    def consultar_progreso_mysql(self):
        """
        Devuelve el registro de progreso de MySQL para el jugador actual.

        Primero utiliza obtener_progreso_perfil(), que ya existe en
        ConexionBD. Si esa versión de ConexionBD no posee el método, hace
        una consulta directa mediante conectar().
        """
        id_jugador = self.obtener_id_jugador()

        if id_jugador is None:
            return {}

        base_datos = ConexionBD()

        # Método utilizado por la pantalla Perfil.
        if hasattr(base_datos, "obtener_progreso_perfil"):
            try:
                registros = (
                    base_datos.obtener_progreso_perfil(
                        id_jugador
                    )
                    or []
                )

                for registro in registros:
                    lenguaje = str(
                        registro.get("lenguaje") or ""
                    ).strip().casefold()

                    if lenguaje == self.LENGUAJE.casefold():
                        return dict(registro)

                return {}

            except Exception as error:
                print(
                    "[NIVELES MYSQL] No se pudo consultar el progreso "
                    "con obtener_progreso_perfil():",
                    error,
                )

        # Compatibilidad con versiones de ConexionBD que solo tienen
        # conectar(). Esta consulta no requiere agregar otro método.
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

            return cursor.fetchone() or {}

        except Exception as error:
            print(
                "[NIVELES MYSQL] No se pudo consultar el progreso:",
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
        """
        registrar_nivel_completado() guarda 20 % por nivel. Por eso la
        cantidad de niveles completados se calcula usando porcentaje_avance.
        """
        try:
            porcentaje = float(
                progreso.get("porcentaje_avance") or 0
            )
        except (TypeError, ValueError):
            porcentaje = 0

        porcentaje = max(
            0,
            min(porcentaje, 100),
        )

        niveles_completados = int(
            porcentaje // 20
        )

        return max(
            0,
            min(niveles_completados, self.TOTAL_NIVELES),
        )

    def cargar_estado_niveles(self):
        """
        Actualiza imágenes y habilitación de todos los botones.

        Estado normal de un jugador nuevo:
        - Nivel 1: BotonDes_1, habilitado.
        - Niveles 2 a 5: Bloqueado, deshabilitados.
        - Prueba final: PruebaBloqueada, deshabilitada.
        """
        if self.nivel_en_ejecucion:
            return

        if self.es_sesion_administrador():
            # El administrador puede probar todos los niveles, pero no se
            # muestran como completados porque no guarda progreso.
            for numero_nivel, boton in self.botones_por_nivel.items():
                self.aplicar_imagen_boton(
                    boton,
                    f"BotonDes_{numero_nivel}",
                )
                self.habilitar_boton_segun_progreso(
                    boton,
                    True,
                )

            self.aplicar_imagen_boton(
                self.btnComenzar,
                self.IMAGEN_PRUEBA_DESBLOQUEADA,
            )
            self.habilitar_boton_segun_progreso(
                self.btnComenzar,
                True,
            )
            return

        progreso = self.consultar_progreso_mysql()
        niveles_completados = (
            self.calcular_niveles_completados(
                progreso
            )
        )

        for numero_nivel, boton in self.botones_por_nivel.items():
            if numero_nivel <= niveles_completados:
                # Estrella naranja: nivel ya completado.
                nombre_imagen = f"boton{numero_nivel}"
                habilitado = True

            elif numero_nivel == niveles_completados + 1:
                # Estrella gris: siguiente nivel desbloqueado.
                nombre_imagen = f"BotonDes_{numero_nivel}"
                habilitado = True

            else:
                # Candado: nivel todavía bloqueado.
                nombre_imagen = self.IMAGEN_NIVEL_BLOQUEADO
                habilitado = False

            self.aplicar_imagen_boton(
                boton,
                nombre_imagen,
            )
            self.habilitar_boton_segun_progreso(
                boton,
                habilitado,
            )

        # La prueba final se desbloquea únicamente después de completar
        # los cinco niveles. No se utiliza prueba_desbloqueada aquí porque
        # el menú actual contiene cinco niveles antes de la prueba.
        prueba_desbloqueada = (
            niveles_completados >= self.TOTAL_NIVELES
            or bool(progreso.get("prueba_completada") or False)
        )

        if prueba_desbloqueada:
            imagen_prueba = self.IMAGEN_PRUEBA_DESBLOQUEADA
        else:
            imagen_prueba = self.IMAGEN_PRUEBA_BLOQUEADA

        self.aplicar_imagen_boton(
            self.btnComenzar,
            imagen_prueba,
        )
        self.habilitar_boton_segun_progreso(
            self.btnComenzar,
            prueba_desbloqueada,
        )

    def habilitar_boton_segun_progreso(self, boton, habilitado):
        habilitado = bool(habilitado)
        self.habilitacion_por_progreso[boton] = habilitado
        boton.setEnabled(habilitado)

        if habilitado:
            cursor = QtCore.Qt.CursorShape.PointingHandCursor
        else:
            cursor = QtCore.Qt.CursorShape.ArrowCursor

        boton.setCursor(
            QtGui.QCursor(cursor)
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

        # La prueba final se envía al cargador como nivel 6.
        self.btnComenzar.clicked.connect(
            self.abrir_prueba_final
        )

    # ========================================================
    # OBTENER SESIÓN DEL JUEGO
    # ========================================================

    def obtener_sesion_juego(self):
        """Devuelve la sesión creada y validada desde Login.py."""
        if isinstance(self.jugador, dict):
            sesion = dict(self.jugador)

            if (
                str(sesion.get("rol", "")).lower()
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

        # Compatibilidad con llamadas antiguas que enviaban solo el ID.
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

    # ========================================================
    # MÉTODOS DE CADA NIVEL
    # ========================================================

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

    # ========================================================
    # ABRIR PYGAME
    # ========================================================

    def abrir_nivel_mysql(self, numero_nivel):
        """
        Oculta este formulario mientras se ejecuta Pygame.

        Al terminar Pygame se vuelve a consultar progreso_jugador para que
        el nivel terminado cambie a boton1/boton2/etc. y el siguiente cambie
        a BotonDes_1/BotonDes_2/etc.
        """
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

            # Deshabilita temporalmente todo mientras Pygame está abierto.
            self.cambiar_estado_botones(False)

            self.hide()
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
            self.nivel_en_ejecucion = False
            self.mostrar_menu_niveles()

            # Consulta nuevamente la base de datos. Esto evita habilitar
            # accidentalmente los niveles que todavía siguen bloqueados.
            self.cambiar_estado_botones(True)

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
        """
        Cuando habilitados es False, desactiva todos temporalmente.
        Cuando es True, restaura el estado real consultando el progreso.
        """
        if not habilitados:
            self.btnVolver.setEnabled(False)

            for boton in self.botones_niveles:
                boton.setEnabled(False)

            return

        self.btnVolver.setEnabled(True)
        self.btnVolver.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )
        self.cargar_estado_niveles()

    def mostrar_menu_niveles(self):
        """Vuelve a mostrar este mismo menú cuando Pygame termina."""
        if self.menu_estaba_maximizado:
            self.showMaximized()
        else:
            self.show()

        self.raise_()
        self.activateWindow()

        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height(),
            )

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
                hasattr(app, "historial_forms")
                and len(app.historial_forms) > 0
            ):
                FormAnterior(self)
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
    # EVENTOS DE LA VENTANA
    # ========================================================

    def showEvent(self, event):
        super().showEvent(event)

        def actualizar_despues_de_mostrar():
            # Primero aplica el tamaño uniforme del botón 1 a los demás.
            self.igualar_tamano_botones_nivel()

            if not self.nivel_en_ejecucion:
                self.cargar_estado_niveles()

            # Después guarda esas geometrías como base del hover.
            self.actualizar_hover_botones()

        # Se ejecuta en el siguiente ciclo de Qt. No añade un delay a
        # FormTransicion; únicamente espera a que termine el showMaximized.
        QtCore.QTimer.singleShot(
            0,
            actualizar_despues_de_mostrar,
        )

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height(),
            )

        # Detiene cualquier hover activo antes de recalcular posiciones.
        for efecto in getattr(
            self,
            "efectos_hover",
            [],
        ):
            efecto.restaurar_sin_animacion()

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        # BotonesResponsivos puede recuperar tamaños diferentes de Designer.
        # Se vuelven a igualar al tamaño actual de btnNivel1.
        if hasattr(self, "botones_por_nivel"):
            self.igualar_tamano_botones_nivel()

        # Actualiza inmediatamente la geometría base del hover. No se usa
        # un temporizador adicional, por lo que no se añade espera.
        if hasattr(self, "efectos_hover"):
            self.actualizar_hover_botones()

        super().resizeEvent(event)

    def actualizar_hover_botones(self):
        """
        Guarda la posición y el tamaño actuales como geometría normal de
        cada efecto hover después del ajuste responsivo y uniforme.
        """
        for efecto in getattr(
            self,
            "efectos_hover",
            [],
        ):
            efecto.actualizar_geometria_base()

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
    app = QtWidgets.QApplication(sys.argv)

    # ID 2 utilizado solamente para probar este archivo.
    ventana = NivelesMySQL(
        jugador=2
    )

    ventana.showMaximized()

    sys.exit(app.exec())