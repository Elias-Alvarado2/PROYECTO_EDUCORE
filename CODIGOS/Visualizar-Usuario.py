import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui, QtCore

from ConexionBD import ConexionBD


class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.ruta_imagen = ruta_imagen
        self.pixmap_original = QtGui.QPixmap(str(self.ruta_imagen))

        self.setScaledContents(True)
        self.setGeometry(0, 0, ventana.width(), ventana.height())
        self.setPixmap(self.pixmap_original)

        # Mandar la imagen al fondo
        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(0, 0, ancho, alto)


class VisualizarUsuario(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Tamaño base del diseño original
        self.ANCHO_BASE = 1920
        self.ALTO_BASE = 1080

        # Carpeta CODIGOS
        BASE_DIR = Path(__file__).resolve().parent

        # Carpeta PROYECTO_EDUCORE
        PROYECTO_DIR = BASE_DIR.parent

        # Ruta del archivo .ui
        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Visualizar-Usuarios.ui"

        # Ruta de la imagen de fondo
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Visualizar_Usuarios.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        # Cargar diseño
        uic.loadUi(str(ruta_ui), self)

        # Tamaño inicial de la ventana
        self.resize(1920, 1080)

        # Crear fondo
        self.fondo = FondoImagen(self, ruta_imagen)

        # Conexión a la base de datos
        self.db = ConexionBD()

        # Configurar y cargar usuarios
        self.configurar_tabla()
        self.cargar_usuarios()

        # Posicionar tabla y total
        self.posicionar_elementos()

        # Botón volver
        if hasattr(self, "btn_Volver"):
            self.btn_Volver.clicked.connect(self.close)

        if hasattr(self, "btn_volver"):
            self.btn_volver.clicked.connect(self.close)

    def resizeEvent(self, event):
        if hasattr(self, "fondo"):
            self.fondo.actualizar_tamano(self.width(), self.height())
            self.fondo.lower()

        self.posicionar_elementos()

        super().resizeEvent(event)

    def posicionar_elementos(self):
        escala_x = self.width() / self.ANCHO_BASE
        escala_y = self.height() / self.ALTO_BASE

        # Área donde van los datos de la tabla
        x_tabla = int(185 * escala_x)
        y_tabla = int(455 * escala_y)
        ancho_tabla = int(1550 * escala_x)
        alto_tabla = int(370 * escala_y)

        self.dgv_visualizarusuarios.setGeometry(
            x_tabla,
            y_tabla,
            ancho_tabla,
            alto_tabla
        )

        self.dgv_visualizarusuarios.raise_()

        self.ajustar_columnas()

        # Número total de usuarios
        if hasattr(self, "lbl_totalusuarios"):
            x_total = int(510 * escala_x)
            y_total = int(882 * escala_y)
            ancho_total = int(80 * escala_x)
            alto_total = int(35 * escala_y)

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
                    font-size: 14px;
                    font-weight: bold;
                }
            """)

            self.lbl_totalusuarios.raise_()

    def configurar_tabla(self):
        # Modelo para llenar el QTableView
        self.modelo = QtGui.QStandardItemModel()

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

        self.modelo.setHorizontalHeaderLabels(encabezados)

        # Conectar modelo al QTableView
        self.dgv_visualizarusuarios.setModel(self.modelo)

        # No permitir editar celdas
        self.dgv_visualizarusuarios.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Seleccionar filas completas
        self.dgv_visualizarusuarios.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        # Solo seleccionar una fila
        self.dgv_visualizarusuarios.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )

        # Ocultar encabezado vertical y horizontal
        self.dgv_visualizarusuarios.verticalHeader().setVisible(False)
        self.dgv_visualizarusuarios.horizontalHeader().setVisible(False)

        # Usar anchos fijos para alinear con los títulos del diseño
        self.dgv_visualizarusuarios.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Fixed
        )

        # Quitar líneas fuertes
        self.dgv_visualizarusuarios.setShowGrid(False)
        self.dgv_visualizarusuarios.setAlternatingRowColors(False)

        # Altura de filas
        self.dgv_visualizarusuarios.verticalHeader().setDefaultSectionSize(42)

        # Quitar scroll horizontal para que no se salga del cuadro
        self.dgv_visualizarusuarios.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Estilo visual de la tabla
        self.dgv_visualizarusuarios.setStyleSheet("""
            QTableView {
                background: transparent;
                border: none;
                color: #082B5F;
                font-size: 12px;
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
        if not hasattr(self, "dgv_visualizarusuarios"):
            return

        ancho_tabla = self.dgv_visualizarusuarios.width()

        # Estos porcentajes controlan el ancho de cada columna.
        # Si un dato queda corrido, ajusta estos valores.
        porcentajes = [
            0.16,  # ID JUGADOR
            0.13,  # NOMBRE_USUARIO
            0.15,  # CORREO
            0.11,  # CONTRASEÑA
            0.12,  # PERSONAJE
            0.08,  # VIDAS
            0.15,  # FECHA_REGISTRO
            0.09   # ESTADO
        ]

        for columna, porcentaje in enumerate(porcentajes):
            self.dgv_visualizarusuarios.setColumnWidth(
                columna,
                int(ancho_tabla * porcentaje)
            )

    def crear_item(self, texto):
        if texto is None:
            texto = ""

        item = QtGui.QStandardItem(str(texto))
        item.setEditable(False)
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        return item

    def cargar_usuarios(self):
        try:
            usuarios = self.db.obtener_jugadores()

            # Limpiar tabla antes de cargar datos
            self.modelo.removeRows(0, self.modelo.rowCount())

            for usuario in usuarios:
                fila = [
                    self.crear_item(usuario["id_jugador"]),
                    self.crear_item(usuario["nombre"]),
                    self.crear_item(usuario["correo"]),
                    self.crear_item(usuario["contraseña"]),
                    self.crear_item(usuario["personaje"]),
                    self.crear_item(usuario["vidas"]),
                    self.crear_item(usuario["fecha_registro"]),
                    self.crear_item(usuario["estado"])
                ]

                self.modelo.appendRow(fila)

            # Aquí solo va el número, porque el texto
            # "Total de usuarios:" ya está en la imagen.
            self.lbl_totalusuarios.setText(str(len(usuarios)))

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error de base de datos",
                str(e)
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = VisualizarUsuario()
    ventana.show()
    sys.exit(app.exec())