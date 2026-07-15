from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets


class LogoReutilizable(QtCore.QObject):
    def __init__(self, ventana, ruta_logo):
        super().__init__(ventana)

        self.ventana = ventana

        self.lbl_logo = ventana.findChild(
            QtWidgets.QLabel,
            "lbl_logo"
        )

        if self.lbl_logo is None:
            print("ERROR: No se encontró el QLabel llamado lbl_logo")
            return

        # Guarda la posición y tamaño establecidos en Qt Designer
        self.geometria_original = QtCore.QRect(
            self.lbl_logo.geometry()
        )

        self.ancho_original_ventana = max(1, ventana.width())
        self.alto_original_ventana = max(1, ventana.height())

        self.ruta_logo = Path(ruta_logo)

        print("Ruta del logo:", self.ruta_logo)
        print("¿Existe?:", self.ruta_logo.exists())
        print("Geometría original:", self.geometria_original)

        if not self.ruta_logo.exists():
            print(f"ERROR: No existe el logo: {self.ruta_logo}")
            return

        self.pixmap_original = QtGui.QPixmap(
            str(self.ruta_logo)
        )

        if self.pixmap_original.isNull():
            print("ERROR: Qt no pudo cargar la imagen")
            return

        self.lbl_logo.setVisible(True)
        self.lbl_logo.setEnabled(True)
        self.lbl_logo.setScaledContents(False)

        self.lbl_logo.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.lbl_logo.setStyleSheet(
            "background-color: transparent;"
            "border: none;"
        )

        # Detecta cambios de tamaño de la ventana
        self.ventana.installEventFilter(self)

        QtCore.QTimer.singleShot(0, self.actualizar)

    def actualizar(self):
        if self.lbl_logo is None:
            return

        factor_x = (
            self.ventana.width()
            / self.ancho_original_ventana
        )

        factor_y = (
            self.ventana.height()
            / self.alto_original_ventana
        )

        geometria = self.geometria_original

        nueva_x = round(geometria.x() * factor_x)
        nueva_y = round(geometria.y() * factor_y)
        nuevo_ancho = round(geometria.width() * factor_x)
        nuevo_alto = round(geometria.height() * factor_y)

        self.lbl_logo.setGeometry(
            nueva_x,
            nueva_y,
            max(1, nuevo_ancho),
            max(1, nuevo_alto)
        )

        pixmap_escalado = self.pixmap_original.scaled(
            self.lbl_logo.size(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )

        self.lbl_logo.setPixmap(pixmap_escalado)

        # Lo coloca encima del fondo
        self.lbl_logo.raise_()

    def eventFilter(self, objeto, evento):
        if (
            objeto is self.ventana
            and evento.type() == QtCore.QEvent.Type.Resize
        ):
            # Espera a que el responsive termine de mover elementos
            QtCore.QTimer.singleShot(0, self.actualizar)

        return super().eventFilter(objeto, evento)