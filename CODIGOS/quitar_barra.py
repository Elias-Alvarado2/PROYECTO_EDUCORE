from PyQt6.QtCore import Qt


def quitar(ventana):
   
    ventana.setWindowFlag(
        Qt.WindowType.FramelessWindowHint,
        True
    )