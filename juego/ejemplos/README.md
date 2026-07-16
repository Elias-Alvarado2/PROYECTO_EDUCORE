# Imagenes para practicas de ejemplo

Guarda aqui las imagenes que deban mostrarse dentro de una practica de tipo
`ejemplo`. Se permiten subcarpetas para organizar las imagenes por lenguaje.

Ejemplo de configuracion dentro de `PRACTICAS` en cualquier nivel:

```python
{
    "x": 2200,
    "y": None,
    "tipo": "ejemplo",
    "pregunta": "Observa la tabla y revisa como se organizan sus columnas.",
    "imagen": "mysql/tabla_usuarios.png",
    "ancho": 1000,
    "alto": 500,
    "nombre": "ejemplo_tabla_usuarios",
}
```

La ruta de `imagen` siempre es relativa a esta carpeta. `ancho` y `alto` son
opcionales; si se omiten, la imagen ocupa el espacio disponible conservando su
proporcion. Si solo se indica una de las dos medidas, la otra se calcula sin
deformar la imagen.
