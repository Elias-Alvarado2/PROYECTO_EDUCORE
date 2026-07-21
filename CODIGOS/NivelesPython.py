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
        self.pixmap_original = QtGui.QPixmap(str(self.ruta_imagen))

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
        self.setGeometry(0, 0, ventana.width(), ventana.height())
        self.setPixmap(self.pixmap_original)
        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(0, 0, ancho, alto)
        self.lower()


class NivelesPython(QtWidgets.QWidget):
    """Menú de Python con desbloqueo progresivo de niveles."""

    LENGUAJE = "python"
    TOTAL_NIVELES = 5

    # Nombres exactos mostrados en la carpeta de imágenes.
    IMAGEN_NIVEL_BLOQUEADO = "Bloqueado"
    IMAGEN_PRUEBA_DESBLOQUEADA = "prueba"
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

        self.base_dir = Path(__file__).resolve().parent
        self.proyecto_dir = self.base_dir.parent

        self.ruta_ui = (
            self.proyecto_dir
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "NivelesPython.ui"
        )

        self.ruta_imagen_fondo = (
            self.proyecto_dir
            / "assets"
            / "DISEÑOS"
            / "Niveles-Python.png"
        )

        self.ruta_botones = (
            self.proyecto_dir
            / "EXPO-DISEÑOS"
            / "Botones"
        )

        self.validar_rutas_principales()

        uic.loadUi(str(self.ruta_ui), self)

        # Corrige las rutas relativas guardadas desde Qt Designer.
        self.corregir_rutas_stylesheet(self.ruta_botones)

        self.resize(1920, 1080)
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)

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

        self.botones_niveles = [
            *self.botones_por_nivel.values(),
            self.btnComenzar,
        ]

        # Guarda la geometría original de Designer. Esta geometría se usa
        # como referencia para hacer más grandes los niveles completados y
        # más pequeños los niveles disponibles o bloqueados sin deformar
        # su posición cuando la ventana cambia de tamaño.
        self.geometrias_base_niveles = {
            boton: QtCore.QRect(boton.geometry())
            for boton in self.botones_por_nivel.values()
        }

        # Estado visual actual de cada botón: completado, disponible o
        # bloqueado. Se reaplica después de cada ajuste responsivo.
        self.estados_visuales_niveles = {}

        # Busca las imágenes también dentro de subcarpetas.
        self.indice_imagenes_botones = (
            self.crear_indice_imagenes_botones()
        )

        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=[
                self.btnVolver,
                self.btnNivel1,
                self.btnNivel2,
                self.btnNivel3,
                self.btnNivel4,
                self.btnNivel5,
                self.btnComenzar,
            ],
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.configurar_botones()
        self.conectar_eventos()
        self.poner_controles_al_frente()

        # Carga el progreso al abrir la ventana.
        self.cargar_estado_niveles()

    # ========================================================
    # RUTAS E IMÁGENES
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

    def crear_indice_imagenes_botones(self):
        """
        Crea un índice con TODAS las imágenes que tengan el mismo nombre.

        Esto es importante porque Java y Python pueden tener archivos como
        "boton 1.png" dentro de carpetas diferentes. La versión anterior
        guardaba solamente el primer archivo encontrado y podía mostrar el
        botón naranja de Java en la pantalla de Python.
        """
        indice = {}

        for archivo in self.ruta_botones.rglob("*"):
            if not archivo.is_file():
                continue

            if archivo.suffix.lower() not in self.EXTENSIONES_IMAGEN:
                continue

            clave = archivo.stem.strip().casefold()
            indice.setdefault(clave, []).append(archivo.resolve())

        return indice

    @staticmethod
    def _ruta_contiene_python(ruta):
        """Indica si alguna carpeta de la ruta pertenece a Python."""
        partes = [parte.strip().casefold() for parte in Path(ruta).parts]
        return any("python" in parte for parte in partes)

    @staticmethod
    def _puntaje_color_azul(ruta):
        """
        Da prioridad a imágenes azules cuando hay nombres duplicados.

        Se utiliza como respaldo cuando las carpetas no incluyen la palabra
        Python. Los botones completados de Python son azules, mientras que
        los de Java usan tonos crema y naranja.
        """
        imagen = QtGui.QImage(str(ruta))

        if imagen.isNull():
            return -1

        imagen = imagen.convertToFormat(
            QtGui.QImage.Format.Format_ARGB32
        ).scaled(
            40,
            40,
            QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
            QtCore.Qt.TransformationMode.FastTransformation,
        )

        puntaje = 0

        for y in range(imagen.height()):
            for x in range(imagen.width()):
                color = QtGui.QColor(imagen.pixel(x, y))

                # Ignora píxeles transparentes.
                if color.alpha() < 40:
                    continue

                rojo = color.red()
                verde = color.green()
                azul = color.blue()

                # Premia los tonos donde el azul domina claramente.
                if azul > rojo + 18 and azul > verde + 8:
                    puntaje += azul - max(rojo, verde)

                # Penaliza los tonos naranja propios de Java.
                if rojo > 170 and verde > 70 and azul < 90:
                    puntaje -= 40

        return puntaje

    def obtener_ruta_imagen_boton(self, nombre_imagen):
        clave = str(nombre_imagen).strip().casefold()
        rutas = self.indice_imagenes_botones.get(clave, [])

        if not rutas:
            nombres_disponibles = sorted(
                {
                    archivo.stem
                    for lista_rutas in self.indice_imagenes_botones.values()
                    for archivo in lista_rutas
                }
            )

            raise FileNotFoundError(
                "No se encontró la imagen del botón "
                f"'{nombre_imagen}' dentro de:\n"
                f"{self.ruta_botones}\n\n"
                "Imágenes detectadas:\n"
                + "\n".join(nombres_disponibles)
            )

        if len(rutas) == 1:
            return rutas[0]

        # Primera prioridad: archivo guardado dentro de una carpeta Python.
        rutas_python = [
            ruta for ruta in rutas
            if self._ruta_contiene_python(ruta)
        ]

        if rutas_python:
            return max(
                rutas_python,
                key=self._puntaje_color_azul,
            )

        # Respaldo: selecciona la imagen con mayor presencia de color azul.
        return max(
            rutas,
            key=self._puntaje_color_azul,
        )

    def aplicar_imagen_boton(self, boton, nombre_imagen):
        """Aplica la imagen sin permitir que el estado disabled la borre."""
        ruta_imagen = self.obtener_ruta_imagen_boton(nombre_imagen)
        ruta_qss = ruta_imagen.as_posix()

        boton.setText("")
        boton.setIcon(QtGui.QIcon())
        boton.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-image: url(\"{ruta_qss}\") 0 0 0 0 stretch stretch;
            }}

            QPushButton:hover {{
                background-color: transparent;
                border: none;
                border-image: url(\"{ruta_qss}\") 0 0 0 0 stretch stretch;
            }}

            QPushButton:pressed {{
                background-color: transparent;
                border: none;
                border-image: url(\"{ruta_qss}\") 0 0 0 0 stretch stretch;
            }}

            QPushButton:disabled {{
                background-color: transparent;
                border: none;
                border-image: url(\"{ruta_qss}\") 0 0 0 0 stretch stretch;
            }}
            """
        )

    def corregir_rutas_stylesheet(self, ruta_botones):
        """Convierte ../Botones/ en una ruta absoluta."""
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
                control.setStyleSheet(estilo_corregido)

    def poner_controles_al_frente(self):
        """Mantiene los botones por encima del QLabel usado como fondo."""
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
        )

        for nombre in nombres:
            control = getattr(self, nombre, None)
            if control is not None:
                control.raise_()


    def aplicar_tamano_segun_estado(self, boton, estado):
        """
        Ajusta el tamaño del botón conservando su centro.

        - completado: se muestra más grande.
        - disponible: se muestra más pequeño.
        - bloqueado: se muestra pequeño, igual que los no completados.
        """
        if boton not in self.geometrias_base_niveles:
            return

        factores = {
            "completado": 1.24,
            "disponible": 0.84,
            "bloqueado": 0.84,
        }
        factor = factores.get(estado, 1.0)

        geometria_base = self.geometrias_base_niveles[boton]

        # Escala la geometría original tomando como referencia 1920x1080.
        escala_x = self.width() / 1920 if self.width() > 0 else 1.0
        escala_y = self.height() / 1080 if self.height() > 0 else 1.0

        x_base = geometria_base.x() * escala_x
        y_base = geometria_base.y() * escala_y
        ancho_base = geometria_base.width() * escala_x
        alto_base = geometria_base.height() * escala_y

        centro_x = x_base + ancho_base / 2
        centro_y = y_base + alto_base / 2

        nuevo_ancho = max(1, round(ancho_base * factor))
        nuevo_alto = max(1, round(alto_base * factor))
        nuevo_x = round(centro_x - nuevo_ancho / 2)
        nuevo_y = round(centro_y - nuevo_alto / 2)

        boton.setGeometry(
            nuevo_x,
            nuevo_y,
            nuevo_ancho,
            nuevo_alto,
        )
        boton.raise_()

    def establecer_estado_visual(self, boton, estado):
        """Guarda y aplica el estado visual de un botón de nivel."""
        self.estados_visuales_niveles[boton] = estado
        self.aplicar_tamano_segun_estado(boton, estado)

    def reaplicar_tamanos_niveles(self):
        """Reaplica los tamaños después de un cambio de resolución."""
        for boton, estado in self.estados_visuales_niveles.items():
            self.aplicar_tamano_segun_estado(boton, estado)

    # ========================================================
    # PROGRESO Y ESTADO DE LOS BOTONES
    # ========================================================

    def es_sesion_administrador(self):
        if not isinstance(self.jugador, dict):
            return False

        rol = str(
            self.jugador.get("rol", "")
        ).strip().casefold()

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

    def consultar_progreso_python(self):
        """Obtiene el progreso de Python del jugador autenticado."""
        id_jugador = self.obtener_id_jugador()

        if id_jugador is None:
            return {}

        base_datos = ConexionBD()

        # Usa el método que ya emplea la pantalla Perfil, si existe.
        if hasattr(base_datos, "obtener_progreso_perfil"):
            try:
                registros = (
                    base_datos.obtener_progreso_perfil(id_jugador)
                    or []
                )

                for registro in registros:
                    lenguaje = str(
                        registro.get("lenguaje") or ""
                    ).strip().casefold()

                    if lenguaje == self.LENGUAJE.casefold():
                        return dict(registro)

            except Exception as error:
                print(
                    "[NIVELES PYTHON] No se pudo consultar el progreso "
                    "con obtener_progreso_perfil():",
                    error,
                )

        conexion = None
        cursor = None

        try:
            conexion = base_datos.conectar()

            if conexion is None:
                return {}

            cursor = conexion.cursor(dictionary=True)
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
                "[NIVELES PYTHON] No se pudo consultar el progreso:",
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
        Calcula cuántos niveles están completos usando tanto
        lecciones_completadas como porcentaje_avance.
        """
        try:
            lecciones = int(
                progreso.get("lecciones_completadas") or 0
            )
        except (TypeError, ValueError):
            lecciones = 0

        try:
            porcentaje = float(
                progreso.get("porcentaje_avance") or 0
            )
        except (TypeError, ValueError):
            porcentaje = 0

        lecciones = max(
            0,
            min(lecciones, self.TOTAL_NIVELES),
        )
        porcentaje = max(0, min(porcentaje, 100))
        niveles_por_porcentaje = int(porcentaje // 20)

        return max(
            lecciones,
            min(niveles_por_porcentaje, self.TOTAL_NIVELES),
        )

    def nombre_imagen_nivel_completado(self, numero_nivel):
        # Los archivos se llaman exactamente: BotonPython_1, BotonPython_2, etc.
        return f"BotonPython_{numero_nivel}"

    def nombre_imagen_nivel_desbloqueado(self, numero_nivel):
        # Los archivos se llaman exactamente: BotonDesPython_1, etc.
        return f"BotonDesPython_{numero_nivel}"

    def cargar_estado_niveles(self):
        """
        Cambia las imágenes según el progreso:

        - Completado: BotonPython_1 ... BotonPython_5.
        - Siguiente disponible: BotonDesPython_1 ... BotonDesPython_5.
        - Bloqueado: Bloqueado.
        - Prueba disponible: prueba.
        - Prueba bloqueada: PruebaBloqueada.
        """
        if self.nivel_en_ejecucion:
            return

        try:
            if self.es_sesion_administrador():
                # El administrador puede probar todos los niveles.
                for numero_nivel, boton in self.botones_por_nivel.items():
                    self.aplicar_imagen_boton(
                        boton,
                        self.nombre_imagen_nivel_desbloqueado(
                            numero_nivel
                        ),
                    )
                    self.habilitar_boton(boton, True)
                    self.establecer_estado_visual(
                        boton,
                        "disponible",
                    )

                self.aplicar_imagen_boton(
                    self.btnComenzar,
                    self.IMAGEN_PRUEBA_DESBLOQUEADA,
                )
                self.habilitar_boton(self.btnComenzar, True)
                self.poner_controles_al_frente()
                return

            progreso = self.consultar_progreso_python()
            niveles_completados = self.calcular_niveles_completados(
                progreso
            )

            for numero_nivel, boton in self.botones_por_nivel.items():
                if numero_nivel <= niveles_completados:
                    nombre_imagen = (
                        self.nombre_imagen_nivel_completado(
                            numero_nivel
                        )
                    )
                    habilitado = True
                    estado_visual = "completado"

                elif numero_nivel == niveles_completados + 1:
                    nombre_imagen = (
                        self.nombre_imagen_nivel_desbloqueado(
                            numero_nivel
                        )
                    )
                    habilitado = True
                    estado_visual = "disponible"

                else:
                    nombre_imagen = self.IMAGEN_NIVEL_BLOQUEADO
                    habilitado = False
                    estado_visual = "bloqueado"

                self.aplicar_imagen_boton(
                    boton,
                    nombre_imagen,
                )
                self.habilitar_boton(
                    boton,
                    habilitado,
                )
                self.establecer_estado_visual(
                    boton,
                    estado_visual,
                )

            prueba_desbloqueada = (
                niveles_completados >= self.TOTAL_NIVELES
                or bool(progreso.get("prueba_desbloqueada") or False)
                or bool(progreso.get("prueba_completada") or False)
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

            self.poner_controles_al_frente()

        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al cargar los botones",
                (
                    "No se pudieron cargar las imágenes de los niveles "
                    "de Python.\n\n"
                    f"Detalles:\n{error}"
                ),
            )

    def habilitar_boton(self, boton, habilitado):
        boton.setEnabled(bool(habilitado))

        cursor = (
            QtCore.Qt.CursorShape.PointingHandCursor
            if habilitado
            else QtCore.Qt.CursorShape.ArrowCursor
        )
        boton.setCursor(QtGui.QCursor(cursor))

    # ========================================================
    # CONEXIÓN DE BOTONES
    # ========================================================

    def conectar_eventos(self):
        self.btnVolver.clicked.connect(self.volver_form_anterior)
        self.btnNivel1.clicked.connect(self.abrir_nivel_1)
        self.btnNivel2.clicked.connect(self.abrir_nivel_2)
        self.btnNivel3.clicked.connect(self.abrir_nivel_3)
        self.btnNivel4.clicked.connect(self.abrir_nivel_4)
        self.btnNivel5.clicked.connect(self.abrir_nivel_5)
        self.btnComenzar.clicked.connect(self.abrir_prueba_final)

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
                    sesion.get("personaje") or "cerdo"
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

    # ========================================================
    # MÉTODOS DE CADA NIVEL
    # ========================================================

    def abrir_nivel_1(self):
        self.abrir_nivel_python(1)

    def abrir_nivel_2(self):
        self.abrir_nivel_python(2)

    def abrir_nivel_3(self):
        self.abrir_nivel_python(3)

    def abrir_nivel_4(self):
        self.abrir_nivel_python(4)

    def abrir_nivel_5(self):
        self.abrir_nivel_python(5)

    def abrir_prueba_final(self):
        self.abrir_nivel_python(6)

    # ========================================================
    # ABRIR PYGAME
    # ========================================================

    def abrir_nivel_python(self, numero_nivel):
        if self.nivel_en_ejecucion:
            return

        sesion = self.obtener_sesion_juego()

        if not validar_vidas_disponibles(self, sesion):
            return

        self.nivel_en_ejecucion = True
        error_nivel = None

        try:
            from main import abrir_nivel as ejecutar_nivel

            self.menu_estaba_maximizado = self.isMaximized()
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

            # Al regresar de Pygame vuelve a consultar la base de datos.
            self.cambiar_estado_botones(True)

        if error_nivel is not None:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al abrir el nivel",
                (
                    "No se pudo abrir el nivel "
                    f"{numero_nivel} de Python."
                    f"\n\nDetalles:\n{error_nivel}"
                ),
            )

    def cambiar_estado_botones(self, habilitados):
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
                ventana_lecciones = Lecciones(self.jugador)

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

        if not self.nivel_en_ejecucion:
            QtCore.QTimer.singleShot(
                0,
                self.cargar_estado_niveles,
            )

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height(),
            )

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        if hasattr(self, "estados_visuales_niveles"):
            self.reaplicar_tamanos_niveles()

        self.poner_controles_al_frente()
        super().resizeEvent(event)

    def configurar_botones(self):
        self.btnVolver.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )

        for boton in self.botones_niveles:
            boton.setText("")
            boton.setFocusPolicy(
                QtCore.Qt.FocusPolicy.NoFocus
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # ID 2 utilizado solamente para probar este archivo.
    ventana = NivelesPython(jugador=2)
    ventana.showMaximized()

    sys.exit(app.exec())