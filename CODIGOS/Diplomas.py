"""Generacion y envio reutilizable de diplomas de EduCore."""

from __future__ import annotations

import os
import re
import smtplib
import ssl
import unicodedata
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from PyQt6 import QtCore, QtGui

from ConexionBD import ConexionBD
from CredencialesCorreo import (
    CONTRASENA_APLICACION,
    CORREO_REMITENTE,
    SMTP_PUERTO as SMTP_PUERTO_CONFIG,
    SMTP_REQUIERE_AUTENTICACION as SMTP_AUTH_CONFIG,
    SMTP_SERVIDOR as SMTP_SERVIDOR_CONFIG,
    SMTP_TIMEOUT_SEGUNDOS as SMTP_TIMEOUT_CONFIG,
    SMTP_USAR_SSL as SMTP_SSL_CONFIG,
    SMTP_USAR_TLS as SMTP_TLS_CONFIG,
)


# ============================================================
# CONFIGURACION FACIL DEL DIPLOMA
# ============================================================

PROYECTO_DIR = Path(__file__).resolve().parent.parent

# Cambia estas rutas para utilizar otra plantilla o tipo de letra.
RUTA_PLANTILLA_DIPLOMA = (
    PROYECTO_DIR
    / "assets"
    / "DISEÑOS"
    / "diseño_diploma.png"
)
RUTA_FUENTE_TEXTO = (
    PROYECTO_DIR / "assets" / "FUENTES" / "Orbitron-Medium.ttf"
)
RUTA_FUENTE_NOMBRE = (
    PROYECTO_DIR / "assets" / "FUENTES" / "Orbitron-Bold.ttf"
)
CARPETA_DIPLOMAS = PROYECTO_DIR / "output" / "diplomas"

# Las posiciones usan las coordenadas de la imagen original (1491x1055).
# Cada valor es: (x, y, ancho, alto). Al cambiar la plantilla, puedes mover
# cada texto editando solamente estos rectangulos.
RECTANGULOS_TEXTO = {
    "certifica": (320, 338, 851, 38),
    "nombre": (150, 380, 1191, 82),
    "descripcion": (255, 460, 981, 70),
    "curso": (245, 528, 1001, 66),
    "identificador": (300, 615, 891, 30),
    "correo": (300, 650, 891, 28),
    "fecha": (310, 780, 300, 38),
    "firma": (880, 780, 270, 38),
}

TAMANOS_TEXTO = {
    "certifica": 18,
    "nombre": 48,
    "descripcion": 17,
    "curso": 36,
    "identificador": 14,
    "correo": 13,
    "fecha": 18,
    "firma": 18,
}

COLOR_TEXTO = (27, 51, 85)
COLOR_TEXTO_SECUNDARIO = (78, 87, 99)
TEXTO_FIRMA = "EduCore"

# Puedes agregar otros nombres o cambiar el texto mostrado sin tocar la
# logica. Si un lenguaje no aparece, se usa su nombre con formato titulo.
NOMBRES_CURSOS = {
    "mysql": "MySQL",
    "python": "Python",
    "java": "Java",
    "c#": "C#",
    "csharp": "C#",
}


# ============================================================
# CONFIGURACION DEL CORREO
# ============================================================

# La configuracion principal vive en CredencialesCorreo.py para que pueda
# copiarse junto con el proyecto. Las variables de entorno siguen siendo una
# opcion y, si existen, tienen prioridad sobre el archivo.
SMTP_SERVIDOR = os.getenv(
    "EDUCORE_SMTP_HOST",
    SMTP_SERVIDOR_CONFIG,
).strip()
SMTP_PUERTO = int(os.getenv(
    "EDUCORE_SMTP_PORT",
    str(SMTP_PUERTO_CONFIG),
))
SMTP_USUARIO = os.getenv(
    "EDUCORE_SMTP_USER",
    CORREO_REMITENTE,
).strip()
SMTP_CONTRASENA = os.getenv(
    "EDUCORE_SMTP_PASSWORD",
    CONTRASENA_APLICACION,
).strip()
SMTP_REMITENTE = os.getenv(
    "EDUCORE_SMTP_FROM",
    CORREO_REMITENTE or SMTP_USUARIO,
).strip()
SMTP_USAR_TLS = os.getenv(
    "EDUCORE_SMTP_TLS",
    "1" if SMTP_TLS_CONFIG else "0",
).strip().casefold() not in {"0", "false", "no"}
SMTP_USAR_SSL = os.getenv(
    "EDUCORE_SMTP_SSL",
    "1" if SMTP_SSL_CONFIG else "0",
).strip().casefold() in {"1", "true", "si", "yes"}
SMTP_REQUIERE_AUTENTICACION = os.getenv(
    "EDUCORE_SMTP_AUTH",
    "1" if SMTP_AUTH_CONFIG else "0",
).strip().casefold() not in {"0", "false", "no"}
SMTP_TIMEOUT_SEGUNDOS = int(os.getenv(
    "EDUCORE_SMTP_TIMEOUT",
    str(SMTP_TIMEOUT_CONFIG),
))

