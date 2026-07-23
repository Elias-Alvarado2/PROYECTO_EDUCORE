# Importa el sistema de alertas personalizado.
from Alertas import Alertas

# Importa la conexión y configuración de la base de datos.
from juego.core.motor import ConexionEduCore, DB_CONFIG


def _mostrar_error_vidas(ventana, mensaje):
    Alertas.mostrar(
        ventana,
        "No se pudieron validar las vidas",
        mensaje,
        "error",
    )


def validar_vidas_disponibles(ventana, sesion):
    """
    Devuelve True cuando se permite abrir el nivel.
    Devuelve False si no hay vidas o no se pudo validar al jugador.
    """
    if not isinstance(sesion, dict):
        _mostrar_error_vidas(ventana, "La sesión actual no es válida.")
        return False

    # Los administradores pueden jugar con vidas infinitas.
    if sesion.get("vidas_infinitas", False):
        return True

    id_jugador = sesion.get("id_jugador")

    if id_jugador is None:
        _mostrar_error_vidas(
            ventana,
            "No se encontró el jugador de la sesión actual.",
        )
        return False

    conexion = None

    try:
        conexion = ConexionEduCore(DB_CONFIG)

        if not conexion.activa:
            _mostrar_error_vidas(
                ventana,
                "No fue posible conectar con la base de datos.",
            )
            return False

        datos_jugador = conexion.obtener_jugador(id_jugador)

        if not isinstance(datos_jugador, dict):
            _mostrar_error_vidas(
                ventana,
                "No se encontraron los datos del jugador.",
            )
            return False

        try:
            vidas = int(datos_jugador.get("vidas", 0))
        except (TypeError, ValueError):
            _mostrar_error_vidas(
                ventana,
                "El valor de vidas guardado no es válido.",
            )
            return False

        if vidas <= 0:
            Alertas.mostrar(
                ventana,
                "Sin vidas",
                "No hay vidas suficientes para realizar la lección.",
                "advertencia",
            )
            return False

        return True
    except Exception as error:
        print(f"[VIDAS] No se pudieron validar las vidas: {error}")
        _mostrar_error_vidas(
            ventana,
            "Ocurrió un error al consultar las vidas del jugador.",
        )
        return False
    finally:
        if conexion is not None:
            conexion.cerrar()
