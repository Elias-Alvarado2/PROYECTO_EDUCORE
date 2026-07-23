USE educore_db;

INSERT INTO administrador (nombre, usuario, correo, contrasena, estado)
VALUES ('Admin EduCore', 'admin', 'admin@educore.com', '1234', 'Activo')
ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    correo = VALUES(correo),
    contrasena = VALUES(contrasena),
    estado = 'Activo';

INSERT INTO lenguaje (nombre, descripcion)
VALUES
('Python', 'Lenguaje sencillo para aprender programacion desde cero.'),
('Java', 'Lenguaje orientado a objetos usado en muchas aplicaciones.'),
('C#', 'Lenguaje usado en aplicaciones de escritorio, juegos y sistemas.'),
('MySQL', 'Sistema de base de datos para guardar y consultar informacion.')
ON DUPLICATE KEY UPDATE
    descripcion = VALUES(descripcion);

INSERT INTO jugador (nombre, correo, contrasena, personaje, vidas, estado)
VALUES
('Elias', 'elias@educore.com', '1234', 'jugador', 5, 'Activo'),
('Jugador Gato', 'gato@educore.com', '1234', 'gato', 5, 'Activo')
ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre),
    contrasena = VALUES(contrasena),
    personaje = VALUES(personaje),
    vidas = VALUES(vidas),
    estado = 'Activo';

