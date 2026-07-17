use educore_db;

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Variables en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Hola! Una variable funciona como una caja donde podemos guardar información.',
        'Para crear una variable escribimos un nombre, el signo igual y el valor que deseamos guardar.'
    ),

    CONCAT_WS(
        CHAR(10),
        'cantidad = 10'
    ),

    CONCAT_WS(
        CHAR(10),
        'cantidad es el nombre de la variable.',
        'El signo = permite guardar el valor.',
        'El número 10 es un número entero porque no tiene decimales.'
    ),

    1,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 1
  );


-- ---------------------------------------------------------
-- NPC 2: SELECCIÓN MÚLTIPLE
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Tipos de datos en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Muy bien! Las variables pueden guardar diferentes tipos de información.',
        'Los textos se escriben entre comillas.',
        'Los números enteros no tienen decimales.',
        'Los números decimales contienen un punto.'
    ),

    CONCAT_WS(
        CHAR(10),
        'nombre = "Ana"',
        'edad = 15',
        'precio = 10.50'
    ),

    CONCAT_WS(
        CHAR(10),
        'nombre guarda un texto.',
        'edad guarda un número entero.',
        'precio guarda un número decimal.'
    ),

    2,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 2
  );


-- ---------------------------------------------------------
-- NPC 3: COMPLETAR CÓDIGO
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Crear variables en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Excelente! Ahora crearás tu propia variable.',
        'Primero escribimos el nombre de la variable.',
        'Después colocamos el signo igual.',
        'Finalmente escribimos el valor que deseamos guardar.'
    ),

    CONCAT_WS(
        CHAR(10),
        'puntos = 20'
    ),

    CONCAT_WS(
        CHAR(10),
        'puntos es el nombre de la variable.',
        'El signo = guarda el valor.',
        '20 es el número almacenado.'
    ),

    3,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 3
  );


-- =========================================================
-- LECCIÓN 2: CONDICIONALES
-- ÓRDENES 4, 5 Y 6
-- =========================================================


-- ---------------------------------------------------------
-- NPC 1: VERDADERO O FALSO
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Condicional if en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Hola de nuevo! Ahora aprenderemos a tomar decisiones en Python.',
        'La palabra if permite comprobar si una condición es verdadera.',
        'El código dentro de if solamente se ejecuta cuando la condición se cumple.'
    ),

    CONCAT_WS(
        CHAR(10),
        'edad = 20',
        'if edad >= 18:',
        '    print("Mayor de edad")'
    ),

    CONCAT_WS(
        CHAR(10),
        'La condición comprueba si edad es mayor o igual que 18.',
        'Como la edad es 20, la condición es verdadera.',
        'Por eso se muestra el mensaje Mayor de edad.'
    ),

    4,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 4
  );


-- ---------------------------------------------------------
-- NPC 2: SELECCIÓN MÚLTIPLE
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Condicional else en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Muy bien! Una condición no siempre será verdadera.',
        'La palabra else indica qué debe suceder cuando la condición de if es falsa.',
        'else significa de lo contrario.'
    ),

    CONCAT_WS(
        CHAR(10),
        'edad = 12',
        'if edad >= 18:',
        '    print("Mayor de edad")',
        'else:',
        '    print("Menor de edad")'
    ),

    CONCAT_WS(
        CHAR(10),
        'La edad es 12 y no cumple la condición.',
        'Por eso se ejecuta el bloque de else.',
        'El programa muestra el mensaje Menor de edad.'
    ),

    5,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 5
  );


-- ---------------------------------------------------------
-- NPC 3: COMPLETAR CÓDIGO
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Decisiones completas en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Excelente! Ahora reuniremos lo aprendido.',
        'if permite comprobar una condición.',
        'else se ejecuta cuando la condición es falsa.',
        'print() permite mostrar un mensaje.'
    ),

    CONCAT_WS(
        CHAR(10),
        'edad = 18',
        'if edad >= 18:',
        '    print("Mayor de edad")',
        'else:',
        '    print("Menor de edad")'
    ),

    CONCAT_WS(
        CHAR(10),
        'El programa comprueba el valor de edad.',
        'Si la edad es mayor o igual que 18 muestra el primer mensaje.',
        'De lo contrario, muestra el mensaje del bloque else.'
    ),

    6,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 6
  );


-- =========================================================
-- LECCIÓN 3: CICLOS
-- ÓRDENES 7, 8 Y 9
-- =========================================================


