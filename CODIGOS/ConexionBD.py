import mysql.connector
from mysql.connector import Error


class ConexionBD:
    def __init__(self):
        self.host = "localhost"
        self.usuario = "root"
        self.password = "123456789"  # Cambia esto por tu contraseña de MySQL
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
                    AND `contraseña` = %s
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
                (nombre, correo, `contraseña`, personaje, vidas, estado)
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

