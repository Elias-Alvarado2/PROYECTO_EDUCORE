select *from leccion;
select *from jugador;
update jugador set vidas=5 where id_jugador=2;
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
VALUES (''Ana'', 15);',
    8,
    10,
    CURRENT_TIMESTAMP,
    'Activa'
);







