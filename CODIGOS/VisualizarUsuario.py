import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from Alertas import Alertas
from ConexionBD import ConexionBD
from quitar_barra import quitar
from Transicion import FormTransicion, FormAnterior
from AjusteResponsive import BotonesResponsivos

class FondoImagen(QtWidgets.QLabel):
    def __init__(self, ventana, ruta_imagen):
        super().__init__(ventana)

        self.ruta_imagen = ruta_imagen
        self.pixmap_original = QtGui.QPixmap(str(self.ruta_imagen))

        self.setScaledContents(True)
        self.setGeometry(0, 0, ventana.width(), ventana.height())
        self.setPixmap(self.pixmap_original)

        self.lower()

    def actualizar_tamano(self, ancho, alto):
        self.setGeometry(0, 0, ancho, alto)


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

        ruta_ui = PROYECTO_DIR / "EXPO-DISEÑOS" / "DESIGNER" / "Visualizar-Usuarios.ui"
        ruta_imagen = PROYECTO_DIR / "assets" / "DISEÑOS" / "Visualizar_Usuarios.png"

        if not ruta_ui.exists():
            raise FileNotFoundError(f"No se encontró el archivo UI:\n{ruta_ui}")

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontró la imagen:\n{ruta_imagen}")

        uic.loadUi(str(ruta_ui), self)

        self.resize(1920, 1080)

        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)

        self.fondo = FondoImagen(self, ruta_imagen)

        self.botones_responsivos = BotonesResponsivos(
            ventana=self,
            botones=[
                self.btn_volver,
            ],
            ancho_base=1920,
            alto_base=1080,
            escalar_iconos=True,
            escalar_fuentes=False,
        )

        self.db = ConexionBD()

        self.configurar_tabla()
        self.cargar_usuarios()
        self.posicionar_elementos()
        self.conectar_eventos()

    def conectar_eventos(self):
        if hasattr(self, "btn_Volver"):
            self.btn_Volver.clicked.connect(self.volver_gestion_usuarios)

        if hasattr(self, "btn_volver"):
            self.btn_volver.clicked.connect(self.volver_gestion_usuarios)

    def volver_gestion_usuarios(self):
        try:
            app = QtWidgets.QApplication.instance()

            if hasattr(app, "historial_forms") and len(app.historial_forms) > 0:
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

        self.posicionar_elementos()

        super().resizeEvent(event)

    def posicionar_elementos(self):
        escala_x = self.width() / self.ANCHO_BASE
        escala_y = self.height() / self.ALTO_BASE

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

        self.dgv_visualizarusuarios.setModel(self.modelo)

        self.dgv_visualizarusuarios.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.dgv_visualizarusuarios.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.dgv_visualizarusuarios.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )

        self.dgv_visualizarusuarios.verticalHeader().setVisible(False)
        self.dgv_visualizarusuarios.horizontalHeader().setVisible(False)

        self.dgv_visualizarusuarios.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Fixed
        )

        self.dgv_visualizarusuarios.setShowGrid(False)
        self.dgv_visualizarusuarios.setAlternatingRowColors(False)

        self.dgv_visualizarusuarios.verticalHeader().setDefaultSectionSize(42)

        self.dgv_visualizarusuarios.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

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

            self.modelo.removeRows(0, self.modelo.rowCount())

            for usuario in usuarios:
                fila = [
                    self.crear_item(usuario["id_jugador"]),
                    self.crear_item(usuario["nombre"]),
                    self.crear_item(usuario["correo"]),
                    self.crear_item(usuario["contrasena"]),
                    self.crear_item(usuario["personaje"]),
                    self.crear_item(usuario["vidas"]),
                    self.crear_item(usuario["fecha_registro"]),
                    self.crear_item(usuario["estado"])
                ]

                self.modelo.appendRow(fila)

            self.lbl_totalusuarios.setText(str(len(usuarios)))

        except Exception as e:
            Alertas.mostrar(
                self,
                "Error de base de datos",
                str(e),
                "error"
            )

    def showEvent(self, event):
        super().showEvent(event)

        QtCore.QTimer.singleShot(0, self.posicionar_elementos)
        QtCore.QTimer.singleShot(100, self.posicionar_elementos)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ventana = VisualizarUsuario()
    ventana.show()

    sys.exit(app.exec())