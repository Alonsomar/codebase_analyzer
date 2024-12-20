import re
import ast


# =========================
# LECTURA DE CONTENIDO
# =========================
def read_file_content(file_path):
    """Lee el contenido completo del archivo con soporte para múltiples codificaciones."""
    encodings_to_try = ["utf-8", "utf-16", "iso-8859-1"]
    for encoding in encodings_to_try:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
            return ""
    print(f"No se pudo leer {file_path} con las codificaciones probadas.")
    return ""



# =========================
# PROCESADOR JS/TS
# =========================
def process_js_ts_file(file_path):
    """
    Extrae funciones, clases y comentarios de archivos JS/TS usando expresiones regulares avanzadas.
    Soporta funciones normales, funciones flecha, clases y comentarios.
    """
    content = read_file_content(file_path)
    info = {"functions": [], "classes": [], "comments": []}

    try:
        # ============================
        # REGEX PARA IDENTIFICAR ELEMENTOS
        # ============================

        # Funciones tradicionales: function nombre(...)
        function_declarations = re.findall(r"function\s+([a-zA-Z0-9_]+)\s*\(", content)

        # Funciones asignadas a variables (incluye arrow functions y funciones anónimas)
        variable_functions = re.findall(
            r"(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(?:function\s*\(|\([^)]*\)\s*=>)", content
        )

        # Funciones flecha anónimas asignadas a objetos ({ nombre: () => ... })
        object_arrow_functions = re.findall(
            r"([a-zA-Z0-9_]+)\s*:\s*\([^)]*\)\s*=>", content
        )

        # Clases declaradas con class
        class_declarations = re.findall(r"class\s+([a-zA-Z0-9_]+)", content)

        # Comentarios de una línea
        single_line_comments = re.findall(r"//\s*(.*)", content)

        # Comentarios multilínea
        multi_line_comments = re.findall(r"/\*([\s\S]*?)\*/", content)

        # ============================
        # ALMACENAR RESULTADOS
        # ============================
        info["functions"].extend(function_declarations)
        info["functions"].extend(variable_functions)
        info["functions"].extend(object_arrow_functions)
        info["classes"].extend(class_declarations)
        info["comments"].extend(single_line_comments)
        info["comments"].extend([comment.strip() for comment in multi_line_comments])

        # El contenido completo del archivo
        info["content"] = content

        return info

    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return {"content": content}


# =========================
# PROCESADOR PYTHON
# =========================
def process_python_file(file_path):
    """Analiza archivos Python usando AST e incluye su contenido."""
    content = read_file_content(file_path)
    info = {"functions": [], "classes": [], "comments": [], "content": content}

    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                info["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                info["classes"].append(node.name)
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                # Captura comentarios como docstrings
                info["comments"].append(node.value.s.strip())

        return info
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return info


# =========================
# PROCESADOR HTML, CSS, Y ARCHIVOS DE CONFIGURACIÓN
# =========================
def process_plain_file(file_path):
    """Procesa archivos HTML, CSS, JSON, YAML, etc. Incluye solo su contenido."""
    content = read_file_content(file_path)
    return {"content": content}


# =========================
# PROCESADOR STATA FILES
# =========================
def process_stata_file(file_path):
    """
    Procesa archivos Stata (.do y .ado) para identificar bases de datos usadas, guardadas y comandos clave.
    """
    content = read_file_content(file_path)
    info = {"used_datasets": [], "saved_datasets": [], "commands": [], "comments": []}

    try:
        # Identificar bases de datos utilizadas (`use`)
        used_datasets = re.findall(r"\buse\s+([^\s,]+)", content, re.IGNORECASE)

        # Identificar bases de datos guardadas (`save`)
        saved_datasets = re.findall(r"\bsave\s+([^\s,]+)", content, re.IGNORECASE)

        # Extraer comandos clave (ejemplo: `graph`, `regress`, `import`, etc.)
        commands = re.findall(r"(?m)^\s*(graph|regress|summarize|import|gen|replace|merge|append)\b", content)

        # Extraer comentarios (`* comentario`)
        comments = re.findall(r"(?m)^\s*\*\s*(.*)", content)

        # Guardar resultados en el diccionario
        info["used_datasets"].extend(used_datasets)
        info["saved_datasets"].extend(saved_datasets)
        info["commands"].extend(commands)
        info["comments"].extend(comments)
        info["content"] = content
        return info
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return {"content": content}
