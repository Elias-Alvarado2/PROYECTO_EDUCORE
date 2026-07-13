import math
from PyQt6 import QtCore, QtGui, QtWidgets


class CapaTransicionPixel(QtWidgets.QWidget):
    def __init__(self, abrir_destino_callback):
        super().__init__()

        self.abrir_destino_callback = abrir_destino_callback

        self.tamano_pixel = 34
        self.color = QtGui.QColor(15, 27, 45)

        self.duracion_cubrir = 750
        self.duracion_mostrar = 850

        self.fase = "cubrir"
        self.progreso = 0
        self.destino_abierto = False
        self.cubrir_todo = False

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
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating)

        pantalla = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(pantalla)

    def iniciar(self):
        self.fase = "cubrir"
        self.progreso = 0
        self.destino_abierto = False
        self.cubrir_todo = False

        pantalla = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(pantalla)

        self.show()
        self.raise_()

        self.reloj.restart()
        self.timer.start(16)

    def actualizar_animacion(self):
        self.raise_()

        tiempo = self.reloj.elapsed()

        if self.fase == "cubrir":
            self.progreso = min(tiempo / self.duracion_cubrir, 0.75)

            if self.progreso >= 0.75 and not self.destino_abierto:
                self.destino_abierto = True

                # Tapa totalmente la pantalla antes de cambiar de form
                self.cubrir_todo = True
                self.update()
                QtWidgets.QApplication.processEvents()

                # Aquí se muestra el form destino ya cargado
                self.abrir_destino_callback()

                self.raise_()
                QtWidgets.QApplication.processEvents()

                # Segunda pasada: revela el nuevo form
                self.cubrir_todo = False
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

        if self.cubrir_todo:
            painter.drawRect(self.rect())
            return

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


def FormDestino(
    clase_o_instancia_destino,
    args,
    kwargs,
    maximizado=True,
    tamano_normal=None
):
    if isinstance(clase_o_instancia_destino, QtWidgets.QWidget):
        ventana_destino = clase_o_instancia_destino
    else:
        ventana_destino = clase_o_instancia_destino(*args, **kwargs)

    ventana_destino.setWindowOpacity(0)

    if maximizado:
        pantalla = QtWidgets.QApplication.primaryScreen().availableGeometry()
        ventana_destino.setGeometry(pantalla)
        ventana_destino.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
    else:
        ventana_destino.setWindowState(QtCore.Qt.WindowState.WindowNoState)

        if tamano_normal is not None:
            ancho, alto = tamano_normal
            ventana_destino.resize(ancho, alto)

    ventana_destino.ensurePolished()
    ventana_destino.update()

    return ventana_destino


def FormTransicion(
    ventana_actual,
    clase_o_instancia_destino,
    *args,
    guardar_actual=True,
    maximizado=True,
    tamano_normal=None,
    **kwargs
):
    app = QtWidgets.QApplication.instance()

    if not hasattr(app, "historial_forms"):
        app.historial_forms = []

    if not hasattr(app, "ventanas_abiertas"):
        app.ventanas_abiertas = []

    # El form destino se crea antes de iniciar la transición
    # para que no cargue a medias cuando se muestre.
    ventana_destino = FormDestino(
        clase_o_instancia_destino,
        args,
        kwargs,
        maximizado=maximizado,
        tamano_normal=tamano_normal
    )

    app.ventanas_abiertas.append(ventana_destino)

    def mostrar_destino_cargado():
        if guardar_actual and ventana_actual is not None:
            app.historial_forms.append(ventana_actual)

        app.ventana_actual = ventana_destino

        # Se muestra invisible primero para que Qt termine de cargarlo
        ventana_destino.show()
        QtWidgets.QApplication.processEvents()

        if maximizado:
            ventana_destino.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        else:
            ventana_destino.setWindowState(QtCore.Qt.WindowState.WindowNoState)

        QtWidgets.QApplication.processEvents()

        # Ya cargado, se vuelve visible debajo de la capa de transición
        ventana_destino.setWindowOpacity(1)

        ventana_destino.raise_()
        ventana_destino.activateWindow()

        if ventana_actual is not None:
            ventana_actual.hide()

    capa = CapaTransicionPixel(
        abrir_destino_callback=mostrar_destino_cargado
    )

    app.capa_transicion = capa
    capa.iniciar()


def FormAnterior(
    ventana_actual,
    maximizado=True,
    tamano_normal=None
):
    app = QtWidgets.QApplication.instance()

    if not hasattr(app, "historial_forms") or len(app.historial_forms) == 0:
        QtWidgets.QMessageBox.warning(
            ventana_actual,
            "Sin pantalla anterior",
            "No hay una pantalla anterior a la cual regresar."
        )
        return

    ventana_anterior = app.historial_forms.pop()

    FormTransicion(
        ventana_actual,
        ventana_anterior,
        guardar_actual=False,
        maximizado=maximizado,
        tamano_normal=tamano_normal
    )