-- ---------------------------------------------------------
-- NPC 1: VERDADERO O FALSO
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Ciclo while en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Hola! Ahora aprenderemos a repetir instrucciones.',
        'Un ciclo permite ejecutar una acción varias veces.',
        'El ciclo while se repite mientras su condición sea verdadera.'
    ),

    CONCAT_WS(
        CHAR(10),
        'contador = 0',
        'while contador < 3:',
        '    print(contador)',
        '    contador += 1'
    ),

    CONCAT_WS(
        CHAR(10),
        'El ciclo comienza con contador igual a 0.',
        'Se repite mientras contador sea menor que 3.',
        'El programa mostrará los números 0, 1 y 2.'
    ),

    7,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 7
  );


-- ---------------------------------------------------------
-- NPC 2: SELECCIÓN MÚLTIPLE
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Condiciones dentro de while',

    CONCAT_WS(
        CHAR(10),
        '¡Muy bien! Antes de ejecutar sus instrucciones, while comprueba la condición.',
        'Si la condición es verdadera, el código se ejecuta.',
        'Si es falsa desde el inicio, el código no se ejecuta.'
    ),

    CONCAT_WS(
        CHAR(10),
        'contador = 5',
        'while contador < 3:',
        '    print(contador)'
    ),

    CONCAT_WS(
        CHAR(10),
        'La condición pregunta si 5 es menor que 3.',
        'Esta condición es falsa.',
        'Por eso el código dentro de while no se ejecuta.'
    ),

    8,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 8
  );


-- ---------------------------------------------------------
-- NPC 3: COMPLETAR CÓDIGO
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Actualizar un contador',

    CONCAT_WS(
        CHAR(10),
        '¡Excelente! Dentro del ciclo debemos cambiar el valor del contador.',
        'El operador += permite aumentar el valor de una variable.',
        'contador += 1 aumenta el contador en uno.'
    ),

    CONCAT_WS(
        CHAR(10),
        'contador = 0',
        'while contador < 3:',
        '    print(contador)',
        '    contador += 1'
    ),

    CONCAT_WS(
        CHAR(10),
        'Primero se muestra el valor del contador.',
        'Después el contador aumenta uno.',
        'Cuando contador llega a 3, la condición es falsa y el ciclo termina.'
    ),

    9,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 9
  );


-- =========================================================
-- LECCIÓN 4: FUNCIONES
-- ÓRDENES 10, 11 Y 12
-- =========================================================


-- ---------------------------------------------------------
-- NPC 1: VERDADERO O FALSO
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Funciones en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Hola! Una función es un grupo de instrucciones que realiza una tarea.',
        'Las funciones permiten organizar y reutilizar el código.',
        'Para crear una función utilizamos la palabra def.'
    ),

    CONCAT_WS(
        CHAR(10),
        'def saludar():',
        '    print("Hola")'
    ),

    CONCAT_WS(
        CHAR(10),
        'def indica que estamos creando una función.',
        'saludar es el nombre de la función.',
        'Las instrucciones de la función deben tener sangría.'
    ),

    10,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 10
  );


-- ---------------------------------------------------------
-- NPC 2: SELECCIÓN MÚLTIPLE
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Ejecutar funciones en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Muy bien! Crear una función no hace que se ejecute inmediatamente.',
        'Para ejecutar una función escribimos su nombre seguido de paréntesis.',
        'A esto se le llama llamar a la función.'
    ),

    CONCAT_WS(
        CHAR(10),
        'def saludar():',
        '    print("Hola")',
        '',
        'saludar()'
    ),

    CONCAT_WS(
        CHAR(10),
        'La función se crea utilizando def.',
        'La instrucción saludar() ejecuta la función.',
        'Al ejecutarse se muestra el mensaje Hola.'
    ),

    11,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 11
  );


-- ---------------------------------------------------------
-- NPC 3: COMPLETAR CÓDIGO
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Crear y ejecutar una función',

    CONCAT_WS(
        CHAR(10),
        '¡Excelente! Para trabajar con una función seguimos dos pasos.',
        'Primero utilizamos def para crearla.',
        'Después escribimos su nombre seguido de paréntesis para ejecutarla.',
        'Dentro de la función podemos utilizar print() para mostrar un mensaje.'
    ),

    CONCAT_WS(
        CHAR(10),
        'def saludar():',
        '    print("Hola")',
        '',
        'saludar()'
    ),

    CONCAT_WS(
        CHAR(10),
        'def saludar() crea la función.',
        'print("Hola") muestra el mensaje.',
        'saludar() ejecuta la función.'
    ),

    12,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 12
  );


