
# NOTA DE ESTRUCTURA
# Este archivo conserva el motor funcional del nivel original.
# Los niveles concretos heredan de JuegoBase en juego/core/juego.py.

# ============================================================
# EDUCORE - JUEGO PYGAME CON MYSQL
# Refactorizacion interna conservadora sin pantalla de carga.
# Mantiene las medidas, rutas, logica visual y consultas del nivel.
# ============================================================

import argparse
import runpy
import sys
import textwrap
import math
import multiprocessing
from functools import lru_cache
from pathlib import Path

import pygame

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from juego.interfaz.practica import PantallaPractica
from juego.interfaz.practica_codigo import PantallaPracticaCodigo

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    mysql = None
    MySQLError = Exception
else:
    mysql = mysql.connector


# ============================================================
# 0. CONFIGURACION DE MYSQL
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",
    "database": "educore_db",
}


# ============================================================
# 1. RUTAS DEL PROYECTO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR = BASE_DIR / "assets"
FONDOS_DIR = ASSETS_DIR / "fondos"

# ============================================================
# FONDO QUE QUIERES USAR
# Cambia solo este valor para reutilizar el mismo codigo.
# Ejemplos:
# FONDO_ACTUAL = "python"
# FONDO_ACTUAL = "java"
# FONDO_ACTUAL = "c#"
# FONDO_ACTUAL = "mysql"
#
# El codigo cargara exactamente estas rutas:
# assets/fondos/<FONDO_ACTUAL>/<FONDO_ACTUAL>_cielo.png
# assets/fondos/<FONDO_ACTUAL>/<FONDO_ACTUAL>_montanas.png
# assets/fondos/<FONDO_ACTUAL>/<FONDO_ACTUAL>_plantas.png
# assets/fondos/<FONDO_ACTUAL>/<FONDO_ACTUAL>_suelo.png
# ============================================================
FONDO_ACTUAL = "python"

FONDO_CIELO = FONDOS_DIR / FONDO_ACTUAL / f"{FONDO_ACTUAL}_cielo.png"
FONDO_MONTANAS = FONDOS_DIR / FONDO_ACTUAL / f"{FONDO_ACTUAL}_montanas.png"
FONDO_ARBOLES = FONDOS_DIR / FONDO_ACTUAL / f"{FONDO_ACTUAL}_plantas.png"
FONDO_SUELO = FONDOS_DIR / FONDO_ACTUAL / f"{FONDO_ACTUAL}_suelo.png"

PERSONAJES_DIR = ASSETS_DIR / "personajes"
OBSTACULOS_DIR = ASSETS_DIR / "obstaculos"
NPC_DIR = ASSETS_DIR / "personajes" / "npc"
UI_DIR = ASSETS_DIR / "ui"
FUENTES_DIR = ASSETS_DIR / "FUENTES"
MUSICA_DIR = ASSETS_DIR / "musica"

RUTA_MUSICA_FONDO = MUSICA_DIR / "musicamecanicogd.ogg"
VOLUMEN_MUSICA = 1000

RUTAS_NPC = [
    NPC_DIR / "profesor1.png",
    NPC_DIR / "profesor2.png",
    NPC_DIR / "profesor3.png",
    NPC_DIR / "profesor4.png",
]

RUTA_CONCEPTO_APRENDIDO = UI_DIR / "concepto_aprendido.png"
RUTA_VIDA_LLENA = UI_DIR / "vidallena.png"
RUTA_VIDA_VACIA = UI_DIR / "vidavacia.png"
RUTA_FUENTE_PIXEL = FUENTES_DIR / "PixelOperator-Bold.ttf"
RUTA_BURBUJA_DIALOGO = UI_DIR / "BurbujaDialogo.png"
RUTA_CUADRO_AVISO = UI_DIR / "cuadro_aviso.png"
RUTA_MONEDA_PRACTICA = UI_DIR / "moneda_practica.png"

RUTA_BOTON_REANUDAR = UI_DIR / "reanudar.png"
RUTA_BOTON_REANUDAR_CLICK = UI_DIR / "reanudar_click.png"
RUTA_BOTON_CONFIGURACION = UI_DIR / "configuracion.png"
RUTA_BOTON_CONFIGURACION_CLICK = UI_DIR / "configuracion_click.png"
RUTA_BOTON_SALIR = UI_DIR / "salir.png"
RUTA_BOTON_SALIR_CLICK = UI_DIR / "salir_click.png"

DISENOS_DIR = ASSETS_DIR / "DISEÑOS"
RUTA_LOGO_MENU_PAUSA = DISENOS_DIR / "logo.png"
RUTA_FUENTE_ORBITRON = FUENTES_DIR / "Orbitron-Medium.ttf"

# ============================================================
# 2. CONFIGURACION GENERAL 1920x1080
# ============================================================

ANCHO = 1920
ALTO = 1080
FPS = 60

# El juego y la interfaz conservan 1920x1080. Solo las capas grandes del
# fondo se componen a media resolución y luego se escalan una sola vez.
# Esto reduce de forma importante el trabajo de mezcla alfa por fotograma.
ESCALA_RENDER_FONDO = 0.50
ANCHO_FONDO = max(1, round(ANCHO * ESCALA_RENDER_FONDO))
ALTO_FONDO = max(1, round(ALTO * ESCALA_RENDER_FONDO))

ESCALA_JUEGO = 1.5

COLOR_CIELO_BASE = (100, 195, 245)
COLOR_RELLENO_INFERIOR = (45, 20, 30)
FRANJA_SEGURIDAD_INFERIOR = max(12, round(8 * ESCALA_JUEGO))

TAMANO_TILE = 32
ESCALA_OBSTACULOS = 5.1
TAMANO_OBSTACULO = round(TAMANO_TILE * ESCALA_OBSTACULOS)

PISO_Y = ALTO - round(122 * ESCALA_JUEGO)

# Piso real que usa la colision del jugador, las plataformas, el NPC y los
# obstaculos.
# Negativo = sube la hitbox del suelo. Positivo = baja la hitbox del suelo.
# Cambia SOLO este valor si el jugador queda enterrado o flotando.
AJUSTE_Y_SUELO = -35
PISO_COLISION_Y = PISO_Y + AJUSTE_Y_SUELO
CONFIGURACION_NPC = -8
MOSTRAR_HITBOXES = False
MOSTRAR_FPS = True

VELOCIDAD_CAMINAR = round(330 * ESCALA_JUEGO)
VELOCIDAD_AIRE = round(420 * ESCALA_JUEGO)

HITBOX_IZQUIERDA = 36
HITBOX_DERECHA = 36
HITBOX_ARRIBA = 36
HITBOX_ABAJO = 18
# Mueve el sprite del jugador Y SU HITBOX al mismo tiempo.
# Negativo = sube, positivo = baja.
AJUSTE_Y_JUGADOR = -25
PISO_INICIO = 0
PISO_FIN = round(5000 * ESCALA_JUEGO)

MARGEN_COLISION_VERTICAL = round(20 * ESCALA_JUEGO)

VIDAS_MAXIMAS = 5

TIPOS_OBSTACULOS_SOLIDOS = frozenset({"piedra", "tronco", "caja"})
TIPOS_OBSTACULOS_DANIO = frozenset({"puas", "laser"})

ALIAS_PERSONAJES = {
    "cerdo": "cerdo",
    "cerdito": "cerdo",
    "jugador": "jugador",
    "gato": "gato",
    "banano": "banano",
    "pato": "pato",
}

ESTADOS_BOTON_FORMULARIO = ("normal", "hover", "clic")
BOTONES_RESPUESTA_FORMULARIO = ("falso", "verdadero", "responder")
TEXTOS_BOTONES_PAUSA = {
    "reanudar": "REANUDAR",
    "ajustes": "AJUSTES",
    "salir": "SALIR",
}

_CAPAS_FONDO_CONFIG = (
    (FONDO_CIELO, 0.10, (100, 195, 245), False, 0),
    (
        FONDO_MONTANAS,
        0.30,
        (0, 0, 0, 0),
        True,
        round(6 * ESCALA_JUEGO),
    ),
    (
        FONDO_ARBOLES,
        0.70,
        (0, 0, 0, 0),
        True,
        round(26 * ESCALA_JUEGO),
    ),
)


# ============================================================
# 3. CONFIGURACION DE PERSONAJES
# ============================================================

_FRAMES_CERDO = tuple(f"jugador_caminar{i}.png" for i in range(1, 5))
_FRAMES_GATO_CAMINAR = tuple(
    f"gato_caminar{i}.png" for i in range(2, 6)
)
_FRAMES_GATO_SALTAR = ("gato_caminar7.png", "gato_caminar8.png",)
_FRAMES_PATO = tuple(f"Pato_Caminar{i}.png" for i in range(1, 6))


def _crear_config_personaje(
    carpetas,
    frames_caminar,
    frames_saltar=(),
    escala=5.1,
    hitbox_abajo=18,
):
    """Crea configuraciones independientes con la estructura publica original."""
    return {
        "carpetas": list(carpetas),
        "caminar": list(frames_caminar),
        "saltar": list(frames_saltar),
        "escala": escala,
        "hitbox": {
            "izquierda": 36,
            "derecha": 36,
            "arriba": 36,
            "abajo": hitbox_abajo,
        },
    }


# Los alias y el orden de busqueda conservan la compatibilidad con MySQL.
PERSONAJES_CONFIG = {
    "cerdo": _crear_config_personaje(("Cerdo", "jugador"), _FRAMES_CERDO),
    "jugador": _crear_config_personaje(("jugador", "Cerdo"), _FRAMES_CERDO),
    "cerdito": _crear_config_personaje(("Cerdo", "jugador"), _FRAMES_CERDO),
    "gato": _crear_config_personaje(
        ("Banano",),
        _FRAMES_GATO_CAMINAR,
        _FRAMES_GATO_SALTAR,
        escala=4.3
    ),
    "banano": _crear_config_personaje(
        ("Banano",),
        _FRAMES_GATO_CAMINAR,
        _FRAMES_GATO_SALTAR,
    ),
    "pato": _crear_config_personaje(
        ("Pato", "pato"),
        _FRAMES_PATO,
        escala=5.6,
        hitbox_abajo=30,
    ),
}


# ============================================================
# 3.1 CONFIGURACION DEL PERSONAJE EN EL MENU DE PAUSA
# Solo se configuraron: pato, gato y cerdo.
# ============================================================

CONFIG_PERSONAJE_MENU_PAUSA = {
    "pato": {
        "max_ancho": 170,
        "max_alto": 210,
        "mover_x": 0,
        "mover_y": 10,
        "sombra_x": -70,
        "sombra_y": 210,
        "sombra_ancho": 140,
        "sombra_alto": 30,
    },

    "gato": {
        "max_ancho": 290,
        "max_alto": 330,
        "mover_x": 0,
        "mover_y": -100,
        "sombra_x": -70,
        "sombra_y": 220,
        "sombra_ancho": 140,
        "sombra_alto": 30,
    },

    "cerdo": {
        "max_ancho": 200,
        "max_alto": 240,
        "mover_x": 0,
        "mover_y": 50,
        "sombra_x": -70,
        "sombra_y": 190,
        "sombra_ancho": 140,
        "sombra_alto": 30,
    },
}

PERSONAJE_DEFAULT = "cerdo"


# ============================================================
# 4. FUNCIONES AUXILIARES
# ============================================================

@lru_cache(maxsize=None)
def cargar_fuente_pixel(tamano):
    if RUTA_FUENTE_PIXEL.exists():
        return pygame.font.Font(str(RUTA_FUENTE_PIXEL), tamano)

    return pygame.font.SysFont("arial", tamano)


@lru_cache(maxsize=None)
def cargar_fuente_orbitron(tamano):
    if RUTA_FUENTE_ORBITRON.exists():
        return pygame.font.Font(str(RUTA_FUENTE_ORBITRON), tamano)

    return pygame.font.SysFont("arial", tamano, bold=True)


def cargar_imagen(ruta, alpha=True):
    if ruta.exists():
        if alpha:
            return pygame.image.load(str(ruta)).convert_alpha()

        return pygame.image.load(str(ruta)).convert()

    return None


def recortar_transparencia_png(superficie, margen=4):
    """Recorta el espacio transparente sobrante alrededor de un PNG."""
    if superficie is None:
        return None

    superficie = superficie.convert_alpha()
    rect_visible = superficie.get_bounding_rect(min_alpha=8)

    if rect_visible.width <= 0 or rect_visible.height <= 0:
        return superficie

    rect_visible.x = max(0, rect_visible.x - margen)
    rect_visible.y = max(0, rect_visible.y - margen)
    rect_visible.width = min(
        superficie.get_width() - rect_visible.x,
        rect_visible.width + margen * 2,
    )
    rect_visible.height = min(
        superficie.get_height() - rect_visible.y,
        rect_visible.height + margen * 2,
    )

    recortada = pygame.Surface(
        (rect_visible.width, rect_visible.height),
        pygame.SRCALPHA,
    )
    recortada.blit(superficie, (0, 0), rect_visible)
    return recortada


def limpiar_transparencia_falsa(superficie):
    superficie = superficie.convert_alpha()
    ancho = superficie.get_width()
    alto = superficie.get_height()

    resultado = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    resultado.blit(superficie, (0, 0))
    resultado.lock()

    for y in range(alto):
        for x in range(ancho):
            r, g, b, _ = resultado.get_at((x, y))
            es_gris_claro = (
                abs(r - g) <= 12
                and abs(g - b) <= 12
                and r >= 155
                and g >= 155
                and b >= 155
            )

            if es_gris_claro:
                resultado.set_at((x, y), (r, g, b, 0))


    resultado.unlock()
    return resultado


def recortar_arriba_transparente(superficie, y_inicio):
    superficie = superficie.convert_alpha()
    ancho = superficie.get_width()
    alto = superficie.get_height()
    y_inicio = max(0, min(int(y_inicio), alto))

    resultado = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    rect_visible = pygame.Rect(0, y_inicio, ancho, alto - y_inicio)
    resultado.blit(superficie, rect_visible.topleft, rect_visible)

    return resultado


def asegurar_borde_inferior(superficie, color=COLOR_RELLENO_INFERIOR, alto_franja=FRANJA_SEGURIDAD_INFERIOR):
    resultado = superficie.convert_alpha().copy()
    ancho = resultado.get_width()
    alto = resultado.get_height()
    alto_franja = max(1, min(int(alto_franja), alto))

    pygame.draw.rect(
        resultado,
        color,
        (0, alto - alto_franja, ancho, alto_franja)
    )

    return resultado


def normalizar_texto(valor):
    if valor is None:
        return ""

    return str(valor).strip()


def dividir_lineas_por_ancho(texto, fuente, ancho_max):
    """Divide texto preservando saltos de parrafo y espacios de renderizado."""
    lineas = []

    for bloque in texto.split("\n"):
        palabras = bloque.split(" ")
        linea = ""

        for palabra in palabras:
            prueba = linea + palabra + " "

            if fuente.size(prueba)[0] <= ancho_max:
                linea = prueba
            else:
                if linea:
                    lineas.append(linea)
                linea = palabra + " "

        if linea:
            lineas.append(linea)

    return lineas


