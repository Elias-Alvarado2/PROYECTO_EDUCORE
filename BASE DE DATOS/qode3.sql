DROP DATABASE IF EXISTS qode_db;
CREATE DATABASE IF NOT EXISTS qode_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE sistema_educativo;
CREATE TABLE carreras (
    id_carrera     INT AUTO_INCREMENT PRIMARY KEY,
    nombre         VARCHAR(150) NOT NULL,
    descripcion    TEXT,
    duracion_anios TINYINT UNSIGNED
);
CREATE TABLE usuarios (
    id_usuario    INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    email         VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol           ENUM('admin', 'coordinator', 'student') NOT NULL DEFAULT 'student',
    estado        ENUM('activo', 'inactivo', 'suspendido') NOT NULL DEFAULT 'activo',
    id_carrera    INT  NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuario_carrera
        FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);
CREATE TABLE cursos (
    id_curso   INT AUTO_INCREMENT PRIMARY KEY,
    id_carrera INT NOT NULL,
    nombre     VARCHAR(150) NOT NULL,
    nivel      VARCHAR(50),
    CONSTRAINT fk_curso_carrera
        FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);
CREATE TABLE modulos (
    id_modulo   INT AUTO_INCREMENT PRIMARY KEY,
    id_curso    INT NOT NULL,
    nombre      VARCHAR(150) NOT NULL,
    descripcion TEXT,
    CONSTRAINT fk_modulo_curso
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);
CREATE TABLE materiales (
    id_material       INT AUTO_INCREMENT PRIMARY KEY,
    id_modulo         INT NOT NULL,
    titulo            VARCHAR(200) NOT NULL,
    archivo_pdf       VARCHAR(255),
    version           VARCHAR(20),
    fecha_publicacion DATE,
    pagina_inicio     SMALLINT UNSIGNED,
    pagina_fin        SMALLINT UNSIGNED,
    obligatorio       BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_material_modulo
        FOREIGN KEY (id_modulo) REFERENCES modulos(id_modulo)
);
CREATE TABLE preguntas (
    id_pregunta       INT AUTO_INCREMENT PRIMARY KEY,
    id_material       INT NOT NULL,
    enunciado         TEXT NOT NULL,
    tipo              ENUM(
                        'multiple_unica',
                        'multiple_varias',
                        'vf',
                        'completar_texto',
                        'completar_figura',
                        'ordenar',
                        'emparejar'
                      ) NOT NULL,
    nivel_dificultad  ENUM('bajo', 'medio', 'alto') NOT NULL,
    imagen_url        VARCHAR(255) NULL
                        COMMENT 'Imagen de apoyo o figura principal para completar_figura',
    fuente_verificada BOOLEAN NOT NULL DEFAULT FALSE,
    activa            BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_pregunta_material
        FOREIGN KEY (id_material) REFERENCES materiales(id_material)
);
CREATE TABLE opciones (
    id_opcion      INT AUTO_INCREMENT PRIMARY KEY,
    id_pregunta    INT NOT NULL,
    texto          TEXT NOT NULL,
    es_correcta    BOOLEAN NOT NULL DEFAULT FALSE,
    orden_correcto TINYINT UNSIGNED NULL
                     COMMENT 'Para tipo ordenar: posición correcta (1, 2, 3...)',
    par_id         TINYINT UNSIGNED NULL
                     COMMENT 'Para tipo emparejar: número de par al que pertenece',
    columna        ENUM('A', 'B') NULL
                     COMMENT 'Para tipo emparejar: A = término, B = definición',
    CONSTRAINT fk_opcion_pregunta
        FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta)
);
CREATE TABLE figura_espacios (
    id_espacio         INT AUTO_INCREMENT PRIMARY KEY,
    id_pregunta        INT NOT NULL,
    numero             TINYINT UNSIGNED NOT NULL
                         COMMENT 'Número del espacio en la figura (1, 2, 3...)',
    respuesta_correcta VARCHAR(200) NOT NULL,
    pos_x              SMALLINT UNSIGNED NULL
                         COMMENT 'Coordenada X del espacio sobre la imagen (px)',
    pos_y              SMALLINT UNSIGNED NULL
                         COMMENT 'Coordenada Y del espacio sobre la imagen (px)',
    CONSTRAINT fk_espacio_pregunta
        FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta)
);
CREATE TABLE evaluaciones (
    id_evaluacion    INT AUTO_INCREMENT PRIMARY KEY,
    id_modulo        INT NOT NULL,
    tipo             ENUM('parcial', 'final', 'quiz') NOT NULL,
    duracion_minutos SMALLINT UNSIGNED,
    intentos_maximos TINYINT UNSIGNED NOT NULL DEFAULT 1,
    fecha_creacion   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activa           BOOLEAN  NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_evaluacion_modulo
        FOREIGN KEY (id_modulo) REFERENCES modulos(id_modulo)
);
CREATE TABLE evaluacion_pregunta (
    id_evaluacion INT NOT NULL,
    id_pregunta   INT NOT NULL,
    orden         TINYINT UNSIGNED,
    PRIMARY KEY (id_evaluacion, id_pregunta),
    CONSTRAINT fk_evp_evaluacion
        FOREIGN KEY (id_evaluacion) REFERENCES evaluaciones(id_evaluacion),
    CONSTRAINT fk_evp_pregunta
        FOREIGN KEY (id_pregunta)   REFERENCES preguntas(id_pregunta)
);
CREATE TABLE intentos (
    id_intento    INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario    INT NOT NULL,
    id_evaluacion INT NOT NULL,
    fecha_inicio  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin     DATETIME,
    puntaje       DECIMAL(5,2),
    aprobado      BOOLEAN,
    CONSTRAINT fk_intento_usuario
        FOREIGN KEY (id_usuario)    REFERENCES usuarios(id_usuario),
    CONSTRAINT fk_intento_evaluacion
        FOREIGN KEY (id_evaluacion) REFERENCES evaluaciones(id_evaluacion)
);
CREATE TABLE respuestas_usuario (
    id_respuesta      INT AUTO_INCREMENT PRIMARY KEY,
    id_intento        INT NOT NULL,
    id_pregunta       INT NOT NULL,
    id_opcion_elegida INT  NULL
                        COMMENT 'Para tipos que usan la tabla opciones',
    respuesta_texto   TEXT NULL
                        COMMENT 'Para completar_texto, completar_figura y emparejar',
    numero_espacio    TINYINT UNSIGNED NULL
                        COMMENT 'Para completar_figura: número del espacio respondido',
    orden_dado        TINYINT UNSIGNED NULL
                        COMMENT 'Para ordenar: posición asignada por el estudiante',
    correcta          BOOLEAN,
    CONSTRAINT fk_resp_intento
        FOREIGN KEY (id_intento)         REFERENCES intentos(id_intento),
    CONSTRAINT fk_resp_pregunta
        FOREIGN KEY (id_pregunta)        REFERENCES preguntas(id_pregunta),
    CONSTRAINT fk_resp_opcion
        FOREIGN KEY (id_opcion_elegida)  REFERENCES opciones(id_opcion)
);