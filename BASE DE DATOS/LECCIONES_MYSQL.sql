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


 delete from leccion where id_leccion=10;
update leccion set estado='Activa' where id_leccion=4;