INSERT INTO leccion (id_lenguaje, titulo, contenido_teoria, codigo_ejemplo, orden, puntos, estado)
VALUES
(
    (SELECT id_lenguaje FROM lenguaje WHERE nombre = 'Python' LIMIT 1),
    'Variables en Python',
    'Una variable sirve para guardar un dato. Ese dato puede ser un numero, un texto o un valor logico. En Python no necesitas escribir el tipo de dato antes del nombre de la variable.',
    'edad = 16\nnombre = "Elias"\nprint(nombre)',
    1,
    10,
    'Activa'
),
(
    (SELECT id_lenguaje FROM lenguaje WHERE nombre = 'Python' LIMIT 1),
    'Condicionales en Python',
    'Una condicional permite que el programa tome decisiones. Si la condicion se cumple, se ejecuta una parte del codigo. Si no se cumple, se puede ejecutar otra parte.',
    'edad = 18\nif edad >= 18:\n    print("Mayor de edad")\nelse:\n    print("Menor de edad")',
    2,
    10,
    'Activa'
),
(
    (SELECT id_lenguaje FROM lenguaje WHERE nombre = 'Python' LIMIT 1),
    'Ciclos en Python',
    'Un ciclo permite repetir instrucciones varias veces. En Python puedes usar for cuando sabes cuantas veces repetir y while cuando depende de una condicion.',
    'for i in range(5):\n    print(i)',
    3,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    puntos = VALUES(puntos),
    estado = 'Activa';

INSERT INTO pregunta (id_leccion, texto_pregunta, puntos, tipo_pregunta)
VALUES
(
    (SELECT le.id_leccion
     FROM leccion le
     JOIN lenguaje l ON l.id_lenguaje = le.id_lenguaje
     WHERE l.nombre = 'Python' AND le.orden = 1
     LIMIT 1),
    'Para que sirve una variable?',
    5,
    'Seleccion multiple'
),
(
    (SELECT le.id_leccion
     FROM leccion le
     JOIN lenguaje l ON l.id_lenguaje = le.id_lenguaje
     WHERE l.nombre = 'Python' AND le.orden = 1
     LIMIT 1),
    'Cual de estas lineas crea una variable en Python?',
    5,
    'Seleccion multiple'
)
ON DUPLICATE KEY UPDATE
    puntos = VALUES(puntos),
    tipo_pregunta = VALUES(tipo_pregunta);

INSERT INTO opcion_respuesta (id_pregunta, texto_respuesta, es_correcta)
VALUES
(
    (SELECT p.id_pregunta
     FROM pregunta p
     JOIN leccion le ON le.id_leccion = p.id_leccion
     JOIN lenguaje l ON l.id_lenguaje = le.id_lenguaje
     WHERE l.nombre = 'Python'
       AND le.orden = 1
       AND p.texto_pregunta = 'Para que sirve una variable?'
     LIMIT 1),
    'Para guardar datos que se pueden usar despues.',
    1
),
(
    (SELECT p.id_pregunta
     FROM pregunta p
     JOIN leccion le ON le.id_leccion = p.id_leccion
     JOIN lenguaje l ON l.id_lenguaje = le.id_lenguaje
     WHERE l.nombre = 'Python'
       AND le.orden = 1
       AND p.texto_pregunta = 'Para que sirve una variable?'
     LIMIT 1),
    'Para borrar todo el programa.',
    0
),
(
    (SELECT p.id_pregunta
     FROM pregunta p
     JOIN leccion le ON le.id_leccion = p.id_leccion
     JOIN lenguaje l ON l.id_lenguaje = le.id_lenguaje
     WHERE l.nombre = 'Python'
       AND le.orden = 1
       AND p.texto_pregunta = 'Cual de estas lineas crea una variable en Python?'
     LIMIT 1),
    'edad = 16',
    1
),
(
    (SELECT p.id_pregunta
     FROM pregunta p
     JOIN leccion le ON le.id_leccion = p.id_leccion
     JOIN lenguaje l ON l.id_lenguaje = le.id_lenguaje
     WHERE l.nombre = 'Python'
       AND le.orden = 1
       AND p.texto_pregunta = 'Cual de estas lineas crea una variable en Python?'
     LIMIT 1),
    'variable edad 16',
    0
)
ON DUPLICATE KEY UPDATE
    es_correcta = VALUES(es_correcta);

INSERT INTO prueba (id_lenguaje, nombre, puntos_totales, puntos_minimos, certificado)
VALUES
(
    (SELECT id_lenguaje FROM lenguaje WHERE nombre = 'Python' LIMIT 1),
    'Prueba final Python',
    30,
    20,
    1
)
ON DUPLICATE KEY UPDATE
    puntos_totales = VALUES(puntos_totales),
    puntos_minimos = VALUES(puntos_minimos),
    certificado = VALUES(certificado);

INSERT INTO pregunta_prueba (id_prueba, id_pregunta, puntos_otorgados)
SELECT pr.id_prueba, p.id_pregunta, p.puntos
FROM prueba pr
JOIN lenguaje l ON l.id_lenguaje = pr.id_lenguaje
JOIN leccion le ON le.id_lenguaje = l.id_lenguaje
JOIN pregunta p ON p.id_leccion = le.id_leccion
WHERE l.nombre = 'Python'
  AND pr.nombre = 'Prueba final Python'
ON DUPLICATE KEY UPDATE
    puntos_otorgados = VALUES(puntos_otorgados);

INSERT INTO progreso_jugador (
    id_jugador,
    id_lenguaje,
    leccion_actual,
    lecciones_completadas,
    puntos,
    prueba_desbloqueada,
    prueba_completada,
    porcentaje_avance
)
SELECT j.id_jugador, l.id_lenguaje, 1, 0, 0, 0, 0, 0
FROM jugador j
JOIN lenguaje l ON l.nombre = 'Python'
WHERE j.correo IN ('elias@educore.com', 'gato@educore.com')
ON DUPLICATE KEY UPDATE
    leccion_actual = VALUES(leccion_actual),
    ultima_actualizacion = CURRENT_TIMESTAMP;

SELECT id_jugador, nombre, correo, personaje, vidas, estado
FROM jugador;

SELECT l.nombre AS lenguaje, le.orden, le.titulo, le.contenido_teoria, le.codigo_ejemplo
FROM leccion le
JOIN lenguaje l ON l.id_lenguaje = le.id_lenguaje
WHERE l.nombre = 'Python'
ORDER BY le.orden;

SELECT j.nombre, l.nombre AS lenguaje, p.leccion_actual, p.lecciones_completadas, p.puntos, p.porcentaje_avance
FROM progreso_jugador p
JOIN jugador j ON j.id_jugador = p.id_jugador
JOIN lenguaje l ON l.id_lenguaje = p.id_lenguaje;

update jugador set vidas=5 where id_jugador=2;
select * from historial;

-- IMPORTANTE PARA INSTALACIONES NUEVAS O BASES EXISTENTES:
-- Después de este archivo, ejecuta CORRECCION_LECCIONES_PROGRESION.sql.
-- Es idempotente y agrega/alinea las lecciones usadas por todos los niveles.
