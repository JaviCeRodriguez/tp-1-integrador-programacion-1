# Gestor de Países – Proyecto Integrador de Programación I - TUPaD

Proyecto final de la materia “Programación I”, cuyo objetivo es desarrollar un sistema que gestione información sobre países a través de un menú interactivo, utilizando listas, diccionarios, funciones, bucles, condicionales, validaciones, parseos y ordenamientos.

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/JaviCeRodriguez/tp-1-integrador-programacion-1.git
cd tp-1-integrador-programacion-1
```

### 2. Instalar Python

Este proyecto requiere **Python 3.10 o superior**. Verificá la versión con:

```bash
python --version
```

### 3. Ejecutar la aplicación

```bash
python main.py
```

## 📂 Estructura del proyecto

```
├── .vscode/                ← configuración del editor (si aplica)
├── data/
│   └── world_population_acotado.csv       ← archivo de datos con los países
├── Consigna TPI.pdf        ← enunciado del trabajo práctico
├── main.py                 ← script principal que gestiona el menú
└── .gitignore              ← archivos/dirs ignorados por Git
```

- `main.py`: Punto de entrada del programa. Contiene el menú principal y la lógica que invoca las distintas funcionalidades.
- `data/world_population_acotado.csv`: Archivo CSV donde se almacena la información de los países (nombre, continente, población, superficie, etc.).
- `.vscode/`: Carpeta de configuración local del editor VS Code (opcional).
- `Consigna TPI.pdf`: Documento de consigna del trabajo práctico.
- `.gitignore`: Lista de archivos/directorios ignorados en el control de versiones.

## 🧭 Menú principal

Al ejecutar el programa se muestra un menú que se repite hasta que el usuario elige la opción de “Salir”. Las opciones típicas son:

1. Agregar un país
2. Actualizar un país
3. Buscar un país
4. Filtrar países
5. Ordenar países
6. Mostrar estadísticas
7. Salir

Cada opción invoca una función que trabaja sobre la lista de países en memoria (leída desde `world_population_acotado.csv`) y, cuando corresponde, persiste los cambios en el archivo.

## ⚙️ Funcionalidades clave

### ✔️ Validaciones

- Verifica que los campos (por ejemplo: nombre del país, continente) sean cadenas no vacías.
- Asegura que los valores numéricos (población, superficie) puedan convertirse a `int` o `float` según corresponda.
- Manejo de entradas inválidas (por ejemplo: letra donde se espera número) para evitar que el programa falle.

### 🧮 Parseos / Normalización

- Uso de `.strip()` para eliminar espacios en blanco al inicio o fin.
- Uso de `.title()` o `.upper()` para estandarizar los nombres (evitar duplicados por mayúsculas/minúsculas).
- Conversión explícita de valores de cadena a tipo numérico antes de procesarlos.

### 🔍 Filtrados

- Filtrado por continente.
- Filtrado por rango de población o superficie (por ejemplo: población mayor que X, superficie entre A y B).
- Retorna una sublista de países que cumplen con los criterios seleccionados.

### ↕️ Ordenamientos

- Utilización de `sorted()` o métodos similares para ordenar la lista de países.
- Opciones de orden ascendente o descendente.
- Ordenamiento por nombre, población o superficie.

### 📊 Estadísticas

- Determinar el país con mayor población y el país con menor población.
- Cálculo del promedio de superficie.
- Conteo de países por continente.

## 🧩 Utilidades adicionales

- Lectura y escritura en CSV para persistir los datos modificados.
- Mensajes amigables de error o confirmación para mejorar la experiencia del usuario.
- Manejo de excepciones para evitar que el programa se interrumpa ante errores de formato o archivo inexistente.

## 👥 Autores

- Sofía Palacios
- Javier Rodriguez
