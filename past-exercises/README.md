# Python - Learning Exercises

Progressive Python exercises organized by topic and difficulty level.
Each folder represents one language concept, ordered from basic to advanced.

---

## Folder naming convention

Folders follow the pattern: `##_topic_name/`

- Two-digit number prefix defines the recommended learning order.
- Topic name in **lowercase with underscores** — no spaces, accents, or special characters.
- To add a new topic, use the next available number.

```
01_fundamentals/
02_functions/
03_dictionaries/
08_new_topic/      ← next available after 07
```

---

## File naming convention

- **Lowercase with underscores.** No spaces, capital letters, or special characters.
- The name must describe **what the file does**, not a generic number.

```
# Correct
functions_is_even.py
dictionaries_advanced.py

# Wrong
funtion1.py
Ejercicios de Iterables y Listas .py
course_information = {.py
```

---

## Code conventions

- **Language:** All comments and variable names must be written in **English**.
- One concept or exercise per file whenever possible.
- Data files (`.txt`, `.csv`, `.json`) must live in the **same folder as the code that reads them**.

---

## When an exercise grows into multiple files

If a single exercise requires more than one `.py` file, create a **subfolder inside the topic folder**.

```
02_functions/
├── functions_1.py
├── functions_2.py
└── calculator/          ← subfolder for a multi-file exercise
    ├── calculator.py
    ├── operations.py
    └── data.txt
```

Do **not** create a new top-level numbered folder for a project — only for entirely new topics.

---

## Current structure

```
python/
├── 01_fundamentals/        # Basic syntax, variables, conditionals, input/output
├── 02_functions/           # Functions, parameters, return values, scope
├── 03_dictionaries/        # Dictionaries, keys(), values(), items(), methods
├── 04_lists_and_loops/     # Lists, for/while loops, range(), iterables
├── 05_classes/             # Object-oriented programming, __init__, methods
├── 06_exceptions/          # Try/except, error handling, input validation
└── 07_files/
    ├── csv/                # Reading and writing CSV files using the csv module
    │   └── video_games/    # Project: video game catalog stored in CSV
    └── json/               # Reading and writing JSON files using the json module
```

---

## How to add new exercises

1. Identify which topic the exercise belongs to.
2. Navigate to the corresponding folder.
3. Create a file with a descriptive lowercase name using underscores.
4. Place any data files (`.txt`, `.csv`, `.json`) in the same folder as the code.
5. If the topic does not exist yet, create a new numbered folder following the naming convention above.

---

## Requirements

- **Language:** Python 3
- **No external dependencies** — all files use only the Python standard library.
