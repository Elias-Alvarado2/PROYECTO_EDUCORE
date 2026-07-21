import mysql.connector
from mysql.connector import Error


class ConexionBD:
    def __init__(self):
        self.host = "localhost"
        self.usuario = "root"
        self.password = "123456789"
        self.database = "educore_db"
        self.port = 3306

    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return conexion

        except Error as e:
            raise Exception(f"Error al conectar con la base de datos:\n{e}")

    def validar_admin(self, usuario_ingresado, contrasena_ingresada):
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    id_admin,
                    nombre,
                    usuario,
                    correo,
                    estado
                FROM administrador
                WHERE
                    (usuario = %s OR correo = %s OR nombre = %s)
                    AND contrasena = %s
                    AND estado = 'Activo'
                LIMIT 1;
            """

            cursor.execute(
                consulta,
                (
                    usuario_ingresado,
                    usuario_ingresado,
                    usuario_ingresado,
                    contrasena_ingresada
                )
            )

            return cursor.fetchone()

        except Error as e:
            raise Exception(f"Error al validar el administrador:\n{e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def validar_jugador(self, usuario_ingresado, contrasena_ingresada):
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    id_jugador,
                    nombre,
                    correo,
                    personaje,
                    vidas,
                    estado
                FROM jugador
                WHERE
                    (nombre = %s OR correo = %s)
                    AND contrasena = %s
                    AND estado = 'Activo'
                LIMIT 1;
            """

            cursor.execute(
                consulta,
                (
                    usuario_ingresado,
                    usuario_ingresado,
                    contrasena_ingresada
                )
            )

            jugador = cursor.fetchone()

            if jugador is None:
                return None

            # Inicia el contador cuando las vidas son menores que cinco.
            cursor.execute(
                """
                UPDATE jugador
                SET fecha_recuperacion_vidas = NOW()
                WHERE id_jugador = %s
                  AND vidas < 5
                  AND fecha_recuperacion_vidas IS NULL
                """,
                (jugador["id_jugador"],),
            )

            # Cuando ya transcurrió una hora, restaura todas las vidas.
            cursor.execute(
                """
                UPDATE jugador
                SET vidas = 5,
                    fecha_recuperacion_vidas = NULL
                WHERE id_jugador = %s
                  AND vidas < 5
                  AND fecha_recuperacion_vidas IS NOT NULL
                  AND NOW() >= DATE_ADD(
                      fecha_recuperacion_vidas,
                      INTERVAL 1 HOUR
                  )
                """,
                (jugador["id_jugador"],),
            )

            conexion.commit()

            # Vuelve a leer el registro para devolver las vidas actualizadas.
            cursor.execute(
                consulta,
                (
                    usuario_ingresado,
                    usuario_ingresado,
                    contrasena_ingresada
                )
            )

            return cursor.fetchone()

        except Error as e:
            raise Exception(f"Error al validar el usuario:\n{e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def existe_jugador(self, nombre, correo):
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT id_jugador
                FROM jugador
                WHERE nombre = %s OR correo = %s
                LIMIT 1;
            """

            cursor.execute(consulta, (nombre, correo))
            return cursor.fetchone() is not None

        except Error as e:
            raise Exception(f"Error al verificar el jugador:\n{e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def registrar_jugador(self, nombre, correo, contrasena):
        conexion = None
        cursor = None

        try:
            if self.existe_jugador(nombre, correo):
                return False

            conexion = self.conectar()
            cursor = conexion.cursor()

            consulta = """
                INSERT INTO jugador
                (nombre, correo, contrasena, personaje, vidas, estado)
                VALUES (%s, %s, %s, %s, %s, %s);
            """

            cursor.execute(
                consulta,
                (
                    nombre,
                    correo,
                    contrasena,
                    "pato",
                    5,
                    "Activo"
                )
            )

            conexion.commit()
            return True

        except Error as e:
            raise Exception(f"Error al registrar el jugador:\n{e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def registrar_historial(self, id_jugador, evento, detalle):
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor()

            consulta = """
                INSERT INTO historial
                (id_jugador, evento, detalle)
                VALUES (%s, %s, %s);
            """

            cursor.execute(consulta, (id_jugador, evento, detalle))
            conexion.commit()

        except Error:
            pass

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def obtener_jugadores(self):
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    id_jugador,
                    nombre,
                    correo,
                    contrasena,
                    personaje,
                    vidas,
                    fecha_registro,
                    estado
                FROM jugador
                ORDER BY id_jugador ASC;
            """

            cursor.execute(consulta)
            return cursor.fetchall()

        except Error as e:
            raise Exception(f"Error al obtener los jugadores:\n{e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def eliminar_jugador(self, id_jugador):
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor()

            consulta = """
                DELETE FROM jugador
                WHERE id_jugador = %s;
            """

            cursor.execute(consulta, (id_jugador,))
            conexion.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False

        except Error as e:
            raise Exception(f"Error al eliminar el jugador:\n{e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def buscar_jugador_por_id(self, id_jugador):
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    id_jugador,
                    nombre,
                    correo,
                    contrasena,
                    personaje,
                    vidas,
                    fecha_registro,
                    estado
                FROM jugador
                WHERE id_jugador = %s
                LIMIT 1;
            """

            cursor.execute(consulta, (id_jugador,))
            return cursor.fetchone()

        except Error as e:
            raise Exception(f"Error al buscar el jugador:\n{e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def verificar_recuperacion_vidas(self, id_jugador):
        """
        Restaura las cinco vidas cuando pasó una hora desde que
        comenzó el contador de recuperación.
        """
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor(dictionary=True)

            cursor.execute(
                """
                UPDATE jugador
                SET fecha_recuperacion_vidas = NOW()
                WHERE id_jugador = %s
                  AND vidas < 5
                  AND fecha_recuperacion_vidas IS NULL
                """,
                (id_jugador,),
            )

            cursor.execute(
                """
                UPDATE jugador
                SET vidas = 5,
                    fecha_recuperacion_vidas = NULL
                WHERE id_jugador = %s
                  AND vidas < 5
                  AND fecha_recuperacion_vidas IS NOT NULL
                  AND NOW() >= DATE_ADD(
                      fecha_recuperacion_vidas,
                      INTERVAL 1 HOUR
                  )
                """,
                (id_jugador,),
            )

            conexion.commit()

            cursor.execute(
                """
                SELECT vidas, fecha_recuperacion_vidas
                FROM jugador
                WHERE id_jugador = %s
                LIMIT 1
                """,
                (id_jugador,),
            )

            jugador = cursor.fetchone()

            if jugador is None:
                return None

            return int(jugador.get("vidas") or 0)

        except Error as e:
            raise Exception(
                f"Error al verificar la recuperación de vidas:\n{e}"
            )

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def actualizar_jugador(self, id_jugador, nombre, correo, contrasena, personaje, vidas, estado):
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor()

            consulta = """
                UPDATE jugador
                SET
                    nombre = %s,
                    correo = %s,
                    contrasena = %s,
                    personaje = %s,
                    vidas = %s,
                    estado = %s
                WHERE id_jugador = %s;
            """

            cursor.execute(
                consulta,
                (
                    nombre,
                    correo,
                    contrasena,
                    personaje,
                    vidas,
                    estado,
                    id_jugador
                )
            )

            conexion.commit()
            return cursor.rowcount > 0

        except Error as e:
            raise Exception(f"Error al actualizar el jugador:\n{e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    # ======================================================
    # OBTENER DATOS DEL PERFIL
    # ======================================================

    def obtener_datos_perfil(self, id_jugador):
        """
        Obtiene nombre, personaje y vidas del jugador.
        """

        conexion = None
        cursor = None

        try:
            conexion = self.conectar()

            cursor = conexion.cursor(
                dictionary=True
            )

            consulta = """
                SELECT
                    id_jugador,
                    nombre,
                    correo,
                    personaje,
                    vidas,
                    estado
                FROM jugador
                WHERE id_jugador = %s
                LIMIT 1;
            """

            cursor.execute(
                consulta,
                (id_jugador,)
            )

            return cursor.fetchone()

        except Error as e:
            raise Exception(
                "Error al obtener los datos del perfil:\n"
                f"{e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

    def registrar_nivel_completado(
            self,
            id_jugador,
            id_lenguaje,
            numero_nivel,
    ):
        """
        Guarda el progreso de los cuatro niveles y la prueba final.

        Nivel 1 = 20%
        Nivel 2 = 40%
        Nivel 3 = 60%
        Nivel 4 = 80%
        Prueba final = 100%
        """

        conexion = None
        cursor = None

        try:
            numero_nivel = int(numero_nivel)
            numero_nivel = max(1, min(numero_nivel, 5))

            porcentaje = numero_nivel * 20
            porcentaje = min(porcentaje, 100)

            siguiente_nivel = min(
                numero_nivel + 1,
                5,
            )

            prueba_desbloqueada = (
                1 if numero_nivel >= 4 else 0
            )

            prueba_completada = (
                1 if numero_nivel >= 5 else 0
            )

            conexion = self.conectar()

            cursor = conexion.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT
                    id_progreso,
                    leccion_actual,
                    lecciones_completadas,
                    porcentaje_avance,
                    prueba_desbloqueada,
                    prueba_completada
                FROM progreso_jugador
                WHERE id_jugador = %s
                  AND id_lenguaje = %s
                LIMIT 1
                FOR UPDATE;
                """,
                (
                    id_jugador,
                    id_lenguaje,
                ),
            )

            progreso = cursor.fetchone()

            if progreso is None:
                cursor.execute(
                    """
                    INSERT INTO progreso_jugador (
                        id_jugador,
                        id_lenguaje,
                        leccion_actual,
                        lecciones_completadas,
                        puntos,
                        prueba_desbloqueada,
                        prueba_completada,
                        porcentaje_avance,
                        ultima_actualizacion
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        0,
                        %s,
                        %s,
                        %s,
                        CURRENT_TIMESTAMP
                    );
                    """,
                    (
                        id_jugador,
                        id_lenguaje,
                        siguiente_nivel,
                        numero_nivel,
                        prueba_desbloqueada,
                        prueba_completada,
                        porcentaje,
                    ),
                )

            else:
                cursor.execute(
                    """
                    UPDATE progreso_jugador
                    SET
                        leccion_actual = GREATEST(
                            leccion_actual,
                            %s
                        ),

                        lecciones_completadas = GREATEST(
                            lecciones_completadas,
                            %s
                        ),

                        porcentaje_avance = GREATEST(
                            porcentaje_avance,
                            %s
                        ),

                        prueba_desbloqueada = GREATEST(
                            prueba_desbloqueada,
                            %s
                        ),

                        prueba_completada = GREATEST(
                            prueba_completada,
                            %s
                        ),

                        ultima_actualizacion =
                            CURRENT_TIMESTAMP

                    WHERE id_jugador = %s
                      AND id_lenguaje = %s;
                    """,
                    (
                        siguiente_nivel,
                        numero_nivel,
                        porcentaje,
                        prueba_desbloqueada,
                        prueba_completada,
                        id_jugador,
                        id_lenguaje,
                    ),
                )

            conexion.commit()
            return True

        except Error as error:
            if conexion is not None:
                try:
                    conexion.rollback()
                except Error:
                    pass

            print(
                "[BD] Error al registrar el nivel completado:",
                error,
            )

            return False

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


    # ======================================================
    # OBTENER PROGRESO DEL JUGADOR
    # ======================================================

    def obtener_progreso_perfil(self, id_jugador):
        """
        Obtiene el progreso del jugador en cada lenguaje.

        Utiliza las columnas:
        - leccion_actual
        - lecciones_completadas
        - porcentaje_avance
        - prueba_completada
        """

        conexion = None
        cursor = None

        try:
            conexion = self.conectar()

            cursor = conexion.cursor(
                dictionary=True
            )

            consulta = """
                SELECT
                    l.id_lenguaje,
                    l.nombre AS lenguaje,

                    COALESCE(
                        MAX(pj.leccion_actual),
                        0
                    ) AS leccion_actual,

                    COALESCE(
                        MAX(pj.lecciones_completadas),
                        0
                    ) AS lecciones_completadas,

                    COALESCE(
                        MAX(pj.porcentaje_avance),
                        0
                    ) AS porcentaje_avance,

                    COALESCE(
                        MAX(pj.prueba_completada),
                        0
                    ) AS prueba_completada

                FROM lenguaje AS l

                LEFT JOIN progreso_jugador AS pj
                    ON pj.id_lenguaje = l.id_lenguaje
                    AND pj.id_jugador = %s

                WHERE LOWER(TRIM(l.nombre)) IN (
                    'python',
                    'java',
                    'c#',
                    'csharp',
                    'c sharp',
                    'mysql'
                )

                GROUP BY
                    l.id_lenguaje,
                    l.nombre

                ORDER BY
                    l.id_lenguaje ASC;
            """

            cursor.execute(
                consulta,
                (id_jugador,)
            )

            return cursor.fetchall()

        except Error as e:
            raise Exception(
                "Error al obtener el progreso del jugador:\n"
                f"{e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()


    # ======================================================
    # OBTENER HISTORIAL DEL JUGADOR
    # ======================================================

    def obtener_historial_perfil(self, id_jugador):
        """
        Obtiene las acciones realizadas por el jugador.

        Actualmente historial solamente contiene:
        - id_jugador
        - evento
        - detalle
        - fecha

        Por eso lenguaje se muestra como General
        y acción utiliza el nombre del evento.
        """

        conexion = None
        cursor = None

        try:
            conexion = self.conectar()

            cursor = conexion.cursor(
                dictionary=True
            )

            consulta = """
                SELECT
                    fecha,
                    evento,
                    detalle,
                    'General' AS lenguaje,
                    evento AS accion

                FROM historial

                WHERE id_jugador = %s

                ORDER BY fecha DESC;
            """

            cursor.execute(
                consulta,
                (id_jugador,)
            )

            return cursor.fetchall()

        except Error as e:
            raise Exception(
                "Error al obtener el historial del jugador:\n"
                f"{e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()