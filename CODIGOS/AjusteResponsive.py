from PyQt6 import QtCore, QtWidgets


class BotonesResponsivos(QtCore.QObject):
    """
    Ajusta automáticamente la posición y el tamaño de botones
    tomando como referencia una resolución base.
    """

    def __init__(
        self,
        ventana: QtWidgets.QWidget,
        botones: list,
        ancho_base: int = 1920,
        alto_base: int = 1080,
        escalar_iconos: bool = True,
        escalar_fuentes: bool = False,
    ):
        super().__init__(ventana)

        self.ventana = ventana
        self.ancho_base = ancho_base
        self.alto_base = alto_base
        self.escalar_iconos = escalar_iconos
        self.escalar_fuentes = escalar_fuentes

        # Elimina elementos vacíos por seguridad.
        self.botones = [
            boton
            for boton in botones
            if boton is not None
        ]

        self.geometrias_originales = {}
        self.iconos_originales = {}
        self.fuentes_originales = {}

        self._guardar_datos_originales()

        # Detecta automáticamente cuando cambia el tamaño de la ventana.
        self.ventana.installEventFilter(self)

        # Realiza el primer ajuste después de mostrar la ventana.
        QtCore.QTimer.singleShot(0, self.ajustar)

    def _guardar_datos_originales(self):
        """
        Guarda la posición y el tamaño que cada botón tiene
        en Qt Designer.
        """

        for boton in self.botones:
            self.geometrias_originales[boton] = QtCore.QRect(
                boton.geometry()
            )

            self.iconos_originales[boton] = QtCore.QSize(
                boton.iconSize()
            )

            self.fuentes_originales[boton] = (
                boton.font().pointSizeF()
            )

            # Permite modificar libremente el tamaño del botón.
            boton.setMinimumSize(0, 0)
            boton.setMaximumSize(
                16777215,
                16777215,
            )

    def eventFilter(self, objeto, evento):
        """
        Se ejecuta cuando la ventana cambia de tamaño
        o termina de mostrarse.
        """

        if objeto is self.ventana:
            if evento.type() in (
                QtCore.QEvent.Type.Resize,
                QtCore.QEvent.Type.Show,
            ):
                self.ajustar()

        return super().eventFilter(objeto, evento)

    def ajustar(self):
        """
        Escala la posición y el tamaño de todos los botones.
        """

        if not self.geometrias_originales:
            return

        ancho_actual = max(1, self.ventana.width())
        alto_actual = max(1, self.ventana.height())

        escala_x = ancho_actual / self.ancho_base
        escala_y = alto_actual / self.alto_base

        for boton in self.botones:
            rect_original = self.geometrias_originales[boton]

            nueva_x = round(
                rect_original.x() * escala_x
            )

            nueva_y = round(
                rect_original.y() * escala_y
            )

            nuevo_ancho = round(
                rect_original.width() * escala_x
            )

            nuevo_alto = round(
                rect_original.height() * escala_y
            )

            boton.setGeometry(
                nueva_x,
                nueva_y,
                max(1, nuevo_ancho),
                max(1, nuevo_alto),
            )

            self._ajustar_icono(
                boton,
                escala_x,
                escala_y,
            )

            self._ajustar_fuente(
                boton,
                escala_x,
                escala_y,
            )

            # Mantiene el botón encima del fondo.
            boton.raise_()

    def _ajustar_icono(
        self,
        boton,
        escala_x,
        escala_y,
    ):
        if not self.escalar_iconos:
            return

        if boton.icon().isNull():
            return

        tamano_original = self.iconos_originales[boton]

        nuevo_ancho = round(
            tamano_original.width() * escala_x
        )

        nuevo_alto = round(
            tamano_original.height() * escala_y
        )

        boton.setIconSize(
            QtCore.QSize(
                max(1, nuevo_ancho),
                max(1, nuevo_alto),
            )
        )

    def _ajustar_fuente(
        self,
        boton,
        escala_x,
        escala_y,
    ):
        if not self.escalar_fuentes:
            return

        tamano_original = self.fuentes_originales[boton]

        if tamano_original <= 0:
            return

        # Usa la escala menor para evitar letras deformadas.
        escala = min(escala_x, escala_y)

        fuente = boton.font()
        fuente.setPointSizeF(
            max(1, tamano_original * escala)
        )

        boton.setFont(fuente)


