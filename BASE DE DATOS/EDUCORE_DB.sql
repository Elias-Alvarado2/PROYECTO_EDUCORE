CREATE DATABASE educore_db;
USE educore_db;

CREATE TABLE jugador (
    id_jugador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    personaje VARCHAR(50),
    vidas INT DEFAULT 5,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE administrador (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE lenguaje (
    id_lenguaje INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE leccion (
    id_leccion INT AUTO_INCREMENT PRIMARY KEY,
    id_lenguaje INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    contenido_teoria TEXT,
    codigo_ejemplo TEXT,
    orden INT NOT NULL,
    puntos INT DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'Activa',
    FOREIGN KEY (id_lenguaje) REFERENCES lenguaje(id_lenguaje)
);

CREATE TABLE pregunta (
    id_pregunta INT AUTO_INCREMENT PRIMARY KEY,
    id_leccion INT,
    texto_pregunta VARCHAR(500) NOT NULL,
    puntos INT DEFAULT 0,
    tipo_pregunta VARCHAR(50),
    FOREIGN KEY (id_leccion) REFERENCES leccion(id_leccion)
);

CREATE TABLE opcion_respuesta (
    id_opcion INT AUTO_INCREMENT PRIMARY KEY,
    id_pregunta INT NOT NULL,
    texto_respuesta VARCHAR(500) NOT NULL,
    es_correcta TINYINT(1) DEFAULT 0,
    FOREIGN KEY (id_pregunta) REFERENCES pregunta(id_pregunta)
);

CREATE TABLE prueba (
    id_prueba INT AUTO_INCREMENT PRIMARY KEY,
    id_lenguaje INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    puntos_totales INT DEFAULT 0,
    puntos_minimos INT DEFAULT 0,
    certificado TINYINT(1) DEFAULT 1,
    FOREIGN KEY (id_lenguaje) REFERENCES lenguaje(id_lenguaje)
);

CREATE TABLE pregunta_prueba (
    id_pregunta_prueba INT AUTO_INCREMENT PRIMARY KEY,
    id_prueba INT NOT NULL,
    id_pregunta INT NOT NULL,
    puntos_otorgados INT DEFAULT 0,
    FOREIGN KEY (id_prueba) REFERENCES prueba(id_prueba),
    FOREIGN KEY (id_pregunta) REFERENCES pregunta(id_pregunta)
);

CREATE TABLE resultado_prueba (
    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    id_jugador INT NOT NULL,
    id_prueba INT NOT NULL,
    puntaje_obtenido INT DEFAULT 0,
    aprobado TINYINT(1) DEFAULT 0,
    intento INT DEFAULT 1,
    fecha_completada DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_jugador) REFERENCES jugador(id_jugador),
    FOREIGN KEY (id_prueba) REFERENCES prueba(id_prueba)
);

CREATE TABLE progreso_jugador (
    id_progreso INT AUTO_INCREMENT PRIMARY KEY,
    id_jugador INT NOT NULL,
    id_lenguaje INT NOT NULL,
    leccion_actual INT DEFAULT 1,
    lecciones_completadas INT DEFAULT 0,
    puntos INT DEFAULT 0,
    prueba_desbloqueada TINYINT(1) DEFAULT 0,
    prueba_completada TINYINT(1) DEFAULT 0,
	porcentaje_avance INT DEFAULT 0,
    ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_jugador) REFERENCES jugador(id_jugador),
    FOREIGN KEY (id_lenguaje) REFERENCES lenguaje(id_lenguaje)
);

CREATE TABLE diploma (
    id_diploma INT AUTO_INCREMENT PRIMARY KEY,
    id_jugador INT NOT NULL,
    id_lenguaje INT NOT NULL,
    fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
    ruta_archivo VARCHAR(255),
    correo_enviado TINYINT(1) DEFAULT 0,
    estado VARCHAR(30) DEFAULT 'Generado',
    FOREIGN KEY (id_jugador) REFERENCES jugador(id_jugador),
    FOREIGN KEY (id_lenguaje) REFERENCES lenguaje(id_lenguaje)
);

CREATE TABLE historial (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_jugador INT NOT NULL,
    evento VARCHAR(100) NOT NULL,
    detalle VARCHAR(255),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_jugador) REFERENCES jugador(id_jugador)
);


INSERT INTO administrador
(nombre, usuario, correo, `contraseña`, estado)
VALUES
('Administrador Principal', 'admin', 'admin@educore.com', '12345', 'Activo');