ASUNTO_CORREO = "Tu diploma de {lenguaje} - EduCore"
CUERPO_CORREO = (
    "Hola {nombre},\n\n"
    "Felicitaciones por completar la leccion final de {lenguaje}. "
    "Adjuntamos tu diploma oficial de EduCore en formato PDF.\n\n"
    "Diploma: {identificador}\n\n"
    "Atentamente,\nEduCore"
)


class DiplomaNoDisponibleError(ValueError):
    """El jugador todavia no cumple los requisitos del diploma."""


class ConfiguracionCorreoError(RuntimeError):
    """La configuracion SMTP no permite realizar el envio."""


_PATRON_CORREO = re.compile(
    r"^[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?"
    r"(?:\.[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?)+$",
    re.IGNORECASE,
)
_FAMILIAS_FUENTES = {}


def correo_es_valido(correo) -> bool:
    """Valida estructura, longitudes y puntos del correo registrado."""
    correo = str(correo or "").strip()

    if not correo or len(correo) > 254 or correo.count("@") != 1:
        return False

    parte_local, dominio = correo.rsplit("@", 1)

    if (
        not parte_local
        or len(parte_local) > 64
        or parte_local.startswith(".")
        or parte_local.endswith(".")
        or ".." in parte_local
        or ".." in dominio
    ):
        return False

    return bool(_PATRON_CORREO.fullmatch(correo))


def _valor_booleano(valor) -> bool:
    if isinstance(valor, str):
        return valor.strip().casefold() in {
            "1",
            "true",
            "si",
            "yes",
        }

    return bool(valor)


def _normalizar_lenguaje(lenguaje) -> str:
    return str(lenguaje or "").strip().casefold()


def _nombre_curso(lenguaje) -> str:
    lenguaje_normalizado = _normalizar_lenguaje(lenguaje)
    return NOMBRES_CURSOS.get(
        lenguaje_normalizado,
        str(lenguaje or "Curso").strip().title(),
    )


def _nombre_archivo_seguro(texto) -> str:
    normalizado = unicodedata.normalize("NFKD", str(texto or ""))
    normalizado = normalizado.encode("ascii", "ignore").decode("ascii")
    normalizado = re.sub(r"[^a-zA-Z0-9_-]+", "_", normalizado)
    return normalizado.strip("_").lower() or "diploma"


def _registrar_fuente(ruta: Path, respaldo: str) -> str:
    clave = str(ruta.resolve())

    if clave in _FAMILIAS_FUENTES:
        return _FAMILIAS_FUENTES[clave]

    familia = respaldo

    if ruta.is_file():
        identificador = QtGui.QFontDatabase.addApplicationFont(str(ruta))

        if identificador >= 0:
            familias = QtGui.QFontDatabase.applicationFontFamilies(
                identificador
            )

            if familias:
                familia = familias[0]

    _FAMILIAS_FUENTES[clave] = familia
    return familia


def preparar_fuentes_diploma():
    """Registra las fuentes en el hilo de interfaz antes de crear el PDF."""
    return {
        "texto": _registrar_fuente(RUTA_FUENTE_TEXTO, "Arial"),
        "nombre": _registrar_fuente(RUTA_FUENTE_NOMBRE, "Arial"),
    }


def _fuente(familia, tamano, negrita=False):
    fuente = QtGui.QFont(familia)
    fuente.setPixelSize(max(1, int(tamano)))

    if negrita:
        fuente.setWeight(QtGui.QFont.Weight.Bold)

    return fuente