def obtener_puntos_rect_pixel(rect, corte):
    return [
        (rect.x + corte, rect.y),
        (rect.right - corte, rect.y),
        (rect.right, rect.y + corte),
        (rect.right, rect.bottom - corte),
        (rect.right - corte, rect.bottom),
        (rect.x + corte, rect.bottom),
        (rect.x, rect.bottom - corte),
        (rect.x, rect.y + corte),
    ]


def dividir_texto_en_paginas(texto, max_caracteres=105):
    texto = normalizar_texto(texto)

    if not texto:
        return []

    paginas = []
    parrafos = [p.strip() for p in texto.split("\n") if p.strip()]

    for parrafo in parrafos:
        if len(parrafo) <= max_caracteres:
            paginas.append(parrafo)
            continue

        partes = textwrap.wrap(
            parrafo,
            width=max_caracteres,
            break_long_words=False,
            replace_whitespace=False,
        )

        paginas.extend(partes)

    return paginas


def construir_paginas_leccion(leccion, nombre_lenguaje):
    if not leccion:
        return [
            "Hola, soy tu guia.",
            "No pude cargar la leccion desde la base de datos.",
            "Revisa tu conexion MySQL o que existan datos en la tabla leccion.",
        ]

    titulo = normalizar_texto(leccion.get("titulo"))
    teoria = normalizar_texto(leccion.get("contenido_teoria"))
    codigo = normalizar_texto(leccion.get("codigo_ejemplo"))

    paginas = [
        f"Leccion de {nombre_lenguaje}: {titulo}",
    ]

    paginas.extend(dividir_texto_en_paginas(teoria, max_caracteres=105))

    if codigo:
        lineas_codigo = codigo.split("\n")
        bloque = "Ejemplo:\n"

        for linea in lineas_codigo:
            posible = bloque + linea + "\n"

            if len(posible) > 115 and bloque.strip() != "Ejemplo:":
                paginas.append(bloque.rstrip())
                bloque = "Ejemplo:\n" + linea + "\n"
            else:
                bloque = posible

        if bloque.strip():
            paginas.append(bloque.rstrip())

    return paginas


# ============================================================
# 6. TRANSICION DE IRIS
# ============================================================

class TransicionIris:
    def __init__(self, duracion=0.8):
        self.duracion = duracion
        self.tiempo = 0
        self.abriendo = False
        self.centro = (ANCHO // 2, ALTO // 2)
        self._capa_negra = None
        self._tamano_capa = None

    def activa(self):
        return self.abriendo

    def iniciar_apertura(self, centro):
        if self.activa():
            return

        self.abriendo = True
        self.tiempo = 0
        self.centro = centro

    def actualizar(self, dt):
        if not self.abriendo:
            return

        self.tiempo += dt

        if self.tiempo >= self.duracion:
            self.abriendo = False
            self.tiempo = 0

    def dibujar(self, pantalla):
        if not self.abriendo:
            return

        ancho, alto = pantalla.get_size()
        tamano = (ancho, alto)

        # Reutiliza la misma superficie durante toda la transición.
        if self._capa_negra is None or self._tamano_capa != tamano:
            self._capa_negra = pygame.Surface(tamano, pygame.SRCALPHA)
            self._tamano_capa = tamano

        radio_maximo = int(math.hypot(ancho, alto))
        progreso = min(self.tiempo / self.duracion, 1)

        radio = int(radio_maximo * progreso)

        self._capa_negra.fill((0, 0, 0, 255))
        pygame.draw.circle(
            self._capa_negra,
            (0, 0, 0, 0),
            self.centro,
            radio,
        )
        pantalla.blit(self._capa_negra, (0, 0))


# ============================================================
# 7. CONEXION A BASE DE DATOS
# ============================================================

class ConexionEduCore:
    def __init__(self, config):
        self.config = config
        self.conexion = None
        self.activa = False
        self.ultimo_error = ""
        self.conectar()

    def _registrar_error(self, contexto, error, desactivar=False):
        self.ultimo_error = str(error)

        if desactivar:
            self.activa = False

        print(f"[BD] {contexto}: {error}")

    def _rollback_seguro(self):
        if self.conexion is None:
            return

        try:
            self.conexion.rollback()
        except MySQLError:
            pass

    def conectar(self):
        if mysql is None:
            self.activa = False
            self.ultimo_error = (
                "No esta instalado mysql-connector-python. "
                "Ejecuta: pip install mysql-connector-python"
            )
            print("[BD]", self.ultimo_error)
            return False

        try:
            self.conexion = mysql.connect(**self.config)
            self.activa = True
            self.ultimo_error = ""
            return True
        except MySQLError as error:
            self._registrar_error("No se pudo conectar", error, desactivar=True)
            return False

    def obtener_cursor(self):
        if not self.activa and not self.conectar():
            return None

        try:
            if not self.conexion.is_connected() and not self.conectar():
                return None

            return self.conexion.cursor(dictionary=True)
        except MySQLError as error:
            self._registrar_error("Error de cursor", error, desactivar=True)
            return None

    def _seleccionar(self, consulta, parametros, varios):
        cursor = self.obtener_cursor()

        if cursor is None:
            return [] if varios else None

        try:
            cursor.execute(consulta, parametros or ())
            return cursor.fetchall() if varios else cursor.fetchone()
        except MySQLError as error:
            self._registrar_error("Error SELECT", error)
            return [] if varios else None
        finally:
            cursor.close()

    def seleccionar_uno(self, consulta, parametros=None):
        return self._seleccionar(consulta, parametros, varios=False)

    def seleccionar_varios(self, consulta, parametros=None):
        return self._seleccionar(consulta, parametros, varios=True)

    def ejecutar(self, consulta, parametros=None, commit=True):
        cursor = self.obtener_cursor()

        if cursor is None:
            return False

        try:
            cursor.execute(consulta, parametros or ())

            if commit:
                self.conexion.commit()

            return True
        except MySQLError as error:
            self._rollback_seguro()
            self._registrar_error("Error SQL", error)
            return False
        finally:
            cursor.close()

    def obtener_jugador(self, id_jugador):
        return self.seleccionar_uno(
            """
            SELECT id_jugador, nombre, correo, personaje, vidas, estado
            FROM jugador
            WHERE id_jugador = %s AND estado = 'Activo'
            LIMIT 1
            """,
            (id_jugador,),
        )

    def obtener_lenguaje(self, nombre_lenguaje):
        return self.seleccionar_uno(
            """
            SELECT id_lenguaje, nombre, descripcion
            FROM lenguaje
            WHERE LOWER(nombre) = LOWER(%s)
            LIMIT 1
            """,
            (nombre_lenguaje,),
        )

    def asegurar_progreso(self, id_jugador, id_lenguaje):
        existe = self.seleccionar_uno(
            """
            SELECT id_progreso
            FROM progreso_jugador
            WHERE id_jugador = %s AND id_lenguaje = %s
            LIMIT 1
            """,
            (id_jugador, id_lenguaje),
        )

        if existe:
            return True

        return self.ejecutar(
            """
            INSERT INTO progreso_jugador (
                id_jugador,
                id_lenguaje,
                leccion_actual,
                lecciones_completadas,
                puntos,
                prueba_desbloqueada,
                prueba_completada,
                porcentaje_avance
            )
            VALUES (%s, %s, 1, 0, 0, 0, 0, 0)
            """,
            (id_jugador, id_lenguaje),
        )

    def obtener_orden_leccion_actual(self, id_jugador, id_lenguaje):
        self.asegurar_progreso(id_jugador, id_lenguaje)

        progreso = self.seleccionar_uno(
            """
            SELECT leccion_actual
            FROM progreso_jugador
            WHERE id_jugador = %s AND id_lenguaje = %s
            LIMIT 1
            """,
            (id_jugador, id_lenguaje),
        )

        if not progreso:
            return 1

        return int(progreso.get("leccion_actual") or 1)

    def obtener_leccion(self, id_jugador, id_lenguaje, orden_leccion=None):
        if orden_leccion is None:
            orden_leccion = self.obtener_orden_leccion_actual(id_jugador, id_lenguaje)

        leccion = self.seleccionar_uno(
            """
            SELECT id_leccion, id_lenguaje, titulo, contenido_teoria,
                   codigo_ejemplo, orden, puntos, estado
            FROM leccion
            WHERE id_lenguaje = %s
              AND orden = %s
              AND estado = 'Activa'
            LIMIT 1
            """,
            (id_lenguaje, orden_leccion),
        )

        if leccion:
            return leccion

        return self.seleccionar_uno(
            """
            SELECT id_leccion, id_lenguaje, titulo, contenido_teoria,
                   codigo_ejemplo, orden, puntos, estado
            FROM leccion
            WHERE id_lenguaje = %s
              AND estado = 'Activa'
            ORDER BY orden ASC
            LIMIT 1
            """,
            (id_lenguaje,),
        )

    def contar_lecciones(self, id_lenguaje):
        fila = self.seleccionar_uno(
            """
            SELECT COUNT(*) AS total
            FROM leccion
            WHERE id_lenguaje = %s AND estado = 'Activa'
            """,
            (id_lenguaje,),
        )

        if not fila:
            return 0

        return int(fila.get("total") or 0)

    def registrar_historial(self, id_jugador, evento, detalle):
        return self.ejecutar(
            """
            INSERT INTO historial (id_jugador, evento, detalle)
            VALUES (%s, %s, %s)
            """,
            (id_jugador, evento, detalle),
        )

    def restar_vida(
        self,
        id_jugador,
        evento="Vida perdida",
        detalle_base="Perdio una vida",
    ):
        cursor = self.obtener_cursor()

        if cursor is None:
            return None

        try:
            cursor.execute(
                """
                UPDATE jugador
                SET vidas = GREATEST(vidas - 1, 0)
                WHERE id_jugador = %s
                """,
                (id_jugador,),
            )

            cursor.execute(
                """
                SELECT vidas
                FROM jugador
                WHERE id_jugador = %s
                LIMIT 1
                """,
                (id_jugador,),
            )

            fila = cursor.fetchone()
            vidas_actuales = int(fila["vidas"] if fila else 0)

            cursor.execute(
                """
                INSERT INTO historial (id_jugador, evento, detalle)
                VALUES (%s, %s, %s)
                """,
                (
                    id_jugador,
                    evento,
                    f"{detalle_base}. Vidas restantes: {vidas_actuales}",
                ),
            )

            self.conexion.commit()

            return vidas_actuales
        except MySQLError as error:
            self._rollback_seguro()
            self._registrar_error("Error al restar vida", error)
            return None
        finally:
            cursor.close()

    def completar_leccion(self, id_jugador, id_lenguaje, leccion):
        if not leccion:
            return False

        orden = int(leccion.get("orden") or 1)
        puntos = int(leccion.get("puntos") or 0)
        total_lecciones = self.contar_lecciones(id_lenguaje)

        if total_lecciones <= 0:
            total_lecciones = 1

        siguiente_leccion = min(orden + 1, total_lecciones)
        lecciones_completadas = min(orden, total_lecciones)
        porcentaje = int((lecciones_completadas / total_lecciones) * 100)
        prueba_desbloqueada = 1 if lecciones_completadas >= total_lecciones else 0

        self.asegurar_progreso(id_jugador, id_lenguaje)

        progreso_actual = self.seleccionar_uno(
            """
            SELECT lecciones_completadas
            FROM progreso_jugador
            WHERE id_jugador = %s AND id_lenguaje = %s
            LIMIT 1
            """,
            (id_jugador, id_lenguaje),
        )

        completadas_actuales = 0

        if progreso_actual:
            completadas_actuales = int(progreso_actual.get("lecciones_completadas") or 0)

        ya_estaba_completada = completadas_actuales >= orden
        puntos_a_sumar = 0 if ya_estaba_completada else puntos

        cursor = self.obtener_cursor()

        if cursor is None:
            return False

        try:
            cursor.execute(
                """
                UPDATE progreso_jugador
                SET
                    leccion_actual = GREATEST(leccion_actual, %s),
                    lecciones_completadas = GREATEST(lecciones_completadas, %s),
                    puntos = puntos + %s,
                    prueba_desbloqueada = GREATEST(prueba_desbloqueada, %s),
                    porcentaje_avance = GREATEST(porcentaje_avance, %s),
                    ultima_actualizacion = CURRENT_TIMESTAMP
                WHERE id_jugador = %s AND id_lenguaje = %s
                """,
                (
                    siguiente_leccion,
                    lecciones_completadas,
                    puntos_a_sumar,
                    prueba_desbloqueada,
                    porcentaje,
                    id_jugador,
                    id_lenguaje,
                ),
            )

            detalle = f"Completo la leccion {orden}: {leccion.get('titulo')}"

            if ya_estaba_completada:
                detalle = f"Repitio la leccion {orden}: {leccion.get('titulo')}. No se sumaron puntos."

            cursor.execute(
                """
                INSERT INTO historial (id_jugador, evento, detalle)
                VALUES (%s, 'Leccion completada', %s)
                """,
                (id_jugador, detalle),
            )

            self.conexion.commit()

            return True
        except MySQLError as error:
            self._rollback_seguro()
            self._registrar_error("Error al completar leccion", error)
            return False
        finally:
            cursor.close()

    def cerrar(self):
        try:
            if self.conexion and self.conexion.is_connected():
                self.conexion.close()
        except MySQLError:
            pass
        finally:
            self.activa = False


# ============================================================
# 8. CLASE CAPA PARALLAX
# ============================================================

class CapaParallax:
    """Capa de fondo optimizada para pixel art.

    Las capas transparentes se recortan verticalmente para evitar mezclar
    millones de píxeles completamente transparentes en cada fotograma.
    """

    def __init__(
        self,
        ruta_imagen,
        factor,
        ancho,
        alto,
        color_fallback,
        limpiar_fondo_falso=False,
        cortar_arriba_y=None,
        offset_y=0,
    ):
        self.ruta_imagen = ruta_imagen
        self.factor = factor
        self.color_fallback = color_fallback
        self.limpiar_fondo_falso = limpiar_fondo_falso
        self.cortar_arriba_y = cortar_arriba_y
        self.offset_y = int(offset_y)
        self.offset_dibujo_y = self.offset_y

        if not ruta_imagen.exists():
            raise FileNotFoundError(
                f"No se encontro la imagen de fondo: {ruta_imagen}"
            )

        cargada = pygame.image.load(str(ruta_imagen))
        mascara_alpha = cargada.get_masks()[3]
        self.tiene_alpha = bool(mascara_alpha)

        if self.tiene_alpha:
            self.original = cargada.convert_alpha()
        else:
            self.original = cargada.convert()

        self.redimensionar(ancho, alto)

    def redimensionar(self, ancho, alto):
        ancho = max(1, int(ancho))
        alto = max(1, int(alto))

        escalada = pygame.transform.scale(self.original, (ancho, alto))
        escalada = (
            escalada.convert_alpha()
            if self.tiene_alpha
            else escalada.convert()
        )

        if self.limpiar_fondo_falso:
            escalada = limpiar_transparencia_falsa(escalada)
            self.tiene_alpha = True

        if self.cortar_arriba_y is not None:
            escalada = recortar_arriba_transparente(
                escalada,
                self.cortar_arriba_y,
            )
            self.tiene_alpha = True

        if self.cortar_arriba_y is not None or "suelo" in self.ruta_imagen.name.lower():
            escalada = asegurar_borde_inferior(escalada)
            self.tiene_alpha = True

        # Conserva el ancho completo para que el patrón se repita sin saltos,
        # pero elimina filas transparentes de arriba y abajo.
        self.offset_dibujo_y = self.offset_y

        if self.tiene_alpha:
            visible = escalada.get_bounding_rect(min_alpha=1)

            # Algunos PNG contienen uno o dos píxeles aislados en filas que
            # deberían ser transparentes. Esos píxeles impedían el recorte y
            # obligaban a mezclar una superficie 1920x1080 completa. Se toman
            # solo componentes visibles de al menos 2x2 píxeles para calcular
            # el recorte vertical, sin alterar el contenido dentro de él.
            try:
                componentes = pygame.mask.from_surface(
                    escalada,
                    threshold=1,
                ).get_bounding_rects()
                componentes = [
                    rect
                    for rect in componentes
                    if rect.width * rect.height >= 4
                ]

                if componentes:
                    y_superior = min(rect.top for rect in componentes)
                    y_inferior = max(rect.bottom for rect in componentes)
                    visible = pygame.Rect(
                        0,
                        y_superior,
                        escalada.get_width(),
                        y_inferior - y_superior,
                    )
            except pygame.error:
                # El bounding rect normal sigue siendo una alternativa segura.
                pass

            if visible.height > 0 and visible.height < escalada.get_height():
                recorte = pygame.Rect(
                    0,
                    visible.y,
                    escalada.get_width(),
                    visible.height,
                )
                escalada = escalada.subsurface(recorte).copy().convert_alpha()
                self.offset_dibujo_y += visible.y

        self.imagen = escalada
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()

    def dibujar(self, pantalla, camara_x):
        if self.ancho <= 0 or self.alto <= 0:
            return

        # Dibuja exactamente el ancho de una pantalla usando dos regiones
        # fuente; evita hacer dos blits completos y depender del recorte.
        # La cámara se conserva como float durante la lógica y se redondea
        # solamente al dibujar. El módulo final evita que round() produzca
        # exactamente self.ancho en el borde de repetición.
        desplazamiento = (
            round((float(camara_x) * self.factor) % self.ancho)
            % self.ancho
        )
        ancho_primera = self.ancho - desplazamiento

        pantalla.blit(
            self.imagen,
            (0, self.offset_dibujo_y),
            pygame.Rect(desplazamiento, 0, ancho_primera, self.alto),
        )

        if desplazamiento > 0:
            pantalla.blit(
                self.imagen,
                (ancho_primera, self.offset_dibujo_y),
                pygame.Rect(0, 0, desplazamiento, self.alto),
            )


# ============================================================
# 9. PLATAFORMA
# ============================================================

class PlataformaInvisible:
    def __init__(self, x_inicio, x_fin, y):
        self.x_inicio = x_inicio
        self.x_fin = x_fin
        self.y = y

    def obtener_rect_mundo(self):
        ancho = self.x_fin - self.x_inicio

        return pygame.Rect(
            self.x_inicio,
            self.y,
            ancho,
            ALTO - self.y
        )


# ============================================================
# 10. OBSTACULO
# ============================================================

class Obstaculo:
    def __init__(
        self,
        x,
        y,
        ancho,
        alto,
        tipo,
        ruta_imagen,
        hitbox_offset_x=0,
        hitbox_offset_y=0,
        hitbox_ancho=None,
        hitbox_alto=None,
    ):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.tipo = tipo

        if not ruta_imagen.exists():
            raise FileNotFoundError(f"No se encontro la imagen del obstaculo: {ruta_imagen}")

        self.imagen = pygame.image.load(str(ruta_imagen)).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (ancho, alto))

        if hitbox_ancho is None:
            hitbox_ancho = ancho

        if hitbox_alto is None:
            hitbox_alto = alto

        self.rect = pygame.Rect(
            x + hitbox_offset_x,
            y + hitbox_offset_y,
            hitbox_ancho,
            hitbox_alto,
        )

    def obtener_rect_pantalla(self, camara_x):
        return pygame.Rect(
            round(self.rect.x - camara_x),
            round(self.rect.y),
            int(self.rect.width),
            int(self.rect.height),
        )

    def dibujar(self, pantalla, camara_x):
        pantalla.blit(
            self.imagen,
            (round(self.x - camara_x), round(self.y)),
        )

    def es_solido(self):
        return self.tipo in TIPOS_OBSTACULOS_SOLIDOS

    def es_danio(self):
        return self.tipo in TIPOS_OBSTACULOS_DANIO


