import sys
import math
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt6.QtGui import (
    QPixmap, QFont, QFontDatabase, QPainter,
    QColor, QPen, QBrush, QPolygon
)
from PyQt6.QtCore import Qt, QTimer, QPoint, QRectF

from Transicion import FormTransicion


class BarraPixelArt(QWidget):

    COLOR_BORDE = QColor("#DCE8FF")
    COLOR_LLENO = QColor("#8EA2FF")
    COLOR_VACIO = QColor("#FFFFFF")
    TRANSPARENTE = QColor(0, 0, 0, 0)

    NUM_SEG = 10
    GAP = 4
    PADDING = 4
    BORDE_G = 4
    CORTE = 7
    RADIO_CUADRO = 6

    def __init__(self, parent=None):
        super().__init__(parent)

        self.progreso = 0

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

    def set_progreso(self, valor: int):
        self.progreso = max(0, min(100, valor))
        self.update()

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        ancho = self.width()
        alto = self.height()

        corte = self.CORTE
        grosor = self.BORDE_G

        contorno = QPolygon([
            QPoint(corte, 0),
            QPoint(ancho - corte, 0),
            QPoint(ancho, corte),
            QPoint(ancho, alto - corte),
            QPoint(ancho - corte, alto),
            QPoint(corte, alto),
            QPoint(0, alto - corte),
            QPoint(0, corte),
        ])

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.TRANSPARENTE))
        painter.drawPolygon(contorno)

        pen = QPen(self.COLOR_BORDE, grosor)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPolygon(contorno)

        padding = self.PADDING + grosor
        area_ancho = ancho - 2 * padding
        area_alto = alto - 2 * padding

        cuadro_alto = area_alto
        cuadro_ancho = int(cuadro_alto * 1.18)

        total_ancho = self.NUM_SEG * cuadro_ancho + (self.NUM_SEG - 1) * self.GAP

        if total_ancho > area_ancho:
            cuadro_ancho = (area_ancho - (self.NUM_SEG - 1) * self.GAP) // self.NUM_SEG
            cuadro_alto = min(area_alto, cuadro_ancho)
            total_ancho = self.NUM_SEG * cuadro_ancho + (self.NUM_SEG - 1) * self.GAP

        inicio_x = padding + (area_ancho - total_ancho) // 2
        inicio_y = padding + (area_alto - cuadro_alto) // 2

        cuadros_llenos = round(self.NUM_SEG * self.progreso / 100)

        painter.setPen(Qt.PenStyle.NoPen)

        for i in range(self.NUM_SEG):
            x = inicio_x + i * (cuadro_ancho + self.GAP)
            y = inicio_y

            color = self.COLOR_LLENO if i < cuadros_llenos else self.COLOR_VACIO
            painter.setBrush(QBrush(color))

            rect = QRectF(x, y, cuadro_ancho, cuadro_alto)
            painter.drawRoundedRect(rect, self.RADIO_CUADRO, self.RADIO_CUADRO)

        painter.end()


