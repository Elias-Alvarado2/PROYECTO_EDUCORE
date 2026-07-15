import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from Alertas import Alertas
from ConexionBD import ConexionBD
from quitar_barra import quitar
from Transicion import FormTransicion, FormAnterior
from AjusteResponsive import BotonesResponsivos
from LogoReutilizable import LogoReutilizable


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


class VisualizarUsuario(QtWidgets.QWidget):
    def __init__(self, ventana_anterior=None):
        super().__init__()

        quitar(self)

        self.ventana_anterior = ventana_anterior
        self.ventana_gestion_usuarios = None

        self.ANCHO_BASE = 1920
        self.ALTO_BASE = 1080

        BASE_DIR = Path(__file__).resolve().parent
        PROYECTO_DIR = BASE_DIR.parent

        ruta_ui = (
            PROYECTO_DIR
            / "EXPO-DISEÑOS"
            / "DESIGNER"
            / "Visualizar-Usuarios.ui"
        )

        ruta_imagen = (
            PROYECTO_DIR
            / "assets"
            / "DISEÑOS"
            / "Visualizar_Usuarios.png"
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

        uic.loadUi(
            str(ruta_ui),
            self
        )

        ruta_fuente = (
            PROYECTO_DIR
            / "assets"
            / "FUENTES"
            / "PixelOperator.ttf"
        )

        self.cargar_fuente_personalizada(
            ruta_fuente
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

        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=[
                self.btn_volver,
                self.btn_anterior,
                self.btn_siguiente,
            ],
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.db = ConexionBD()

        # ==================================================
        # CONFIGURACIÓN DE LA PAGINACIÓN
        # ==================================================

        # Cantidad de usuarios mostrados por página.
        self.usuarios_por_pagina = 5

        # La primera página internamente es la página 0.
        self.pagina_actual = 0

        # Aquí se almacenan todos los usuarios de la BD.
        self.lista_usuarios = []

        self.configurar_tabla()
        self.posicionar_elementos()
        self.conectar_eventos()
        self.cargar_usuarios()

    def conectar_eventos(self):
        if hasattr(self, "btn_Volver"):
            self.btn_Volver.clicked.connect(
                self.volver_gestion_usuarios
            )

        if hasattr(self, "btn_volver"):
            self.btn_volver.clicked.connect(
                self.volver_gestion_usuarios
            )

        # Botón para mostrar los siguientes 5 usuarios.
        self.btn_siguiente.clicked.connect(
            self.mostrar_pagina_siguiente
        )

        # Botón para mostrar los 5 usuarios anteriores.
        self.btn_anterior.clicked.connect(
            self.mostrar_pagina_anterior
        )

    def volver_gestion_usuarios(self):
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
                    guardar_actual=False
                )
                return

            from GestionUsuario import GestionUsuario

            FormTransicion(
                self,
                GestionUsuario,
                guardar_actual=False
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error al volver",
                f"No se pudo abrir Gestión Usuarios:\n{e}",
                "error"
            )

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(
                self.width(),
                self.height()
            )
            self.fondo.lower()

        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        if hasattr(self, "logo_reutilizable"):
            self.logo_reutilizable.actualizar()

        if hasattr(self, "Visualizar_Usuarios"):
            self.Visualizar_Usuarios.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )
            self.Visualizar_Usuarios.raise_()

        self.posicionar_elementos()

        super().resizeEvent(event)

    def posicionar_elementos(self):
        escala_x = (
            self.width()
            / self.ANCHO_BASE
        )

        escala_y = (
            self.height()
            / self.ALTO_BASE
        )

        x_tabla = int(
            185 * escala_x
        )

        y_tabla = int(
            455 * escala_y
        )

        ancho_tabla = int(
            1550 * escala_x
        )

        alto_tabla = int(
            370 * escala_y
        )

        self.dgv_visualizarusuarios.setGeometry(
            x_tabla,
            y_tabla,
            ancho_tabla,
            alto_tabla
        )

        self.dgv_visualizarusuarios.raise_()

        self.ajustar_columnas()
        self.ajustar_altura_filas()

        if hasattr(self, "lbl_totalusuarios"):
            x_total = int(
                510 * escala_x
            )

            y_total = int(
                882 * escala_y
            )

            ancho_total = int(
                80 * escala_x
            )

            alto_total = int(
                35 * escala_y
            )

            self.lbl_totalusuarios.setGeometry(
                x_total,
                y_total,
                ancho_total,
                alto_total
            )

            self.lbl_totalusuarios.setStyleSheet("""
                QLabel {
                    background: transparent;
                    color: #082B5F;
                }
            """)

            self.lbl_totalusuarios.raise_()

    def configurar_tabla(self):
        self.modelo = QtGui.QStandardItemModel(
            self
        )

        encabezados = [
            "ID JUGADOR",
            "NOMBRE_USUARIO",
            "CORREO",
            "CONTRASEÑA",
            "PERSONAJE",
            "VIDAS",
            "FECHA_REGISTRO",
            "ESTADO"
        ]

        self.modelo.setHorizontalHeaderLabels(
            encabezados
        )

        self.dgv_visualizarusuarios.setModel(
            self.modelo
        )

        self.dgv_visualizarusuarios.setEditTriggers(
            QtWidgets.QAbstractItemView
            .EditTrigger
            .NoEditTriggers
        )

        self.dgv_visualizarusuarios.setSelectionBehavior(
            QtWidgets.QAbstractItemView
            .SelectionBehavior
            .SelectRows
        )

        self.dgv_visualizarusuarios.setSelectionMode(
            QtWidgets.QAbstractItemView
            .SelectionMode
            .SingleSelection
        )

        self.dgv_visualizarusuarios.verticalHeader().setVisible(
            False
        )

        self.dgv_visualizarusuarios.horizontalHeader().setVisible(
            False
        )

        self.dgv_visualizarusuarios.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Fixed
        )

        self.dgv_visualizarusuarios.setShowGrid(
            False
        )

        self.dgv_visualizarusuarios.setAlternatingRowColors(
            False
        )

        self.dgv_visualizarusuarios.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Fixed
        )

        self.dgv_visualizarusuarios.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.dgv_visualizarusuarios.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.dgv_visualizarusuarios.setStyleSheet("""
            QTableView {
                background: transparent;
                border: none;
                color: #082B5F;
                gridline-color: transparent;
                selection-background-color: #0B73D9;
                selection-color: white;
            }

            QTableView::item {
                background: transparent;
                border: none;
                padding: 2px;
            }

            QTableView::item:selected {
                background-color: #0B73D9;
                color: white;
            }
        """)

    def ajustar_columnas(self):
        if not hasattr(
            self,
            "dgv_visualizarusuarios"
        ):
            return

        ancho_tabla = (
            self.dgv_visualizarusuarios.width()
        )

        porcentajes = [
            0.16,
            0.13,
            0.15,
            0.11,
            0.12,
            0.08,
            0.15,
            0.09
        ]

        for columna, porcentaje in enumerate(
            porcentajes
        ):
            self.dgv_visualizarusuarios.setColumnWidth(
                columna,
                int(ancho_tabla * porcentaje)
            )

    def crear_item(self, texto):
        if texto is None:
            texto = ""

        item = QtGui.QStandardItem(
            str(texto)
        )

        item.setEditable(
            False
        )

        item.setTextAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        return item

    def cargar_usuarios(self):
        """
        Obtiene todos los usuarios de la base de datos,
        pero solamente muestra los primeros cinco.
        """

        try:
            usuarios = self.db.obtener_jugadores()

            if usuarios is None:
                usuarios = []

            # Guardar todos los usuarios.
            self.lista_usuarios = list(
                usuarios
            )

            # Regresar siempre a la primera página.
            self.pagina_actual = 0

            # Mostrar únicamente la página actual.
            self.mostrar_pagina_actual()

            # El total muestra todos los usuarios registrados.
            self.lbl_totalusuarios.setText(
                str(len(self.lista_usuarios))
            )

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error de base de datos",
                str(e),
                "error"
            )

    def mostrar_pagina_actual(self):
        """
        Muestra los cinco usuarios que corresponden
        a la página seleccionada.
        """

        # Eliminar los usuarios mostrados anteriormente.
        self.modelo.removeRows(
            0,
            self.modelo.rowCount()
        )

        # Ejemplo:
        # Página 0: inicio 0, final 5
        # Página 1: inicio 5, final 10
        # Página 2: inicio 10, final 15
        inicio = (
            self.pagina_actual
            * self.usuarios_por_pagina
        )

        final = (
            inicio
            + self.usuarios_por_pagina
        )

        usuarios_pagina = self.lista_usuarios[
            inicio:final
        ]

        for usuario in usuarios_pagina:
            fila = [
                self.crear_item(
                    usuario["id_jugador"]
                ),
                self.crear_item(
                    usuario["nombre"]
                ),
                self.crear_item(
                    usuario["correo"]
                ),
                self.crear_item(
                    usuario["contrasena"]
                ),
                self.crear_item(
                    usuario["personaje"]
                ),
                self.crear_item(
                    usuario["vidas"]
                ),
                self.crear_item(
                    usuario["fecha_registro"]
                ),
                self.crear_item(
                    usuario["estado"]
                )
            ]

            self.modelo.appendRow(
                fila
            )

        self.ajustar_altura_filas()
        self.actualizar_botones_paginacion()

    def mostrar_pagina_siguiente(self):
        """
        Avanza a los siguientes cinco usuarios.
        """

        inicio_siguiente_pagina = (
            self.pagina_actual + 1
        ) * self.usuarios_por_pagina

        # Solamente avanza si todavía existen usuarios.
        if inicio_siguiente_pagina < len(
            self.lista_usuarios
        ):
            self.pagina_actual += 1
            self.mostrar_pagina_actual()

    def mostrar_pagina_anterior(self):
        """
        Regresa a los cinco usuarios anteriores.
        """

        # No permite retroceder antes de la primera página.
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.mostrar_pagina_actual()

    def actualizar_botones_paginacion(self):
        """
        Desactiva los botones cuando no existe una
        página anterior o siguiente.
        """

        # Anterior se desactiva en la primera página.
        self.btn_anterior.setEnabled(
            self.pagina_actual > 0
        )

        inicio_siguiente_pagina = (
            self.pagina_actual + 1
        ) * self.usuarios_por_pagina

        # Siguiente se desactiva en la última página.
        self.btn_siguiente.setEnabled(
            inicio_siguiente_pagina
            < len(self.lista_usuarios)
        )

    def showEvent(self, event):
        super().showEvent(event)

        QtCore.QTimer.singleShot(
            0,
            self.posicionar_elementos
        )

        QtCore.QTimer.singleShot(
            100,
            self.posicionar_elementos
        )

    def cargar_fuente_personalizada(
        self,
        ruta_fuente
    ):
        if not ruta_fuente.exists():
            print(
                f"No se encontró la fuente:\n"
                f"{ruta_fuente}"
            )
            return

        id_fuente = (
            QtGui.QFontDatabase
            .addApplicationFont(
                str(ruta_fuente)
            )
        )

        if id_fuente == -1:
            print(
                "No se pudo cargar la fuente "
                "PixelOperator."
            )
            return

        familias = (
            QtGui.QFontDatabase
            .applicationFontFamilies(
                id_fuente
            )
        )

        if not familias:
            print(
                "No se encontró una familia válida "
                "en la fuente."
            )
            return

        nombre_fuente = familias[0]

        self.fuente_tabla = QtGui.QFont(
            nombre_fuente,
            15
        )
        self.fuente_tabla.setBold(
            False
        )

        self.fuente_total = QtGui.QFont(
            nombre_fuente,
            18
        )
        self.fuente_total.setBold(
            False
        )

        self.fuente_boton = QtGui.QFont(
            nombre_fuente,
            16
        )
        self.fuente_boton.setBold(
            False
        )

        self.dgv_visualizarusuarios.setFont(
            self.fuente_tabla
        )

        if hasattr(
            self,
            "lbl_totalusuarios"
        ):
            self.lbl_totalusuarios.setFont(
                self.fuente_total
            )

        if hasattr(
            self,
            "btn_volver"
        ):
            self.btn_volver.setFont(
                self.fuente_boton
            )

        if hasattr(
            self,
            "btn_Volver"
        ):
            self.btn_Volver.setFont(
                self.fuente_boton
            )

        if hasattr(
            self,
            "btn_anterior"
        ):
            self.btn_anterior.setFont(
                self.fuente_boton
            )

        if hasattr(
            self,
            "btn_siguiente"
        ):
            self.btn_siguiente.setFont(
                self.fuente_boton
            )

    def ajustar_altura_filas(self):
        """
        Divide la altura disponible de la tabla entre las
        cinco filas mostradas por página.
        """

        if not hasattr(self, "dgv_visualizarusuarios"):
            return

        if not hasattr(self, "modelo"):
            return

        # Altura interior disponible dentro del QTableView.
        alto_disponible = (
            self.dgv_visualizarusuarios.viewport().height()
        )

        if alto_disponible <= 0:
            return

        # Como aparecen 5 usuarios por página, divide
        # todo el espacio de la tabla entre 5.
        alto_fila = int(
            alto_disponible / self.usuarios_por_pagina
        )

        self.dgv_visualizarusuarios.verticalHeader().setDefaultSectionSize(
            alto_fila
        )

        # Aplicar la altura a cada fila que se está mostrando.
        for fila in range(self.modelo.rowCount()):
            self.dgv_visualizarusuarios.setRowHeight(
                fila,
                alto_fila
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(
        sys.argv
    )

    ventana = VisualizarUsuario()
    ventana.show()

    sys.exit(
        app.exec()
    )