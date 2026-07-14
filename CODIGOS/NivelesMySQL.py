import sys
from pathlib import Path

from PyQt6 import QtGui, QtWidgets, uic
from Transicion import FormAnterior, FormTransicion
from AjusteResponsive import BotonesResponsivos
from quitar_barra import quitar
from ValidarVidas import validar_vidas_disponibles

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


class NivelesMySQL(QtWidgets.QWidget):
    # Este valor indica qué lenguaje debe abrir el cargador.
    LENGUAJE = "mysql"

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

        base_dir = Path(__file__).resolve().parent
        proyecto_dir = base_dir.parent

        ruta_ui = (
            proyecto_dir
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "NivelesMySQL.ui"
        )

        ruta_imagen = (
            proyecto_dir
            / "assets"
            / "DISEÑOS"
            / "Niveles-MySQL.png"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        uic.loadUi(
            str(ruta_ui),
            self,
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
            ruta_imagen,
        )

        self.botones_niveles = [
            self.btnNivel1,
            self.btnNivel2,
            self.btnNivel3,
            self.btnNivel4,
            self.btnNivel5,
            self.btnComenzar,
        ]

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

        self.conectar_eventos()

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
                str(sesion.get("rol", "")).lower() == "administrador"
                or sesion.get("id_admin") is not None
            ):
                sesion["rol"] = "administrador"
                sesion["id_jugador"] = None
                sesion["personaje"] = sesion.get("personaje") or "cerdo"
                sesion["vidas_infinitas"] = True
                return sesion

            if sesion.get("id_jugador") is not None:
                sesion["rol"] = "jugador"
                sesion["vidas_infinitas"] = False
                return sesion

        # Compatibilidad con llamadas antiguas que enviaban solo el ID.
        if isinstance(self.jugador, int) and not isinstance(self.jugador, bool):
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

        Cuando el jugador pulsa SALIR en Pygame, juego.ejecutar()
        termina y el control regresa a este método. Finalmente se
        vuelve a mostrar exactamente este mismo menú de MySQL.
        """
        if self.nivel_en_ejecucion:
            return

        # Obtiene la sesión que fue creada desde el login.
        sesion = self.obtener_sesion_juego()

        # Usa la validación reutilizable antes de abrir cualquier nivel.
        if not validar_vidas_disponibles(self, sesion):
            return

        self.nivel_en_ejecucion = True
        error_nivel = None

        try:
            from main import abrir_nivel as ejecutar_nivel

            # Conserva el estado visual antes de ocultar la ventana.
            self.menu_estaba_maximizado = self.isMaximized()

            self.cambiar_estado_botones(False)

            # Se oculta, pero no se cierra ni se destruye.
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
            self.cambiar_estado_botones(True)
            self.mostrar_menu_niveles()

        if error_nivel is not None:
            QtWidgets.QMessageBox.critical(
                self,
                "Error al abrir el nivel",
                (
                    f"No se pudo abrir el nivel "
                    f"{numero_nivel} de MySQL."
                    f"\n\nDetalles:\n{error_nivel}"
                ),
            )

    def cambiar_estado_botones(self, habilitados):
        self.btnVolver.setEnabled(
            habilitados
        )

        for boton in self.botones_niveles:
            boton.setEnabled(
                habilitados
            )

    def mostrar_menu_niveles(self):
        """
        Vuelve a mostrar este mismo menú cuando Pygame termina.
        """
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
            self.fondo.lower()

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
    # AJUSTE RESPONSIVO
    # ========================================================

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height(),
            )
            self.fondo.lower()

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # ID 2 utilizado solamente para probar este archivo.
    ventana = NivelesMySQL(
        jugador=2
    )

    ventana.showMaximized()

    sys.exit(app.exec())
