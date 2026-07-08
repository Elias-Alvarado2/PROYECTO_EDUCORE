import math
from PyQt6 import QtCore, QtGui, QtWidgets


class CapaTransicionPixel(QtWidgets.QWidget):
    def __init__(self, ventana_actual, abrir_destino_callback):
        super().__init__()

        self.ventana_actual = ventana_actual
        self.abrir_destino_callback = abrir_destino_callback

        self.tamano_pixel = 34
        self.color = QtGui.QColor(15, 27, 45)

        self.duracion_cubrir = 750
        self.duracion_mostrar = 850

        self.fase = "cubrir"
        self.progreso = 0
        self.destino_abierto = False

        self.reloj = QtCore.QElapsedTimer()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.actualizar_animacion)

        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.Tool |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        pantalla = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(pantalla)

    def iniciar(self):
        self.fase = "cubrir"
        self.progreso = 0
        self.destino_abierto = False

        pantalla = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(pantalla)

        self.show()
        self.raise_()
        self.reloj.start()
        self.timer.start(16)

    def actualizar_animacion(self):
        self.raise_()

        tiempo = self.reloj.elapsed()

        if self.fase == "cubrir":
            self.progreso = min(tiempo / self.duracion_cubrir, 0.75)

            if self.progreso >= 0.75 and not self.destino_abierto:
                self.destino_abierto = True

                self.abrir_destino_callback()

                self.fase = "mostrar"
                self.progreso = 0
                self.reloj.restart()

        elif self.fase == "mostrar":
            self.progreso = min(tiempo / self.duracion_mostrar, 1)

            if self.progreso >= 1:
                self.timer.stop()
                self.hide()
                self.deleteLater()
                return

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, False)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self.color)

        columnas = math.ceil(self.width() / self.tamano_pixel)
        filas = math.ceil(self.height() / self.tamano_pixel)

        diagonal_maxima = columnas + filas
        limite = int(self.progreso * diagonal_maxima)

        for fila in range(filas):
            for columna in range(columnas):
                diagonal = fila + columna

                if self.fase == "cubrir":
                    dibujar = diagonal <= limite
                else:
                    dibujar = diagonal > limite

                if dibujar:
                    x = columna * self.tamano_pixel
                    y = fila * self.tamano_pixel

                    painter.drawRect(
                        x,
                        y,
                        self.tamano_pixel,
                        self.tamano_pixel
                    )


def FormTransicion(ventana_actual, clase_o_instancia_destino, *args, **kwargs):
    app = QtWidgets.QApplication.instance()

    def abrir_destino():
        if isinstance(clase_o_instancia_destino, QtWidgets.QWidget):
            ventana_destino = clase_o_instancia_destino
        else:
            ventana_destino = clase_o_instancia_destino(*args, **kwargs)

        app.ventana_actual = ventana_destino

        ventana_destino.showMaximized()

        if ventana_actual is not None:
            ventana_actual.close()

    capa = CapaTransicionPixel(
        ventana_actual=ventana_actual,
        abrir_destino_callback=abrir_destino
    )

    app.capa_transicion = capa
    capa.iniciar()