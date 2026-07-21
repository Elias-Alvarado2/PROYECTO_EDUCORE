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

class EfectoHoverBoton(QtCore.QObject):
    """
    Agranda suavemente un botón y aumenta su sombra
    cuando el cursor pasa sobre él.
    """

    def __init__(
        self,
        boton,
        factor=1.04,
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
            boton.geometry()
        )

        # Animación de tamaño y posición.
        self.animacion_geometria = QtCore.QPropertyAnimation(
            boton,
            b"geometry",
            self
        )

        self.animacion_geometria.setDuration(
            duracion
        )

        self.animacion_geometria.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        # Sombra inicial.
        self.sombra = QtWidgets.QGraphicsDropShadowEffect(
            boton
        )

        self.sombra.setColor(
            QtGui.QColor(0, 0, 0, 170)
        )

        self.sombra.setBlurRadius(10)
        self.sombra.setOffset(0, 3)

        boton.setGraphicsEffect(
            self.sombra
        )

        # Animación de la sombra.
        self.animacion_sombra = QtCore.QPropertyAnimation(
            self.sombra,
            b"blurRadius",
            self
        )

        self.animacion_sombra.setDuration(
            duracion
        )

        self.animacion_sombra.setEasingCurve(
            QtCore.QEasingCurve.Type.OutCubic
        )

        boton.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
        )

        boton.installEventFilter(self)

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
        Guarda la posición y tamaño asignados por
        BotonesResponsivos.
        """

        self.animacion_geometria.stop()

        if not self.cursor_encima:
            self.geometria_normal = QtCore.QRect(
                self.boton.geometry()
            )

    def restaurar_inmediatamente(self):
        """
        Restaura el botón cuando queda deshabilitado.
        """

        self.cursor_encima = False

        self.animacion_geometria.stop()
        self.animacion_sombra.stop()

        self.boton.setGeometry(
            self.geometria_normal
        )

        self.sombra.setBlurRadius(10)

    def eventFilter(self, objeto, evento):
        if objeto is self.boton:

            if (
                evento.type() == QtCore.QEvent.Type.Enter
                and self.boton.isEnabled()
            ):
                self.cursor_encima = True

                # Guarda la geometría responsiva actual.
                self.geometria_normal = QtCore.QRect(
                    self.boton.geometry()
                )

                self.boton.raise_()

                self.animar_geometria(
                    self.obtener_geometria_grande()
                )

                self.animar_sombra(28)

            elif evento.type() == QtCore.QEvent.Type.Leave:
                if self.cursor_encima:
                    self.cursor_encima = False

                    self.animar_geometria(
                        self.geometria_normal
                    )

                    self.animar_sombra(10)

            elif evento.type() == QtCore.QEvent.Type.EnabledChange:
                if not self.boton.isEnabled():
                    self.restaurar_inmediatamente()

        return super().eventFilter(
            objeto,
            evento
        )

class DelegadoFilasEspaciadas(QtWidgets.QStyledItemDelegate):
    """
    Reduce el área pintada de cada celda para dejar
    un espacio transparente entre usuarios.
    """

    def __init__(
        self,
        espacio_vertical=20,
        parent=None
    ):
        super().__init__(parent)

        self.espacio_vertical = espacio_vertical

    def paint(self, painter, option, index):
        opcion = QtWidgets.QStyleOptionViewItem(
            option
        )

        mitad_espacio = (
            self.espacio_vertical // 2
        )

        opcion.rect = option.rect.adjusted(
            0,
            mitad_espacio,
            0,
            -mitad_espacio
        )

        super().paint(
            painter,
            opcion,
            index
        )

    def establecer_espacio(self, espacio):
        """
        Permite modificar la separación después de
        crear el delegado.
        """

        self.espacio_vertical = max(
            0,
            int(espacio)
        )

        if self.parent() is not None:
            self.parent().viewport().update()


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

        self.botones_navegacion = [
            self.btn_volver,
            self.btn_anterior,
            self.btn_siguiente,
        ]

        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=self.botones_navegacion,
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.configurar_botones()

        self.efectos_hover = [
            EfectoHoverBoton(
                boton=boton,
                factor=1.04,
                duracion=120,
                parent=self
            )
            for boton in self.botones_navegacion
        ]

        QtCore.QTimer.singleShot(
            0,
            self.actualizar_hover_botones
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

        # Configuración visual de las filas.
        self.alto_contenido_usuario = 50
        self.espacio_entre_usuarios = 32

        self.configurar_tabla()
        self.posicionar_elementos()
        self.conectar_eventos()
        self.cargar_usuarios()

    def configurar_botones(self):
        for boton in self.botones_navegacion:
            boton.setCursor(
                QtGui.QCursor(
                    QtCore.Qt.CursorShape.PointingHandCursor
                )
            )

    def actualizar_hover_botones(self):
        """
        Actualiza la geometría base después de que
        BotonesResponsivos cambia el tamaño de los botones.
        """

        for efecto in getattr(
            self,
            "efectos_hover",
            []
        ):
            efecto.actualizar_geometria_base()

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

        if hasattr(self, "Visualizar_Usuarios"):
            self.Visualizar_Usuarios.setGeometry(
                0,
                0,
                self.width(),
                self.height()
            )

            self.Visualizar_Usuarios.raise_()

        if hasattr(self, "lbl_logo"):
            self.lbl_logo.raise_()

        if hasattr(self, "logo_reutilizable"):
            self.logo_reutilizable.actualizar()

        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        self.posicionar_elementos()

        if hasattr(self, "efectos_hover"):
            QtCore.QTimer.singleShot(
                0,
                self.actualizar_hover_botones
            )

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

        # Tabla un poco más pequeña y centrada.
        x_tabla = int(
            201 * escala_x
        )

        y_tabla = int(
            435 * escala_y
        )

        ancho_tabla = int(
            1530 * escala_x
        )

        alto_tabla = int(
            700 * escala_y
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

        self.delegado_filas = DelegadoFilasEspaciadas(
            espacio_vertical=self.espacio_entre_usuarios,
            parent=self.dgv_visualizarusuarios
        )

        self.dgv_visualizarusuarios.setItemDelegate(
            self.delegado_filas
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
                selection-background-color: transparent;
                selection-color: white;
                outline: none;
            }

            QTableView::item {
                background: transparent;
                border: none;
                padding: 4px 6px;
            }

            QTableView::item:selected {
                background-color: #0B73D9;
                color: white;
                border: none;
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
            self.actualizar_interfaz
        )

        QtCore.QTimer.singleShot(
            100,
            self.actualizar_interfaz
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
        Ajusta la altura real de las filas y deja espacio
        visible entre cada usuario.
        """

        if not hasattr(
                self,
                "dgv_visualizarusuarios"
        ):
            return

        if not hasattr(
                self,
                "modelo"
        ):
            return

        escala_y = (
                self.height()
                / self.ALTO_BASE
        )

        # Evita que las filas queden demasiado pequeñas.
        escala_y = max(
            0.70,
            escala_y
        )

        alto_contenido = int(
            self.alto_contenido_usuario
            * escala_y
        )

        espacio = int(
            self.espacio_entre_usuarios
            * escala_y
        )

        # La altura total incluye el contenido y el espacio.
        alto_fila = (
                alto_contenido
                + espacio
        )

        encabezado_vertical = (
            self.dgv_visualizarusuarios
            .verticalHeader()
        )

        encabezado_vertical.setMinimumSectionSize(
            1
        )

        encabezado_vertical.setDefaultSectionSize(
            alto_fila
        )

        for fila in range(
                self.modelo.rowCount()
        ):
            self.dgv_visualizarusuarios.setRowHeight(
                fila,
                alto_fila
            )

        # Mantiene sincronizado el delegado.
        if hasattr(
                self,
                "delegado_filas"
        ):
            self.delegado_filas.establecer_espacio(
                espacio
            )

    def actualizar_interfaz(self):
        if hasattr(self, "botones_responsivos"):
            self.botones_responsivos.ajustar()

        self.posicionar_elementos()
        self.actualizar_hover_botones()


if __name__ == "__main__":
    app = QtWidgets.QApplication(
        sys.argv
    )

    ventana = VisualizarUsuario()
    ventana.show()

    sys.exit(
        app.exec()
    )