def _dibujar_texto(
    pintor,
    texto,
    nombre_rectangulo,
    familia,
    color,
    *,
    negrita=False,
    tamano_minimo=11,
    multilinea=False,
):
    rectangulo = QtCore.QRectF(*RECTANGULOS_TEXTO[nombre_rectangulo])
    tamano = int(TAMANOS_TEXTO[nombre_rectangulo])
    texto = str(texto or "")

    while tamano > tamano_minimo:
        fuente = _fuente(familia, tamano, negrita=negrita)
        metricas = QtGui.QFontMetricsF(fuente)

        if multilinea or metricas.horizontalAdvance(texto) <= rectangulo.width():
            break

        tamano -= 1

    pintor.setFont(_fuente(familia, tamano, negrita=negrita))
    pintor.setPen(QtGui.QColor(*color))
    banderas = (
        QtCore.Qt.AlignmentFlag.AlignHCenter
        | QtCore.Qt.AlignmentFlag.AlignVCenter
    )

    if multilinea:
        banderas |= QtCore.Qt.TextFlag.TextWordWrap

    pintor.drawText(rectangulo, int(banderas), texto)


def obtener_datos_diploma(id_jugador, lenguaje):
    """Obtiene usuario y progreso usando los metodos compartidos del perfil."""
    id_jugador = int(id_jugador)
    lenguaje_normalizado = _normalizar_lenguaje(lenguaje)

    if not lenguaje_normalizado:
        raise ValueError("No se indico el lenguaje del diploma.")

    base_datos = ConexionBD()
    jugador = base_datos.obtener_datos_perfil(id_jugador)

    if not jugador:
        raise ValueError("No se encontro el jugador vinculado al diploma.")

    if str(jugador.get("estado") or "Activo").strip().casefold() != "activo":
        raise DiplomaNoDisponibleError(
            "El usuario no esta activo y no puede recibir diplomas."
        )

    progreso = None

    for registro in base_datos.obtener_progreso_perfil(id_jugador) or []:
        if _normalizar_lenguaje(registro.get("lenguaje")) == lenguaje_normalizado:
            progreso = dict(registro)
            break

    if not progreso or not _valor_booleano(
        progreso.get("prueba_completada")
    ):
        raise DiplomaNoDisponibleError(
            "Debes completar la leccion final antes de solicitar el diploma."
        )

    correo = str(jugador.get("correo") or "").strip()

    if not correo_es_valido(correo):
        raise ValueError(
            "El correo registrado no es valido. Actualizalo antes de "
            "solicitar el diploma."
        )

    ahora = datetime.now().astimezone()
    identificador = (
        f"EDUCORE-{_nombre_archivo_seguro(lenguaje).upper()}-"
        f"{id_jugador:06d}"
    )

    return {
        "id_jugador": id_jugador,
        "id_lenguaje": int(progreso.get("id_lenguaje") or 0),
        "nombre": str(jugador.get("nombre") or "Jugador").strip(),
        "correo": correo,
        "lenguaje": _nombre_curso(lenguaje),
        "lenguaje_clave": lenguaje_normalizado,
        "fecha": ahora.strftime("%d/%m/%Y"),
        "fecha_iso": ahora.isoformat(),
        "identificador": identificador,
    }