# ============================================================
# 10.1 OBJETO DE PRACTICA
# ============================================================

class ObjetoPractica:
    def __init__(
        self,
        x,
        y,
        pregunta,
        respuesta_correcta=True,
        nombre="objeto",
        tipo="verdadero_falso",
        configuracion_codigo=None,
    ):
        self.nombre = nombre
        self.pregunta = pregunta
        self.respuesta_correcta = respuesta_correcta
        self.tipo = str(tipo or "verdadero_falso").lower()
        self.configuracion_codigo = dict(configuracion_codigo or {})
        self.completado = False
        self.tiempo_animacion = 0

        # Tamaño visual de la moneda PNG.
        self.ancho = round(35 * ESCALA_JUEGO)
        self.alto = round(35 * ESCALA_JUEGO)

        self.rect = pygame.Rect(
            int(x),
            int(y),
            self.ancho,
            self.alto
        )

        self.imagen = self.crear_imagen()

    def crear_imagen(self):
        """Carga la imagen PNG utilizada por todas las prácticas."""
        if not RUTA_MONEDA_PRACTICA.exists():
            raise FileNotFoundError(
                "No se encontró la imagen de la moneda de práctica. "
                f"Colócala en: {RUTA_MONEDA_PRACTICA}"
            )

        imagen = pygame.image.load(
            str(RUTA_MONEDA_PRACTICA)
        ).convert_alpha()

        # Elimina espacio transparente sobrante del archivo.
        imagen = recortar_transparencia_png(
            imagen,
            margen=0,
        )

        # Mantiene el aspecto pixel art al ajustar el tamaño.
        imagen = pygame.transform.scale(
            imagen,
            (
                self.ancho,
                self.alto,
            ),
        )

        return imagen

    def actualizar(self, dt):
        self.tiempo_animacion += dt

    def dibujar(self, pantalla, camara_x):
        if self.completado:
            return

        movimiento_y = round(
            math.sin(self.tiempo_animacion * 5)
            * round(5 * ESCALA_JUEGO)
        )
        pantalla.blit(
            self.imagen,
            (
                round(self.rect.x - camara_x),
                round(self.rect.y + movimiento_y)
            )
        )

    def obtener_rect_pantalla(self, camara_x):
        return pygame.Rect(
            round(self.rect.x - camara_x),
            round(self.rect.y),
            int(self.rect.width),
            int(self.rect.height)
        )

# ============================================================
# 11. JUGADOR CON PERSONAJE VARIABLE
# ============================================================

class Jugador:
    def __init__(self, nombre_personaje, escala_default=5.1):
        self.nombre_personaje = self.normalizar_personaje(nombre_personaje)
        self.config = self.obtener_config(self.nombre_personaje)
        self.escala = float(self.config.get("escala", escala_default))

        self.hitbox_config = self.config.get("hitbox", {
            "izquierda": HITBOX_IZQUIERDA,
            "derecha": HITBOX_DERECHA,
            "arriba": HITBOX_ARRIBA,
            "abajo": HITBOX_ABAJO,
        })

        self.frames_caminar = []
        self.frames_saltar = []
        self._frames_reflejados = {}

        self.cargar_frames()

        # Hitbox estable: se calcula una sola vez.
        # Esto evita que el personaje se trabe por cambios de tamaño entre frames.
        self.hitbox_base = self.calcular_hitbox_base()

        self.x_pantalla = round(170 * ESCALA_JUEGO)
        self.y = 0

        self.frame_actual = 0
        self.frame_salto_actual = 0
        self.contador_animacion = 0
        self.contador_salto = 0
        self.velocidad_animacion = 6
        self.velocidad_animacion_salto = 10

        self.velocidad_y = 0
        self.fuerza_salto = -14
        self.gravedad = 0.975
        self.velocidad_caida_maxima = 22.5

        self.en_suelo = False
        self.mirando_derecha = True

    def normalizar_personaje(self, nombre_personaje):
        nombre = normalizar_texto(nombre_personaje).lower()

        if not nombre:
            return PERSONAJE_DEFAULT

        return ALIAS_PERSONAJES.get(nombre, nombre)

    def obtener_config(self, nombre_personaje):
        if nombre_personaje in PERSONAJES_CONFIG:
            return PERSONAJES_CONFIG[nombre_personaje]

        self.nombre_personaje = PERSONAJE_DEFAULT

        return PERSONAJES_CONFIG[PERSONAJE_DEFAULT]

    def resolver_carpeta_personaje(self):
        carpetas = []

        if "carpetas" in self.config:
            carpetas.extend(self.config["carpetas"])

        if "carpeta" in self.config:
            carpetas.append(self.config["carpeta"])

        for nombre_carpeta in carpetas:
            carpeta = PERSONAJES_DIR / nombre_carpeta

            if carpeta.exists():
                return carpeta

            if PERSONAJES_DIR.exists():
                for posible in PERSONAJES_DIR.iterdir():
                    if posible.is_dir() and posible.name.lower() == nombre_carpeta.lower():
                        return posible

        raise FileNotFoundError(
            "No se encontro la carpeta del personaje. Rutas probadas: "
            + ", ".join(str(PERSONAJES_DIR / nombre) for nombre in carpetas)
        )

    def resolver_archivo_frame(self, carpeta, archivo):
        ruta = carpeta / archivo

        if ruta.exists():
            return ruta

        if carpeta.exists():
            for posible in carpeta.iterdir():
                if posible.is_file() and posible.name.lower() == archivo.lower():
                    return posible

        raise FileNotFoundError(f"No se encontro el frame del personaje: {ruta}")

    def cargar_lista_frames(self, carpeta, archivos):
        frames = []

        for archivo in archivos:
            ruta = self.resolver_archivo_frame(carpeta, archivo)
            imagen = pygame.image.load(str(ruta)).convert_alpha()

            ancho = int(imagen.get_width() * self.escala)
            alto = int(imagen.get_height() * self.escala)

            imagen = pygame.transform.scale(imagen, (ancho, alto))

            frames.append(imagen)

        return frames

    def cargar_frames(self):
        carpeta = self.resolver_carpeta_personaje()

        self.frames_caminar = self.cargar_lista_frames(carpeta, self.config["caminar"])

        archivos_salto = self.config.get("saltar", [])

        if archivos_salto:
            self.frames_saltar = self.cargar_lista_frames(carpeta, archivos_salto)
        else:
            self.frames_saltar = []

    def calcular_hitbox_base(self):
        sprite = self.frames_caminar[0]

        izquierda = int(self.hitbox_config.get("izquierda", HITBOX_IZQUIERDA))
        derecha = int(self.hitbox_config.get("derecha", HITBOX_DERECHA))
        arriba = int(self.hitbox_config.get("arriba", HITBOX_ARRIBA))
        abajo = int(self.hitbox_config.get("abajo", HITBOX_ABAJO))

        ancho = sprite.get_width() - izquierda - derecha
        alto = sprite.get_height() - arriba - abajo

        ancho = max(1, ancho)
        alto = max(1, alto)

        return pygame.Rect(
            izquierda,
            arriba,
            ancho,
            alto,
        )

    def obtener_sprite_actual(self):
        if not self.en_suelo and self.frames_saltar:
            sprite = self.frames_saltar[self.frame_salto_actual]
        else:
            sprite = self.frames_caminar[self.frame_actual]

        if self.mirando_derecha:
            return sprite

        clave = id(sprite)
        reflejado = self._frames_reflejados.get(clave)

        if reflejado is None:
            reflejado = pygame.transform.flip(sprite, True, False)
            self._frames_reflejados[clave] = reflejado

        return reflejado

    def obtener_ajuste_y_total(self):
        # Se deja por compatibilidad con partes antiguas del codigo.
        # La solucion definitiva usa una sola posicion Y: self.y.
        return 0

    def obtener_y_sprite(self):
        return self.y

    def obtener_rect_sprite_pantalla(self):
        sprite = self.obtener_sprite_actual()

        return pygame.Rect(
            int(self.x_pantalla),
            int(self.y),
            sprite.get_width(),
            sprite.get_height(),
        )

    def obtener_hitbox_local(self):
        return self.hitbox_base.copy()

    def colocar_sobre_piso(self, piso_y):
        hitbox_local = self.obtener_hitbox_local()

        self.y = piso_y - hitbox_local.bottom
        self.velocidad_y = 0
        self.en_suelo = True

    def saltar(self):
        if self.en_suelo:
            self.velocidad_y = self.fuerza_salto
            self.en_suelo = False
            self.frame_salto_actual = 0
            self.contador_salto = 0

    def aplicar_gravedad(self):
        self.velocidad_y += self.gravedad

        if self.velocidad_y > self.velocidad_caida_maxima:
            self.velocidad_y = self.velocidad_caida_maxima

        self.y += self.velocidad_y

    def actualizar_animacion(self, direccion):
        if direccion > 0:
            self.mirando_derecha = True
        elif direccion < 0:
            self.mirando_derecha = False

        esta_caminando = direccion != 0 and self.en_suelo

        if esta_caminando:
            self.contador_animacion += 1

            if self.contador_animacion >= self.velocidad_animacion:
                self.contador_animacion = 0
                self.frame_actual = (self.frame_actual + 1) % len(self.frames_caminar)

        elif not self.en_suelo:
            if self.frames_saltar:
                self.contador_salto += 1

                if self.contador_salto >= self.velocidad_animacion_salto:
                    self.contador_salto = 0
                    self.frame_salto_actual = (self.frame_salto_actual + 1) % len(self.frames_saltar)
            else:
                self.frame_actual = min(1, len(self.frames_caminar) - 1)

        else:
            self.frame_actual = 0
            self.frame_salto_actual = 0
            self.contador_animacion = 0
            self.contador_salto = 0

    def obtener_rect_pantalla(self):
        hitbox_local = self.obtener_hitbox_local()

        return pygame.Rect(
            round(self.x_pantalla + hitbox_local.x),
            round(self.y + hitbox_local.y),
            int(hitbox_local.width),
            int(hitbox_local.height),
        )

    def obtener_rect_mundo(self, camara_x):
        rect_pantalla = self.obtener_rect_pantalla()

        return pygame.Rect(
            round(rect_pantalla.x + camara_x),
            rect_pantalla.y,
            rect_pantalla.width,
            rect_pantalla.height,
        )

    def dibujar(self, pantalla):
        sprite = self.obtener_sprite_actual()
        pantalla.blit(
            sprite,
            (round(self.x_pantalla), round(self.y)),
        )

