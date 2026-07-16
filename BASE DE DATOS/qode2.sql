USE Qode_db;

-- CARRERA


INSERT INTO carreras (
    nombre,
    descripcion,
    duracion_anios
)
VALUES (
    'Médico y Cirujano',
    'Carrera de Medicina y Cirugía basada en el pensum de formación general y específica.',
    5
);

SET @id_medicina = LAST_INSERT_ID();

-- PRIMER AÑO

INSERT INTO cursos (id_carrera,nombre,nivel)
VALUES
(@id_medicina,'Química','Primero'),
(@id_medicina,'Física','Primero'),
(@id_medicina,'Biología Celular y Molecular','Primero'),
(@id_medicina,'Psicología','Primero'),
(@id_medicina,'Salud Pública I','Primero'),
(@id_medicina,'Propedéutica Médica','Primero'),
(@id_medicina,'Fundamentos de la Investigación Científica','Primero'),
(@id_medicina,'Bioestadística','Primero');

-- SEGUNDO AÑO

INSERT INTO cursos (id_carrera,nombre,nivel)
VALUES
(@id_medicina,'Anatomía Humana','Segundo'),
(@id_medicina,'Histología y Embriología','Segundo'),
(@id_medicina,'Bioquímica','Segundo'),
(@id_medicina,'Fisiología','Segundo'),
(@id_medicina,'Salud Pública II','Segundo'),
(@id_medicina,'Semiología Médica I','Segundo');

-- TERCER AÑO

INSERT INTO cursos (id_carrera,nombre,nivel)
VALUES
(@id_medicina,'Patología','Tercero'),
(@id_medicina,'Farmacología Clínica','Tercero'),
(@id_medicina,'Inmunología y Microbiología Médica','Tercero'),
(@id_medicina,'Salud Pública III','Tercero'),
(@id_medicina,'Semiología Médica II','Tercero'),
(@id_medicina,'Métodos de Investigación en Medicina','Tercero');

-- CUARTO AÑO

INSERT INTO cursos (id_carrera,nombre,nivel)
VALUES
(@id_medicina,'Medicina Interna','Cuarto'),
(@id_medicina,'Cirugía General','Cuarto'),
(@id_medicina,'Medicina Familiar','Cuarto');

-- QUINTO AÑO

INSERT INTO cursos (id_carrera,nombre,nivel)
VALUES
(@id_medicina,'Práctica Electiva de Especialidades','Quinto'),
(@id_medicina,'Pediatría','Quinto'),
(@id_medicina,'Ginecología y Obstetricia','Quinto'),
(@id_medicina,'Traumatología y Ortopedia','Quinto'),
(@id_medicina,'Salud Mental y Psiquiatría','Quinto');


-- CURSOS ROSADOS = 5 MÓDULOS

INSERT INTO modulos (id_curso,nombre)
SELECT id_curso,'Módulo 1'
FROM cursos
WHERE nombre IN (
'Química',
'Física',
'Biología Celular y Molecular',
'Psicología',
'Anatomía Humana',
'Histología y Embriología',
'Bioquímica',
'Fisiología',
'Patología',
'Farmacología Clínica',
'Inmunología y Microbiología Médica'
);

INSERT INTO modulos (id_curso,nombre)
SELECT id_curso,'Módulo 2'
FROM cursos
WHERE nombre IN (
'Química',
'Física',
'Biología Celular y Molecular',
'Psicología',
'Anatomía Humana',
'Histología y Embriología',
'Bioquímica',
'Fisiología',
'Patología',
'Farmacología Clínica',
'Inmunología y Microbiología Médica'
);

INSERT INTO modulos (id_curso,nombre)
SELECT id_curso,'Módulo 3'
FROM cursos
WHERE nombre IN (
'Química',
'Física',
'Biología Celular y Molecular',
'Psicología',
'Anatomía Humana',
'Histología y Embriología',
'Bioquímica',
'Fisiología',
'Patología',
'Farmacología Clínica',
'Inmunología y Microbiología Médica'
);

INSERT INTO modulos (id_curso,nombre)
SELECT id_curso,'Módulo 4'
FROM cursos
WHERE nombre IN (
'Química',
'Física',
'Biología Celular y Molecular',
'Psicología',
'Anatomía Humana',
'Histología y Embriología',
'Bioquímica',
'Fisiología',
'Patología',
'Farmacología Clínica',
'Inmunología y Microbiología Médica'
);

INSERT INTO modulos (id_curso,nombre)
SELECT id_curso,'Módulo 5'
FROM cursos
WHERE nombre IN (
'Química',
'Física',
'Biología Celular y Molecular',
'Psicología',
'Anatomía Humana',
'Histología y Embriología',
'Bioquímica',
'Fisiología',
'Patología',
'Farmacología Clínica',
'Inmunología y Microbiología Médica'
);


INSERT INTO modulos (id_curso,nombre)
SELECT id_curso,'Módulo 1'
FROM cursos
WHERE nombre NOT IN (
'Química',
'Física',
'Biología Celular y Molecular',
'Psicología',
'Anatomía Humana',
'Histología y Embriología',
'Bioquímica',
'Fisiología',
'Patología',
'Farmacología Clínica',
'Inmunología y Microbiología Médica'
);

INSERT INTO modulos (id_curso,nombre)
SELECT id_curso,'Módulo 2'
FROM cursos
WHERE nombre NOT IN (
'Química',
'Física',
'Biología Celular y Molecular',
'Psicología',
'Anatomía Humana',
'Histología y Embriología',
'Bioquímica',
'Fisiología',
'Patología',
'Farmacología Clínica',
'Inmunología y Microbiología Médica'
);

INSERT INTO modulos (id_curso,nombre)
SELECT id_curso,'Módulo 3'
FROM cursos
WHERE nombre NOT IN (
'Química',
'Física',
'Biología Celular y Molecular',
'Psicología',
'Anatomía Humana',
'Histología y Embriología',
'Bioquímica',
'Fisiología',
'Patología',
'Farmacología Clínica',
'Inmunología y Microbiología Médica'
);

INSERT INTO modulos (id_curso,nombre)
SELECT id_curso,'Módulo 4'
FROM cursos
WHERE nombre NOT IN (
'Química',
'Física',
'Biología Celular y Molecular',
'Psicología',
'Anatomía Humana',
'Histología y Embriología',
'Bioquímica',
'Fisiología',
'Patología',
'Farmacología Clínica',
'Inmunología y Microbiología Médica'
);
