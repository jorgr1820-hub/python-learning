# Archivados

Memoria de largo plazo de mi aprendizaje tecnico. Cada vez que termino una
tarea, el chat completo se condensa aqui en un documento permanente.

El objetivo no es guardar conversaciones. Es que dentro de seis meses pueda
reconstruir **que aprendi, por que se decidio asi y como se veia el codigo**,
sin volver a leer el chat ni depender de que la IA recuerde nada.

---

## La regla estandar

> **Cada vez que se finaliza una tarea, se archiva.**

No es opcional ni depende de que yo lo pida. Al cerrar una tarea se crea un
documento en esta carpeta siguiendo [PLANTILLA.md](PLANTILLA.md), y se agrega
su linea al indice de abajo.

Una tarea esta "finalizada" cuando se cumple cualquiera de estas:

- el codigo corre y fue verificado
- se abrio el pull request
- yo digo `done` / `d`
- se cierra la sesion sobre ese tema

## Convencion de nombres

```
AAAA-MM-DD-tema-en-kebab-case.md
```

Ejemplo: `2026-10-04-practica-oop.md`

**Por que la fecha primero:** ordena cronologicamente solo, sin metadatos ni
herramientas. `ls` ya es una linea de tiempo.

**Por que kebab-case y sin tildes:** rutas sin espacios ni acentos funcionan
igual en la terminal, en Git, en URLs y en cualquier sistema operativo.

## Estructura de la carpeta

```
Archivados/
├── README.md                     Este archivo: reglas, indice y guia de lectura
├── PLANTILLA.md                  Molde obligatorio de cada resumen
└── AAAA-MM-DD-tema.md            Un archivo por tarea finalizada
```

Un archivo plano por tarea, no una carpeta por tarea. Razon: un solo archivo se
busca con `grep`, se lee de arriba a abajo y se abre en cualquier parte. Si
algun resumen llega a necesitar archivos adjuntos, ese caso particular pasa a
carpeta y se anota aqui.

---

## Indice

| Fecha | Documento | Tema | Estado |
|-------|-----------|------|--------|
| 2026-10-04 | [Practica OOP](2026-10-04-practica-oop.md) | Composicion, referencias, fachada, properties, fabrica, recursion, serializacion CSV, Git y PR | PR #3 abierto |
| 2026-10-20 | [Los 4 pilares de OOP y criterio de diseno](2026-10-20-pilares-oop.md) | Invariantes y sus puertas, Template Method, clases abstractas (ABC), herencia multiple, MRO y mixins, Liskov, Decimal vs float | PR #3 abierto |

---

## Como leer un resumen (guia estructurada)

Cada documento sigue siempre el mismo orden, y ese orden **no es decorativo**:
reproduce mi forma de aprender, de lo concreto a lo abstracto.

```
analogia  ->  diagrama  ->  concepto tecnico  ->  codigo  ->  verificacion
```

### Las 10 secciones y para que sirve cada una

| # | Seccion | Que responde | Cuando leerla |
|---|---------|--------------|---------------|
| 0 | **Ficha rapida** | que se hizo, donde quedo, en que estado | siempre, son 20 segundos |
| 1 | **Analogia maestra** | el modelo mental que une todo el tema | cuando volvi despues de meses y perdi el contexto |
| 2 | **Mapa** | como se conectan las piezas, en diagrama | cuando necesito ubicarme rapido |
| 3 | **Conceptos** | el nucleo: un concepto por bloque, con su codigo | cuando necesito entender o reusar uno especifico |
| 4 | **Errores** | cada error real, su causa y como se reconoce | cuando un error se parece a algo que ya vi |
| 5 | **Decisiones** | por que se eligio A y no B | cuando quiero cambiar algo y necesito saber que se rompe |
| 6 | **Codigo final** | el resultado completo, copiable | cuando necesito el codigo, no la explicacion |
| 7 | **Metodo** | como se razono, no que se escribio | lo mas valioso a largo plazo: es transferible |
| 8 | **Comandos** | terminal y Git usados, con su explicacion | cuando repito el flujo en otra tarea |
| 9 | **Pendientes** | lo que quedo sin hacer | al retomar el tema |

### Tres formas de usar un resumen

**Repaso de 10 minutos:** seccion 0, seccion 1, seccion 2, y la tabla de
"Dónde se reusa" de cada concepto. Nada mas.

**Buscar algo puntual:** ve directo a la seccion 3 y busca el concepto por
nombre. Cada bloque es autocontenido: incluye su codigo y su verificacion.

**Retomar el trabajo:** seccion 0, seccion 9 (pendientes) y seccion 5
(decisiones), para no reabrir algo que ya se decidio.

### Estructura interna de cada concepto

Todos los conceptos de la seccion 3 se explican en el mismo orden:

1. **Que es** — una frase
2. **Por que existe** — el problema real que resuelve
3. **Analogia** — el modelo mental
4. **Codigo** — el ejemplo real de la tarea, en ingles
5. **Que ocurre al ejecutar** — incluido que pasa en memoria
6. **Como verificar** — el comando o la prueba concreta
7. **Que problema futuro evita**
8. **Donde se reusa** — otros proyectos y otros stacks

Si una seccion no aplica, se escribe "no aplica" en vez de borrarla. La
estructura fija es lo que hace que todos los documentos se puedan leer en
diagonal.

---

## Para la IA que lea esta carpeta

Si me estas ayudando y necesitas contexto de algo que ya trabaje:

1. Lee el **indice** de este README para ubicar el documento por tema.
2. Lee la **seccion 0** de ese documento para el estado actual.
3. Lee solo el **concepto** o la **decision** relevante. No hace falta el
   documento completo.
4. Las secciones 5 (decisiones) y 9 (pendientes) son las que evitan que
   reabras algo ya resuelto o que repitas trabajo.

Busqueda rapida por tema:

```bash
grep -ril "serializacion" Archivados/
grep -n "^### " Archivados/2026-10-04-practica-oop.md   # lista de conceptos
```

Al cerrar una tarea nueva: copia `PLANTILLA.md`, renombralo con la convencion
de fecha, llenalo, y agrega la fila al indice. El documento se escribe en
espanol y el codigo en ingles.
