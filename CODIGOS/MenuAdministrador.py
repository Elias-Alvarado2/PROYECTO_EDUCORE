from pathlib import Path

from PyQt6 import QtWidgets, uic, QtGui
from Alertas import Alertas
from quitar_barra import quitar
from Transicion import FormTransicion
from AjusteResponsive import BotonesResponsivos


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
        self.setPixmap(self.pixmap_original)

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(
            0,
            0,
            ancho,
            alto
        )


class MenuAdministrador(QtWidgets.QWidget):
    def __init__(self, admin=None):
        super().__init__()
        quitar(self)
        self.admin = admin

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = (
                PROYECTO_DIR
                / "EXPO-DISEÑOS"
                / "DESIGNER"
                / "Menu-Administrador.ui"
        )

        ruta_imagen = (
                PROYECTO_DIR
                / "assets"
                / "DISEÑOS"
                / "Menu-Administrador.png"
        )

        ruta_botones = (
                PROYECTO_DIR
                / "EXPO-DISEÑOS"
                / "Botones"
        )

        if not ruta_ui.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo UI:\n{ruta_ui}"
            )

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen:\n{ruta_imagen}"
            )

        if not ruta_botones.exists():
            raise FileNotFoundError(
                f"No se encontró la carpeta de botones:\n{ruta_botones}"
            )

        uic.loadUi(str(ruta_ui), self)

        # Conserva los StyleSheet de Designer y corrige sus rutas.
        self.corregir_rutas_stylesheet(ruta_botones)

        # Resolución original del diseño.
        self.resize(1920, 1080)

        # Permite cambiar libremente el tamaño de la ventana.
        self.setMinimumSize(0, 0)
        self.setMaximumSize(
            16777215,
            16777215
        )

        # Fondo adaptable.
        self.fondo = FondoImagen(
            self,
            ruta_imagen
        )

        # Hace responsivos todos los botones del menú.
        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=[
                self.btnAjustes,
                self.btnCerrarSesion,
                self.btnGestionUsuarios,
                self.btnJugar,
                self.btnPerfil,
            ],
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.conectar_eventos()

    def conectar_eventos(self):

        if hasattr(self, "btnGestionUsuarios"):
            self.btnGestionUsuarios.clicked.connect(self.abrir_gestionar_usuarios)
        else:
            Alertas.mostrar(
                self,
                "Botón no encontrado",
                "No existe un botón llamado btnGestionUsuarios en el archivo .ui.",
                "error"
            )

        self.btnJugar.clicked.connect(
            self.abrir_lecciones
        )

        self.btnCerrarSesion.clicked.connect(
            self.cerrar_sesion
        )

        # Cuando tengas las ventanas de ajustes y perfil,
        # puedes conectar aquí sus eventos.
        #
        # self.btnAjustes.clicked.connect(self.abrir_ajustes)
        # self.btnPerfil.clicked.connect(self.abrir_perfil)

    def abrir_gestionar_usuarios(self):
        try:
            from GestionUsuario import GestionUsuario

            FormTransicion(
                self,
                GestionUsuario
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir Gestión de Usuarios.\n\nDetalles:\n{e}",
                "error"
            )

    def abrir_lecciones(self):
        try:
            from Lecciones import Lecciones

            try:
                ventana_lecciones = Lecciones(
                    self.admin
                )
            except TypeError:
                ventana_lecciones = Lecciones()

            FormTransicion(
                self,
                ventana_lecciones
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error",
                f"No se pudo abrir Lecciones.\n\nDetalles:\n{e}",
                "error"
            )

    def cerrar_sesion(self):
        respuesta = Alertas.confirmar(
            self,
            "Cerrar sesión",
            "¿Seguro que deseas cerrar sesión?",
            tipo="error",
            texto_confirmar="SÍ, ELIMINAR",
            texto_cancelar="CANCELAR"
        )

        if not respuesta:
            return

        try:
            from Login import LoginWindow

            app = QtWidgets.QApplication.instance()

            # Limpia el historial para evitar que el usuario
            # pueda regresar al menú después de cerrar sesión.
            if hasattr(app, "historial_forms"):
                app.historial_forms.clear()

            self.ventana_login = LoginWindow()
            app.ventana_login = self.ventana_login

            # El Login se abre en tamaño normal.
            self.ventana_login.resize(1020, 720)
            self.ventana_login.showNormal()

            self.close()

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error al cerrar sesión",
                f"No se pudo abrir el Login:\n{e}",
                "error"
            )

    def resizeEvent(self, event):
        # Ajusta el fondo a la ventana.
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )
            self.fondo.lower()

        # El QFrame contiene todos los botones y también
        # debe ocupar toda la ventana.
        if hasattr(self, "MenuAdministrador"):
            self.MenuAdministrador.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )
            self.MenuAdministrador.raise_()

        # Actualiza los botones después de cambiar
        # el tamaño del QFrame.
        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        super().resizeEvent(event)

    def corregir_rutas_stylesheet(self, ruta_botones):
        """
        Conserva los StyleSheet creados en Qt Designer,
        pero transforma ../Botones/ en una ruta absoluta.
        """

        ruta_absoluta = ruta_botones.resolve().as_posix()

        botones = [
            self.btnAjustes,
            self.btnCerrarSesion,
            self.btnGestionUsuarios,
            self.btnJugar,
            self.btnPerfil,
        ]

        for boton in botones:
            estilo = boton.styleSheet()

            if not estilo:
                continue

            estilo_corregido = estilo.replace(
                'url("../Botones/',
                f'url("{ruta_absoluta}/'
            )

            boton.setStyleSheet(estilo_corregido)