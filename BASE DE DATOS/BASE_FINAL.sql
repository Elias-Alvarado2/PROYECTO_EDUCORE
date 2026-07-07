CREATE DATABASE educore_db;
USE educore_db;

CREATE TABLE jugador (
    id_jugador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
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
    contrasena VARCHAR(255) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE lenguaje (
    id_lenguaje INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
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

    CONSTRAINT uq_leccion_lenguaje_orden
    UNIQUE (id_lenguaje, orden),

    CONSTRAINT uq_leccion_lenguaje_titulo
    UNIQUE (id_lenguaje, titulo),

    CONSTRAINT fk_leccion_lenguaje
    FOREIGN KEY (id_lenguaje)
    REFERENCES lenguaje(id_lenguaje)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE pregunta (
    id_pregunta INT AUTO_INCREMENT PRIMARY KEY,
    id_leccion INT,
    texto_pregunta VARCHAR(500) NOT NULL,
    puntos INT DEFAULT 0,
    tipo_pregunta VARCHAR(50),

    CONSTRAINT uq_pregunta_leccion_texto
    UNIQUE (id_leccion, texto_pregunta),

    CONSTRAINT fk_pregunta_leccion
    FOREIGN KEY (id_leccion)
    REFERENCES leccion(id_leccion)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE opcion_respuesta (
    id_opcion INT AUTO_INCREMENT PRIMARY KEY,
    id_pregunta INT NOT NULL,
    texto_respuesta VARCHAR(500) NOT NULL,
    es_correcta TINYINT(1) DEFAULT 0,

    CONSTRAINT uq_opcion_pregunta_texto
    UNIQUE (id_pregunta, texto_respuesta),

    CONSTRAINT fk_opcion_pregunta
    FOREIGN KEY (id_pregunta)
    REFERENCES pregunta(id_pregunta)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE prueba (
    id_prueba INT AUTO_INCREMENT PRIMARY KEY,
    id_lenguaje INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    puntos_totales INT DEFAULT 0,
    puntos_minimos INT DEFAULT 0,
    certificado TINYINT(1) DEFAULT 1,

    CONSTRAINT uq_prueba_lenguaje_nombre
    UNIQUE (id_lenguaje, nombre),

    CONSTRAINT fk_prueba_lenguaje
    FOREIGN KEY (id_lenguaje)
    REFERENCES lenguaje(id_lenguaje)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE pregunta_prueba (
    id_pregunta_prueba INT AUTO_INCREMENT PRIMARY KEY,
    id_prueba INT NOT NULL,
    id_pregunta INT NOT NULL,
    puntos_otorgados INT DEFAULT 0,

    CONSTRAINT uq_pregunta_prueba
    UNIQUE (id_prueba, id_pregunta),

    CONSTRAINT fk_pregunta_prueba_prueba
    FOREIGN KEY (id_prueba)
    REFERENCES prueba(id_prueba)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    CONSTRAINT fk_pregunta_prueba_pregunta
    FOREIGN KEY (id_pregunta)
    REFERENCES pregunta(id_pregunta)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE resultado_prueba (
    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    id_jugador INT NOT NULL,
    id_prueba INT NOT NULL,
    puntaje_obtenido INT DEFAULT 0,
    aprobado TINYINT(1) DEFAULT 0,
    intento INT DEFAULT 1,
    fecha_completada DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_resultado_jugador_prueba_intento
    UNIQUE (id_jugador, id_prueba, intento),

    CONSTRAINT fk_resultado_jugador
    FOREIGN KEY (id_jugador)
    REFERENCES jugador(id_jugador)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    CONSTRAINT fk_resultado_prueba
    FOREIGN KEY (id_prueba)
    REFERENCES prueba(id_prueba)
    ON DELETE CASCADE
    ON UPDATE CASCADE
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

    CONSTRAINT uq_progreso_jugador_lenguaje
    UNIQUE (id_jugador, id_lenguaje),

    CONSTRAINT fk_progreso_jugador
    FOREIGN KEY (id_jugador)
    REFERENCES jugador(id_jugador)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    CONSTRAINT fk_progreso_lenguaje
    FOREIGN KEY (id_lenguaje)
    REFERENCES lenguaje(id_lenguaje)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE diploma (
    id_diploma INT AUTO_INCREMENT PRIMARY KEY,
    id_jugador INT NOT NULL,
    id_lenguaje INT NOT NULL,
    fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
    ruta_archivo VARCHAR(255),
    correo_enviado TINYINT(1) DEFAULT 0,
    estado VARCHAR(30) DEFAULT 'Generado',

    CONSTRAINT uq_diploma_jugador_lenguaje
    UNIQUE (id_jugador, id_lenguaje),

    CONSTRAINT fk_diploma_jugador
    FOREIGN KEY (id_jugador)
    REFERENCES jugador(id_jugador)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    CONSTRAINT fk_diploma_lenguaje
    FOREIGN KEY (id_lenguaje)
    REFERENCES lenguaje(id_lenguaje)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE historial (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_jugador INT NOT NULL,
    evento VARCHAR(100) NOT NULL,
    detalle VARCHAR(255),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_historial_jugador
    FOREIGN KEY (id_jugador)
    REFERENCES jugador(id_jugador)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);