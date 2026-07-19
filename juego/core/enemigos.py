"""Sistema reutilizable de enemigos animados para los niveles."""

from __future__ import annotations

import re
from pathlib import Path

import pygame


RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
ENEMIGOS_DIR = RAIZ_PROYECTO / "assets" / "personajes" / "enemigos"

COLISION_PISADO = "pisado"
COLISION_DANO = "dano"

CONFIGURACION_PREDETERMINADA = {
    "ancho": 110,
    "alto": 78,
    "velocidad": 55,
    "fps_animacion": 8,
    "orientacion_original": "izquierda",
    "hitbox_reducir_ancho": 10,
    "hitbox_reducir_alto": 8,
    "hitbox_offset_x": 0,
    "hitbox_offset_y": 2,
    "tolerancia_pisada": 8,
    "rebote_al_pisar": -12,
    "hace_dano": True,
}


def _clave_orden_natural(ruta: Path):
    """Ordena frame2 antes que frame10."""
    partes = re.split(r"(\d+)", ruta.stem.casefold())
    return tuple(
        int(parte) if parte.isdigit() else parte
        for parte in partes
    )


def _normalizar_tipo(tipo) -> str:
    nombre = str(tipo or "").strip().lower().replace(" ", "_")

    if not nombre:
        raise ValueError("Cada enemigo necesita indicar su tipo.")

    if any(separador in nombre for separador in ("/", "\\", "..")):
        raise ValueError(f"Tipo de enemigo no valido: {tipo!r}")

    return nombre


def _normalizar_movimiento(movimiento) -> str:
    nombre = str(movimiento or "horizontal").strip().lower()
    nombre = nombre.replace("-", "_").replace(" ", "_")
    alias = {
        "horizontal": "horizontal",
        "x": "horizontal",
        "derecha_izquierda": "horizontal",
        "izquierda_derecha": "horizontal",
        "vertical": "vertical",
        "y": "vertical",
        "abajo_arriba": "vertical",
        "arriba_abajo": "vertical",
    }

    if nombre not in alias:
        raise ValueError(
            "El movimiento del enemigo debe ser 'horizontal' o 'vertical'."
        )

    return alias[nombre]


def _resolver_carpeta(tipo: str) -> Path:
    carpeta = ENEMIGOS_DIR / tipo

    if carpeta.is_dir():
        return carpeta

    if ENEMIGOS_DIR.is_dir():
        for posible in ENEMIGOS_DIR.iterdir():
            if posible.is_dir() and posible.name.casefold() == tipo.casefold():
                return posible

    raise FileNotFoundError(
        f"No existe la carpeta del enemigo: {carpeta}"
    )


def _obtener_rect_visible(imagen: pygame.Surface) -> pygame.Rect:
    mascara = pygame.mask.from_surface(imagen, threshold=8)
    componentes = mascara.get_bounding_rects()

    if not componentes:
        return imagen.get_rect()

    rect_visible = componentes[0].copy()

    for componente in componentes[1:]:
        rect_visible.union_ip(componente)

    return rect_visible


