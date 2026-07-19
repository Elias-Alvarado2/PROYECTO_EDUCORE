from __future__ import annotations

from pathlib import Path

import pygame
from PyQt6 import QtCore


class GestorAudio(QtCore.QObject):
    """
    Gestor global de audio de EduCore.

    Controla:
    - Volumen general de 0 a 100.
    - Silencio global.
    - Música de fondo.
    - Efectos de sonido.
    - Guardado permanente del volumen.
    - Sincronización entre PyQt6 y Pygame.
    """

    volumen_cambiado = QtCore.pyqtSignal(int)
    silencio_cambiado = QtCore.pyqtSignal(bool)

    ORGANIZACION = "EduCore"
    APLICACION = "EduCore"

    def __init__(self):
        super().__init__()

        self.configuracion = QtCore.QSettings(
            self.ORGANIZACION,
            self.APLICACION,
        )

        self._volumen = 70
        self._ultimo_volumen = 70
        self._silenciado = False

        # Guarda los canales creados por el gestor.
        self._canales_activos: list[
            pygame.mixer.Channel
        ] = []

        self.recargar(
            aplicar=False,
            emitir=False,
        )

    # =========================================================
    # CONVERSIONES
    # =========================================================

    @staticmethod
    def _limitar_volumen(valor) -> int:
        """
        Limita el volumen al rango de 0 a 100.
        """

        try:
            valor = int(valor)
        except (TypeError, ValueError):
            valor = 70

        return max(
            0,
            min(100, valor),
        )

    @staticmethod
    def _convertir_booleano(valor) -> bool:
        if isinstance(valor, bool):
            return valor

        return str(valor).strip().lower() in {
            "1",
            "true",
            "yes",
            "si",
            "sí",
        }

    # =========================================================
    # PROPIEDADES
    # =========================================================

    @property
    def volumen(self) -> int:
        """
        Volumen guardado de 0 a 100.
        """

        return self._volumen

    @property
    def silenciado(self) -> bool:
        return self._silenciado

    @property
    def porcentaje_actual(self) -> int:
        """
        Porcentaje que se debe mostrar en Ajustes.

        Cuando está silenciado devuelve 0.
        """

        if self._silenciado:
            return 0

        return self._volumen

    @property
    def volumen_normalizado(self) -> float:
        """
        Convierte el volumen de 0-100 al formato
        0.0-1.0 utilizado por Pygame.
        """

        if self._silenciado:
            return 0.0

        return self._volumen / 100.0

    # =========================================================
    # GUARDAR Y RECARGAR
    # =========================================================

    def guardar(self):
        """
        Guarda el volumen para que se conserve al cerrar EduCore.
        """

        self.configuracion.setValue(
            "audio/volumen",
            self._volumen,
        )

        self.configuracion.setValue(
            "audio/ultimo_volumen",
            self._ultimo_volumen,
        )

        self.configuracion.setValue(
            "audio/silenciado",
            self._silenciado,
        )

        self.configuracion.sync()

    def recargar(
        self,
        aplicar: bool = True,
        emitir: bool = False,
    ):
        """
        Vuelve a leer el volumen almacenado.

        El motor puede llamar este método mientras Ajustes está
        abierto en otro proceso para obtener los cambios del slider.
        """

        self.configuracion.sync()

        volumen_guardado = self.configuracion.value(
            "audio/volumen",
            70,
        )

        ultimo_guardado = self.configuracion.value(
            "audio/ultimo_volumen",
            70,
        )

        silencio_guardado = self.configuracion.value(
            "audio/silenciado",
            False,
        )

        self._volumen = self._limitar_volumen(
            volumen_guardado
        )

        self._ultimo_volumen = self._limitar_volumen(
            ultimo_guardado
        )

        self._silenciado = self._convertir_booleano(
            silencio_guardado
        )

        if self._ultimo_volumen <= 0:
            self._ultimo_volumen = 70

        if aplicar:
            self.aplicar_volumen()

        if emitir:
            self.volumen_cambiado.emit(
                self.porcentaje_actual
            )

            self.silencio_cambiado.emit(
                self._silenciado
            )

    # =========================================================
    # CAMBIAR VOLUMEN
    # =========================================================

    def establecer_volumen(
        self,
        valor: int,
    ):
        valor = self._limitar_volumen(
            valor
        )

        if valor > 0:
            self._volumen = valor
            self._ultimo_volumen = valor
            self._silenciado = False

        else:
            if self._volumen > 0:
                self._ultimo_volumen = self._volumen

            self._volumen = 0
            self._silenciado = True

        self.guardar()
        self.aplicar_volumen()

        self.volumen_cambiado.emit(
            self.porcentaje_actual
        )

        self.silencio_cambiado.emit(
            self._silenciado
        )

    def silenciar(self):
        """
        Silencia música y efectos sin perder el volumen anterior.
        """

        if self._volumen > 0:
            self._ultimo_volumen = self._volumen

        self._silenciado = True

        self.guardar()
        self.aplicar_volumen()

        self.volumen_cambiado.emit(0)
        self.silencio_cambiado.emit(True)

    def activar_sonido(self):
        """
        Recupera el volumen utilizado antes de silenciar.
        """

        self._silenciado = False

        if self._volumen <= 0:
            self._volumen = self._ultimo_volumen

        if self._volumen <= 0:
            self._volumen = 70

        self._ultimo_volumen = self._volumen

        self.guardar()
        self.aplicar_volumen()

        self.volumen_cambiado.emit(
            self._volumen
        )

        self.silencio_cambiado.emit(False)

    def alternar_silencio(self):
        if self._silenciado:
            self.activar_sonido()
        else:
            self.silenciar()

    # =========================================================
    # INICIALIZAR PYGAME MIXER
    # =========================================================

    def inicializar_mixer(self) -> bool:
        """
        Inicializa el mezclador de Pygame.

        Este método debe utilizarse desde el motor o antes de
        reproducir música y efectos.
        """

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()

            return True

        except pygame.error as error:
            print(
                "[AUDIO] No se pudo inicializar "
                f"pygame.mixer: {error}"
            )

            return False

    # =========================================================
    # APLICAR VOLUMEN
    # =========================================================

    def aplicar_volumen(self):
        """
        Aplica el volumen general a la música y a los canales.

        No inicializa el mixer automáticamente para evitar que
        el formulario PyQt6 abierto en otro proceso intente
        apropiarse del dispositivo de audio.
        """

        if pygame.mixer.get_init() is None:
            return

        volumen = self.volumen_normalizado

        try:
            pygame.mixer.music.set_volume(
                volumen
            )

            cantidad_canales = (
                pygame.mixer.get_num_channels()
            )

            for numero_canal in range(
                cantidad_canales
            ):
                canal = pygame.mixer.Channel(
                    numero_canal
                )

                canal.set_volume(
                    volumen
                )

            # Elimina referencias a canales que ya terminaron.
            self._canales_activos = [
                canal
                for canal in self._canales_activos
                if canal.get_busy()
            ]

        except pygame.error as error:
            print(
                "[AUDIO] No se pudo aplicar "
                f"el volumen: {error}"
            )

    # =========================================================
    # MÚSICA
    # =========================================================

    def reproducir_musica(
        self,
        ruta: str | Path,
        repetir: int = -1,
        fade_ms: int = 0,
    ) -> bool:
        """
        Reproduce música de fondo.

        repetir=-1 hace que se reproduzca infinitamente.
        """

        ruta = Path(ruta)

        if not ruta.is_file():
            print(
                "[AUDIO] No se encontró la música:",
                ruta,
            )
            return False

        if not self.inicializar_mixer():
            return False

        try:
            pygame.mixer.music.load(
                str(ruta)
            )

            pygame.mixer.music.set_volume(
                self.volumen_normalizado
            )

            pygame.mixer.music.play(
                loops=repetir,
                fade_ms=max(0, int(fade_ms)),
            )

            return True

        except pygame.error as error:
            print(
                "[AUDIO] No se pudo reproducir "
                f"la música: {error}"
            )

            return False

    def pausar_musica(self):
        if pygame.mixer.get_init() is not None:
            pygame.mixer.music.pause()

    def reanudar_musica(self):
        if pygame.mixer.get_init() is not None:
            pygame.mixer.music.unpause()
            self.aplicar_volumen()

    def detener_musica(
        self,
        fade_ms: int = 0,
    ):
        if pygame.mixer.get_init() is None:
            return

        try:
            if fade_ms > 0:
                pygame.mixer.music.fadeout(
                    int(fade_ms)
                )
            else:
                pygame.mixer.music.stop()

        except pygame.error as error:
            print(
                "[AUDIO] No se pudo detener "
                f"la música: {error}"
            )

    # =========================================================
    # EFECTOS
    # =========================================================

    def cargar_efecto(
        self,
        ruta: str | Path,
    ) -> pygame.mixer.Sound | None:
        """
        Carga un efecto de sonido.
        """

        ruta = Path(ruta)

        if not ruta.is_file():
            print(
                "[AUDIO] No se encontró el efecto:",
                ruta,
            )
            return None

        if not self.inicializar_mixer():
            return None

        try:
            return pygame.mixer.Sound(
                str(ruta)
            )

        except pygame.error as error:
            print(
                "[AUDIO] No se pudo cargar "
                f"el efecto: {error}"
            )

            return None

    def reproducir_efecto(
        self,
        sonido: pygame.mixer.Sound | None,
        volumen_relativo: float = 1.0,
        repeticiones: int = 0,
    ) -> pygame.mixer.Channel | None:
        """
        Reproduce un efecto respetando el volumen global.

        volumen_relativo:
            1.0 = volumen normal.
            0.5 = mitad del volumen global.
            0.0 = inaudible.
        """

        if sonido is None:
            return None

        if not self.inicializar_mixer():
            return None

        try:
            volumen_relativo = float(
                volumen_relativo
            )

        except (TypeError, ValueError):
            volumen_relativo = 1.0

        volumen_relativo = max(
            0.0,
            min(1.0, volumen_relativo),
        )

        try:
            canal = sonido.play(
                loops=int(repeticiones)
            )

            if canal is None:
                return None

            canal.set_volume(
                self.volumen_normalizado
                * volumen_relativo
            )

            self._canales_activos.append(
                canal
            )

            return canal

        except pygame.error as error:
            print(
                "[AUDIO] No se pudo reproducir "
                f"el efecto: {error}"
            )

            return None

    # =========================================================
    # DETENER AUDIO
    # =========================================================

    def detener_efectos(self):
        if pygame.mixer.get_init() is None:
            return

        try:
            pygame.mixer.stop()
            self._canales_activos.clear()

        except pygame.error as error:
            print(
                "[AUDIO] No se pudieron detener "
                f"los efectos: {error}"
            )

    def detener_todo(self):
        """
        Detiene la música y todos los efectos.
        """

        if pygame.mixer.get_init() is None:
            return

        try:
            pygame.mixer.music.stop()
            pygame.mixer.stop()

            self._canales_activos.clear()

        except pygame.error as error:
            print(
                "[AUDIO] No se pudo detener "
                f"todo el audio: {error}"
            )


# =============================================================
# INSTANCIA GLOBAL
# =============================================================

gestor_audio = GestorAudio()


__all__ = [
    "GestorAudio",
    "gestor_audio",
]
