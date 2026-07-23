USE educore_db;


-- Asegura que el lenguaje Python exista.
INSERT INTO lenguaje (nombre, descripcion, fecha_creacion)
SELECT 'Python', 'Lenguaje de programación Python', CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM lenguaje
    WHERE LOWER(TRIM(nombre)) = 'python'
);

SET @id_python := (
    SELECT id_lenguaje
    FROM lenguaje
    WHERE LOWER(TRIM(nombre)) = 'python'
    ORDER BY id_lenguaje
    LIMIT 1
);

-- Muestra si el lenguaje Python fue localizado correctamente.
SELECT IF(
    @id_python IS NULL,
    'ERROR: No se encontró el lenguaje Python.',
    CONCAT('Python localizado con id_lenguaje = ', @id_python)
) AS resultado_preparacion;


-- =============================================================
-- NIVEL 1 - NPC 1 - VERDADERO O FALSO
-- Orden 1
-- =============================================================
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
VALUES (
    @id_python,
    'Variables en Python',
    CONCAT_WS(CHAR(10),
            '¡Hola! Una variable permite guardar un dato para utilizarlo después.',
            'Para crearla escribimos un nombre, el signo igual (=) y el valor que deseamos guardar.',
            'Los números que no tienen decimales se llaman números enteros.'
        ),
    CONCAT_WS(CHAR(10),
            'cantidad = 10'
        ),
    CONCAT_WS(CHAR(10),
            'cantidad es el nombre de la variable.',
            'El signo = asigna el valor 10 a cantidad.',
            'Como 10 no tiene decimales, es un número entero.'
        ),
    1,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 1 - NPC 2 - SELECCIÓN MÚLTIPLE
-- Orden 2
-- =============================================================
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
VALUES (
    @id_python,
    'Tipos de datos en Python',
    CONCAT_WS(CHAR(10),
            'Las variables también pueden guardar textos.',
            'En Python, un texto se escribe entre comillas simples o dobles.',
            'Este tipo de dato se conoce como cadena de texto o str.'
        ),
    CONCAT_WS(CHAR(10),
            'nombre = ''Ana'''
        ),
    CONCAT_WS(CHAR(10),
            'La variable nombre guarda el valor Ana.',
            'Como Ana está escrita entre comillas, la variable guarda un texto.',
            'Por lo tanto, nombre no guarda un número ni un valor verdadero o falso.'
        ),
    2,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 1 - NPC 3 - COMPLETAR CÓDIGO
-- Orden 3
-- =============================================================
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
VALUES (
    @id_python,
    'Crear variables en Python',
    CONCAT_WS(CHAR(10),
            'Para crear una variable, primero escribimos su nombre.',
            'Después colocamos el signo igual (=) y finalmente el valor.',
            'Los números enteros se escriben sin comillas.'
        ),
    CONCAT_WS(CHAR(10),
            'edad = 15'
        ),
    CONCAT_WS(CHAR(10),
            'edad es el nombre de la variable.',
            'El signo = guarda el valor dentro de la variable.',
            '15 se escribe sin comillas porque debe almacenarse como número entero.'
        ),
    3,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 2 - NPC 1 - VERDADERO O FALSO
-- Orden 4
-- =============================================================
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
VALUES (
    @id_python,
    'Condicional if en Python',
    CONCAT_WS(CHAR(10),
            'La palabra if permite tomar decisiones en Python.',
            'if comprueba una condición y ejecuta su bloque solamente cuando la condición es verdadera.',
            'El código que pertenece al if debe llevar sangría.'
        ),
    CONCAT_WS(CHAR(10),
            'edad = 20',
            'if edad >= 18:',
            '    print("Mayor de edad")'
        ),
    CONCAT_WS(CHAR(10),
            'La condición comprueba si 20 es mayor o igual que 18.',
            'La condición es verdadera.',
            'Por eso el programa muestra el mensaje Mayor de edad.'
        ),
    4,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 2 - NPC 2 - SELECCIÓN MÚLTIPLE
-- Orden 5
-- =============================================================
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
VALUES (
    @id_python,
    'Condicional else en Python',
    CONCAT_WS(CHAR(10),
            'La palabra else indica qué debe ocurrir cuando la condición del if es falsa.',
            'El programa ejecuta solamente uno de los dos bloques: if o else.',
            'El bloque de else también termina con dos puntos y su contenido lleva sangría.'
        ),
    CONCAT_WS(CHAR(10),
            'edad = 12',
            'if edad >= 18:',
            '    print("Mayor de edad")',
            'else:',
            '    print("Menor de edad")'
        ),
    CONCAT_WS(CHAR(10),
            'La condición 12 >= 18 es falsa.',
            'Por eso no se ejecuta el bloque de if.',
            'Se ejecuta el bloque de else y se muestra Menor de edad.'
        ),
    5,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 2 - NPC 3 - COMPLETAR CÓDIGO
-- Orden 6
-- =============================================================
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
VALUES (
    @id_python,
    'Decisiones completas en Python',
    CONCAT_WS(CHAR(10),
            'Para construir una decisión completa usamos if, print() y else.',
            'if comprueba la condición y print() muestra el mensaje correspondiente.',
            'else se ejecuta cuando la condición del if es falsa.'
        ),
    CONCAT_WS(CHAR(10),
            'edad = 18',
            'if edad >= 18:',
            '    print("Mayor de edad")',
            'else:',
            '    print("Menor de edad")'
        ),
    CONCAT_WS(CHAR(10),
            'La primera palabra que falta es if.',
            'La función que muestra el mensaje es print.',
            'La alternativa que se ejecuta cuando la condición es falsa es else.'
        ),
    6,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 3 - NPC 1 - VERDADERO O FALSO
-- Orden 7
-- =============================================================
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
VALUES (
    @id_python,
    'Ciclo while en Python',
    CONCAT_WS(CHAR(10),
            'Un ciclo permite repetir instrucciones.',
            'El ciclo while repite su bloque mientras su condición sea verdadera.',
            'Cuando la condición se vuelve falsa, el ciclo termina.'
        ),
    CONCAT_WS(CHAR(10),
            'contador = 0',
            'while contador < 3:',
            '    print(contador)',
            '    contador += 1'
        ),
    CONCAT_WS(CHAR(10),
            'while comprueba la condición contador < 3 antes de cada repetición.',
            'Mientras la condición sea verdadera, las instrucciones se ejecutan.',
            'El ciclo termina cuando contador llega a 3.'
        ),
    7,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 3 - NPC 2 - SELECCIÓN MÚLTIPLE
-- Orden 8
-- =============================================================
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
VALUES (
    @id_python,
    'Condiciones dentro de while',
    CONCAT_WS(CHAR(10),
            'while comprueba su condición antes de ejecutar el bloque.',
            'Si la condición es falsa desde el inicio, el bloque no se ejecuta ninguna vez.',
            'Para saber qué ocurrirá, primero debemos evaluar la condición.'
        ),
    CONCAT_WS(CHAR(10),
            'contador = 5',
            'while contador < 3:',
            '    print(contador)'
        ),
    CONCAT_WS(CHAR(10),
            'La condición pregunta si 5 es menor que 3.',
            'La condición es falsa desde el inicio.',
            'Por eso el código dentro del ciclo no se ejecuta.'
        ),
    8,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 3 - NPC 3 - COMPLETAR CÓDIGO
-- Orden 9
-- =============================================================
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
VALUES (
    @id_python,
    'Actualizar un contador',
    CONCAT_WS(CHAR(10),
            'Para mostrar los números del 0 al 2 podemos usar un ciclo while.',
            'print(contador) muestra el valor actual del contador.',
            'El operador += aumenta el valor de una variable; contador += 1 lo aumenta en uno.'
        ),
    CONCAT_WS(CHAR(10),
            'contador = 0',
            'while contador < 3:',
            '    print(contador)',
            '    contador += 1'
        ),
    CONCAT_WS(CHAR(10),
            'La palabra que crea el ciclo es while.',
            'La función que muestra el contador es print.',
            'El operador que aumenta el contador es +=.'
        ),
    9,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 4 - NPC 1 - VERDADERO O FALSO
-- Orden 10
-- =============================================================
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
VALUES (
    @id_python,
    'Funciones en Python',
    CONCAT_WS(CHAR(10),
            'Una función es un bloque de instrucciones que realiza una tarea.',
            'Las funciones permiten organizar y reutilizar el código.',
            'Para crear una función en Python utilizamos la palabra def.'
        ),
    CONCAT_WS(CHAR(10),
            'def saludar():',
            '    print("Hola")'
        ),
    CONCAT_WS(CHAR(10),
            'def indica que estamos creando una función.',
            'saludar es el nombre de la función.',
            'El código que pertenece a la función debe llevar sangría.'
        ),
    10,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 4 - NPC 2 - SELECCIÓN MÚLTIPLE
-- Orden 11
-- =============================================================
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
VALUES (
    @id_python,
    'Ejecutar funciones en Python',
    CONCAT_WS(CHAR(10),
            'Crear una función no hace que se ejecute inmediatamente.',
            'Para ejecutar una función escribimos su nombre seguido de paréntesis.',
            'A esta acción se le llama llamar a la función.'
        ),
    CONCAT_WS(CHAR(10),
            'def saludar():',
            '    print("Hola")',
            '',
            'saludar()'
        ),
    CONCAT_WS(CHAR(10),
            'def saludar(): crea la función.',
            'La instrucción saludar() llama y ejecuta la función.',
            'Al ejecutarse, la función muestra el mensaje Hola.'
        ),
    11,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 4 - NPC 3 - COMPLETAR CÓDIGO
-- Orden 12
-- =============================================================
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
VALUES (
    @id_python,
    'Crear y ejecutar una función',
    CONCAT_WS(CHAR(10),
            'Para crear y ejecutar una función utilizamos tres elementos.',
            'def inicia la definición, print() muestra el mensaje y el nombre seguido de () ejecuta la función.',
            'En este ejercicio la función se llama saludar.'
        ),
    CONCAT_WS(CHAR(10),
            'def saludar():',
            '    print("Hola")',
            '',
            'saludar()'
        ),
    CONCAT_WS(CHAR(10),
            'La palabra que define la función es def.',
            'La función que muestra Hola es print.',
            'La palabra que completa la llamada final es saludar.'
        ),
    12,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 5 - NPC 1 - VERDADERO O FALSO
-- Orden 13
-- =============================================================
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
VALUES (
    @id_python,
    'Listas en Python',
    CONCAT_WS(CHAR(10),
            'Una lista permite guardar varios valores dentro de una sola variable.',
            'Los elementos de una lista se escriben entre corchetes.',
            'Cada elemento se separa con una coma.'
        ),
    CONCAT_WS(CHAR(10),
            'frutas = ["manzana", "pera", "uva"]'
        ),
    CONCAT_WS(CHAR(10),
            'La variable frutas contiene una lista.',
            'Dentro de los corchetes hay tres elementos.',
            'Los elementos son manzana, pera y uva.'
        ),
    13,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 5 - NPC 2 - SELECCIÓN MÚLTIPLE
-- Orden 14
-- =============================================================
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
VALUES (
    @id_python,
    'Posiciones de una lista',
    CONCAT_WS(CHAR(10),
            'Cada elemento de una lista tiene una posición llamada índice.',
            'En Python, el primer índice es 0.',
            'Para obtener un elemento escribimos el nombre de la lista y el índice entre corchetes.'
        ),
    CONCAT_WS(CHAR(10),
            'frutas = ["manzana", "pera", "uva"]',
            'print(frutas[0])'
        ),
    CONCAT_WS(CHAR(10),
            'frutas[0] obtiene el primer elemento de la lista.',
            'El primer elemento es manzana.',
            'Por eso el programa muestra manzana.'
        ),
    14,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- NIVEL 5 - NPC 3 - COMPLETAR CÓDIGO
-- Orden 15
-- =============================================================
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
VALUES (
    @id_python,
    'Agregar elementos a una lista',
    CONCAT_WS(CHAR(10),
            'El método append() agrega un nuevo elemento al final de una lista.',
            'Después podemos usar print() para mostrar la lista completa.',
            'El método se escribe después del nombre de la lista y un punto.'
        ),
    CONCAT_WS(CHAR(10),
            'frutas = ["manzana", "pera"]',
            'frutas.append("uva")',
            'print(frutas)'
        ),
    CONCAT_WS(CHAR(10),
            'append agrega uva al final de la lista.',
            'print muestra el contenido completo de frutas.',
            'El resultado contiene manzana, pera y uva.'
        ),
    15,
    10,
    'Activa'
)
ON DUPLICATE KEY UPDATE
    titulo = VALUES(titulo),
    contenido_teoria = VALUES(contenido_teoria),
    codigo_ejemplo = VALUES(codigo_ejemplo),
    contenido_final = VALUES(contenido_final),
    puntos = VALUES(puntos),
    estado = VALUES(estado);


-- =============================================================
-- VERIFICACIÓN FINAL
-- Deben aparecer exactamente 15 registros, ordenados del 1 al 15.
-- =============================================================
SELECT
    le.id_leccion,
    le.orden,
    le.titulo,
    le.codigo_ejemplo,
    le.puntos,
    le.estado
FROM leccion AS le
WHERE le.id_lenguaje = @id_python
  AND le.orden BETWEEN 1 AND 15
ORDER BY le.orden;

SELECT COUNT(*) AS total_lecciones_python
FROM leccion
WHERE id_lenguaje = @id_python
  AND orden BETWEEN 1 AND 15;