def _ajustar_frame(
    imagen: pygame.Surface,
    ancho: int,
    alto: int,
) -> pygame.Surface:
    """Recorta transparencia y centra el frame en un lienzo estable."""
    rect_visible = _obtener_rect_visible(imagen)
    visible = imagen.subsurface(rect_visible).copy()
    escala = min(
        ancho / max(1, visible.get_width()),
        alto / max(1, visible.get_height()),
    )
    nuevo_tamano = (
        max(1, round(visible.get_width() * escala)),
        max(1, round(visible.get_height() * escala)),
    )
    visible = pygame.transform.scale(visible, nuevo_tamano)
    lienzo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    destino = visible.get_rect(
        midbottom=(ancho // 2, alto),
    )
    lienzo.blit(visible, destino)
    return lienzo


class Enemigo:
    """Enemigo animado que patrulla en un recorrido horizontal o vertical."""

    def __init__(
        self,
        *,
        tipo: str,
        x_inicial: float,
        x_limite: float,
        suelo_y: int,
        ajuste_y: int,
        ancho: int,
        alto: int,
        velocidad: float,
        fps_animacion: float,
        orientacion_original: str,
        hitbox_reducir_ancho: int,
        hitbox_reducir_alto: int,
        hitbox_offset_x: int,
        hitbox_offset_y: int,
        tolerancia_pisada: int,
        rebote_al_pisar: float,
        hace_dano: bool,
        movimiento: str = "horizontal",
        y_inicial: float = 0,
        y_limite: float = 0,
    ):
        self.tipo = _normalizar_tipo(tipo)
        self.movimiento = _normalizar_movimiento(movimiento)
        self.es_enemigo = True
        self.x_inicial = float(x_inicial)
        self.x_limite = float(x_limite)
        self.limite_izquierdo = min(self.x_inicial, self.x_limite)
        self.limite_derecho = max(self.x_inicial, self.x_limite)
        self.x = self.x_inicial
        self.suelo_y = int(suelo_y)
        self.ajuste_y = int(ajuste_y)
        self.ancho = max(1, int(ancho))
        self.alto = max(1, int(alto))
        self.y_base = self.suelo_y - self.alto + self.ajuste_y
        self.y_inicial = self.y_base + float(y_inicial)
        self.y_limite = self.y_base + float(y_limite)
        self.limite_superior = min(self.y_inicial, self.y_limite)
        self.limite_inferior = max(self.y_inicial, self.y_limite)
        self.y = self.y_inicial
        self.velocidad = max(0.0, abs(float(velocidad)))
        self.fps_animacion = max(0.1, float(fps_animacion))
        self.orientacion_original = str(
            orientacion_original or "izquierda"
        ).strip().lower()
        self.tolerancia_pisada = max(0, int(tolerancia_pisada))
        self.rebote_al_pisar = float(rebote_al_pisar)
        self.hace_dano = bool(hace_dano)

        if self.movimiento == "vertical":
            posicion_inicial = self.y_inicial
            posicion_limite = self.y_limite
        else:
            posicion_inicial = self.x_inicial
            posicion_limite = self.x_limite

        if posicion_limite < posicion_inicial:
            self.direccion_inicial = -1
        elif posicion_limite > posicion_inicial:
            self.direccion_inicial = 1
        else:
            self.direccion_inicial = 0

        self.direccion = self.direccion_inicial
        self.frame_actual = 0
        self.tiempo_animacion = 0.0
        self.vivo = True

        self.frames = self._cargar_frames()
        self.frames_reflejados = [
            pygame.transform.flip(frame, True, False)
            for frame in self.frames
        ]
        self.hitbox_local = self._calcular_hitbox(
            hitbox_reducir_ancho,
            hitbox_reducir_alto,
            hitbox_offset_x,
            hitbox_offset_y,
        )

    @classmethod
    def desde_configuracion(
        cls,
        configuracion: dict,
        *,
        suelo_y: int,
        escala_juego: float,
    ) -> "Enemigo":
        """Convierte las unidades pequenas del nivel a pixeles del mundo."""
        config = dict(CONFIGURACION_PREDETERMINADA)
        config.update(configuracion)

        tipo = config.get("tipo", config.get("enemigo"))
        movimiento = _normalizar_movimiento(
            config.get("movimiento", config.get("eje", "horizontal"))
        )

        if movimiento == "vertical":
            x_inicial = config.get(
                "x",
                config.get("x_inicial", config.get("posicion_x")),
            )
            x_limite = x_inicial
            y_inicial = config.get(
                "y_inicial",
                config.get(
                    "posicion_inicial_y",
                    config.get("posicion_inicial", 0),
                ),
            )
            y_limite = config.get(
                "y_limite",
                config.get(
                    "posicion_limite_y",
                    config.get("posicion_limite", config.get("limite")),
                ),
            )

            if x_inicial is None or y_limite is None:
                raise ValueError(
                    "Un enemigo vertical necesita x y y_limite."
                )
        else:
            x_inicial = config.get(
                "x_inicial",
                config.get("posicion_inicial", config.get("x")),
            )
            x_limite = config.get(
                "x_limite",
                config.get("posicion_limite", config.get("limite")),
            )
            y_inicial = 0
            y_limite = 0

            if x_inicial is None or x_limite is None:
                raise ValueError(
                    "Un enemigo horizontal necesita x_inicial y x_limite."
                )

        def escalar(valor):
            return round(float(valor) * escala_juego)

        return cls(
            tipo=tipo,
            movimiento=movimiento,
            x_inicial=escalar(x_inicial),
            x_limite=escalar(x_limite),
            suelo_y=suelo_y,
            ajuste_y=escalar(config.get("ajuste_y", 0)),
            y_inicial=escalar(y_inicial),
            y_limite=escalar(y_limite),
            ancho=escalar(config["ancho"]),
            alto=escalar(config["alto"]),
            velocidad=float(config["velocidad"]) * escala_juego,
            fps_animacion=config["fps_animacion"],
            orientacion_original=config["orientacion_original"],
            hitbox_reducir_ancho=escalar(
                config["hitbox_reducir_ancho"]
            ),
            hitbox_reducir_alto=escalar(
                config["hitbox_reducir_alto"]
            ),
            hitbox_offset_x=escalar(config["hitbox_offset_x"]),
            hitbox_offset_y=escalar(config["hitbox_offset_y"]),
            tolerancia_pisada=escalar(config["tolerancia_pisada"]),
            rebote_al_pisar=config["rebote_al_pisar"],
            hace_dano=config["hace_dano"],
        )

    def _cargar_frames(self) -> list[pygame.Surface]:
        carpeta = _resolver_carpeta(self.tipo)
        rutas = sorted(
            (
                ruta
                for ruta in carpeta.iterdir()
                if ruta.is_file() and ruta.suffix.casefold() == ".png"
            ),
            key=_clave_orden_natural,
        )

        if not rutas:
            raise FileNotFoundError(
                f"El enemigo {self.tipo!r} no tiene frames PNG en {carpeta}"
            )

        frames = []

        for ruta in rutas:
            imagen = pygame.image.load(str(ruta)).convert_alpha()
            frames.append(_ajustar_frame(imagen, self.ancho, self.alto))

        return frames

    def _calcular_hitbox(
        self,
        reducir_ancho: int,
        reducir_alto: int,
        offset_x: int,
        offset_y: int,
    ) -> pygame.Rect:
        visibles = [
            _obtener_rect_visible(frame)
            for frame in self.frames
        ]
        hitbox = visibles[0].copy()

        for visible in visibles[1:]:
            hitbox.union_ip(visible)

        hitbox.inflate_ip(
            -min(max(0, reducir_ancho), hitbox.width - 1),
            -min(max(0, reducir_alto), hitbox.height - 1),
        )
        hitbox.move_ip(offset_x, offset_y)
        hitbox = hitbox.clip(pygame.Rect(0, 0, self.ancho, self.alto))

        if hitbox.width <= 0 or hitbox.height <= 0:
            return pygame.Rect(0, 0, self.ancho, self.alto)

        return hitbox

    @property
    def rect_imagen(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.x),
            round(self.y),
            self.ancho,
            self.alto,
        )

    @property
    def rect(self) -> pygame.Rect:
        rect = self.hitbox_local.copy()
        rect.move_ip(round(self.x), round(self.y))
        return rect

    def obtener_rect_pantalla(
        self,
        camara_x: float,
        *,
        usar_hitbox: bool = False,
    ) -> pygame.Rect:
        rect = self.rect if usar_hitbox else self.rect_imagen
        rect.x = round(rect.x - camara_x)
        return rect

    def obtener_sprite_actual(self) -> pygame.Surface:
        if self.movimiento == "vertical":
            return self.frames[self.frame_actual]

        mira_izquierda = self.direccion <= 0
        original_mira_izquierda = (
            self.orientacion_original != "derecha"
        )
        debe_reflejar = mira_izquierda != original_mira_izquierda
        coleccion = self.frames_reflejados if debe_reflejar else self.frames
        return coleccion[self.frame_actual]

    def actualizar(self, dt: float):
        if not self.vivo:
            return

        dt = max(0.0, float(dt))

        if self.direccion != 0 and self.velocidad > 0:
            if self.movimiento == "vertical":
                self.y += self.direccion * self.velocidad * dt

                if self.y <= self.limite_superior:
                    self.y = self.limite_superior
                    self.direccion = 1
                elif self.y >= self.limite_inferior:
                    self.y = self.limite_inferior
                    self.direccion = -1
            else:
                self.x += self.direccion * self.velocidad * dt

                if self.x <= self.limite_izquierdo:
                    self.x = self.limite_izquierdo
                    self.direccion = 1
                elif self.x >= self.limite_derecho:
                    self.x = self.limite_derecho
                    self.direccion = -1

        self.tiempo_animacion += dt
        frames_avanzados = int(
            self.tiempo_animacion * self.fps_animacion
        )

        if frames_avanzados > 0:
            self.tiempo_animacion -= (
                frames_avanzados / self.fps_animacion
            )
            self.frame_actual = (
                self.frame_actual + frames_avanzados
            ) % len(self.frames)

    def eliminar(self) -> bool:
        if not self.vivo:
            return False

        self.vivo = False
        return True

    def reiniciar(self):
        self.x = self.x_inicial
        self.y = self.y_inicial
        self.direccion = self.direccion_inicial
        self.frame_actual = 0
        self.tiempo_animacion = 0.0
        self.vivo = True

    def dibujar(self, pantalla: pygame.Surface, camara_x: float):
        if not self.vivo:
            return

        pantalla.blit(
            self.obtener_sprite_actual(),
            self.obtener_rect_pantalla(camara_x).topleft,
        )


