# Importa el sistema de alertas personalizado.
from Alertas import Alertas

# Importa la conexión y configuración de la base de datos.
from juego.core.motor import ConexionEduCore, DB_CONFIG


def validar_vidas_disponibles(ventana, sesion):
    """
    Devuelve True cuando se permite abrir el nivel.
    Devuelve False cuando el jugador no tiene vidas.
    """

    # Los administradores pueden jugar con vidas infinitas.
    if sesion.get("vidas_infinitas", False):
        return True

    # Abre la conexión con la base de datos.
    conexion = ConexionEduCore(DB_CONFIG)

    # Obtiene las vidas actuales del jugador.
    datos_jugador = conexion.obtener_jugador(
        sesion["id_jugador"]
    )

    # Cierra la conexión después de consultar.
    conexion.cerrar()

    # Comprueba si las vidas llegaron a cero.
    if int(datos_jugador["vidas"]) <= 0:
        Alertas.mostrar(
            ventana,
            "Sin vidas",
            "No hay vidas suficientes para realizar la lección.",
            "advertencia",
        )

        # No permite abrir el nivel.
        return False

    # Permite abrir el nivel.
    return True