def generar_pdf_diploma(datos, ruta_salida=None) -> Path:
    """Genera un PDF de una pagina usando la plantilla configurada."""
    if not RUTA_PLANTILLA_DIPLOMA.is_file():
        raise FileNotFoundError(
            "No se encontro la plantilla del diploma:\n"
            f"{RUTA_PLANTILLA_DIPLOMA}"
        )

    plantilla = QtGui.QImage(str(RUTA_PLANTILLA_DIPLOMA))

    if plantilla.isNull():
        raise ValueError(
            "La imagen configurada para el diploma no se pudo abrir."
        )

    if ruta_salida is None:
        CARPETA_DIPLOMAS.mkdir(parents=True, exist_ok=True)
        archivo = (
            f"diploma_{_nombre_archivo_seguro(datos['lenguaje_clave'])}_"
            f"{int(datos['id_jugador'])}.pdf"
        )
        ruta_salida = CARPETA_DIPLOMAS / archivo
    else:
        ruta_salida = Path(ruta_salida)
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    familias = preparar_fuentes_diploma()
    escritor = QtGui.QPdfWriter(str(ruta_salida))
    escritor.setResolution(72)
    escritor.setPageSize(
        QtGui.QPageSize(
            QtCore.QSizeF(plantilla.width(), plantilla.height()),
            QtGui.QPageSize.Unit.Point,
            "Diploma EduCore",
        )
    )
    escritor.setPageMargins(
        QtCore.QMarginsF(0, 0, 0, 0),
        QtGui.QPageLayout.Unit.Point,
    )
    escritor.setTitle(f"Diploma de {datos['lenguaje']} - EduCore")
    escritor.setCreator("EduCore")

    pintor = QtGui.QPainter(escritor)

    if not pintor.isActive():
        raise RuntimeError("No se pudo iniciar la escritura del diploma PDF.")

    try:
        pintor.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        pintor.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
        pintor.setRenderHint(
            QtGui.QPainter.RenderHint.SmoothPixmapTransform,
            True,
        )
        pintor.drawImage(
            QtCore.QRectF(
                0,
                0,
                plantilla.width(),
                plantilla.height(),
            ),
            plantilla,
        )

        _dibujar_texto(
            pintor,
            "Se certifica que",
            "certifica",
            familias["texto"],
            COLOR_TEXTO_SECUNDARIO,
        )
        _dibujar_texto(
            pintor,
            datos["nombre"],
            "nombre",
            familias["nombre"],
            COLOR_TEXTO,
            negrita=True,
            tamano_minimo=25,
        )
        _dibujar_texto(
            pintor,
            (
                "ha completado satisfactoriamente el curso, demostrando\n"
                "comprension teorica y practica de"
            ),
            "descripcion",
            familias["texto"],
            COLOR_TEXTO_SECUNDARIO,
            multilinea=True,
        )
        _dibujar_texto(
            pintor,
            datos["lenguaje"],
            "curso",
            familias["nombre"],
            COLOR_TEXTO,
            negrita=True,
        )
        _dibujar_texto(
            pintor,
            datos["identificador"],
            "identificador",
            familias["texto"],
            COLOR_TEXTO_SECUNDARIO,
        )
        _dibujar_texto(
            pintor,
            datos["correo"],
            "correo",
            familias["texto"],
            COLOR_TEXTO_SECUNDARIO,
        )
        _dibujar_texto(
            pintor,
            datos["fecha"],
            "fecha",
            familias["texto"],
            COLOR_TEXTO,
            negrita=True,
        )
        _dibujar_texto(
            pintor,
            TEXTO_FIRMA,
            "firma",
            familias["texto"],
            COLOR_TEXTO,
            negrita=True,
        )
    finally:
        pintor.end()

    return ruta_salida.resolve()


def validar_configuracion_correo():
    if not SMTP_SERVIDOR or not SMTP_REMITENTE:
        raise ConfiguracionCorreoError(
            "Falta configurar el servidor o CORREO_REMITENTE en "
            "CredencialesCorreo.py."
        )

    if not correo_es_valido(SMTP_REMITENTE):
        raise ConfiguracionCorreoError(
            "El CORREO_REMITENTE de CredencialesCorreo.py no es valido."
        )

    if not 1 <= SMTP_PUERTO <= 65535:
        raise ConfiguracionCorreoError(
            "El SMTP_PUERTO debe estar entre 1 y 65535."
        )

    if SMTP_USAR_TLS and SMTP_USAR_SSL:
        raise ConfiguracionCorreoError(
            "Activa SMTP_USAR_TLS o SMTP_USAR_SSL, pero no ambos."
        )

    if SMTP_REQUIERE_AUTENTICACION and (
        not SMTP_USUARIO or not SMTP_CONTRASENA
    ):
        raise ConfiguracionCorreoError(
            "Completa CORREO_REMITENTE y CONTRASENA_APLICACION en "
            "CredencialesCorreo.py. Usa una contrasena de aplicacion."
        )


def enviar_pdf_por_correo(datos, ruta_pdf):
    """Envia el PDF al correo validado que pertenece al jugador."""
    validar_configuracion_correo()
    ruta_pdf = Path(ruta_pdf)

    if not ruta_pdf.is_file():
        raise FileNotFoundError(f"No se encontro el diploma: {ruta_pdf}")

    mensaje = EmailMessage()
    mensaje["Subject"] = ASUNTO_CORREO.format(
        lenguaje=datos["lenguaje"]
    )
    mensaje["From"] = SMTP_REMITENTE
    mensaje["To"] = datos["correo"]
    mensaje.set_content(
        CUERPO_CORREO.format(**datos)
    )
    mensaje.add_attachment(
        ruta_pdf.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=ruta_pdf.name,
    )

    contexto_ssl = ssl.create_default_context()

    if SMTP_USAR_SSL:
        cliente_contexto = smtplib.SMTP_SSL(
            SMTP_SERVIDOR,
            SMTP_PUERTO,
            timeout=SMTP_TIMEOUT_SEGUNDOS,
            context=contexto_ssl,
        )
    else:
        cliente_contexto = smtplib.SMTP(
            SMTP_SERVIDOR,
            SMTP_PUERTO,
            timeout=SMTP_TIMEOUT_SEGUNDOS,
        )

    with cliente_contexto as cliente:
        cliente.ehlo()

        if SMTP_USAR_TLS and not SMTP_USAR_SSL:
            cliente.starttls(context=contexto_ssl)
            cliente.ehlo()

        if SMTP_REQUIERE_AUTENTICACION:
            cliente.login(SMTP_USUARIO, SMTP_CONTRASENA)

        cliente.send_message(mensaje)


