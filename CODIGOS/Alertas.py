from PyQt6 import QtCore, QtGui, QtWidgets


class Alertas(QtWidgets.QDialog):

    TIPOS = {
        "informacion": {
            "icono": "i",
            "color": "#168FA0"
        },
        "exito": {
            "icono": "✓",
            "color": "#079B87"
        },
        "advertencia": {
            "icono": "!",
            "color": "#F28C18"
        },
        "error": {
            "icono": "×",
            "color": "#E94B35"
        }
    }

    def __init__(
        self,
        parent=None,
        titulo="Información",
        mensaje="",
        tipo="informacion",
        confirmacion=False,
        texto_confirmar="ACEPTAR",
        texto_cancelar="CANCELAR"
    ):
        super().__init__(parent)

        self.confirmacion = confirmacion

        # =====================================================
        # CONFIGURACIÓN DE LA VENTANA
        # =====================================================

        self.setModal(True)
        self.setFixedSize(520, 320)

        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
        )

        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )

        configuracion = self.TIPOS.get(
            tipo.lower(),
            self.TIPOS["informacion"]
        )

        icono = configuracion["icono"]
        color = configuracion["color"]

        # =====================================================
        # LAYOUT PRINCIPAL
        # =====================================================

        layout_principal = QtWidgets.QVBoxLayout(self)
        layout_principal.setContentsMargins(12, 12, 12, 12)

        self.contenedor = QtWidgets.QFrame()
        self.contenedor.setObjectName("contenedor")

        layout_principal.addWidget(self.contenedor)

        # Sombra
        sombra = QtWidgets.QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(30)
        sombra.setOffset(0, 8)
        sombra.setColor(QtGui.QColor(0, 0, 0, 110))

        self.contenedor.setGraphicsEffect(sombra)

        layout_contenedor = QtWidgets.QVBoxLayout(self.contenedor)
        layout_contenedor.setContentsMargins(0, 0, 0, 22)
        layout_contenedor.setSpacing(0)

        # =====================================================
        # ENCABEZADO
        # =====================================================

        encabezado = QtWidgets.QFrame()
        encabezado.setObjectName("encabezado")
        encabezado.setFixedHeight(62)

        layout_encabezado = QtWidgets.QHBoxLayout(encabezado)
        layout_encabezado.setContentsMargins(24, 0, 14, 0)
        layout_encabezado.setSpacing(10)

        lbl_titulo = QtWidgets.QLabel(titulo)
        lbl_titulo.setObjectName("titulo")

        btn_cerrar = QtWidgets.QPushButton("×")
        btn_cerrar.setObjectName("btnCerrar")
        btn_cerrar.setFixedSize(36, 36)
        btn_cerrar.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )
        btn_cerrar.clicked.connect(self.reject)

        layout_encabezado.addWidget(lbl_titulo)
        layout_encabezado.addStretch()
        layout_encabezado.addWidget(btn_cerrar)

        layout_contenedor.addWidget(encabezado)

        # =====================================================
        # CUERPO DE LA ALERTA
        # =====================================================

        cuerpo = QtWidgets.QWidget()

        layout_cuerpo = QtWidgets.QHBoxLayout(cuerpo)
        layout_cuerpo.setContentsMargins(32, 28, 32, 20)
        layout_cuerpo.setSpacing(22)

        lbl_icono = QtWidgets.QLabel(icono)
        lbl_icono.setObjectName("icono")
        lbl_icono.setFixedSize(64, 64)
        lbl_icono.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        lbl_mensaje = QtWidgets.QLabel(mensaje)
        lbl_mensaje.setObjectName("mensaje")
        lbl_mensaje.setWordWrap(True)
        lbl_mensaje.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        lbl_mensaje.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        layout_cuerpo.addWidget(
            lbl_icono,
            alignment=QtCore.Qt.AlignmentFlag.AlignTop
        )
        layout_cuerpo.addWidget(lbl_mensaje, 1)

        layout_contenedor.addWidget(cuerpo, 1)

        # =====================================================
        # BOTONES
        # =====================================================

        layout_botones = QtWidgets.QHBoxLayout()
        layout_botones.setContentsMargins(32, 0, 32, 0)
        layout_botones.setSpacing(12)

        layout_botones.addStretch()

        if self.confirmacion:
            self.btn_cancelar = QtWidgets.QPushButton(texto_cancelar)
            self.btn_cancelar.setObjectName("btnCancelar")
            self.btn_cancelar.setFixedSize(135, 44)
            self.btn_cancelar.setCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
            self.btn_cancelar.clicked.connect(self.reject)

            self.btn_confirmar = QtWidgets.QPushButton(texto_confirmar)
            self.btn_confirmar.setObjectName("btnPrincipal")
            self.btn_confirmar.setFixedSize(165, 44)
            self.btn_confirmar.setCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
            self.btn_confirmar.clicked.connect(self.accept)
            self.btn_confirmar.setDefault(True)

            layout_botones.addWidget(self.btn_cancelar)
            layout_botones.addWidget(self.btn_confirmar)

        else:
            self.btn_aceptar = QtWidgets.QPushButton(texto_confirmar)
            self.btn_aceptar.setObjectName("btnPrincipal")
            self.btn_aceptar.setFixedSize(155, 44)
            self.btn_aceptar.setCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
            )
            self.btn_aceptar.clicked.connect(self.accept)
            self.btn_aceptar.setDefault(True)

            layout_botones.addWidget(self.btn_aceptar)

        layout_contenedor.addLayout(layout_botones)

        # =====================================================
        # ESTILOS
        # =====================================================

        self.setStyleSheet(f"""
            QFrame#contenedor {{
                background-color: #FFF8E9;
                border: 2px solid #3658C9;
                border-radius: 22px;
            }}

            QFrame#encabezado {{
                background-color: #071B4D;
                border: none;
                border-top-left-radius: 19px;
                border-top-right-radius: 19px;
            }}

            QLabel#titulo {{
                color: white;
                background-color: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 18px;
                font-weight: 700;
            }}

            QLabel#mensaje {{
                color: #14234D;
                background-color: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 15px;
            }}

            QLabel#icono {{
                color: white;
                background-color: {color};
                border: none;
                border-radius: 32px;
                font-family: "Segoe UI";
                font-size: 32px;
                font-weight: bold;
            }}

            QPushButton#btnCerrar {{
                color: white;
                background-color: transparent;
                border: none;
                border-radius: 18px;
                font-family: "Segoe UI";
                font-size: 27px;
                font-weight: bold;
            }}

            QPushButton#btnCerrar:hover {{
                background-color: #E94B35;
            }}

            QPushButton#btnCerrar:pressed {{
                background-color: #C83C2B;
            }}

            QPushButton#btnPrincipal {{
                color: white;
                background-color: {color};
                border: none;
                border-radius: 12px;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: bold;
                padding: 4px 12px;
            }}

            QPushButton#btnPrincipal:hover {{
                border: 2px solid rgba(255, 255, 255, 150);
            }}

            QPushButton#btnPrincipal:pressed {{
                padding-top: 6px;
                padding-bottom: 2px;
            }}

            QPushButton#btnCancelar {{
                color: #14234D;
                background-color: #E8EAF0;
                border: 1px solid #C5CAD6;
                border-radius: 12px;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: bold;
            }}

            QPushButton#btnCancelar:hover {{
                background-color: #D9DDE7;
                border: 1px solid #AEB5C4;
            }}

            QPushButton#btnCancelar:pressed {{
                background-color: #CACFDC;
            }}
        """)

    # =========================================================
    # CENTRAR LA ALERTA SOBRE LA VENTANA PADRE
    # =========================================================

    def showEvent(self, event):
        super().showEvent(event)

        ventana_padre = self.parentWidget()

        if ventana_padre is not None:
            geometria = self.frameGeometry()
            centro = ventana_padre.window().frameGeometry().center()

            geometria.moveCenter(centro)
            self.move(geometria.topLeft())
        else:
            pantalla = QtGui.QGuiApplication.primaryScreen()

            if pantalla is not None:
                geometria = self.frameGeometry()
                geometria.moveCenter(
                    pantalla.availableGeometry().center()
                )
                self.move(geometria.topLeft())

    # =========================================================
    # ALERTA NORMAL
    # =========================================================

    @staticmethod
    def mostrar(
        parent,
        titulo,
        mensaje,
        tipo="informacion",
        texto_boton="ACEPTAR"
    ):
        alerta = Alertas(
            parent=parent,
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo,
            confirmacion=False,
            texto_confirmar=texto_boton
        )

        alerta.exec()

    # =========================================================
    # ALERTA DE CONFIRMACIÓN
    # =========================================================

    @staticmethod
    def confirmar(
        parent,
        titulo,
        mensaje,
        tipo="advertencia",
        texto_confirmar="SÍ",
        texto_cancelar="NO"
    ):
        alerta = Alertas(
            parent=parent,
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo,
            confirmacion=True,
            texto_confirmar=texto_confirmar,
            texto_cancelar=texto_cancelar
        )

        resultado = alerta.exec()

        return (
            resultado
            == QtWidgets.QDialog.DialogCode.Accepted
        )