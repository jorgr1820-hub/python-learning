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
data.py      Importacion y exportacion CSV
```

## Persistencia

El listado vive en memoria durante la sesion. Para conservarlo entre
ejecuciones hay que exportar con la opcion 5 y volver a cargarlo con la 6.
El archivo `students.csv` no se versiona.
