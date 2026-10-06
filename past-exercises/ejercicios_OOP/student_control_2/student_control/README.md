# Student Control

Sistema de control de estudiantes por consola. Permite registrar alumnos con
sus notas por materia, consultar promedios y rankings, y persistir el listado
en un archivo CSV.

## Requisitos

- Python 3.10 o superior (probado en 3.14)

No usa dependencias externas: solo la biblioteca estandar.

## Ejecucion

```bash
python3 main.py
```

## Funcionalidades

| Opcion | Accion | Descripcion |
|--------|--------|-------------|
| 1 | Add Student | Registra un alumno con nombre, seccion y cuatro notas |
| 2 | Show Students | Lista todos los alumnos con su promedio |
| 3 | Top 3 Students | Los tres mejores promedios |
| 4 | General Average | Promedio de todo el grupo |
| 5 | Export CSV | Guarda el listado en `students.csv` |
| 6 | Import CSV | Carga el listado desde `students.csv` |
| 7 | Exit | Sale del programa |
| 8 | Delete Student | Elimina un alumno, con confirmacion |
| 9 | Show Failing Students | Alumnos con alguna nota menor a 60 |

## Materias

Cada alumno tiene una nota (0-100) en: Spanish, English, Social Studies y Science.

## Validaciones

- **Nombre**: solo letras, espacios y guiones. Acepta tildes y enie.
- **Seccion**: formato digito-digito-letra (por ejemplo `11B`). Se normaliza a mayusculas.
- **Notas**: enteros entre 0 y 100.
- **Duplicados**: no se admiten dos alumnos con el mismo nombre y seccion.

Todos los campos se vuelven a pedir hasta que la entrada sea valida.

## Estructura

```
main.py      Punto de entrada; posee la lista de alumnos
menu.py      Menu de consola y despacho de opciones
actions.py   Operaciones sobre alumnos y validaciones
model.py     Clase Student: que ES un alumno y como se traduce a/desde CSV
data.py      Importacion y exportacion CSV
```

Cada archivo tiene una sola responsabilidad: `menu.py` habla con el usuario,
`actions.py` aplica las reglas, `model.py` define el dato y `data.py` se encarga
del disco. Se puede cambiar el formato de persistencia reescribiendo solo
`data.py`.

## Modelo de datos

Cada alumno es una instancia de la clase `Student` (en `model.py`), no un
diccionario. La clase es la unica que conoce la forma de un alumno y ofrece
la traduccion en los dos sentidos:

| Metodo | Tipo | Para que sirve |
|--------|------|----------------|
| `student.to_dict()` | de instancia | convierte el objeto en diccionario para escribirlo al CSV |
| `Student.from_dict(row)` | de clase | construye un objeto desde una fila del CSV |
| `Student.FIELDS` | atributo de clase | nombre y orden de las columnas del CSV |

`from_dict` convierte las notas a `int`, porque todo lo que se lee de un CSV
llega como texto. La conversion de tipos ocurre en la frontera del sistema:
hacia adentro siempre hay objetos con tipos correctos.

## Persistencia

El listado vive en memoria durante la sesion. Para conservarlo entre
ejecuciones hay que exportar con la opcion 5 y volver a cargarlo con la 6.
El archivo `students.csv` no se versiona.