def registrar_diploma_en_bd(datos, ruta_pdf, correo_enviado, estado):
    """Registra el resultado si la tabla diploma esta disponible."""
    id_lenguaje = int(datos.get("id_lenguaje") or 0)

    if id_lenguaje <= 0:
        return False

    conexion = None
    cursor = None

    try:
        conexion = ConexionBD().conectar()
        cursor = conexion.cursor()

        try:
            ruta_guardada = str(
                Path(ruta_pdf).resolve().relative_to(PROYECTO_DIR.resolve())
            )
        except ValueError:
            ruta_guardada = str(Path(ruta_pdf).resolve())

        cursor.execute(
            """
            INSERT INTO diploma (
                id_jugador,
                id_lenguaje,
                fecha_emision,
                ruta_archivo,
                correo_enviado,
                estado
            )
            VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                fecha_emision = CURRENT_TIMESTAMP,
                ruta_archivo = VALUES(ruta_archivo),
                correo_enviado = VALUES(correo_enviado),
                estado = VALUES(estado);
            """,
            (
                int(datos["id_jugador"]),
                id_lenguaje,
                ruta_guardada,
                1 if correo_enviado else 0,
                str(estado)[:30],
            ),
        )
        conexion.commit()
        return True
    except Exception as error:
        if conexion is not None:
            try:
                conexion.rollback()
            except Exception:
                pass

        print("[DIPLOMA] No se pudo registrar en la base de datos:", error)
        return False
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass

        if conexion is not None:
            try:
                conexion.close()
            except Exception:
                pass


def generar_y_enviar_diploma(id_jugador, lenguaje):
    """Revalida el progreso, genera el PDF, lo envia y registra el resultado."""
    datos = obtener_datos_diploma(id_jugador, lenguaje)
    validar_configuracion_correo()
    ruta_pdf = generar_pdf_diploma(datos)

    try:
        enviar_pdf_por_correo(datos, ruta_pdf)
    except Exception:
        registrar_diploma_en_bd(
            datos,
            ruta_pdf,
            correo_enviado=False,
            estado="Error de envio",
        )
        raise

    registrado = registrar_diploma_en_bd(
        datos,
        ruta_pdf,
        correo_enviado=True,
        estado="Enviado",
    )

    return {
        "nombre": datos["nombre"],
        "correo": datos["correo"],
        "lenguaje": datos["lenguaje"],
        "identificador": datos["identificador"],
        "ruta_pdf": str(ruta_pdf),
        "registrado_en_bd": registrado,
    }


class SenalesEnvioDiploma(QtCore.QObject):
    terminado = QtCore.pyqtSignal(object)
    error = QtCore.pyqtSignal(str)


class TareaEnvioDiploma(QtCore.QRunnable):
    """Genera y envia el diploma fuera del hilo de la interfaz."""

    def __init__(self, id_jugador, lenguaje):
        super().__init__()
        self.id_jugador = int(id_jugador)
        self.lenguaje = str(lenguaje)
        self.senales = SenalesEnvioDiploma()
        self.setAutoDelete(True)

    @QtCore.pyqtSlot()
    def run(self):
        try:
            resultado = generar_y_enviar_diploma(
                self.id_jugador,
                self.lenguaje,
            )
            self.senales.terminado.emit(resultado)
        except Exception as error:
            self.senales.error.emit(str(error))


__all__ = [
    "CARPETA_DIPLOMAS",
    "NOMBRES_CURSOS",
    "RECTANGULOS_TEXTO",
    "RUTA_FUENTE_NOMBRE",
    "RUTA_FUENTE_TEXTO",
    "RUTA_PLANTILLA_DIPLOMA",
    "TAMANOS_TEXTO",
    "TareaEnvioDiploma",
    "correo_es_valido",
    "generar_pdf_diploma",
    "generar_y_enviar_diploma",
    "obtener_datos_diploma",
    "preparar_fuentes_diploma",
]