def clasificar_colision_jugador(
    enemigo: Enemigo,
    jugador_actual: pygame.Rect,
    jugador_anterior: pygame.Rect,
    velocidad_y: float,
):
    """Distingue una pisada desde arriba de un contacto danino."""
    if not enemigo.vivo:
        return None

    rect_enemigo = enemigo.rect

    if not jugador_actual.colliderect(rect_enemigo):
        return None

    coincide_horizontalmente = (
        jugador_actual.right > rect_enemigo.left
        and jugador_actual.left < rect_enemigo.right
    )
    cayo_encima = (
        velocidad_y > 0
        and coincide_horizontalmente
        and jugador_anterior.bottom
        <= rect_enemigo.top + enemigo.tolerancia_pisada
        and jugador_actual.bottom >= rect_enemigo.top
    )

    if cayo_encima:
        return COLISION_PISADO

    if enemigo.hace_dano:
        return COLISION_DANO

    return None


def crear_enemigos_desde_configuraciones(
    configuraciones,
    *,
    suelo_y: int,
    escala_juego: float,
) -> list[Enemigo]:
    enemigos = []

    for indice, configuracion in enumerate(configuraciones or (), start=1):
        if not isinstance(configuracion, dict):
            print(
                f"[ENEMIGOS] Se ignoro el enemigo {indice}: "
                "la configuracion debe ser un diccionario."
            )
            continue

        if not bool(configuracion.get("activo", True)):
            continue

        try:
            enemigos.append(
                Enemigo.desde_configuracion(
                    configuracion,
                    suelo_y=suelo_y,
                    escala_juego=escala_juego,
                )
            )
        except (FileNotFoundError, KeyError, TypeError, ValueError) as error:
            print(
                f"[ENEMIGOS] Se ignoro el enemigo {indice}: {error}"
            )

    return enemigos


__all__ = [
    "COLISION_DANO",
    "COLISION_PISADO",
    "ENEMIGOS_DIR",
    "Enemigo",
    "clasificar_colision_jugador",
    "crear_enemigos_desde_configuraciones",
]