# ============================================================
# 12. NPC ANIMADO
# ============================================================

class NPC:
    def __init__(self, x_mundo, suelo_y, escala=3.6):
        self.x_mundo = x_mundo
        self.suelo_y = suelo_y
        self.escala = escala
        self.frames = []

        for ruta in RUTAS_NPC:
            if not ruta.exists():
                raise FileNotFoundError(f"No se encontro el frame del NPC: {ruta}")

            imagen = pygame.image.load(str(ruta)).convert_alpha()

            ancho = int(imagen.get_width() * escala * 1.5)
            alto = int(imagen.get_height() * escala * 1.5)

            imagen = pygame.transform.scale(imagen, (ancho, alto))

            self.frames.append(imagen)

        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 0.18
        self.imagen = self.frames[self.frame_actual]

        self.rect = self.imagen.get_rect()
        self.rect.x = int(self.x_mundo)
        self.rect.bottom = self.suelo_y

        self.zona_dialogo = pygame.Rect(0, 0, 1, 1)
        self.dialogo_terminado = False
        self.burbuja_dialogo = cargar_imagen(RUTA_BURBUJA_DIALOGO)
        self.burbuja_dialogo_escalada = None

        if self.burbuja_dialogo is not None:
            tamano_burbuja = round(70 * ESCALA_JUEGO)
            self.burbuja_dialogo_escalada = pygame.transform.scale(
                self.burbuja_dialogo,
                (tamano_burbuja, tamano_burbuja),
            )

        self.actualizar(self.suelo_y, 0)

    def actualizar(self, suelo_y, dt):
        self.suelo_y = suelo_y
        self.contador_animacion += dt

        if self.contador_animacion >= self.velocidad_animacion:
            self.contador_animacion = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)

        self.imagen = self.frames[self.frame_actual]

        self.rect = self.imagen.get_rect()
        self.rect.x = int(self.x_mundo)
        self.rect.bottom = self.suelo_y

        self.zona_dialogo = pygame.Rect(
            self.rect.x - round(70 * ESCALA_JUEGO),
            self.rect.y,
            self.rect.width + round(140 * ESCALA_JUEGO),
            self.rect.height,
        )

    def dibujar_burbuja(self, pantalla, x, y):
        if self.burbuja_dialogo_escalada is None:
            return

        pantalla.blit(self.burbuja_dialogo_escalada, (x, y))

    def dibujar(self, pantalla, camara_x):
        x_pantalla = round(self.rect.x - camara_x)

        pantalla.blit(self.imagen, (x_pantalla, self.rect.y))

        # La burbuja/exclamacion se mantiene visible siempre,
        # incluso despues de haber leido la leccion.
        control_burbuja_x = 5
        control_burbuja_y = 12

        self.dibujar_burbuja(
            pantalla,
            int(x_pantalla + self.rect.width // 2 - round(24 * ESCALA_JUEGO) + control_burbuja_x),
            int(self.rect.y - round(65 * ESCALA_JUEGO) + control_burbuja_y),
        )


# ============================================================
# 13. CAJA DE DIALOGO
# ============================================================

class CajaDialogo:
    def __init__(self):
        self.visible = False

        self.paginas = []
        self.pagina_actual = 0

        self.texto_completo = ""
        self.texto_actual = ""
        self.indice = 0

        self.velocidad_texto = 40
        self.contador_tiempo = 0

        self.fuente = cargar_fuente_pixel(33)
        self.fuente_pequena = cargar_fuente_pixel(24)

        self.rect = pygame.Rect(40, 0, 100, 100)

    def redimensionar(self, ancho, alto):
        margen_inferior = round(30 * ESCALA_JUEGO)

        ancho_caja = min(ancho - 120, round(760 * ESCALA_JUEGO))
        alto_caja = round(150 * ESCALA_JUEGO)

        ancho_caja = max(round(360 * ESCALA_JUEGO), ancho_caja)
        alto_caja = max(round(120 * ESCALA_JUEGO), alto_caja)

        x = (ancho - ancho_caja) // 2
        y = alto - alto_caja - margen_inferior

        self.rect = pygame.Rect(x, y, ancho_caja, alto_caja)

    def iniciar(self, paginas):
        self.visible = True
        self.paginas = paginas
        self.pagina_actual = 0
        self.cargar_pagina()

    def cargar_pagina(self):
        self.texto_completo = self.paginas[self.pagina_actual]
        self.texto_actual = ""
        self.indice = 0
        self.contador_tiempo = 0

    def actualizar(self, dt):
        if not self.visible:
            return

        if self.indice < len(self.texto_completo):
            self.contador_tiempo += dt

            while self.contador_tiempo >= 1 / self.velocidad_texto:
                self.contador_tiempo -= 1 / self.velocidad_texto

                if self.indice < len(self.texto_completo):
                    self.texto_actual += self.texto_completo[self.indice]
                    self.indice += 1

    def texto_terminado(self):
        return self.indice >= len(self.texto_completo)

    def completar_texto(self):
        self.texto_actual = self.texto_completo
        self.indice = len(self.texto_completo)

    def avanzar(self):
        if not self.texto_terminado():
            self.completar_texto()
            return False

        if self.pagina_actual < len(self.paginas) - 1:
            self.pagina_actual += 1
            self.cargar_pagina()
            return False

        self.visible = False
        return True

    def dividir_lineas(self, texto, ancho_max):
        return dividir_lineas_por_ancho(texto, self.fuente, ancho_max)

    def obtener_puntos_caja(self, rect, corte):
        return obtener_puntos_rect_pixel(rect, corte)

    def dibujar_fondo(self, pantalla):
        rect = self.rect

        fondo = (246, 242, 232)
        borde_oscuro = (15, 27, 45)
        borde_medio = (57, 76, 96)
        borde_claro = (165, 174, 180)
        sombra = (6, 12, 22)

        corte = round(16 * ESCALA_JUEGO)

        rect_sombra = rect.move(4, 4)
        pygame.draw.polygon(pantalla, sombra, self.obtener_puntos_caja(rect_sombra, corte))
        pygame.draw.polygon(pantalla, borde_oscuro, self.obtener_puntos_caja(rect, corte))

        rect_medio = rect.inflate(-9, -9)
        pygame.draw.polygon(pantalla, borde_medio, self.obtener_puntos_caja(rect_medio, corte - 4))

        rect_linea = rect.inflate(-18, -18)
        pygame.draw.polygon(pantalla, borde_oscuro, self.obtener_puntos_caja(rect_linea, corte - 9))

        rect_fondo = rect.inflate(-27, -27)
        pygame.draw.polygon(pantalla, fondo, self.obtener_puntos_caja(rect_fondo, corte - 12))

        rect_claro = rect.inflate(-36, -36)
        pygame.draw.lines(pantalla, borde_claro, True, self.obtener_puntos_caja(rect_claro, corte - 15), 2)

        pixel = 6

        pygame.draw.rect(pantalla, borde_oscuro, (rect.x + 15, rect.y + 6, pixel, pixel))
        pygame.draw.rect(pantalla, borde_oscuro, (rect.right - 21, rect.y + 6, pixel, pixel))
        pygame.draw.rect(pantalla, borde_oscuro, (rect.x + 15, rect.bottom - 12, pixel, pixel))
        pygame.draw.rect(pantalla, borde_oscuro, (rect.right - 21, rect.bottom - 12, pixel, pixel))

    def dibujar_indicador_espacio(self, pantalla):
        if not self.texto_terminado():
            return

        color = (18, 28, 45)
        texto = self.fuente_pequena.render("ESPACIO", False, color)

        margen_derecho = 48
        separacion = 22

        flecha_x = self.rect.right - margen_derecho
        flecha_y = self.rect.bottom - 42

        texto_x = flecha_x - texto.get_width() - separacion - 8
        texto_y = flecha_y - texto.get_height() // 2 - 2

        pantalla.blit(texto, (texto_x, texto_y))

        pygame.draw.polygon(
            pantalla,
            color,
            [
                (flecha_x - 15, flecha_y - 9),
                (flecha_x + 15, flecha_y - 9),
                (flecha_x, flecha_y + 9),
            ],
        )

    def dibujar(self, pantalla):
        if not self.visible:
            return

        self.dibujar_fondo(pantalla)

        margen_x = int(self.rect.width * 0.075)
        margen_y = int(self.rect.height * 0.24)
        ancho_texto = self.rect.width - (margen_x * 2)
        salto_linea = self.fuente.get_height() + 7

        lineas = self.dividir_lineas(self.texto_actual, ancho_texto)

        for i, linea in enumerate(lineas):
            y_texto = self.rect.y + margen_y + i * salto_linea

            if y_texto > self.rect.bottom - 65:
                break

            render = self.fuente.render(linea, False, (18, 28, 45))
            pantalla.blit(render, (self.rect.x + margen_x, y_texto))

        self.dibujar_indicador_espacio(pantalla)


# ============================================================
# 14. PANTALLA PRACTICA VERDADERO / FALSO
# ============================================================
# PantallaPractica fue movida a juego/interfaz/practica.py


# ============================================================
# 15. SISTEMA REUTILIZABLE DE INTERACCIONES
# ============================================================

class Interaccion:
    def __init__(
        self,
        nombre,
        obtener_rect,
        mensaje,
        accion,
        requiere_suelo=True,
        activa=True,
        usar_una_vez=False,
    ):
        self.nombre = nombre
        self.obtener_rect = obtener_rect
        self.mensaje = mensaje
        self.accion = accion
        self.requiere_suelo = requiere_suelo
        self.activa = activa
        self.usar_una_vez = usar_una_vez
        self.usada = False

    def puede_usarse(self, juego):
        if not self.activa:
            return False

        if self.usar_una_vez and self.usada:
            return False

        if juego.game_over:
            return False

        if hasattr(juego, "transicion_iris") and juego.transicion_iris.activa():
            return False

        if juego.en_dialogo:
            return False

        if (
            hasattr(juego, "hay_practica_visible")
            and juego.hay_practica_visible()
        ):
            return False

        if self.requiere_suelo and not juego.jugador.en_suelo:
            return False

        zona = self.obtener_rect()

        if zona is None:
            return False

        jugador_rect_mundo = juego.jugador.obtener_rect_mundo(juego.camara_x)

        return jugador_rect_mundo.colliderect(zona)

    def ejecutar(self, juego):
        if not self.puede_usarse(juego):
            return False

        self.accion()

        if self.usar_una_vez:
            self.usada = True

        return True

# ============================================================
# 15.1 BOTON DE IMAGEN PARA MENU DE PAUSA
# ============================================================

class BotonImagenPausa:
    def __init__(self, nombre, imagen_normal, imagen_hover=None):
        self.nombre = nombre

        # Se recorta la transparencia sobrante para que el rect sea del
        # tamaño real visible del PNG y no del lienzo exportado.
        self.imagen_normal_original = self.recortar_transparencia(imagen_normal)
        self.imagen_hover_original = self.recortar_transparencia(imagen_hover)

        self.imagen_normal = self.imagen_normal_original
        self.imagen_hover = self.imagen_hover_original
        self.imagen_actual = self.imagen_normal
        self._ultima_configuracion = None

        if self.imagen_normal is not None:
            self.rect = self.imagen_normal.get_rect(topleft=(0, 0))
        else:
            self.rect = pygame.Rect(0, 0, 1, 1)

    def recortar_transparencia(self, imagen):
        if imagen is None:
            return None

        rect_visible = imagen.get_bounding_rect()

        if rect_visible.width <= 0 or rect_visible.height <= 0:
            return imagen

        imagen_recortada = pygame.Surface(
            (rect_visible.width, rect_visible.height),
            pygame.SRCALPHA
        )

        imagen_recortada.blit(imagen, (0, 0), rect_visible)

        return imagen_recortada

    def configurar_posicion(self, x, y, ancho_objetivo=None, alto_objetivo=None, escala=1.0):
        if self.imagen_normal_original is None:
            self.rect = pygame.Rect(int(x), int(y), 1, 1)
            return

        ancho_original = self.imagen_normal_original.get_width()
        alto_original = self.imagen_normal_original.get_height()
        configuracion = (
            int(x),
            int(y),
            ancho_objetivo,
            alto_objetivo,
            float(escala),
            ancho_original,
            alto_original,
        )

        if configuracion == self._ultima_configuracion:
            return

        if ancho_objetivo is not None and alto_objetivo is not None:
            factor_escala = min(
                ancho_objetivo / ancho_original,
                alto_objetivo / alto_original
            )
        elif ancho_objetivo is not None:
            factor_escala = ancho_objetivo / ancho_original
        elif alto_objetivo is not None:
            factor_escala = alto_objetivo / alto_original
        else:
            factor_escala = escala

        nuevo_ancho = max(1, int(ancho_original * factor_escala))
        nuevo_alto = max(1, int(alto_original * factor_escala))

        self.imagen_normal = pygame.transform.scale(
            self.imagen_normal_original,
            (nuevo_ancho, nuevo_alto)
        )

        if self.imagen_hover_original is not None:
            self.imagen_hover = pygame.transform.scale(
                self.imagen_hover_original,
                (nuevo_ancho, nuevo_alto)
            )
        else:
            self.imagen_hover = None

        # El rect SIEMPRE toma el tamaño final del PNG.
        self.rect = self.imagen_normal.get_rect(topleft=(int(x), int(y)))
        self._ultima_configuracion = configuracion

    def configurar_rect(self, x, y, ancho, alto):
        # Compatibilidad con código anterior.
        # No deforma la imagen: la ajusta dentro de ancho/alto manteniendo proporción.
        self.configurar_posicion(
            x,
            y,
            ancho_objetivo=ancho,
            alto_objetivo=alto
        )

    def mouse_encima(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def fue_presionado(self, posicion):
        return self.rect.collidepoint(posicion)

    def obtener_imagen_actual(self):
        if self.mouse_encima() and self.imagen_hover is not None:
            return self.imagen_hover

        return self.imagen_normal

    def dibujar(self, pantalla):
        imagen = self.obtener_imagen_actual()

        if imagen is None:
            return

        self.imagen_actual = imagen
        pantalla.blit(self.imagen_actual, self.rect.topleft)

# ============================================================
# 16. INTEGRACION DE LA PANTALLA DE CARGA
# La clase PantallaCarga original no se modifica. Main la ejecuta en otro
# proceso y sincroniza su porcentaje mientras se inicializa Pygame.
# ============================================================

def _cargar_clase_pantalla_carga():
    """Carga PantallaCarga desde su archivo real sin modificarlo ni usar caché."""
    codigos_dir = Path(__file__).resolve().parent.parent.parent / "CODIGOS"
    ruta_pantalla_carga = codigos_dir / "pantalla_carga.py"

    if not ruta_pantalla_carga.is_file():
        raise FileNotFoundError(
            f"No se encontro pantalla_carga.py en: {ruta_pantalla_carga}"
        )

    # La pantalla original importa Transicion.py por nombre.
    if str(codigos_dir) not in sys.path:
        sys.path.insert(0, str(codigos_dir))

    # run_path ejecuta directamente el archivo fuente y evita problemas con
    # módulos o .pyc antiguos almacenados en __pycache__.
    namespace = runpy.run_path(
        str(ruta_pantalla_carga),
        run_name="_educore_pantalla_carga_original",
    )

    pantalla_carga = namespace.get("PantallaCarga")
    if not isinstance(pantalla_carga, type):
        nombres_disponibles = ", ".join(
            sorted(nombre for nombre in namespace if not nombre.startswith("__"))
        )
        raise ImportError(
            "No se encontro una clase llamada PantallaCarga en "
            f"{ruta_pantalla_carga}. Nombres encontrados: {nombres_disponibles}"
        )

    return pantalla_carga


def _ejecutar_pantalla_carga_desde_main(progreso_compartido, carga_finalizada):
    """Ejecuta la PantallaCarga original sin modificar pantalla_carga.py."""
    try:
        from PyQt6.QtCore import QTimer, Qt
        from PyQt6.QtWidgets import QApplication

        PantallaCarga = _cargar_clase_pantalla_carga()
    except Exception as error:
        print("[CARGA] No se pudo abrir pantalla_carga.py:", error)
        return

    class PantallaCargaJuego(PantallaCarga):
        """Adaptador local; no altera la clase ni el archivo originales."""

        INTERVALO_PROGRESO_MS = 350

        def __init__(self):
            self._carga_finalizada = carga_finalizada
            self._juego_termino_carga = False
            self._cierre_programado = False

            super().__init__(ventana_destino=None)

            # Se detiene el temporizador original para impedir que intente
            # abrir una ventana PyQt al llegar a 100 %.
            self.timer_carga.stop()
            self._establecer_progreso(0)

            # El porcentaje avanza siempre de 10 en 10. Mientras Pygame sigue
            # cargando se detiene en 90 %; cuando termina, avanza a 100 %.
            self.timer_incremento = QTimer(self)
            self.timer_incremento.timeout.connect(self._avanzar_progreso)
            self.timer_incremento.start(self.INTERVALO_PROGRESO_MS)

            self.timer_estado_juego = QTimer(self)
            self.timer_estado_juego.timeout.connect(self._sincronizar_estado)
            self.timer_estado_juego.start(30)

        def _establecer_progreso(self, valor):
            valor = max(0, min(100, int(valor)))

            if valor == self.porcentaje:
                return

            self.porcentaje = valor
            self.lbl_porcentaje.setText(f"{valor}%")
            self.barra.set_progreso(valor)

        def _sincronizar_estado(self):
            if self._carga_finalizada.is_set():
                self._juego_termino_carga = True

        def _avanzar_progreso(self):
            if self._cierre_programado:
                return

            limite = 100 if self._juego_termino_carga else 90

            if self.porcentaje < limite:
                self._establecer_progreso(
                    min(self.porcentaje + 10, limite)
                )

            if self._juego_termino_carga and self.porcentaje >= 100:
                self._cierre_programado = True
                self.timer_incremento.stop()
                QTimer.singleShot(350, self._cerrar)

        def _cerrar(self):
            if self.timer_animacion.isActive():
                self.timer_animacion.stop()

            if self.timer_incremento.isActive():
                self.timer_incremento.stop()

            if self.timer_estado_juego.isActive():
                self.timer_estado_juego.stop()

            self.close()
            QApplication.instance().quit()

        def abrir_ventana_destino(self):
            # Main se encarga de mostrar Pygame cuando termina la carga.
            self._cerrar()

    app = QApplication([])
    ventana = PantallaCargaJuego()

    # La configuracion se aplica solo a esta instancia creada por main.py.
    ventana.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
    ventana.showMaximized()

    app.exec()


def _iniciar_pantalla_carga():
    contexto = multiprocessing.get_context("spawn")
    progreso = contexto.Value("i", 0)
    carga_finalizada = contexto.Event()
    proceso = contexto.Process(
        target=_ejecutar_pantalla_carga_desde_main,
        args=(progreso, carga_finalizada),
        name="EduCorePantallaCarga",
    )
    proceso.start()
    return proceso, progreso, carga_finalizada


def _actualizar_progreso_compartido(progreso_compartido, valor):
    if progreso_compartido is None:
        return

    valor = max(0, min(100, int(valor)))

    with progreso_compartido.get_lock():
        progreso_compartido.value = valor


def _cerrar_pantalla_carga(proceso, progreso, carga_finalizada):
    _actualizar_progreso_compartido(progreso, 100)
    carga_finalizada.set()
    proceso.join(timeout=4)

    if proceso.is_alive():
        proceso.terminate()
        proceso.join(timeout=1)


# ============================================================
# 16. JUEGO PRINCIPAL
# ============================================================

class JuegoEduCore:
    def __init__(
        self,
        id_jugador=1,
        nombre_lenguaje="Python",
        orden_leccion=None,
        actualizar_progreso_carga=None,
    ):
        self._actualizar_progreso_carga = actualizar_progreso_carga
        self._informar_progreso_carga(2)

        self._inicializar_pygame()
        self._informar_progreso_carga(8)

        self._inicializar_pantalla()
        self._informar_progreso_carga(14)

        self.id_jugador = id_jugador
        self.nombre_lenguaje_solicitado = nombre_lenguaje
        self.orden_leccion_solicitado = orden_leccion

        self.db = ConexionEduCore(DB_CONFIG)
        self._informar_progreso_carga(22)

        self._cargar_datos_iniciales(nombre_lenguaje)
        self._informar_progreso_carga(30)

        self._inicializar_estado()
        self._informar_progreso_carga(35)

        self._inicializar_mundo()
        self._informar_progreso_carga(70)

        self._cargar_assets_interfaz()
        self._informar_progreso_carga(82)

        self._crear_botones_pausa()
        self.personaje_menu_pausa_original = self.cargar_personaje_menu_pausa()
        self._cache_personaje_menu_pausa = {}
        self._informar_progreso_carga(90)

        self.registrar_interacciones()
        self.preparar_musica_fondo()
        self._informar_progreso_carga(97)

        pygame.display.set_caption("EduCore - Juego conectado a MySQL")
        self.iniciar_musica_fondo_preparada()
        self.clock.tick()
        self._informar_progreso_carga(100)

    def _informar_progreso_carga(self, valor):
        if self._actualizar_progreso_carga is None:
            return

        self._actualizar_progreso_carga(valor)

    def _inicializar_pygame(self):
        pygame.init()

        try:
            pygame.mixer.init()
        except pygame.error as error:
            print("[AUDIO] No se pudo iniciar el audio:", error)

    def _inicializar_pantalla(self):
        self.pantalla_real = pygame.display.set_mode(
            (ANCHO, ALTO),
            pygame.DOUBLEBUF,
        )
        pygame.display.set_caption("EduCore - Juego conectado a MySQL")

        self.superficie_logica = self.pantalla_real

        # Las capas grandes del fondo se mezclan aquí a 960x540 y después
        # se escalan una sola vez al tamaño real de la ventana.
        self.superficie_fondo = pygame.Surface(
            (ANCHO_FONDO, ALTO_FONDO)
        ).convert()

        self.clock = pygame.time.Clock()
        self.fuente_titulo = pygame.font.SysFont("arial", 66, bold=True)
        self.fuente_texto = pygame.font.SysFont("arial", 36)
        self.fuente_fps = pygame.font.SysFont("arial", 28)
        self.fuente_ui = cargar_fuente_pixel(30)
        self.fuente_ui_pequena = cargar_fuente_pixel(22)

        self._cache_escalado_ui = {}
        self._cache_texto_interaccion = {}
        self._fps_superficie = None
        self._fps_ultima_actualizacion = 0
        self._fondo_pausa_cache = None

    def _inicializar_estado(self):
        self.camara_x = 0
        self.game_over = self.vidas <= 0
        self.mostrar_hitboxes = MOSTRAR_HITBOXES
        self.salto_presionado_anterior = False
        self.en_dialogo = False
        self.en_pausa = False
        self.boton_pausa_rects = {}
        self.musica_silenciada = False
        self.musica_fondo_preparada = False
        self.interacciones = []
        self.interaccion_actual = None
        self.mensaje_aprendido_visible = False
        self.tiempo_mensaje_aprendido = 0
        self.transicion_iris = TransicionIris(duracion=0.8)

    def _cargar_datos_iniciales(self, nombre_lenguaje):
        self.datos_jugador = (
            self.db.obtener_jugador(self.id_jugador) if self.db.activa else None
        )
        self.datos_lenguaje = (
            self.db.obtener_lenguaje(nombre_lenguaje) if self.db.activa else None
        )

        if self.datos_jugador:
            self.nombre_jugador = self.datos_jugador.get("nombre") or "Jugador"
            self.personaje_elegido = (
                self.datos_jugador.get("personaje") or PERSONAJE_DEFAULT
            )
            self.vidas = int(self.datos_jugador.get("vidas") or 0)
        else:
            self.nombre_jugador = "Jugador local"
            self.personaje_elegido = PERSONAJE_DEFAULT
            self.vidas = 5

        if self.datos_lenguaje:
            self.id_lenguaje = int(self.datos_lenguaje.get("id_lenguaje"))
            self.nombre_lenguaje = (
                self.datos_lenguaje.get("nombre") or nombre_lenguaje
            )
        else:
            self.id_lenguaje = None
            self.nombre_lenguaje = nombre_lenguaje

        if self.id_lenguaje and self.datos_jugador:
            self.leccion_actual = self.db.obtener_leccion(
                self.id_jugador,
                self.id_lenguaje,
                self.orden_leccion_solicitado,
            )
        else:
            self.leccion_actual = None

        self.dialogo_leccion = construir_paginas_leccion(
            self.leccion_actual,
            self.nombre_lenguaje,
        )
        self.leccion_ya_completada = False
        self.leccion_npc_leida = False

    def _inicializar_mundo(self):
        self.capas = []
        self.capas_primer_plano = []
        self.capa_suelo = None
        self.cargar_fondo_personalizado()

        self.jugador = Jugador(self.personaje_elegido, escala_default=5.1)
        self.plataformas = [
            PlataformaInvisible(PISO_INICIO, PISO_FIN, PISO_COLISION_Y),
        ]
        self.limite_camara_x = max(0, PISO_FIN - ANCHO)
        self.obstaculos = [
            Obstaculo(
                round(500 * ESCALA_JUEGO),
                PISO_COLISION_Y - TAMANO_OBSTACULO + round(40 * ESCALA_JUEGO),
                TAMANO_OBSTACULO,
                TAMANO_OBSTACULO,
                "tronco",
                OBSTACULOS_DIR / "tronco.png",
                hitbox_offset_x=round(10 * ESCALA_JUEGO),
                hitbox_offset_y=round(40 * ESCALA_JUEGO),
                hitbox_ancho=TAMANO_OBSTACULO - round(20 * ESCALA_JUEGO),
                hitbox_alto=TAMANO_OBSTACULO - round(70 * ESCALA_JUEGO),
            )
        ]
        self.jugador.colocar_sobre_piso(PISO_COLISION_Y)

        self.npc = NPC(
            x_mundo=round(720 * ESCALA_JUEGO),
            suelo_y=PISO_Y + CONFIGURACION_NPC,
            escala=3.6,
        )
        self.caja_dialogo = CajaDialogo()
        self.caja_dialogo.redimensionar(ANCHO, ALTO)

        self.practica = PantallaPractica()
        self.practica_codigo = PantallaPracticaCodigo(ANCHO, ALTO)
        self.objeto_practica_actual = None
        self.objeto_en_contacto = None
        self.objetos_practica = []

    def hay_practica_visible(self):
        return bool(
            (hasattr(self, "practica") and self.practica.visible)
            or (
                hasattr(self, "practica_codigo")
                and self.practica_codigo.visible
            )
        )

    def obtener_practica_visible(self):
        if (
            hasattr(self, "practica_codigo")
            and self.practica_codigo.visible
        ):
            return self.practica_codigo

        if hasattr(self, "practica") and self.practica.visible:
            return self.practica

        return None

    def cerrar_practicas(self):
        if hasattr(self, "practica"):
            self.practica.cerrar()

        if hasattr(self, "practica_codigo"):
            self.practica_codigo.cerrar()

    def _cargar_assets_interfaz(self):
        rutas_por_atributo = (
            ("concepto_aprendido_original", RUTA_CONCEPTO_APRENDIDO),
            ("vida_llena_original", RUTA_VIDA_LLENA),
            ("vida_vacia_original", RUTA_VIDA_VACIA),
            ("cuadro_aviso", RUTA_CUADRO_AVISO),
            ("logo_menu_pausa_original", RUTA_LOGO_MENU_PAUSA),
            ("boton_reanudar_original", RUTA_BOTON_REANUDAR),
            ("boton_reanudar_click_original", RUTA_BOTON_REANUDAR_CLICK),
            ("boton_configuracion_original", RUTA_BOTON_CONFIGURACION),
            (
                "boton_configuracion_click_original",
                RUTA_BOTON_CONFIGURACION_CLICK,
            ),
            ("boton_salir_original", RUTA_BOTON_SALIR),
            ("boton_salir_click_original", RUTA_BOTON_SALIR_CLICK),
        )

        for atributo, ruta in rutas_por_atributo:
            setattr(self, atributo, cargar_imagen(ruta))

    def _crear_botones_pausa(self):
        configuracion = {
            "reanudar": (
                self.boton_reanudar_original,
                self.boton_reanudar_click_original,
            ),
            "ajustes": (
                self.boton_configuracion_original,
                self.boton_configuracion_click_original,
            ),
            "salir": (
                self.boton_salir_original,
                self.boton_salir_click_original,
            ),
        }
        self.botones_pausa = {
            nombre: BotonImagenPausa(nombre, imagen_normal, imagen_hover)
            for nombre, (imagen_normal, imagen_hover) in configuracion.items()
        }

    def cargar_fondo_personalizado(self):
        # Capas lejanas: se mantienen a media resolución para reducir carga.
        self.capas = []

        for configuracion in _CAPAS_FONDO_CONFIG[:2]:
            (
                ruta,
                factor,
                color_fallback,
                limpiar_fondo_falso,
                offset_y,
            ) = configuracion

            self.capas.append(
                CapaParallax(
                    ruta,
                    factor,
                    ANCHO_FONDO,
                    ALTO_FONDO,
                    color_fallback,
                    limpiar_fondo_falso=limpiar_fondo_falso,
                    offset_y=round(offset_y * ESCALA_RENDER_FONDO),
                )
            )

        # La capa de plantas está cerca de la cámara. Dibujarla directamente
        # a 1920x1080 evita los saltos de dos píxeles que aparecían al ampliar
        # el fondo de 960x540.
        (
            ruta_plantas,
            factor_plantas,
            color_plantas,
            limpiar_plantas,
            offset_plantas,
        ) = _CAPAS_FONDO_CONFIG[2]

        self.capas_primer_plano = [
            CapaParallax(
                ruta_plantas,
                factor_plantas,
                ANCHO,
                ALTO,
                color_plantas,
                limpiar_fondo_falso=limpiar_plantas,
                offset_y=offset_plantas,
            )
        ]

        # El suelo también se dibuja a resolución completa para que avance
        # exactamente un píxel cuando la cámara avanza un píxel.
        self.capa_suelo = CapaParallax(
            FONDO_SUELO,
            1.00,
            ANCHO,
            ALTO,
            (0, 0, 0, 0),
            limpiar_fondo_falso=True,
            cortar_arriba_y=(
                PISO_COLISION_Y - round(70 * ESCALA_JUEGO)
            ),
        )

    def obtener_practica_activa(self):
        """Devuelve únicamente el primer ejercicio que todavía no se completó."""
        for objeto in self.objetos_practica:
            if not objeto.completado:
                return objeto

        return None

    def obtener_zona_interaccion_practica(self):
        """Devuelve la zona de la moneda que está cerca del jugador."""
        objeto = self.objeto_en_contacto

        if objeto is None or objeto.completado:
            return None

        return objeto.rect.inflate(
            round(80 * ESCALA_JUEGO),
            round(45 * ESCALA_JUEGO),
        )

    def abrir_practica_en_contacto(self):
        """Abre con ENTER la práctica de la moneda cercana."""
        objeto = self.objeto_en_contacto

        if objeto is None or objeto.completado:
            return

        self.abrir_practica_objeto(objeto)

    def registrar_interacciones(self):
        self.interacciones = []

        # Interacción del profesor.
        self.interacciones.append(
            Interaccion(
                nombre="leccion_npc",
                obtener_rect=lambda: self.npc.zona_dialogo if self.npc else None,
                mensaje="Presiona ENTER para iniciar la leccion",
                accion=self.iniciar_dialogo_npc,
                requiere_suelo=True,
                activa=True,
                usar_una_vez=False,
            )
        )

        # Interacción de las monedas de verdadero/falso y completar código.
        self.interacciones.append(
            Interaccion(
                nombre="practica_moneda",
                obtener_rect=self.obtener_zona_interaccion_practica,
                mensaje="Presiona ENTER para hacer el ejercicio",
                accion=self.abrir_practica_en_contacto,
                requiere_suelo=False,
                activa=True,
                usar_una_vez=False,
            )
        )

    def actualizar_interaccion_actual(self):
        self.interaccion_actual = None

        for interaccion in self.interacciones:
            if interaccion.puede_usarse(self):
                self.interaccion_actual = interaccion
                return

    def usar_interaccion_actual(self):
        if self.interaccion_actual:
            self.interaccion_actual.ejecutar(self)

    def desactivar_interaccion(self, nombre):
        for interaccion in self.interacciones:
            if interaccion.nombre == nombre:
                interaccion.activa = False
                interaccion.usada = True

    def preparar_musica_fondo(self):
        self.musica_fondo_preparada = False

        if not pygame.mixer.get_init():
            return False

        if not RUTA_MUSICA_FONDO.exists():
            print("[AUDIO] No se encontro la musica:", RUTA_MUSICA_FONDO)
            return False

        try:
            pygame.mixer.music.load(str(RUTA_MUSICA_FONDO))
            self._aplicar_volumen_musica()
            self.musica_fondo_preparada = True
            return True
        except pygame.error as error:
            print("[AUDIO] No se pudo reproducir la musica:", error)
            return False

    def iniciar_musica_fondo_preparada(self):
        if not pygame.mixer.get_init() or not self.musica_fondo_preparada:
            return

        try:
            pygame.mixer.music.play(-1)
        except pygame.error as error:
            print("[AUDIO] No se pudo reproducir la musica:", error)

    def reproducir_musica_fondo(self):
        if self.preparar_musica_fondo():
            self.iniciar_musica_fondo_preparada()

    def _aplicar_volumen_musica(self):
        volumen = 0 if self.musica_silenciada else VOLUMEN_MUSICA
        pygame.mixer.music.set_volume(volumen)

    def alternar_musica(self):
        if not pygame.mixer.get_init():
            return

        self.musica_silenciada = not self.musica_silenciada
        self._aplicar_volumen_musica()

    def reiniciar(self):
        self.camara_x = 0
        self.en_dialogo = False
        self.mensaje_aprendido_visible = False
        self.objeto_practica_actual = None
        self.objeto_en_contacto = None

        self.cerrar_practicas()

        self.jugador.velocidad_y = 0
        self.jugador.colocar_sobre_piso(PISO_COLISION_Y)

        if self.vidas > 0:
            self.game_over = False

    def obtener_centro_transicion_jugador(self):
        jugador_rect = self.jugador.obtener_rect_pantalla()
        centro_x = jugador_rect.centerx
        centro_y = jugador_rect.centery
        centro_x = max(0, min(ANCHO, centro_x))
        centro_y = max(0, min(ALTO, centro_y))
        return centro_x, centro_y

    def iniciar_transicion_entrada(self):
        self.transicion_iris.iniciar_apertura(
            self.obtener_centro_transicion_jugador()
        )

    def _restar_vida(self, evento=None, detalle_base=None):
        if self.datos_jugador and self.db.activa:
            if evento is None:
                vidas_bd = self.db.restar_vida(self.id_jugador)
            else:
                vidas_bd = self.db.restar_vida(
                    self.id_jugador,
                    evento=evento,
                    detalle_base=detalle_base,
                )

            if vidas_bd is not None:
                self.vidas = vidas_bd
            else:
                self.vidas = max(self.vidas - 1, 0)
        else:
            self.vidas = max(self.vidas - 1, 0)

        if self.vidas <= 0:
            self.game_over = True

    def obtener_direccion(self):
        if (
            self.en_dialogo
            or self.en_pausa
            or self.game_over
            or self.transicion_iris.activa()
            or self.hay_practica_visible()
        ):
            return 0

        teclas = pygame.key.get_pressed()

        derecha = teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
        izquierda = teclas[pygame.K_LEFT] or teclas[pygame.K_a]

        if derecha and not izquierda:
            return 1

        if izquierda and not derecha:
            return -1

        return 0

    def manejar_salto(self):
        teclas = pygame.key.get_pressed()

        salto_actual = (
            teclas[pygame.K_SPACE]
            or teclas[pygame.K_w]
            or teclas[pygame.K_UP]
        )

        if salto_actual and not self.salto_presionado_anterior:
            if (
                not self.game_over
                and not self.en_dialogo
                and not self.en_pausa
                and not self.transicion_iris.activa()
                and not self.hay_practica_visible()
            ):
                self.jugador.saltar()

        self.salto_presionado_anterior = salto_actual

    def iniciar_dialogo_npc(self):
        self.en_dialogo = True
        self.interaccion_actual = None

        if not self.caja_dialogo.visible:
            self.caja_dialogo.iniciar(self.dialogo_leccion)

    def cerrar_dialogo_npc(self):
        self.en_dialogo = False
        self.leccion_npc_leida = True

        # La moneda aparece únicamente después de terminar todas las
        # páginas de la lección. No se muestra ningún cuadro adicional.
        if not self.objetos_practica:
            self.crear_objeto_practica_prueba()

    def crear_objeto_practica_prueba(self):
        """Crea una sola moneda de prueba para el nivel base."""
        tamano_objeto = round(48 * ESCALA_JUEGO)
        x_moneda = round(1260 * ESCALA_JUEGO)
        y_moneda = PISO_COLISION_Y - tamano_objeto - round(18 * ESCALA_JUEGO)

        pregunta = (
            "En Python, una variable sirve para guardar datos "
            "que puedes usar despues en el programa."
        )

        self.objetos_practica = [
            ObjetoPractica(
                x=x_moneda,
                y=y_moneda,
                pregunta=pregunta,
                respuesta_correcta=True,
                nombre="moneda_variable",
            )
        ]

    def abrir_practica_objeto(self, objeto):
        practica_activa = self.obtener_practica_activa()

        if (
            objeto is None
            or objeto.completado
            or self.game_over
            or objeto is not practica_activa
        ):
            return

        self.objeto_practica_actual = objeto
        self.interaccion_actual = None

        if objeto.tipo == "codigo":
            self.practica_codigo.iniciar(
                objeto.pregunta,
                objeto.configuracion_codigo,
            )
        else:
            self.practica.iniciar(
                objeto.pregunta,
                objeto.respuesta_correcta,
            )

    def restar_vida_por_respuesta_incorrecta(self):
        self._restar_vida(
            evento="Respuesta incorrecta",
            detalle_base="Respondio incorrectamente una practica",
        )

    def completar_leccion_desde_practica(self):
        if self.leccion_ya_completada:
            return

        if (
            self.datos_jugador
            and self.id_lenguaje
            and self.leccion_actual
            and self.db.activa
        ):
            self.db.completar_leccion(
                self.id_jugador,
                self.id_lenguaje,
                self.leccion_actual,
            )

        self.leccion_ya_completada = True

    def finalizar_practica_objeto(self, respuesta_correcta):
        objeto = self.objeto_practica_actual
        self.objeto_practica_actual = None

        if respuesta_correcta:
            if objeto is not None:
                objeto.completado = True

            self.objeto_en_contacto = None

            if self.objetos_practica and all(
                practica.completado
                for practica in self.objetos_practica
            ):
                self.completar_leccion_desde_practica()
            return

        # No se crea ningun pozo y tampoco se reinicia la posicion.
        # Solamente se descuenta una vida y la moneda permanece para reintentar.
        self.restar_vida_por_respuesta_incorrecta()

    def revisar_colision_objeto_practica(self):
        """Detecta solamente la primera práctica pendiente."""
        if (
            self.game_over
            or self.en_dialogo
            or self.en_pausa
            or self.hay_practica_visible()
            or self.transicion_iris.activa()
            or not self.leccion_npc_leida
        ):
            self.objeto_en_contacto = None
            return

        objeto = self.obtener_practica_activa()

        if objeto is None:
            self.objeto_en_contacto = None
            return

        jugador_rect_mundo = self.jugador.obtener_rect_mundo(
            self.camara_x
        )

        zona_interaccion = objeto.rect.inflate(
            round(80 * ESCALA_JUEGO),
            round(45 * ESCALA_JUEGO),
        )

        if jugador_rect_mundo.colliderect(zona_interaccion):
            self.objeto_en_contacto = objeto
        else:
            self.objeto_en_contacto = None


    def revisar_colision_piso(self, y_anterior):
        self.jugador.en_suelo = False

        jugador_rect_mundo = self.jugador.obtener_rect_mundo(self.camara_x)
        hitbox_local = self.jugador.obtener_hitbox_local()

        bottom_anterior = y_anterior + hitbox_local.bottom
        viene_cayendo = self.jugador.velocidad_y >= 0

        if not viene_cayendo:
            return

        pisos_posibles = []

        for plataforma in self.plataformas:
            rect = plataforma.obtener_rect_mundo()

            esta_sobre_x = (
                jugador_rect_mundo.right > rect.left
                and jugador_rect_mundo.left < rect.right
            )

            cruzo_el_piso = (
                bottom_anterior <= rect.top + MARGEN_COLISION_VERTICAL
                and jugador_rect_mundo.bottom >= rect.top
            )

            if esta_sobre_x and cruzo_el_piso:
                pisos_posibles.append(rect)

        for obstaculo in self.obstaculos:
            if not obstaculo.es_solido():
                continue

            rect = obstaculo.rect

            esta_sobre_x = (
                jugador_rect_mundo.right > rect.left
                and jugador_rect_mundo.left < rect.right
            )

            cruzo_el_piso = (
                bottom_anterior <= rect.top + MARGEN_COLISION_VERTICAL
                and jugador_rect_mundo.bottom >= rect.top
            )

            if esta_sobre_x and cruzo_el_piso:
                pisos_posibles.append(rect)

        if pisos_posibles:
            piso = min(pisos_posibles, key=lambda r: r.top)
            self.jugador.colocar_sobre_piso(piso.top)

    def revisar_colision_obstaculos(self, y_anterior, x_mundo_anterior):
        jugador_rect_mundo = self.jugador.obtener_rect_mundo(self.camara_x)
        hitbox_local = self.jugador.obtener_hitbox_local()

        bloqueo_horizontal = False

        for obstaculo in self.obstaculos:
            if not jugador_rect_mundo.colliderect(obstaculo.rect):
                continue

            if obstaculo.es_danio():
                self.game_over = True
                return False

            if not obstaculo.es_solido():
                continue

            rect_x_anterior = pygame.Rect(
                int(x_mundo_anterior + hitbox_local.x),
                jugador_rect_mundo.y,
                jugador_rect_mundo.width,
                jugador_rect_mundo.height,
            )

            bottom_anterior = y_anterior + hitbox_local.bottom

            viene_subiendo = self.jugador.velocidad_y < 0
            viene_cayendo = self.jugador.velocidad_y >= 0

            cayo_encima = (
                viene_cayendo
                and bottom_anterior <= obstaculo.rect.top + MARGEN_COLISION_VERTICAL
                and jugador_rect_mundo.bottom >= obstaculo.rect.top
                and jugador_rect_mundo.right > obstaculo.rect.left
                and jugador_rect_mundo.left < obstaculo.rect.right
            )

            if cayo_encima:
                self.jugador.colocar_sobre_piso(obstaculo.rect.top)
                continue

            toco_techo = (
                viene_subiendo
                and jugador_rect_mundo.top <= obstaculo.rect.bottom
                and jugador_rect_mundo.bottom > obstaculo.rect.bottom
            )

            if toco_techo:
                y_sprite = obstaculo.rect.bottom - hitbox_local.top
                self.jugador.y = y_sprite
                self.jugador.velocidad_y = 0
                self.jugador.en_suelo = False
                continue

            choque_lateral = not rect_x_anterior.colliderect(obstaculo.rect)

            if choque_lateral:
                bloqueo_horizontal = True

        return bloqueo_horizontal

    def actualizar(self, dt):
        if self.en_pausa:
            return

        practica_visible = self.obtener_practica_visible()

        if practica_visible is not None:
            # Se detiene al jugador, pero la interfaz sigue actualizandose.
            practica_visible.actualizar(dt)
            self.jugador.actualizar_animacion(0)
            return

        objeto_activo = self.obtener_practica_activa()

        if objeto_activo is not None:
            objeto_activo.actualizar(dt)

        # Mientras la transicion de entrada esta activa, se pausa el
        # movimiento, las colisiones y las interacciones del jugador.
        if self.transicion_iris.activa():
            self.transicion_iris.actualizar(dt)
            self.jugador.actualizar_animacion(0)
            return

        direccion = self.obtener_direccion()
        self.manejar_salto()

        velocidad_actual = VELOCIDAD_CAMINAR if self.jugador.en_suelo else VELOCIDAD_AIRE

        camara_anterior = self.camara_x
        y_anterior = self.jugador.y
        x_mundo_anterior = self.jugador.x_pantalla + camara_anterior

        if not self.game_over and not self.en_dialogo:
            self.camara_x += direccion * velocidad_actual * dt

        if self.camara_x < 0:
            self.camara_x = 0

        if self.camara_x > self.limite_camara_x:
            self.camara_x = self.limite_camara_x

        if not self.game_over:
            self.jugador.aplicar_gravedad()
            self.revisar_colision_piso(y_anterior)

            if self.revisar_colision_obstaculos(y_anterior, x_mundo_anterior):
                self.camara_x = camara_anterior

        if self.npc:
            self.npc.actualizar(PISO_COLISION_Y + CONFIGURACION_NPC, dt)

        if self.caja_dialogo:
            self.caja_dialogo.actualizar(dt)

        # Primero se detecta la moneda cercana y después se decide qué
        # aviso de interacción debe mostrarse.
        self.revisar_colision_objeto_practica()
        self.actualizar_interaccion_actual()

        if self.mensaje_aprendido_visible:
            self.tiempo_mensaje_aprendido -= dt

            if self.tiempo_mensaje_aprendido <= 0:
                self.mensaje_aprendido_visible = False

        self.jugador.actualizar_animacion(direccion)

    def dibujar_hitboxes_debug(self):
        if not self.mostrar_hitboxes:
            return

        pantalla = self.superficie_logica

        pygame.draw.rect(
            pantalla,
            (0, 255, 0),
            self.jugador.obtener_rect_pantalla(),
            2
        )

        for plataforma in self.plataformas:
            rect = plataforma.obtener_rect_mundo()

            rect_pantalla = pygame.Rect(
                int(rect.x - self.camara_x),
                int(rect.y),
                int(rect.width),
                int(rect.height)
            )

            pygame.draw.rect(pantalla, (0, 120, 255), rect_pantalla, 2)

        for obstaculo in self.obstaculos:
            pygame.draw.rect(
                pantalla,
                (255, 140, 0),
                obstaculo.obtener_rect_pantalla(self.camara_x),
                2
            )

        objeto_activo = self.obtener_practica_activa()

        if objeto_activo is not None:
            pygame.draw.rect(
                pantalla,
                (255, 230, 0),
                objeto_activo.obtener_rect_pantalla(self.camara_x),
                2,
            )

        if self.npc:
            zona_npc = pygame.Rect(
                int(self.npc.zona_dialogo.x - self.camara_x),
                int(self.npc.zona_dialogo.y),
                int(self.npc.zona_dialogo.width),
                int(self.npc.zona_dialogo.height),
            )

            pygame.draw.rect(pantalla, (180, 0, 255), zona_npc, 2)

    def dibujar_fps(self):
        if not MOSTRAR_FPS:
            return

        ahora = pygame.time.get_ticks()

        # Renderizar texto crea una superficie nueva. Se actualiza solo cuatro
        # veces por segundo, no sesenta veces por segundo.
        if (
            self._fps_superficie is None
            or ahora - self._fps_ultima_actualizacion >= 250
        ):
            fps = int(self.clock.get_fps())
            self._fps_superficie = self.fuente_fps.render(
                f"FPS: {fps}",
                True,
                (255, 255, 255),
            )
            self._fps_ultima_actualizacion = ahora

        self.superficie_logica.blit(
            self._fps_superficie,
            (20, 20),
        )

    def obtener_imagen_escalada_ui(self, imagen, ancho, alto, suavizar=False):
        if imagen is None:
            return None

        tamano = (max(1, int(ancho)), max(1, int(alto)))
        clave = (id(imagen), tamano, bool(suavizar))
        escalada = self._cache_escalado_ui.get(clave)

        if escalada is None:
            transformacion = pygame.transform.smoothscale if suavizar else pygame.transform.scale
            escalada = transformacion(imagen, tamano)
            self._cache_escalado_ui[clave] = escalada

        return escalada

    def dibujar_corazones(self, pantalla, x_inicial, y, total_corazones, vidas_visibles, tamano_corazon, separacion):
        vidas_visibles = max(0, min(int(vidas_visibles), total_corazones))

        for i in range(total_corazones):
            if i < vidas_visibles:
                imagen_corazon = self.vida_llena_original
            else:
                imagen_corazon = self.vida_vacia_original

            if imagen_corazon is None:
                continue

            x = x_inicial + i * (tamano_corazon + separacion)

            corazon = self.obtener_imagen_escalada_ui(
                imagen_corazon,
                tamano_corazon,
                tamano_corazon,
            )
            pantalla.blit(corazon, (x, y))

    def dibujar_panel_jugador(self):
        pantalla = self.superficie_logica

        total_corazones = VIDAS_MAXIMAS
        vidas_visibles = self.vidas

        tamano_corazon = 180
        separacion_corazones = -100
        margen_derecho = 1
        margen_superior = -30

        ancho_total = total_corazones * tamano_corazon + (total_corazones - 1) * separacion_corazones

        x_inicial = ANCHO - ancho_total - margen_derecho
        y = margen_superior

        self.dibujar_corazones(
            pantalla,
            x_inicial,
            y,
            total_corazones,
            vidas_visibles,
            tamano_corazon,
            separacion_corazones,
        )

    def dibujar_instruccion_interaccion(self):
        if self.en_dialogo or self.game_over or self.hay_practica_visible():
            return

        if not self.interaccion_actual:
            return

        pantalla = self.superficie_logica
        x = 5
        y = 50
        ancho_cuadro = 750
        alto_cuadro = 150

        if self.cuadro_aviso is None:
            return

        cuadro = self.obtener_imagen_escalada_ui(
            self.cuadro_aviso,
            ancho_cuadro,
            alto_cuadro,
        )
        pantalla.blit(cuadro, (x, y))

        texto_mensaje = self.interaccion_actual.mensaje
        cache = self._cache_texto_interaccion.get(texto_mensaje)

        if cache is None:
            fuente = cargar_fuente_pixel(24)
            color_texto = (255, 255, 255)
            color_enter = (240, 140, 85)

            if "ENTER" in texto_mensaje:
                parte_1, parte_3 = texto_mensaje.split("ENTER", 1)
                cache = (
                    fuente.render(parte_1, False, color_texto),
                    fuente.render("ENTER", False, color_enter),
                    fuente.render(parte_3, False, color_texto),
                )
            else:
                cache = (fuente.render(texto_mensaje, False, color_texto),)

            self._cache_texto_interaccion[texto_mensaje] = cache

        if len(cache) == 3:
            texto_1, texto_2, texto_3 = cache
            ancho_total_texto = sum(texto.get_width() for texto in cache)
            texto_x = x + ancho_cuadro // 2 - ancho_total_texto // 2
            texto_y = y + alto_cuadro // 2 - texto_1.get_height() // 2

            pantalla.blit(texto_1, (texto_x, texto_y))
            pantalla.blit(texto_2, (texto_x + texto_1.get_width(), texto_y))
            pantalla.blit(
                texto_3,
                (texto_x + texto_1.get_width() + texto_2.get_width(), texto_y),
            )
        else:
            texto = cache[0]
            texto_x = x + ancho_cuadro // 2 - texto.get_width() // 2
            texto_y = y + alto_cuadro // 2 - texto.get_height() // 2
            pantalla.blit(texto, (texto_x, texto_y))

    def dibujar_game_over(self):
        if not self.game_over:
            return

        pantalla = self.superficie_logica

        texto = self.fuente_titulo.render("GAME OVER", True, (255, 255, 255))
        texto_2 = self.fuente_texto.render("Te quedaste sin vidas", True, (255, 255, 255))
        texto_3 = self.fuente_texto.render("Presiona ESC para salir", True, (255, 255, 255))

        panel = pygame.Rect(
            ANCHO // 2 - 380,
            ALTO // 2 - 165,
            760,
            330
        )

        pygame.draw.rect(pantalla, (0, 0, 0), panel)
        pygame.draw.rect(pantalla, (255, 255, 255), panel, 4)

        pantalla.blit(
            texto,
            (
                ANCHO // 2 - texto.get_width() // 2,
                ALTO // 2 - 115
            )
        )

        pantalla.blit(
            texto_2,
            (
                ANCHO // 2 - texto_2.get_width() // 2,
                ALTO // 2 - 10
            )
        )

        pantalla.blit(
            texto_3,
            (
                ANCHO // 2 - texto_3.get_width() // 2,
                ALTO // 2 + 55
            )
        )


    def alternar_pausa(self):
        if self.game_over or self.transicion_iris.activa():
            return

        self.en_pausa = not self.en_pausa

        if self.en_pausa:
            self.interaccion_actual = None
            self._fondo_pausa_cache = None
            self._generar_fondo_pausa_cache()
        else:
            self._fondo_pausa_cache = None

    def dibujar_rect_pixel(
        self,
        pantalla,
        rect,
        color_fondo,
        color_borde=(5, 8, 18),
        grosor_borde=5,
        corte=18,
        sombra=True,
    ):
        puntos_sombra = obtener_puntos_rect_pixel(rect.move(8, 8), corte)
        puntos = obtener_puntos_rect_pixel(rect, corte)

        if sombra:
            pygame.draw.polygon(pantalla, (0, 0, 0), puntos_sombra)

        pygame.draw.polygon(pantalla, color_borde, puntos)

        interior = rect.inflate(-grosor_borde * 2, -grosor_borde * 2)
        corte_interior = max(4, corte - grosor_borde)
        puntos_interior = obtener_puntos_rect_pixel(interior, corte_interior)

        pygame.draw.polygon(pantalla, color_fondo, puntos_interior)

        brillo = interior.inflate(-10, -10)
        if brillo.width > 0 and brillo.height > 0:
            pygame.draw.line(
                pantalla,
                tuple(min(255, c + 35) for c in color_fondo),
                (brillo.x + 16, brillo.y),
                (brillo.right - 16, brillo.y),
                3,
            )

    def dibujar_icono_play(self, pantalla, centro, tamano, color):
        x, y = centro
        puntos = [
            (x - tamano // 3, y - tamano // 2),
            (x - tamano // 3, y + tamano // 2),
            (x + tamano // 2, y),
        ]
        pygame.draw.polygon(pantalla, color, puntos)
        pygame.draw.polygon(pantalla, (5, 8, 18), puntos, 3)

    def dibujar_icono_ajustes(self, pantalla, centro, tamano, color):
        x, y = centro
        radio = tamano // 4

        for angulo in range(0, 360, 45):
            rad = math.radians(angulo)
            x1 = x + int(math.cos(rad) * radio)
            y1 = y + int(math.sin(rad) * radio)
            x2 = x + int(math.cos(rad) * (radio + tamano // 5))
            y2 = y + int(math.sin(rad) * (radio + tamano // 5))
            pygame.draw.line(pantalla, color, (x1, y1), (x2, y2), 8)

        pygame.draw.circle(pantalla, color, (x, y), radio + 6)
        pygame.draw.circle(pantalla, (15, 27, 45), (x, y), radio // 2)

    def dibujar_icono_salir(self, pantalla, centro, tamano, color):
        x, y = centro
        puerta = pygame.Rect(x - tamano // 2, y - tamano // 2, tamano // 2, tamano)
        pygame.draw.rect(pantalla, color, puerta, 5)
        pygame.draw.line(pantalla, color, (x - 2, y), (x + tamano // 2, y), 6)
        pygame.draw.polygon(
            pantalla,
            color,
            [
                (x + tamano // 2, y),
                (x + tamano // 4, y - tamano // 4),
                (x + tamano // 4, y + tamano // 4),
            ],
        )

    def dibujar_boton_png_pausa(self, pantalla, rect, imagen_normal, imagen_click):
        if imagen_normal is None:
            return

        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)

        if hover and imagen_click is not None:
            imagen = imagen_click
        else:
            imagen = imagen_normal

        boton = self.obtener_imagen_escalada_ui(
            imagen,
            rect.width,
            rect.height,
        )
        pantalla.blit(boton, rect.topleft)

    def dibujar_boton_pausa(self, pantalla, rect, texto, color_fondo, icono):
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)

        color = color_fondo
        if hover:
            color = tuple(min(255, c + 25) for c in color_fondo)

        self.dibujar_rect_pixel(
            pantalla,
            rect,
            color,
            color_borde=(5, 8, 18),
            grosor_borde=5,
            corte=20,
            sombra=True,
        )

        icono_x = rect.x + 115
        icono_y = rect.centery
        tamano_icono = 58

        if icono == "play":
            self.dibujar_icono_play(pantalla, (icono_x, icono_y), tamano_icono, (28, 185, 175))
        elif icono == "ajustes":
            self.dibujar_icono_ajustes(pantalla, (icono_x, icono_y), tamano_icono, (15, 42, 78))
        elif icono == "salir":
            self.dibujar_icono_salir(pantalla, (icono_x, icono_y), tamano_icono, (15, 42, 78))

        fuente = cargar_fuente_pixel(42)
        texto_render = fuente.render(texto, False, (255, 255, 255))
        pantalla.blit(
            texto_render,
            (
                rect.centerx - texto_render.get_width() // 2 + 45,
                rect.centery - texto_render.get_height() // 2,
            ),
        )

    def cargar_personaje_menu_pausa(self):
        # Usa el personaje actual que viene de MySQL y que ya fue cargado en self.jugador.
        # No busca personaje1.png; toma el sprite real del personaje seleccionado.
        if self.jugador.frames_caminar:
            return self.jugador.frames_caminar[0].copy()

        sprite_actual = self.jugador.obtener_sprite_actual()

        if sprite_actual is not None:
            return sprite_actual.copy()

        return None

    def dibujar_logo_pausa(self, pantalla):
        x = 275
        y = 165

        if self.logo_menu_pausa_original is not None:
            alto_logo = 170
            proporcion = self.logo_menu_pausa_original.get_width() / self.logo_menu_pausa_original.get_height()
            ancho_logo = int(alto_logo * proporcion)

            logo = self.obtener_imagen_escalada_ui(
                self.logo_menu_pausa_original,
                ancho_logo,
                alto_logo,
                suavizar=True,
            )
            pantalla.blit(logo, (x, y))

        # ============================================================
        # PALABRA EDUCORE CON COLOR INDIVIDUAL POR LETRA
        # Cambia los colores de esta lista para personalizar el logo.
        # Cada color corresponde a una letra de "educore".
        # ============================================================
        texto = "educore"

        colores = [
            "#223051",  # e
            "#223051",  # d
            "#223051",  # u
            "#5B6EA6",  # c
            "#FF7A00",  # o
            "#00B8A9",  # r
            "#00B8A9",  # e
        ]

        fuente_logo = cargar_fuente_orbitron(82)

        tx = x + 160
        ty = y + 58

        x_letra = tx

        espacio_letras = 8

        for letra, color_hex in zip(texto, colores):
            color = pygame.Color(color_hex)

            letra_render = fuente_logo.render(letra, True, color)

            pantalla.blit(letra_render, (x_letra, ty))

            x_letra += letra_render.get_width() + espacio_letras

    def dibujar_linea_punteada(self, pantalla, x1, x2, y, color=(150, 135, 120)):
        for x in range(x1, x2, 18):
            pygame.draw.rect(pantalla, color, (x, y, 10, 4))

    def _obtener_personaje_menu_pausa_escalado(self, config_menu):
        if self.personaje_menu_pausa_original is None:
            return None

        clave = (
            id(self.personaje_menu_pausa_original),
            config_menu["max_ancho"],
            config_menu["max_alto"],
        )
        personaje = self._cache_personaje_menu_pausa.get(clave)

        if personaje is not None:
            return personaje

        rect_visible = self.personaje_menu_pausa_original.get_bounding_rect()

        if rect_visible.width <= 0 or rect_visible.height <= 0:
            return None

        personaje_recortado = pygame.Surface(
            (rect_visible.width, rect_visible.height),
            pygame.SRCALPHA,
        )
        personaje_recortado.blit(
            self.personaje_menu_pausa_original,
            (0, 0),
            rect_visible,
        )

        escala = min(
            config_menu["max_ancho"] / personaje_recortado.get_width(),
            config_menu["max_alto"] / personaje_recortado.get_height(),
        )
        nuevo_ancho = max(1, int(personaje_recortado.get_width() * escala))
        nuevo_alto = max(1, int(personaje_recortado.get_height() * escala))
        personaje = pygame.transform.scale(
            personaje_recortado,
            (nuevo_ancho, nuevo_alto),
        )
        self._cache_personaje_menu_pausa[clave] = personaje
        return personaje

    def dibujar_personaje_pausa_draw(self, pantalla, centro_x, y):
        if self.personaje_menu_pausa_original is None:
            return

        nombre_personaje = self.jugador.nombre_personaje
        config_menu = CONFIG_PERSONAJE_MENU_PAUSA.get(
            nombre_personaje,
            CONFIG_PERSONAJE_MENU_PAUSA["cerdo"],
        )
        personaje = self._obtener_personaje_menu_pausa_escalado(config_menu)

        if personaje is None:
            return

        x = centro_x - personaje.get_width() // 2 + config_menu["mover_x"]
        y_sprite = y + 10 + config_menu["mover_y"]
        sombra_x = centro_x + config_menu["sombra_x"]
        sombra_y = y + config_menu["sombra_y"]
        sombra_ancho = config_menu["sombra_ancho"]
        sombra_alto = config_menu["sombra_alto"]

        pygame.draw.ellipse(
            pantalla,
            (175, 145, 115),
            (sombra_x, sombra_y, sombra_ancho, sombra_alto),
        )
        pantalla.blit(personaje, (x, y_sprite))

    def dibujar_panel_pausa(self, pantalla):
        panel = pygame.Rect(1140, 210, 540, 690)
        self.dibujar_rect_pixel(
            pantalla,
            panel,
            (255, 226, 194),
            color_borde=(5, 8, 18),
            grosor_borde=6,
            corte=26,
            sombra=True,
        )

        self.dibujar_personaje_pausa_draw(pantalla, panel.centerx, panel.y + 80)

        self.dibujar_linea_punteada(pantalla, panel.x + 70, panel.right - 70, panel.y + 365)

        fuente = cargar_fuente_pixel(50)
        texto_vidas = fuente.render("VIDAS:", False, (15, 42, 78))


        pantalla.blit(texto_vidas, (panel.x + 78, panel.y + 415))

        # Aqui controlas los 5 corazones del menu de pausa.
        # separacion_corazones_pausa puede ser positivo, 0 o negativo.
        # Mas grande = mas separados. Mas pequeno/negativo = mas juntos.
        corazones_pausa_x = panel.x + 193
        corazones_pausa_y = panel.y + 392
        tamano_corazon_pausa = 100
        separacion_corazones_pausa = -50

        self.dibujar_corazones(
            pantalla,
            corazones_pausa_x,
            corazones_pausa_y,
            VIDAS_MAXIMAS,
            self.vidas,
            tamano_corazon_pausa,
            separacion_corazones_pausa,
        )

        self.dibujar_linea_punteada(pantalla, panel.x + 70, panel.right - 70, panel.y + 520)

        nivel_icono = pygame.Rect(panel.x + 72, panel.y + 575, 58, 58)
        self.dibujar_rect_pixel(
            pantalla,
            nivel_icono,
            (25, 170, 160),
            color_borde=(5, 8, 18),
            grosor_borde=4,
            corte=8,
            sombra=False,
        )
        numero_nivel = int(self.leccion_actual.get("orden", 1)) if self.leccion_actual else 1
        num = fuente.render(str(numero_nivel), False, (255, 225, 90))
        pantalla.blit(num, (nivel_icono.centerx - num.get_width() // 2, nivel_icono.centery - num.get_height() // 2))

        titulo = fuente.render("NIVEL ACTUAL", False, (15, 42, 78))
        pantalla.blit(titulo, (panel.x + 160, panel.y + 570))

        fuente_chica = cargar_fuente_pixel(27)
        if self.leccion_actual:
            texto_nivel = f"{self.nombre_lenguaje} - Leccion {self.leccion_actual.get('orden', 1)}"
        else:
            texto_nivel = f"{self.nombre_lenguaje} - Leccion 1"

        texto_nivel_render = fuente_chica.render(texto_nivel[:26], False, (15, 42, 78))
        pantalla.blit(texto_nivel_render, (panel.x + 160, panel.y + 620))

    def _generar_fondo_pausa_cache(self):
        if self._fondo_pausa_cache is not None:
            return

        captura = self.superficie_logica.copy()
        pequeno = pygame.transform.smoothscale(
            captura,
            (max(1, ANCHO // 10), max(1, ALTO // 10)),
        )
        blur = pygame.transform.smoothscale(pequeno, (ANCHO, ALTO))

        capa_oscura = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        capa_oscura.fill((0, 0, 0, 135))
        blur.blit(capa_oscura, (0, 0))
        self._fondo_pausa_cache = blur.convert()

    def dibujar_fondo_pausa(self, pantalla):
        self._generar_fondo_pausa_cache()

        if self._fondo_pausa_cache is not None:
            pantalla.blit(self._fondo_pausa_cache, (0, 0))

    def dibujar_menu_pausa(self):
        pantalla = self.superficie_logica

        self.dibujar_fondo_pausa(pantalla)
        self.dibujar_logo_pausa(pantalla)

        # ============================================================
        # CONFIGURACION DE BOTONES PNG DEL MENU DE PAUSA
        # Ahora NO se usa boton_alto fijo.
        # El alto sale automaticamente del PNG para que no se deforme.
        # El rect siempre queda del mismo tamaño que la imagen dibujada.
        # ============================================================
        boton_x = 345
        boton_y = 385
        boton_ancho = 500
        separacion = 35

        self.botones_pausa["reanudar"].configurar_posicion(
            boton_x,
            boton_y,
            ancho_objetivo=boton_ancho,
        )

        self.botones_pausa["ajustes"].configurar_posicion(
            boton_x,
            self.botones_pausa["reanudar"].rect.bottom + separacion,
            ancho_objetivo=boton_ancho,
        )

        self.botones_pausa["salir"].configurar_posicion(
            boton_x,
            self.botones_pausa["ajustes"].rect.bottom + separacion,
            ancho_objetivo=boton_ancho,
        )

        # Se mantiene este diccionario solo por compatibilidad con partes antiguas.
        # Cada rect ya tiene el mismo tamaño que su PNG final.
        self.boton_pausa_rects = {
            nombre: boton.rect
            for nombre, boton in self.botones_pausa.items()
        }
        self.dibujar_panel_pausa(pantalla)
        # Dibujar las imágenes de los botones
        self.botones_pausa["reanudar"].dibujar(pantalla)
        self.botones_pausa["ajustes"].dibujar(pantalla)
        self.botones_pausa["salir"].dibujar(pantalla)

        # Texto centrado dentro de cada botón.
        fuente_botones = cargar_fuente_pixel(42)
        color_texto = (255, 255, 255)

        for nombre, texto in TEXTOS_BOTONES_PAUSA.items():
            boton = self.botones_pausa[nombre]

            texto_renderizado = fuente_botones.render(
                texto,
                False,
                color_texto
            )

            texto_rect = texto_renderizado.get_rect(center=boton.rect.center)
            pantalla.blit(texto_renderizado, texto_rect)

    def manejar_click_pausa(self, posicion):
        if self.botones_pausa["reanudar"].fue_presionado(posicion):
            self.en_pausa = False
            return None

        if self.botones_pausa["ajustes"].fue_presionado(posicion):
            return None

        if self.botones_pausa["salir"].fue_presionado(posicion):
            return "salir"

        return None

    def dibujar(self):
        surface = self.superficie_logica

        # Durante la pausa el mundo está congelado. No se vuelve a componer
        # todo el escenario; se reutiliza la captura desenfocada.
        if self.en_pausa:
            self.dibujar_menu_pausa()
            self.transicion_iris.dibujar(surface)
            pygame.display.flip()
            return

        # Se calcula una sola posición entera de cámara por fotograma.
        # Obstáculos, NPC, plantas y suelo reciben exactamente ese valor,
        # evitando que cada elemento redondee en un instante diferente.
        camara_px = round(self.camara_x)

        # ----------------------------------------------------
        # CAPAS LEJANAS EN MEDIA RESOLUCIÓN
        # ----------------------------------------------------
        fondo = self.superficie_fondo
        fondo.fill(COLOR_CIELO_BASE)
        camara_fondo = camara_px * ESCALA_RENDER_FONDO

        for capa in self.capas:
            capa.dibujar(fondo, camara_fondo)

        # Escalado nearest-neighbor apropiado para pixel art.
        pygame.transform.scale(
            fondo,
            (ANCHO, ALTO),
            surface,
        )

        # ----------------------------------------------------
        # CAPAS CERCANAS A RESOLUCIÓN COMPLETA
        # ----------------------------------------------------
        for capa in getattr(self, "capas_primer_plano", ()):
            capa.dibujar(surface, camara_px)

        if self.capa_suelo is not None:
            self.capa_suelo.dibujar(surface, camara_px)

        pygame.draw.rect(
            surface,
            COLOR_RELLENO_INFERIOR,
            (
                0,
                ALTO - FRANJA_SEGURIDAD_INFERIOR,
                ANCHO,
                FRANJA_SEGURIDAD_INFERIOR,
            ),
        )

        # ----------------------------------------------------
        # OBJETOS: no se dibujan cuando están fuera de pantalla
        # ----------------------------------------------------
        margen = 220

        for obstaculo in self.obstaculos:
            rect = obstaculo.obtener_rect_pantalla(camara_px)
            if rect.right >= -margen and rect.left <= ANCHO + margen:
                obstaculo.dibujar(surface, camara_px)

        objeto_activo = self.obtener_practica_activa()

        if objeto_activo is not None:
            rect = objeto_activo.obtener_rect_pantalla(camara_px)

            if rect.right >= -margen and rect.left <= ANCHO + margen:
                objeto_activo.dibujar(surface, camara_px)

        if self.npc:
            npc_x = round(self.npc.rect.x - camara_px)
            if (
                npc_x + self.npc.rect.width >= -margen
                and npc_x <= ANCHO + margen
            ):
                self.npc.dibujar(surface, camara_px)

        self.jugador.dibujar(surface)
        self.dibujar_panel_jugador()
        self.dibujar_instruccion_interaccion()

        if self.caja_dialogo:
            self.caja_dialogo.dibujar(surface)

        pygame.draw.rect(
            surface,
            COLOR_RELLENO_INFERIOR,
            (
                0,
                ALTO - max(2, FRANJA_SEGURIDAD_INFERIOR // 2),
                ANCHO,
                max(2, FRANJA_SEGURIDAD_INFERIOR // 2),
            ),
        )

        self.dibujar_hitboxes_debug()
        self.dibujar_game_over()
        self.dibujar_fps()

        if self.practica:
            self.practica.dibujar(surface)

        if hasattr(self, "practica_codigo") and self.practica_codigo:
            self.practica_codigo.dibujar(surface)

        self.transicion_iris.dibujar(surface)
        pygame.display.flip()

    def _manejar_evento_practica(self, evento):
        practica_visible = self.obtener_practica_visible()

        if practica_visible is None:
            return False

        estaba_visible = practica_visible.visible
        practica_visible.manejar_evento(evento)

        # Cada fallo descuenta una vida inmediatamente, aunque el formulario
        # siga abierto para mostrar el botón REINTENTAR.
        if practica_visible.consumir_intento_incorrecto():
            self.restar_vida_por_respuesta_incorrecta()

            if self.game_over:
                practica_visible.cerrar()

        # Solo una respuesta correcta completa y elimina la práctica.
        # Cerrar con X o cerrar después de fallar no descuenta otra vida.
        if estaba_visible and not practica_visible.visible:
            if (
                practica_visible.respondido
                and practica_visible.respuesta_final is True
            ):
                self.finalizar_practica_objeto(True)
            else:
                self.objeto_practica_actual = None

        return True

    def _manejar_evento_teclado(self, evento):
        global MOSTRAR_FPS

        if evento.key == pygame.K_ESCAPE:
            if self.game_over:
                return True

            self.alternar_pausa()
            return False

        if self.en_pausa:
            if evento.key == pygame.K_m:
                self.alternar_musica()
            return False

        if (
            evento.key == pygame.K_r
            and not self.game_over
            and not self.transicion_iris.activa()
        ):
            self.reiniciar()

        if evento.key == pygame.K_h:
            self.mostrar_hitboxes = not self.mostrar_hitboxes

        if evento.key == pygame.K_f:
            MOSTRAR_FPS = not MOSTRAR_FPS

        if evento.key == pygame.K_m:
            self.alternar_musica()

        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if not self.transicion_iris.activa():
                # ENTER abre la lección o el ejercicio según el aviso visible.
                self.usar_interaccion_actual()
            return False

        # ESPACIO se conserva únicamente para avanzar el diálogo.
        if evento.key == pygame.K_SPACE and self.en_dialogo:
            dialogo_cerrado = self.caja_dialogo.avanzar()

            if dialogo_cerrado:
                self.cerrar_dialogo_npc()

            return False

        return False

    def _cerrar(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

        self.db.cerrar()
        pygame.quit()
        sys.exit()

    def ejecutar(self):
        # La pantalla de carga puede tardar varios segundos en cerrarse.
        # Reiniciamos el reloj aquí para evitar que el primer dt salte
        # directamente toda la animación de iris.
        self.clock.tick()
        pygame.event.clear()
        self.iniciar_transicion_entrada()

        ejecutando = True

        while ejecutando:
            dt = min(
                self.clock.tick_busy_loop(FPS) / 1000.0,
                0.05,
            )

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                if self._manejar_evento_practica(evento):
                    continue

                if (
                    evento.type == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                    and self.en_pausa
                ):
                    accion_pausa = self.manejar_click_pausa(evento.pos)

                    if accion_pausa == "salir":
                        ejecutando = False

                if (
                    evento.type == pygame.KEYDOWN
                    and self._manejar_evento_teclado(evento)
                ):
                    ejecutando = False

            if not self.en_pausa:
                self.actualizar(dt)
            self.dibujar()

        self._cerrar()
