from __future__ import annotations

from typing import Any


class GestorResultadoPrueba:
    """Gestiona el resultado de una prueba final usando la conexión del motor."""

    def __init__(self, conexion_db: Any) -> None:
        self.db = conexion_db
        self.resultado_registrado = False

    @staticmethod
    def es_prueba_final(juego: Any) -> bool:
        """Acepta ES_PRUEBA_FINAL=True o NIVEL_ACTUAL=6."""
        if bool(getattr(juego, "ES_PRUEBA_FINAL", False)):
            return True

        try:
            return int(getattr(juego, "NIVEL_ACTUAL", 0) or 0) == 6
        except (TypeError, ValueError):
            return False

    def obtener_prueba(self, id_lenguaje: int):
        """Obtiene la prueba registrada para el lenguaje actual."""
        if id_lenguaje is None:
            return None

        return self.db.seleccionar_uno(
            """
            SELECT id_prueba, id_lenguaje
            FROM prueba
            WHERE id_lenguaje = %s
            ORDER BY id_prueba ASC
            LIMIT 1
            """,
            (id_lenguaje,),
        )

    def obtener_puntaje_total(self, id_lenguaje: int) -> int:
        """Suma leccion.puntos de todas las lecciones activas del lenguaje."""
        if id_lenguaje is None:
            return 0

        fila = self.db.seleccionar_uno(
            """
            SELECT COALESCE(
                SUM(COALESCE(puntos, 0)),
                0
            ) AS puntaje_total
            FROM leccion
            WHERE id_lenguaje = %s
              AND estado = 'Activa'
            """,
            (id_lenguaje,),
        )

        if not fila:
            return 0

        return int(fila.get("puntaje_total") or 0)

    def guardar(
        self,
        id_jugador: int,
        id_lenguaje: int,
        id_prueba: int,
        puntaje_obtenido: int,
    ) -> bool:
        """
        Inserta o actualiza resultado_prueba.

        La tabla resultado_prueba no posee una columna ``puntaje``. La suma
        de leccion.puntos se guarda únicamente en ``puntaje_obtenido``.
        """
        if (
            id_jugador is None
            or id_lenguaje is None
            or id_prueba is None
        ):
            return False

        if not self.db.asegurar_progreso(id_jugador, id_lenguaje):
            return False

        cursor = self.db.obtener_cursor()

        if cursor is None:
            return False

        try:
            cursor.execute(
                """
                SELECT id_resultado
                FROM resultado_prueba
                WHERE id_jugador = %s
                  AND id_prueba = %s
                ORDER BY id_resultado DESC
                LIMIT 1
                """,
                (id_jugador, id_prueba),
            )
            existente = cursor.fetchone()

            if existente:
                cursor.execute(
                    """
                    UPDATE resultado_prueba
                    SET puntaje_obtenido = %s,
                        aprobado = 1,
                        intento = NULL,
                        fecha_completada = CURRENT_DATE()
                    WHERE id_resultado = %s
                    """,
                    (
                        puntaje_obtenido,
                        existente["id_resultado"],
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO resultado_prueba (
                        id_jugador,
                        id_prueba,
                        puntaje_obtenido,
                        aprobado,
                        intento,
                        fecha_completada
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        1,
                        NULL,
                        CURRENT_DATE()
                    )
                    """,
                    (
                        id_jugador,
                        id_prueba,
                        puntaje_obtenido,
                    ),
                )

            cursor.execute(
                """
                UPDATE progreso_jugador
                SET prueba_desbloqueada = 1,
                    prueba_completada = 1,
                    porcentaje_avance = 100,
                    ultima_actualizacion = CURRENT_TIMESTAMP
                WHERE id_jugador = %s
                  AND id_lenguaje = %s
                """,
                (id_jugador, id_lenguaje),
            )

            # Evita duplicar el historial si el jugador abre nuevamente
            # una prueba final que ya había terminado.
            if not existente:
                cursor.execute(
                    """
                    INSERT INTO historial (
                        id_jugador,
                        evento,
                        detalle
                    )
                    VALUES (
                        %s,
                        'Prueba final completada',
                        %s
                    )
                    """,
                    (
                        id_jugador,
                        (
                            "Aprobo la prueba final con "
                            f"{puntaje_obtenido} puntos."
                        ),
                    ),
                )

            self.db.conexion.commit()
            return True

        except Exception as error:
            rollback = getattr(self.db, "_rollback_seguro", None)
            if callable(rollback):
                rollback()

            registrar_error = getattr(self.db, "_registrar_error", None)
            if callable(registrar_error):
                registrar_error(
                    "Error al guardar resultado de prueba",
                    error,
                )
            else:
                print(
                    "[RESULTADO PRUEBA] Error al guardar:",
                    error,
                )

            return False
        finally:
            cursor.close()

    def registrar_desde_juego(self, juego: Any) -> bool:
        """Registra el resultado cuando se abre el cartel final."""
        if self.resultado_registrado:
            return True

        if not self.es_prueba_final(juego):
            return False

        if bool(getattr(juego, "es_administrador", False)):
            print(
                "[RESULTADO PRUEBA] El administrador no genera "
                "resultados de jugador."
            )
            return False

        if not bool(getattr(self.db, "activa", False)):
            print(
                "[RESULTADO PRUEBA] No hay conexión activa con MySQL."
            )
            return False

        id_jugador = getattr(juego, "id_jugador", None)
        id_lenguaje = getattr(juego, "id_lenguaje", None)

        if id_jugador is None or id_lenguaje is None:
            print(
                "[RESULTADO PRUEBA] Faltan el jugador o el lenguaje."
            )
            return False

        prueba = self.obtener_prueba(id_lenguaje)

        if not prueba:
            nombre_lenguaje = getattr(
                juego,
                "nombre_lenguaje",
                "el lenguaje actual",
            )
            print(
                "[RESULTADO PRUEBA] No existe una prueba registrada "
                f"para {nombre_lenguaje}."
            )
            return False

        id_prueba = prueba.get("id_prueba")
        puntaje_obtenido = self.obtener_puntaje_total(id_lenguaje)

        guardado = self.guardar(
            id_jugador=id_jugador,
            id_lenguaje=id_lenguaje,
            id_prueba=id_prueba,
            puntaje_obtenido=puntaje_obtenido,
        )

        if not guardado:
            print(
                "[RESULTADO PRUEBA] No se pudo guardar el resultado."
            )
            return False

        self.resultado_registrado = True
        print(
            "[RESULTADO PRUEBA] Resultado guardado:",
            {
                "id_jugador": id_jugador,
                "id_prueba": id_prueba,
                "puntaje_obtenido": puntaje_obtenido,
                "aprobado": 1,
                "intento": None,
                "fecha_completada": "CURRENT_DATE()",
            },
        )
        return True