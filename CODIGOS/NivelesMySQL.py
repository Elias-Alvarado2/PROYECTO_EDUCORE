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

        self.botones_niveles = [
            *self.botones_por_nivel.values(),
            self.btnComenzar,
        ]

        # Crea un índice por nombre, sin importar mayúsculas ni extensión.
        # También busca dentro de subcarpetas de EXPO-DISEÑOS/Botones.
        self.indice_imagenes_botones = (
            self.crear_indice_imagenes_botones()
        )

        # Guarda qué botones deben estar habilitados según el progreso.
        self.habilitacion_por_progreso = {
            boton: False
            for boton in self.botones_niveles
        }

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

        # Carga las imágenes correctas al abrir el formulario.
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
        """Coloca una imagen como border-image sin deformar el botón."""
        ruta_imagen = self.obtener_ruta_imagen_boton(
            nombre_imagen
        )
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

        # También actualiza los botones cuando se regresa desde otro form.
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
    ventana = NivelesMySQL(
        jugador=2
    )

    ventana.showMaximized()

    sys.exit(app.exec())