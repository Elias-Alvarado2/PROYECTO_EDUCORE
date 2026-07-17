
select *from leccion;
select *from jugador;
update jugador set vidas=100 where id_jugador=8;
INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Introducción a las bases de datos',
    'Una base de datos permite almacenar y organizar información de manera estructurada. En MySQL, la información se guarda dentro de tablas formadas por columnas y filas. En esta lección aprenderás a crear una base de datos y seleccionarla para trabajar.',
    'CREATE DATABASE educore;
USE educore;',
    1,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);
INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4
    ,
    'Creación de una base de datos',
    'MySQL funciona mediante instrucciones SQL. Para crear una base de datos, se utiliza CREATE DATABASE seguido del nombre que tendrá la base de datos. Después de crearla, se utiliza USE seguido de su nombre para seleccionarla y comenzar a trabajar con ella. Cada instrucción debe terminar con un punto y coma (;), el cual indica que la instrucción ha finalizado.',
    'CREATE DATABASE educore;
USE educore;',
    2,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);
INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4
    ,
    'Conclusion',
    'En esta lección aprendiste a crear una base de datos con CREATE DATABASE y a seleccionarla con USE. Estos comandos son el primer paso para organizar la información, ya que antes de crear tablas o guardar datos debemos indicar en qué base de datos trabajaremos. Ahora puedes crear la base de datos de una escuela',
    'CREATE DATABASE emiliani;
USE emiliani;',
    3,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);
INSERT INTO leccion (
	id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Creación de tablas',
    'Una tabla sirve para guardar información de manera organizada. Imagínala como una hoja formada por columnas y filas. Las columnas indican qué tipo de información se guardará, por ejemplo:
    -Nombre \n -Correo \n-Edad
	Cada columna debe tener un nombre y un tipo de dato. Las filas contienen los datos de cada persona o registro.',
    '',
    4,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);
INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Como crear una tabla',
    'Para crear una tabla nueva en MySQL se utiliza la instrucción CREATE TABLE, seguida del nombre de la tabla. Después, entre paréntesis, se escriben los campos que tendrá la tabla junto con su tipo de dato. Cada campo debe estar separado por una coma. Algunos de los tipos de datos mas usados son: 
    INT=enteros \n VARCHAR=texto (para este se deben indicar el maximo de caracteres)\n DECIMAL=numeros con punto decimal \n DATE=fechas',
    'CREATE TABLE estudiantes(
id INT,
nombre VARCHAR(50));',
    5,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Claves primarias',
    'Una clave primaria es un campo que identifica de forma única cada registro de una tabla. No permite valores duplicados ni valores nulos, lo que ayuda a mantener los datos organizados y evita que dos registros tengan el mismo identificador.
Generalmente, la clave primaria se coloca como el primer campo de la tabla y suele tener nombres como id, id_estudiante o id_producto.
Para definir una clave primaria se utiliza PRIMARY KEY. También puede utilizarse AUTO_INCREMENT en campos numéricos para que MySQL genere automáticamente un identificador diferente cada vez que se inserta un nuevo registro.',
    'CREATE TABLE estudiantes (
id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(50)
);',
    6,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);
INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Campos Obligatorios',
    'En MYSQL para indicar que un campo es obligatorio y no puede quedar vacio se usa la restricción NOT NULL',
    'CREATE TABLE estudiantes (
id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(50) NOT NULL
);',
    7,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);
INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Insercion de datos',
    'Para guardar nuevos registros en una tabla se utiliza la instrucción INSERT INTO. Después se escribe el nombre de la tabla y, entre paréntesis, los campos que recibirán información. Luego se utiliza VALUES para indicar los valores que se guardarán, los textos deben estar escritos entre comillas simples, mientras que los numeros se escriben sin comillas.',
    'INSERT INTO estudiantes(nombre, edad)
VALUES (''Ana'', 15);
no es necesario colocar id_estudiante, porque AUTO_INCREMENT genera el valor.',
    8,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);
INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Clausula Select',
    'Para consultar información almacenada se utiliza la instrucción SELECT seguido de los campos que queremos ver separados por comas y por ultimo la palabra FROM para indicar la tabla que queremos ver los campos. Tambien, para seleccionar todos los campos de una tabla puedes usar
    SELECT *FROM seguido del nombre de la tabla.',
    'Supongamos que tenemos la tabla estudiantes con los campos nombre, edad y grado:
SELECT nombre, edad
FROM estudiantes;
SELECT *FROM estudiantes;',
'la primera consulta solo nos muestra los campos "nombre" y "edad", mientras que la segunda nos muestra todos los campos.',
    9,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);
-- =====================================================
-- ORDEN 10: FILTROS CON WHERE
-- =====================================================

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Filtros con WHERE',
    'Cuando una tabla contiene muchos registros, no siempre necesitamos mostrar toda la información. La cláusula WHERE permite mostrar únicamente los registros que cumplen una condición. WHERE se escribe después del nombre de la tabla. Una condición está formada por el nombre de un campo, un operador de comparación y un valor. Los textos deben escribirse entre comillas simples, mientras que los números se escriben sin comillas.',
    'SELECT * FROM estudiantes WHERE edad = 15;',
    'Esta consulta muestra todos los campos de los estudiantes cuya edad sea exactamente 15. Los estudiantes que tengan una edad diferente no aparecerán en el resultado.',
    10,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);


-- =====================================================
-- ORDEN 11: OPERADORES DE COMPARACIÓN
-- =====================================================

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Operadores de comparación',
    'Los operadores de comparación permiten indicar qué condición debe cumplir un registro. El operador = significa igual que, <> significa diferente de, > significa mayor que, < significa menor que, >= significa mayor o igual que y <= significa menor o igual que. La consulta solamente muestra los registros en los que la comparación sea verdadera.',
    'SELECT nombre, edad FROM estudiantes WHERE edad >= 15;',
    'Esta consulta muestra el nombre y la edad de los estudiantes que tengan 15 años o más. El operador >= significa mayor o igual que.',
    11,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);


-- =====================================================
-- ORDEN 12: USO DE AND
-- =====================================================

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Varias condiciones con AND',
    'La palabra AND permite unir dos o más condiciones dentro de WHERE. Para que un registro aparezca en el resultado, todas las condiciones unidas con AND deben cumplirse. AND se escribe entre la primera condición y la siguiente condición.',
    'SELECT * FROM estudiantes WHERE edad >= 15 AND grado = ''Segundo'';',
    'Esta consulta muestra únicamente a los estudiantes que tengan 15 años o más y que también pertenezcan al grado Segundo. Si solamente se cumple una de las condiciones, el estudiante no aparecerá.',
    12,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);


-- =====================================================
-- ORDEN 13: USO DE OR
-- =====================================================

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    fecha_creacion,
    estado
)
VALUES (
    4,
    'Varias opciones con OR',
    'La palabra OR permite unir dos o más condiciones dentro de WHERE. Para que un registro aparezca en el resultado, es suficiente con que se cumpla al menos una de las condiciones. OR se escribe entre una condición y la siguiente condición.',
    'SELECT * FROM estudiantes WHERE grado = ''Primero'' OR grado = ''Segundo'';',
    'Esta consulta muestra a los estudiantes que pertenecen al grado Primero o al grado Segundo. Si un estudiante pertenece a cualquiera de esos dos grados, aparecerá en el resultado.',
    13,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);