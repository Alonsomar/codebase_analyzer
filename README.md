# Codebase Analyzer

Codebase Analyzer es una herramienta que analiza un directorio de código fuente y genera un archivo `codebase_summary.json`. El archivo incluye información detallada sobre:

- **Estructura de carpetas** del proyecto.
- **Archivos de código** (`.js`, `.ts`, `.py`, `.html`, `.css`, etc.).
- **Funciones, clases y comentarios** encontrados en archivos **JavaScript/TypeScript** y **Python**.
- **Contenido de archivos** HTML, CSS, JSON, YAML, y otros archivos comunes.
- Un resumen **meta** con estadísticas del proyecto.

---

## **Características**

- Admite múltiples tipos de archivos: `.js`, `.ts`, `.py`, `.html`, `.css`, `.json`, `.yaml`, `.yml`, `.toml`, `.md`, `.txt`.
- Excluye archivos y carpetas ignorados en `.gitignore` o `.codebaseignore`.
- Genera un archivo JSON estructurado con información del codebase.
- Se puede ejecutar como **script Python** o como **ejecutable PyInstaller**.

### Archivos soportados:
- Código fuente: `.js`, `.ts`, `.py`
- Documentación: `.md`, `.txt`
- Configuración: `.json`, `.yaml`, `.yml`, `.toml`
- Archivos web: `.html`, `.css`
- **Stata**: `.do`, `.ado` (detecta bases usadas, guardadas y comandos clave)

---

## **Requisitos**

- **Python 3.12+** instalado.
- Instalación de dependencias mediante `pip`.

---

## **Instalación y Ejecución**

### **1. Usando el Script desde Python**

#### **Paso 1: Clonar el repositorio**
```bash
git clone https://github.com/alonsomar/codebase_analyzer.git
cd codebase_analyzer
```

#### **Paso 2: Crear un entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate     # En Linux/Mac
.venv\Scripts\activate        # En Windows
```

#### **Paso 3: Instalar dependencias**
```bash
pip install -r requirements.txt
```

#### **Paso 4: Ejecutar el script**
```bash
python main.py
```

- El programa te pedirá:
  - **Ruta del directorio a analizar** (puedes dejarlo vacío para analizar la carpeta actual).
  - **Carpeta donde guardar el `codebase_summary.json`** (puedes dejarlo vacío para guardarlo en la carpeta actual).

---

### **2. Usando el Ejecutable (PyInstaller)**

Si no deseas instalar Python ni dependencias, puedes usar el ejecutable generado.

#### **Paso 1: Descargar el ejecutable**
Descarga el archivo `codebase_analyzer.exe` desde la carpeta **`dist`** o desde tu distribución.

#### **Paso 2: Ejecutar en la terminal**
Abre una terminal (**CMD** en Windows) y ejecuta el archivo `.exe`:

```bash
codebase_analyzer.exe
```

- El programa te pedirá:
  - **Ruta del directorio a analizar**.
  - **Carpeta donde guardar el archivo JSON**.

---

## **Formato del Archivo Generado**

El archivo `codebase_summary.json` tendrá la siguiente estructura:

```json
{
  "directories": [
    "components",
    "static",
    "docs"
  ],
  "files": [
    {
      "file": "README.md",
      "functions": [],
      "classes": [],
      "comments": [],
      "content": "# My Project\nThis is a sample project."
    },
    {
      "file": "app.py",
      "functions": ["main"],
      "classes": ["App"],
      "comments": ["Main function"],
      "content": "import os\nclass App:\n    pass\nif __name__ == '__main__':\n    main()"
    }
  ],
  "meta": {
    "total_files": 12,
    "total_directories": 3,
    "file_types": {
      ".py": 5,
      ".md": 2,
      ".html": 3,
      ".css": 1,
      ".json": 1
    },
    "generated_at": "2024-06-17T14:00:00"
  }
}
```

---

## **Ejemplo de Ejecución**

### **Desde el Script**
```bash
python main.py
```

**Salida en la consola**:
```
Introduce el directorio a analizar (default: actual): C:\Proyectos\mi_app
Introduce la carpeta para guardar el resultado (default: actual): C:\Resultados

Resumen generado en: C:\Resultados\codebase_summary.json
```

### **Desde el Ejecutable**
```bash
codebase_analyzer.exe
```

---

## **Desarrollo del Proyecto**

### **Estructura del Código**
```
codebase_analyzer/
│-- main.py                # Script principal
│-- file_processors.py     # Procesa archivos JS/TS, Python y otros
│-- ignore_patterns.py     # Maneja archivos de ignorados
│-- requirements.txt       # Dependencias
└-- README.md              # Documentación
```

### **Cómo Generar el Ejecutable con PyInstaller**
Si quieres generar tu propio ejecutable:

1. Instala **PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. Crea el ejecutable:
   ```bash
   pyinstaller --onefile --name codebase_analyzer main.py
   ```

3. El ejecutable estará en la carpeta **`dist`**.

---

## **Contribuir**

¡Toda contribución es bienvenida! Si tienes sugerencias o mejoras, abre un **issue** o envía un **pull request**.

---

## **Licencia**

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

¡Espero que esta herramienta te ayude a entender y analizar tus codebases de forma rápida y eficiente! 🚀