class ElementosResponsivos(QtCore.QObject):
    """
    Ajusta automáticamente cualquier QWidget:
    QPushButton, QLineEdit, QLabel, QTableView, etc.
    """

    def __init__(
        self,
        ventana,
        elementos,
        ancho_base=1920,
        alto_base=1080,
        escalar_iconos=True,
        escalar_fuentes=False,
    ):
        super().__init__(ventana)

        self.ventana = ventana
        self.elementos = [
            elemento
            for elemento in elementos
            if elemento is not None
        ]

        self.ancho_base = ancho_base
        self.alto_base = alto_base
        self.escalar_iconos = escalar_iconos
        self.escalar_fuentes = escalar_fuentes

        self.geometrias_originales = {}
        self.iconos_originales = {}
        self.fuentes_originales = {}

        self.guardar_datos_originales()

        self.ventana.installEventFilter(self)

        QtCore.QTimer.singleShot(0, self.ajustar)

    def guardar_datos_originales(self):
        for elemento in self.elementos:
            self.geometrias_originales[elemento] = QtCore.QRect(
                elemento.geometry()
            )

            self.fuentes_originales[elemento] = (
                elemento.font().pointSizeF()
            )

            # Solo los botones tienen iconSize().
            if isinstance(
                elemento,
                QtWidgets.QAbstractButton
            ):
                self.iconos_originales[elemento] = QtCore.QSize(
                    elemento.iconSize()
                )

            elemento.setMinimumSize(0, 0)
            elemento.setMaximumSize(
                16777215,
                16777215
            )

    def eventFilter(self, objeto, evento):
        if objeto is self.ventana:
            if evento.type() in (
                QtCore.QEvent.Type.Resize,
                QtCore.QEvent.Type.Show,
            ):
                self.ajustar()

        return super().eventFilter(objeto, evento)

    def ajustar(self):
        if not self.geometrias_originales:
            return

        escala_x = (
            self.ventana.width() / self.ancho_base
        )

        escala_y = (
            self.ventana.height() / self.alto_base
        )

        for elemento in self.elementos:
            rect_original = (
                self.geometrias_originales[elemento]
            )

            elemento.setGeometry(
                round(rect_original.x() * escala_x),
                round(rect_original.y() * escala_y),
                max(
                    1,
                    round(
                        rect_original.width()
                        * escala_x
                    )
                ),
                max(
                    1,
                    round(
                        rect_original.height()
                        * escala_y
                    )
                ),
            )

            self.ajustar_icono(
                elemento,
                escala_x,
                escala_y,
            )

            self.ajustar_fuente(
                elemento,
                escala_x,
                escala_y,
            )

            elemento.raise_()

    def ajustar_icono(
        self,
        elemento,
        escala_x,
        escala_y,
    ):
        if not self.escalar_iconos:
            return

        if not isinstance(
            elemento,
            QtWidgets.QAbstractButton
        ):
            return

        if elemento.icon().isNull():
            return

        tamano_original = self.iconos_originales[elemento]

        elemento.setIconSize(
            QtCore.QSize(
                max(
                    1,
                    round(
                        tamano_original.width()
                        * escala_x
                    )
                ),
                max(
                    1,
                    round(
                        tamano_original.height()
                        * escala_y
                    )
                ),
            )
        )

    def ajustar_fuente(
        self,
        elemento,
        escala_x,
        escala_y,
    ):
        if not self.escalar_fuentes:
            return

        tamano_original = (
            self.fuentes_originales[elemento]
        )

        if tamano_original <= 0:
            return

        escala = min(escala_x, escala_y)

        fuente = elemento.font()
        fuente.setPointSizeF(
            max(
                1,
                tamano_original * escala
            )
        )

        elemento.setFont(fuente)