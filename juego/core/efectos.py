"""Efectos de sonido reutilizables para los niveles de EduCore.

Para reemplazar un tono generado, coloca un archivo con el nombre indicado
en ``assets/efectos``. Se aceptan las extensiones .ogg, .wav y .mp3.
"""

from __future__ import annotations

from array import array
from dataclasses import dataclass
import math
from pathlib import Path

import pygame

from juego.sistemas.audio import gestor_audio


RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
EFECTOS_DIR = RAIZ_PROYECTO / "assets" / "efectos"

ENEMIGO_ELIMINADO = "enemigo_eliminado"
SALTO = "salto"
RESPUESTA_INCORRECTA = "respuesta_incorrecta"
RECIBIR_DANO = "recibir_dano"
RESPUESTA_CORRECTA = "respuesta_correcta"
MUERTE = "muerte"


@dataclass(frozen=True)
class ConfiguracionEfecto:
    """Nombre del archivo, volumen y tono usado cuando el archivo falta."""

    archivo: str
    volumen: float
    tonos_respaldo: tuple[tuple[float, int], ...]


# Este es el único bloque que debes editar para cambiar nombres o volúmenes.
CONFIGURACIONES = {
    ENEMIGO_ELIMINADO: ConfiguracionEfecto(
        archivo="enemigo_eliminado.ogg",
        volumen=0.85,
        tonos_respaldo=((520, 65), (760, 110)),
    ),
    SALTO: ConfiguracionEfecto(
        archivo="efecto_salto.ogg",
        volumen=0.30,
        tonos_respaldo=((420, 65), (620, 75)),
    ),
    RESPUESTA_INCORRECTA: ConfiguracionEfecto(
        archivo="respuesta_incorrecta.ogg",
        volumen=0.80,
        tonos_respaldo=((270, 110), (180, 170)),
    ),
    RECIBIR_DANO: ConfiguracionEfecto(
        archivo="recibir_dano.ogg",
        volumen=0.90,
        tonos_respaldo=((170, 80), (110, 120)),
    ),
    RESPUESTA_CORRECTA: ConfiguracionEfecto(
        archivo="respuesta_correcta.ogg",
        volumen=0.80,
        tonos_respaldo=((620, 80), (820, 80), (1040, 120)),
    ),
    MUERTE: ConfiguracionEfecto(
        archivo="sonido_muerte.ogg",
        volumen=0.80,
        tonos_respaldo=((210, 120), (150, 150), (90, 240)),
    ),
}


class GestorEfectos:
    """Carga y reproduce los efectos específicos del juego."""

    EXTENSIONES_ADMITIDAS = (".ogg", ".wav", ".mp3")

    def __init__(self):
        self.sonidos: dict[str, pygame.mixer.Sound | None] = {}
        self._configuracion_mixer = None
        self._faltantes_informados: set[str] = set()

    def _resolver_ruta(self, nombre_archivo: str) -> Path | None:
        ruta_preferida = EFECTOS_DIR / nombre_archivo

        if ruta_preferida.is_file():
            return ruta_preferida

        base = Path(nombre_archivo).stem

        for extension in self.EXTENSIONES_ADMITIDAS:
            alternativa = EFECTOS_DIR / f"{base}{extension}"

            if alternativa.is_file():
                return alternativa

        return None

    @staticmethod
    def _crear_tono_respaldo(
        tonos: tuple[tuple[float, int], ...],
    ) -> pygame.mixer.Sound | None:
        configuracion = pygame.mixer.get_init()

        if configuracion is None:
            return None

        frecuencia_muestreo, formato, canales = configuracion

        # Pygame utiliza -16 bits con signo de forma predeterminada.
        if formato != -16 or canales not in (1, 2):
            return None

        muestras = array("h")
        amplitud = 0.24 * 32767

        for frecuencia, duracion_ms in tonos:
            cantidad = max(
                1,
                round(frecuencia_muestreo * duracion_ms / 1000),
            )
            ataque = max(1, round(cantidad * 0.08))

            for indice in range(cantidad):
                entrada = min(1.0, indice / ataque)
                salida = max(0.0, 1.0 - indice / cantidad)
                envolvente = entrada * salida
                valor = round(
                    amplitud
                    * envolvente
                    * math.sin(
                        2.0
                        * math.pi
                        * float(frecuencia)
                        * indice
                        / frecuencia_muestreo
                    )
                )

                for _ in range(canales):
                    muestras.append(valor)

            silencio = round(frecuencia_muestreo * 0.012)

            for _ in range(silencio * canales):
                muestras.append(0)

        try:
            return pygame.mixer.Sound(buffer=muestras.tobytes())
        except pygame.error as error:
            print("[EFECTOS] No se pudo crear el tono de respaldo:", error)
            return None

    def cargar(self, forzar: bool = False) -> bool:
        """Carga archivos reales y crea tonos para los que aún falten."""
        if not gestor_audio.inicializar_mixer():
            return False

        configuracion_mixer = pygame.mixer.get_init()

        if (
            not forzar
            and self.sonidos
            and self._configuracion_mixer == configuracion_mixer
        ):
            return True

        self.sonidos = {}
        self._configuracion_mixer = configuracion_mixer

        for nombre, configuracion in CONFIGURACIONES.items():
            ruta = self._resolver_ruta(configuracion.archivo)

            if ruta is not None:
                sonido = gestor_audio.cargar_efecto(ruta)
            else:
                sonido = self._crear_tono_respaldo(
                    configuracion.tonos_respaldo
                )

                if nombre not in self._faltantes_informados:
                    print(
                        f"[EFECTOS] Falta {configuracion.archivo}; "
                        "se usará un tono generado."
                    )
                    self._faltantes_informados.add(nombre)

            self.sonidos[nombre] = sonido

        return any(sonido is not None for sonido in self.sonidos.values())

    def recargar(self) -> bool:
        """Vuelve a leer archivos; úsalo después de añadir un sonido."""
        return self.cargar(forzar=True)

    def reproducir(self, nombre: str):
        configuracion = CONFIGURACIONES.get(nombre)

        if configuracion is None:
            print(f"[EFECTOS] Efecto desconocido: {nombre}")
            return None

        if not self.cargar():
            return None

        return gestor_audio.reproducir_efecto(
            self.sonidos.get(nombre),
            volumen_relativo=configuracion.volumen,
        )

    def reproducir_enemigo_eliminado(self):
        return self.reproducir(ENEMIGO_ELIMINADO)

    def reproducir_salto(self):
        return self.reproducir(SALTO)

    def reproducir_respuesta_incorrecta(self):
        return self.reproducir(RESPUESTA_INCORRECTA)

    def reproducir_dano(self):
        return self.reproducir(RECIBIR_DANO)

    def reproducir_respuesta_correcta(self):
        return self.reproducir(RESPUESTA_CORRECTA)

    def reproducir_muerte(self):
        return self.reproducir(MUERTE)


efectos = GestorEfectos()


__all__ = [
    "CONFIGURACIONES",
    "EFECTOS_DIR",
    "ENEMIGO_ELIMINADO",
    "GestorEfectos",
    "MUERTE",
    "RECIBIR_DANO",
    "RESPUESTA_CORRECTA",
    "RESPUESTA_INCORRECTA",
    "SALTO",
    "efectos",
]