class PantallaCarga(QWidget):
    def __init__(self, ventana_destino=None):
        super().__init__()

        self.ventana_destino = ventana_destino

        self.setWindowTitle("EduCore - Cargando")
        self.setFixedSize(1920, 1080)

        self.BASE_DIR = Path(__file__).resolve().parent
        self.PROYECTO_DIR = self.BASE_DIR.parent

        self.ruta_fondo = self.PROYECTO_DIR / "assets" / "DISEÑOS" / "fondo_carga.png"
        self.ruta_fuente = self.PROYECTO_DIR / "assets" / "FUENTES" / "Orbitron-Medium.ttf"
        self.ruta_logo = self.PROYECTO_DIR / "assets" / "DISEÑOS" / "logoblanco.png"

        self.nombre_fuente = self._cargar_fuente()

        self.fondo = QLabel(self)
        self.fondo.setGeometry(0, 0, 1920, 1080)

        if self.ruta_fondo.exists():
            pixmap_fondo = QPixmap(str(self.ruta_fondo))

            self.fondo.setPixmap(
                pixmap_fondo.scaled(
                    self.size(),
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            self.fondo.setStyleSheet("""
                QLabel {
                    background-color: #F6E6C9;
                }
            """)
            print("No se encontró el fondo:", self.ruta_fondo)

        self.fondo.lower()

        self.logo = QLabel(self)

        self.logo_x = 810
        self.logo_y_neutro = 145
        self.logo_ancho = 300
        self.logo_alto = 400

        self.logo.setGeometry(
            self.logo_x,
            self.logo_y_neutro,
            self.logo_ancho,
            self.logo_alto
        )

        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.logo.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
            }
        """)

        if self.ruta_logo.exists():
            pixmap_logo = QPixmap(str(self.ruta_logo))

            self.logo.setPixmap(
                pixmap_logo.scaled(
                    300,
                    300,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            self.logo.setText("LOGO")
            self.logo.setFont(QFont(self.nombre_fuente, 24, QFont.Weight.Bold))
            self.logo.setStyleSheet("""
                QLabel {
                    color: #172B55;
                    background: transparent;
                    border: none;
                }
            """)
            print("No se encontró el logo:", self.ruta_logo)

        colores = [
            "#FFFFFF",
            "#FFFFFF",
            "#FFFFFF",
            "#FFFFFF",
            "#FFFFFF",
            "#FFFFFF",
            "#FFFFFF",
        ]

        texto = "educore"

        FONT_PT = 100
        STEP = 130

        X_INI = 505
        Y_BASE = 540

        CELL_W = 120
        CELL_H = 140

        self.y_neutro = [Y_BASE for _ in range(len(texto))]
        self.letras = []

        for i, letra in enumerate(texto):
            label_letra = QLabel(letra, self)

            label_letra.setGeometry(
                X_INI + i * STEP,
                self.y_neutro[i],
                CELL_W,
                CELL_H
            )

            label_letra.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_letra.setFont(QFont(self.nombre_fuente, FONT_PT, QFont.Weight.Bold))
            label_letra.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            label_letra.setStyleSheet(f"""
                QLabel {{
                    color: {colores[i]};
                    background: transparent;
                    border: none;
                }}
            """)

            self.letras.append(label_letra)

        self.porcentaje = 0

        self.lbl_porcentaje = QLabel("0%", self)
        self.lbl_porcentaje.setGeometry(0, 735, 1920, 45)
        self.lbl_porcentaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_porcentaje.setFont(QFont(self.nombre_fuente, 24, QFont.Weight.Bold))
        self.lbl_porcentaje.setStyleSheet("""
            QLabel {
                color: #DCE8FF;
                background: transparent;
                border: none;
            }
        """)

        BARRA_W = 520
        BARRA_H = 70
        BARRA_X = (1920 - BARRA_W) // 2
        BARRA_Y = 800

        self.barra = BarraPixelArt(self)
        self.barra.setGeometry(BARRA_X, BARRA_Y, BARRA_W, BARRA_H)

        self.t = 0.0

        self.VELOCIDAD_LETRAS = 0.35
        self.AMPLITUD_LETRAS = 35
        self.DESFASE_LETRAS = 0.70

        self.VELOCIDAD_LOGO = 0.18
        self.AMPLITUD_LOGO = 12

        self.timer_animacion = QTimer(self)
        self.timer_animacion.timeout.connect(self._tick_animaciones)
        self.timer_animacion.start(16)

        self.timer_carga = QTimer(self)
        self.timer_carga.timeout.connect(self._tick_carga)
        self.timer_carga.start(350)

    def _cargar_fuente(self) -> str:
        if not self.ruta_fuente.exists():
            print("WARN: Orbitron no encontrada. Se usará Arial.")
            return "Arial"

        id_fuente = QFontDatabase.addApplicationFont(str(self.ruta_fuente))

        if id_fuente == -1:
            print("WARN: No se pudo cargar Orbitron. Se usará Arial.")
            return "Arial"

        familias = QFontDatabase.applicationFontFamilies(id_fuente)

        if familias:
            return familias[0]

        return "Arial"

    def _tick_animaciones(self):
        self.t += 0.016

        omega_letras = self.VELOCIDAD_LETRAS * 2 * math.pi

        for i, label_letra in enumerate(self.letras):
            fase = omega_letras * self.t + i * self.DESFASE_LETRAS
            offset = int(self.AMPLITUD_LETRAS * math.sin(fase))
            nueva_y = self.y_neutro[i] + offset

            rect = label_letra.geometry()
            label_letra.setGeometry(
                rect.x(),
                nueva_y,
                rect.width(),
                rect.height()
            )

        omega_logo = self.VELOCIDAD_LOGO * 2 * math.pi
        offset_logo = int(self.AMPLITUD_LOGO * math.sin(omega_logo * self.t))

        rect_logo = self.logo.geometry()
        self.logo.setGeometry(
            rect_logo.x(),
            self.logo_y_neutro + offset_logo,
            rect_logo.width(),
            rect_logo.height()
        )

    def _tick_carga(self):
        if self.porcentaje >= 100:
            self.timer_carga.stop()
            return

        self.porcentaje = min(self.porcentaje + 10, 100)

        self.lbl_porcentaje.setText(f"{self.porcentaje}%")
        self.barra.set_progreso(self.porcentaje)

        if self.porcentaje == 100:
            self.timer_carga.stop()
            QTimer.singleShot(500, self.abrir_ventana_destino)

    def abrir_ventana_destino(self):
        if self.timer_animacion.isActive():
            self.timer_animacion.stop()

        if self.ventana_destino is None:
            QMessageBox.warning(
                self,
                "Sin ventana destino",
                "La pantalla de carga llegó al 100%, pero no tiene una ventana destino."
            )
            return

        FormTransicion(
            self,
            self.ventana_destino
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = PantallaCarga()
    ventana.showMaximized()

    sys.exit(app.exec())