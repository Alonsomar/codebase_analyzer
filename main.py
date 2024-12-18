import datetime
import os
import json
from ignore_patterns import load_ignored_patterns, list_code_files
from file_processors import process_js_ts_file, process_python_file, process_plain_file, process_stata_file


# =========================
# CONFIGURACIÓN
# =========================
OUTPUT_FILE = "codebase_summary.json"
CODE_EXTENSIONS = {".js", ".ts", ".py", ".html", ".css", ".json", ".yaml", ".yml", ".toml", ".md", ".txt", ".do", ".ado"}
DOC_FILES = {"README.md", "CHANGELOG.md", "LICENSE", "CONTRIBUTING.md"}


# =========================
# FUNCIÓN PARA LISTAR CARPETAS
# =========================
def list_directories(base_path, ignored_patterns):
    """
    Recorre un directorio y lista todas las carpetas, ignorando patrones especificados.
    """
    directories = []
    for root, dirs, _ in os.walk(base_path):
        # Filtrar directorios ignorados
        dirs[:] = [d for d in dirs if d not in ignored_patterns]
        relative_path = os.path.relpath(root, base_path)
        if relative_path != ".":
            directories.append(relative_path)
    return directories


# =========================
# FUNCIÓN PRINCIPAL
# =========================
def analyze_codebase(base_path=".", output_dir=None):
    """Analiza el codebase y genera un resumen en JSON."""
    base_path = os.path.abspath(base_path)
    ignored_patterns = load_ignored_patterns(base_path)

    # Obtener archivos y carpetas
    code_files = list_code_files(base_path, ignored_patterns, CODE_EXTENSIONS)
    directories = list_directories(base_path, ignored_patterns)

    summary = {"files": [], "directories": directories, "meta": {}}

    # Contadores para meta
    file_type_count = {}
    total_files = 0

    for file_path in code_files:
        relative_path = os.path.relpath(file_path, base_path)
        ext = os.path.splitext(file_path)[1]
        total_files += 1
        file_type_count[ext] = file_type_count.get(ext, 0) + 1

        file_info = {
            "file": relative_path,
            "functions": [],
            "classes": [],
            "comments": [],
            "content": ""
        }

        # Procesar según el tipo de archivo
        if ext in {".js", ".ts"}:
            extracted_info = process_js_ts_file(file_path)
        elif ext == ".py":
            extracted_info = process_python_file(file_path)
        elif ext in {".html", ".css", ".json", ".yaml", ".yml", ".toml", ".md", ".txt"}:
            extracted_info = process_plain_file(file_path)
        elif ext in {".do", ".ado"}:
            extracted_info = process_stata_file(file_path)
        else:
            extracted_info = {"content": ""}

        if extracted_info:
            file_info.update(extracted_info)
        summary["files"].append(file_info)

    # Agregar sección meta
    summary["meta"] = {
        "total_files": total_files,
        "total_directories": len(directories),
        "file_types": file_type_count,
        "generated_at": datetime.datetime.now().isoformat()
    }

    # Definir ruta de salida para codebase_summary.json
    output_file = os.path.join(output_dir or os.getcwd(), "codebase_summary.json")

    # Generar archivo JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Resumen generado en: {output_file}")


# =========================
# EJECUCIÓN DEL SCRIPT
# =========================
if __name__ == "__main__":
    base_dir = input("Introduce el directorio a analizar (default: actual): ").strip() or "."
    output_dir = input("Introduce la carpeta para guardar el resultado (default: actual): ").strip()
    output_dir = output_dir or os.getcwd()
    analyze_codebase(base_dir, output_dir)
