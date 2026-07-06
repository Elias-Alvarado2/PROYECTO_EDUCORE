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
                    "Jugador1",
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