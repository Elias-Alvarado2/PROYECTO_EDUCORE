drop database if exists qode_db;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS Qode_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
USE Qode_db ;

-- -----------------------------------------------------
-- Tabla Qode_db.carreras
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.carreras (
  id_carrera INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(150) NOT NULL,
  descripcion TEXT NULL DEFAULT NULL,
  duracion_anios TINYINT UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (id_carrera))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Tabla Qode_db.cursos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.cursos (
  id_curso INT NOT NULL AUTO_INCREMENT,
  id_carrera INT NOT NULL,
  nombre VARCHAR(150) NOT NULL,
  nivel VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (id_curso),
  INDEX fk_curso_carrera (id_carrera ASC) VISIBLE,
  CONSTRAINT fk_curso_carrera
    FOREIGN KEY (id_carrera)
    REFERENCES Qode_db.carreras (id_carrera))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Tabla Qode_db.modulos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.modulos (
  id_modulo INT NOT NULL AUTO_INCREMENT,
  id_curso INT NOT NULL,
  nombre VARCHAR(150) NOT NULL,
  descripcion TEXT NULL DEFAULT NULL,
  PRIMARY KEY (id_modulo),
  INDEX fk_modulo_curso (id_curso ASC) VISIBLE,
  CONSTRAINT fk_modulo_curso
    FOREIGN KEY (id_curso)
    REFERENCES Qode_db.cursos (id_curso))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table Qode_db.evaluaciones
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.evaluaciones (
  id_evaluacion INT NOT NULL AUTO_INCREMENT,
  id_modulo INT NOT NULL,
  tipo ENUM('parcial', 'final', 'quiz') NOT NULL,
  duracion_minutos SMALLINT UNSIGNED NULL DEFAULT NULL,
  intentos_maximos TINYINT UNSIGNED NOT NULL DEFAULT '1',
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  activa TINYINT(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (id_evaluacion),
  INDEX fk_evaluacion_modulo (id_modulo ASC) VISIBLE,
  CONSTRAINT fk_evaluacion_modulo
    FOREIGN KEY (id_modulo)
    REFERENCES Qode_db.modulos (id_modulo))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table Qode_db.materiales
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.materiales (
  id_material INT NOT NULL AUTO_INCREMENT,
  id_modulo INT NOT NULL,
  titulo VARCHAR(200) NOT NULL,
  archivo_pdf VARCHAR(255) NULL DEFAULT NULL,
  version VARCHAR(20) NULL DEFAULT NULL,
  fecha_publicacion DATE NULL DEFAULT NULL,
  pagina_inicio SMALLINT UNSIGNED NULL DEFAULT NULL,
  pagina_fin SMALLINT UNSIGNED NULL DEFAULT NULL,
  obligatorio TINYINT(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (id_material),
  INDEX fk_material_modulo (id_modulo ASC) VISIBLE,
  CONSTRAINT fk_material_modulo
    FOREIGN KEY (id_modulo)
    REFERENCES Qode_db.modulos (id_modulo))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table Qode_db.preguntas
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.preguntas (
  id_pregunta INT NOT NULL AUTO_INCREMENT,
  id_material INT NOT NULL,
  enunciado TEXT NOT NULL,
  tipo ENUM('multiple_unica', 'multiple_varias', 'vf', 'completar_texto', 'completar_figura', 'ordenar', 'emparejar') NOT NULL,
  nivel_dificultad ENUM('bajo', 'medio', 'alto') NOT NULL,
  imagen_url VARCHAR(255) NULL DEFAULT NULL COMMENT 'Imagen de apoyo o figura principal para completar_figura',
  fuente_verificada TINYINT(1) NOT NULL DEFAULT '0',
  activa TINYINT(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (id_pregunta),
  INDEX fk_pregunta_material (id_material ASC) VISIBLE,
  CONSTRAINT fk_pregunta_material
    FOREIGN KEY (id_material)
    REFERENCES Qode_db.materiales (id_material))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table Qode_db.evaluacion_pregunta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.evaluacion_pregunta (
  id_evaluacion INT NOT NULL,
  id_pregunta INT NOT NULL,
  orden TINYINT UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (id_evaluacion, id_pregunta),
  INDEX fk_evp_pregunta (id_pregunta ASC) VISIBLE,
  CONSTRAINT fk_evp_evaluacion
    FOREIGN KEY (id_evaluacion)
    REFERENCES Qode_db.evaluaciones (id_evaluacion),
  CONSTRAINT fk_evp_pregunta
    FOREIGN KEY (id_pregunta)
    REFERENCES Qode_db.preguntas (id_pregunta))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table Qode_db.figura_espacios
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.figura_espacios (
  id_espacio INT NOT NULL AUTO_INCREMENT,
  id_pregunta INT NOT NULL,
  numero TINYINT UNSIGNED NOT NULL COMMENT 'Número del espacio en la figura (1, 2, 3...)',
  respuesta_correcta VARCHAR(200) NOT NULL,
  pos_x SMALLINT UNSIGNED NULL DEFAULT NULL COMMENT 'Coordenada X del espacio sobre la imagen (px)',
  pos_y SMALLINT UNSIGNED NULL DEFAULT NULL COMMENT 'Coordenada Y del espacio sobre la imagen (px)',
  PRIMARY KEY (id_espacio),
  INDEX fk_espacio_pregunta (id_pregunta ASC) VISIBLE,
  CONSTRAINT fk_espacio_pregunta
    FOREIGN KEY (id_pregunta)
    REFERENCES Qode_db.preguntas (id_pregunta))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table Qode_db.usuarios
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.usuarios (
  id_usuario INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  rol ENUM('admin', 'coordinator', 'student') NOT NULL DEFAULT 'student',
  estado ENUM('activo', 'inactivo', 'suspendido') NOT NULL DEFAULT 'activo',
  id_carrera INT NULL DEFAULT NULL,
  fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_usuario),
  UNIQUE INDEX email (email ASC) VISIBLE,
  INDEX fk_usuario_carrera (id_carrera ASC) VISIBLE,
  CONSTRAINT fk_usuario_carrera
    FOREIGN KEY (id_carrera)
    REFERENCES Qode_db.carreras (id_carrera))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Tabla Qode_db.intentos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.intentos (
  id_intento INT NOT NULL AUTO_INCREMENT,
  id_usuario INT NOT NULL,
  id_evaluacion INT NOT NULL,
  fecha_inicio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_fin DATETIME NULL DEFAULT NULL,
  puntaje DECIMAL(5,2) NULL DEFAULT NULL,
  aprobado TINYINT(1) NULL DEFAULT NULL,
  PRIMARY KEY (id_intento),
  INDEX fk_intento_usuario (id_usuario ASC) VISIBLE,
  INDEX fk_intento_evaluacion (id_evaluacion ASC) VISIBLE,
  CONSTRAINT fk_intento_evaluacion
    FOREIGN KEY (id_evaluacion)
    REFERENCES Qode_db.evaluaciones (id_evaluacion),
  CONSTRAINT fk_intento_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Qode_db.usuarios (id_usuario))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Tabla Qode_db.opciones
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.opciones (
  id_opcion INT NOT NULL AUTO_INCREMENT,
  id_pregunta INT NOT NULL,
  texto TEXT NOT NULL,
  es_correcta TINYINT(1) NOT NULL DEFAULT '0',
  orden_correcto TINYINT UNSIGNED NULL DEFAULT NULL COMMENT 'Para tipo ordenar: posición correcta (1, 2, 3...)',
  par_id TINYINT UNSIGNED NULL DEFAULT NULL COMMENT 'Para tipo emparejar: número de par al que pertenece',
  columna ENUM('A', 'B') NULL DEFAULT NULL COMMENT 'Para tipo emparejar: A = término, B = definición',
  PRIMARY KEY (id_opcion),
  INDEX fk_opcion_pregunta (id_pregunta ASC) VISIBLE,
  CONSTRAINT fk_opcion_pregunta
    FOREIGN KEY (id_pregunta)
    REFERENCES Qode_db.preguntas (id_pregunta))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Tabla Qode_db.respuestas_usuario
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Qode_db.respuestas_usuario (
  id_respuesta INT NOT NULL AUTO_INCREMENT,
  id_intento INT NOT NULL,
  id_pregunta INT NOT NULL,
  id_opcion_elegida INT NULL DEFAULT NULL COMMENT 'Para tipos que usan la tabla opciones',
  respuesta_texto TEXT NULL DEFAULT NULL COMMENT 'Para completar_texto, completar_figura y emparejar',
  numero_espacio TINYINT UNSIGNED NULL DEFAULT NULL COMMENT 'Para completar_figura: número del espacio respondido',
  orden_dado TINYINT UNSIGNED NULL DEFAULT NULL COMMENT 'Para ordenar: posición asignada por el estudiante',
  correcta TINYINT(1) NULL DEFAULT NULL,
  PRIMARY KEY (id_respuesta),
  INDEX fk_resp_intento (id_intento ASC) VISIBLE,
  INDEX fk_resp_pregunta (id_pregunta ASC) VISIBLE,
  INDEX fk_resp_opcion (id_opcion_elegida ASC) VISIBLE,
  CONSTRAINT fk_resp_intento
    FOREIGN KEY (id_intento)
    REFERENCES Qode_db.intentos (id_intento),
  CONSTRAINT fk_resp_opcion
    FOREIGN KEY (id_opcion_elegida)
    REFERENCES Qode_db.opciones (id_opcion),
  CONSTRAINT fk_resp_pregunta
    FOREIGN KEY (id_pregunta)
    REFERENCES Qode_db.preguntas (id_pregunta))
ENGINE = InnoDB



DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

Select * from usuarios;