"""Cofre reutilizable para generar y enviar diplomas por correo."""

from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets

from Alertas import Alertas
from Diplomas import TareaEnvioDiploma, preparar_fuentes_diploma


# Posición y tamaño base del cofre en las ventanas de 1920 x 1080.
GEOMETRIA_COFRE = (1600, 890, 281, 171)

# Para cambiar las imágenes solo hay que editar estas rutas.
CARPETAS_COFRE = {
    "python": "botones pyhton",
    "java": "botones java",
    "mysql": "botones_MySQL",
}
IMAGEN_COFRE_CERRADO = "Cofre.png"
IMAGEN_COFRE_ABIERTO = "CofreAbierto.png"


def _valor_booleano(valor):
    if isinstance(valor, str):
        return valor.strip().casefold() in {
            "1",
            "true",
            "si",
            "sí",
            "yes",
        }

    return bool(valor)


class CofreDiplomaMixin:
    """Añade el mismo cofre y flujo de diploma a un selector de niveles."""

    def inicializar_cofre_diploma(self):
        self._envio_diploma_en_curso = False
        self._tarea_envio_diploma = None
        self._cofre_diploma_abierto = False
        self._progreso_actual = {}

        boton = getattr(self, "btnDiploma", None)

        if boton is None:
            boton = QtWidgets.QPushButton(self)
            boton.setObjectName("btnDiploma")
            boton.setGeometry(*GEOMETRIA_COFRE)
            self.btnDiploma = boton

        lenguaje = str(self.LENGUAJE).strip().casefold()
        carpeta = CARPETAS_COFRE.get(lenguaje)

        if not carpeta:
            raise ValueError(
                f"No hay imágenes de cofre configuradas para {self.LENGUAJE}."
            )

        base_botones = (
            Path(self.proyecto_dir)
            / "EXPO-DISEÑOS"
            / "botones"
            / carpeta
        )
        self._ruta_cofre_cerrado = base_botones / IMAGEN_COFRE_CERRADO
        self._ruta_cofre_abierto = base_botones / IMAGEN_COFRE_ABIERTO

        for ruta in (self._ruta_cofre_cerrado, self._ruta_cofre_abierto):
            if not ruta.is_file():
                raise FileNotFoundError(
                    f"No se encontró la imagen del cofre:\n{ruta}"
                )

        boton.setText("")
        boton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        boton.setToolTip("")
        boton.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor)
        )
        boton.clicked.connect(self.solicitar_envio_diploma)

        # QFontDatabase debe prepararse desde el hilo de la interfaz.
        preparar_fuentes_diploma()
        self.actualizar_estado_boton_diploma()

    def prueba_final_completada(self):
        return _valor_booleano(
            self._progreso_actual.get("prueba_completada", False)
        )

    def diploma_ya_enviado(self):
        return (
            self._cofre_diploma_abierto
            or _valor_booleano(
                self._progreso_actual.get("diploma_enviado", False)
            )
        )

    def _establecer_imagen_cofre(self, ruta):
        ruta_qss = Path(ruta).resolve().as_posix()
        self.btnDiploma.setStyleSheet(
            "QPushButton#btnDiploma {"
            "border: 0px;"
            "background-color: transparent;"
            "padding: 0px;"
            "margin: 0px;"
            f'border-image: url("{ruta_qss}") 0 0 0 0 stretch stretch;'
            "}"
        )

    def actualizar_estado_boton_diploma(self):
        boton = getattr(self, "btnDiploma", None)

        if boton is None:
            return

        completada = self.prueba_final_completada()
        sesion_valida = (
            not self.es_sesion_administrador()
            and self.obtener_id_jugador() is not None
        )
        visible = completada and sesion_valida
        abierto = visible and self.diploma_ya_enviado()

        if abierto:
            self._cofre_diploma_abierto = True

        ruta = (
            self._ruta_cofre_abierto
            if abierto
            else self._ruta_cofre_cerrado
        )
        self._establecer_imagen_cofre(ruta)
        boton.setVisible(visible)

        accionable = (
            visible
            and not abierto
            and not self._envio_diploma_en_curso
            and not self.nivel_en_ejecucion
        )
        boton.setEnabled(accionable)
        boton.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            abierto,
        )
        boton.setCursor(
            QtGui.QCursor(
                QtCore.Qt.CursorShape.PointingHandCursor
                if accionable
                else QtCore.Qt.CursorShape.ArrowCursor
            )
        )

        # Un cofre abierto es decorativo: no muestra mensajes ni ayuda.
        boton.setToolTip(
            ""
            if abierto or not visible
            else (
                "Enviando diploma..."
                if self._envio_diploma_en_curso
                else "Haz clic para enviar tu diploma por correo."
            )
        )

        if abierto:
            efecto = getattr(
                self,
                "efectos_hover_por_boton",
                {},
            ).get(boton)
            if efecto is not None:
                efecto.restaurar_sin_animacion()

    def solicitar_envio_diploma(self):
        # Si está abierto se ignora por completo: no hay alerta ni acción.
        if self.diploma_ya_enviado() or self._envio_diploma_en_curso:
            return

        # El cofre permanece oculto hasta completar la prueba final.
        if not self.prueba_final_completada():
            return

        id_jugador = self.obtener_id_jugador()
        if id_jugador is None or self.es_sesion_administrador():
            return

        correo = "el correo registrado"
        if isinstance(self.jugador, dict):
            correo = str(
                self.jugador.get("correo") or correo
            ).strip()

        respuesta = Alertas.confirmar(
            self,
            "Enviar diploma",
            (
                f"Se generará el diploma de {self.LENGUAJE} y se "
                f"enviará a:\n\n{correo}\n\n¿Deseas continuar?"
            ),
            tipo="informacion",
            texto_confirmar="ENVIAR",
            texto_cancelar="CANCELAR",
        )
        if not respuesta:
            return

        self._envio_diploma_en_curso = True
        self.actualizar_estado_boton_diploma()

        tarea = TareaEnvioDiploma(
            id_jugador=id_jugador,
            lenguaje=self.LENGUAJE,
        )
        tarea.senales.terminado.connect(self._al_enviar_diploma)
        tarea.senales.error.connect(self._al_fallar_envio_diploma)
        self._tarea_envio_diploma = tarea
        QtCore.QThreadPool.globalInstance().start(tarea)

    @QtCore.pyqtSlot(object)
    def _al_enviar_diploma(self, resultado):
        self._envio_diploma_en_curso = False
        self._tarea_envio_diploma = None
        self._cofre_diploma_abierto = True
        self._progreso_actual["diploma_enviado"] = True
        self.actualizar_estado_boton_diploma()

        print(
            "[DIPLOMA] Envío completado:",
            resultado.get("correo", ""),
            resultado.get("ruta_pdf", ""),
        )
        if not resultado.get("registrado_en_bd", False):
            print(
                "[DIPLOMA] El correo se envió, pero no se pudo guardar "
                "el estado abierto en la base de datos."
            )

    @QtCore.pyqtSlot(str)
    def _al_fallar_envio_diploma(self, detalle):
        self._envio_diploma_en_curso = False
        self._tarea_envio_diploma = None
        self.actualizar_estado_boton_diploma()

        Alertas.mostrar(
            self,
            "No se pudo enviar el diploma",
            (
                "No se generó o envió el diploma.\n\n"
                f"Detalles:\n{detalle}"
            ),
            "error",
        )
