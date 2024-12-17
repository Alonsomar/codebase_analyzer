import os

DEFAULT_IGNORE_FILE = ".codebaseignore"  # Archivo predeterminado en la carpeta del script
GITIGNORE_FILE = ".gitignore"


def find_ignore_file(base_path, file_name, fallback_path):
    """
    Busca el archivo especificado en la raíz del proyecto. Si no existe, usa el archivo predeterminado.
    """
    root_ignore_file = os.path.join(base_path, file_name)
    if os.path.exists(root_ignore_file):
        return root_ignore_file  # Usa el archivo de la raíz del proyecto
    return os.path.join(fallback_path, file_name)  # Usa el archivo predeterminado


def load_ignored_patterns(base_path, fallback_ignore_file=DEFAULT_IGNORE_FILE):
    """
    Carga patrones a ignorar desde .gitignore y .codebaseignore.
    Si .codebaseignore no existe en el proyecto, usa uno por defecto.
    """
    ignored_patterns = set()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Encontrar archivos .codebaseignore y .gitignore
    codebaseignore_file = find_ignore_file(base_path, ".codebaseignore", script_dir)
    gitignore_file = os.path.join(base_path, GITIGNORE_FILE)

    # Cargar patrones desde .codebaseignore
    if os.path.exists(codebaseignore_file):
        print(f"Usando .codebaseignore: {codebaseignore_file}")
        with open(codebaseignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignored_patterns.add(line)

    # Cargar patrones desde .gitignore
    if os.path.exists(gitignore_file):
        print(f"Usando .gitignore: {gitignore_file}")
        with open(gitignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignored_patterns.add(line)

    return ignored_patterns


def list_code_files(base_path, ignored_patterns, extensions):
    """
    Recorre un directorio y lista archivos de código válidos, ignorando patrones.
    """
    code_files = []
    for root, dirs, files in os.walk(base_path):
        # Filtrar directorios ignorados
        dirs[:] = [d for d in dirs if d not in ignored_patterns]

        for file in files:
            file_path = os.path.join(root, file)
            # Filtrar archivos según extensiones y patrones ignorados
            if any(file.endswith(ext) for ext in extensions) and not any(
                p in file_path for p in ignored_patterns
            ):
                code_files.append(file_path)
    return code_files
