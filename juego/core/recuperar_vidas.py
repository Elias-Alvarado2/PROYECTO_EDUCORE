from datetime import datetime, timedelta
from ConexionBD import ConexionBD


VIDAS_MAXIMAS = 5
TIEMPO_RECUPERACION = timedelta(hours=1)


def verificar_recuperacion_vidas(id_jugador):
    conexion = None
    cursor = None

    try:
        conexion = ConexionBD.obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT vidas, fecha_recuperacion_vidas
            FROM jugador
            WHERE id_jugador = %s
            """,
            (id_jugador,)
        )

        jugador = cursor.fetchone()

        if jugador is None:
            print("No se encontró al jugador.")
            return 0

        vidas_actuales = jugador["vidas"]
        ultima_recuperacion = jugador["fecha_recuperacion_vidas"]

        if ultima_recuperacion is None:
            ultima_recuperacion = datetime.now()

            cursor.execute(
                """
                UPDATE jugador
                SET fecha_recuperacion_vidas = %s
                WHERE id_jugador = %s
                """,
                (ultima_recuperacion, id_jugador)
            )

            conexion.commit()
            return vidas_actuales

        tiempo_transcurrido = datetime.now() - ultima_recuperacion

        if (
            vidas_actuales < VIDAS_MAXIMAS
            and tiempo_transcurrido >= TIEMPO_RECUPERACION
        ):
            cursor.execute(
                """
                UPDATE jugador
                SET vidas = %s,
                    fecha_recuperacion_vidas = NOW()
                WHERE id_jugador = %s
                """,
                (VIDAS_MAXIMAS, id_jugador)
            )

            conexion.commit()
            vidas_actuales = VIDAS_MAXIMAS

        return vidas_actuales

    except Exception as error:
        print(f"Error al verificar las vidas: {error}")
        return 0

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()