-- =========================================================
-- LECCIÓN 5: LISTAS
-- ÓRDENES 13, 14 Y 15
-- =========================================================


-- ---------------------------------------------------------
-- NPC 1: VERDADERO O FALSO
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Listas en Python',

    CONCAT_WS(
        CHAR(10),
        '¡Hola! Una lista permite guardar varios valores dentro de una sola variable.',
        'Los elementos se escriben dentro de corchetes.',
        'Cada elemento se separa utilizando una coma.'
    ),

    CONCAT_WS(
        CHAR(10),
        'frutas = ["manzana", "pera", "uva"]'
    ),

    CONCAT_WS(
        CHAR(10),
        'La variable frutas contiene una lista.',
        'La lista tiene tres elementos.',
        'Los tres elementos son textos porque están escritos entre comillas.'
    ),

    13,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 13
  );


-- ---------------------------------------------------------
-- NPC 2: SELECCIÓN MÚLTIPLE
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Posiciones de una lista',

    CONCAT_WS(
        CHAR(10),
        '¡Muy bien! Cada elemento de una lista tiene una posición.',
        'En Python, la primera posición es 0.',
        'Para obtener un elemento escribimos el nombre de la lista y su posición entre corchetes.'
    ),

    CONCAT_WS(
        CHAR(10),
        'frutas = ["manzana", "pera", "uva"]',
        'print(frutas[0])'
    ),

    CONCAT_WS(
        CHAR(10),
        'frutas[0] obtiene el primer elemento.',
        'El primer elemento de la lista es manzana.',
        'Por eso el programa muestra manzana.'
    ),

    14,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 14
  );


-- ---------------------------------------------------------
-- NPC 3: COMPLETAR CÓDIGO
-- ---------------------------------------------------------

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,

    'Agregar elementos a una lista',

    CONCAT_WS(
        CHAR(10),
        '¡Excelente! Podemos agregar nuevos elementos a una lista.',
        'Para hacerlo utilizamos el método append().',
        'El nuevo elemento se agrega al final de la lista.'
    ),

    CONCAT_WS(
        CHAR(10),
        'frutas = ["manzana", "pera"]',
        'frutas.append("uva")',
        'print(frutas)'
    ),

    CONCAT_WS(
        CHAR(10),
        'append("uva") agrega uva al final de la lista.',
        'Después, print(frutas) muestra todos los elementos.',
        'El resultado contiene manzana, pera y uva.'
    ),

    15,
    10,
    'Activa'

FROM lenguaje AS l
WHERE l.nombre = 'Python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 15
  );
  
  -- ======================================================
  select * from leccion;
  -- Verifica en qué base de datos estás trabajando
SELECT DATABASE();

-- Revisa los lenguajes existentes
SELECT *
FROM lenguaje;

-- Busca específicamente Python y detecta espacios
SELECT
    id_lenguaje,
    nombre,
    LENGTH(nombre) AS longitud,
    HEX(nombre) AS contenido_hexadecimal
FROM lenguaje
WHERE LOWER(TRIM(nombre)) = 'python';

-- =============================================================
INSERT INTO lenguaje (
    nombre,
    descripcion,
    fecha_creacion
)
VALUES (
    'Python',
    'Lenguaje de programación Python',
    CURRENT_TIMESTAMP
);
-- ===============================================================
SELECT *
FROM lenguaje
WHERE LOWER(TRIM(nombre)) = 'python';

INSERT INTO leccion (
    id_lenguaje,
    titulo,
    contenido_teoria,
    codigo_ejemplo,
    contenido_final,
    orden,
    puntos,
    estado
)
SELECT
    l.id_lenguaje,
    'Variables en Python',
    'Una variable funciona como una caja donde guardamos información.',
    'cantidad = 10',
    'El número 10 es un número entero porque no tiene decimales.',
    1,
    10,
    'Activa'
FROM lenguaje AS l
WHERE LOWER(TRIM(l.nombre)) = 'python'
  AND NOT EXISTS (
      SELECT 1
      FROM leccion AS le
      WHERE le.id_lenguaje = l.id_lenguaje
        AND le.orden = 1
  );

SELECT ROW_COUNT() AS filas_insertadas;
select *from leccion;