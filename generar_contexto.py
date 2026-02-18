#!/usr/bin/env python3
import os
from pathlib import Path

# ================= CONFIGURACIÓN =================
# Directorios a ignorar (añade aquí carpetas de temporales, venv, etc.)
EXCLUDE_DIRS = {
    "node_modules", ".next", "venv", ".venv", "__pycache__", ".git", 
    "dist", "build", ".idea", ".vscode", "migrations"
}

# Archivos a ignorar
EXCLUDE_FILES = {
    "package-lock.json", "yarn.lock", "*.log", "*.pyc", ".DS_Store", 
    "poetry.lock", "*.png", "*.jpg", "*.jpeg", "*.gif", "*.ico", "*.svg", "*.md",
    "CONTEXTO_COMPLETO.md", "generar_contexto.py", ".env", ".env.local"
}

# Extensiones permitidas (Stack FastAPI + Jinja + Tailwind)
ALLOWED_EXTENSIONS = {
    '.py',    # Backend FastAPI
    '.html',  # Templates Jinja2
    '.css',   # Estilos globales
    '.js',    # Scripts (Alpine/HTMX config)
    '.sql',   # Esquemas DB
    '.env',   # Configuración (se limpian valores)
    '.ini',
    '.toml',
    '.ts',   # TypeScript (frontend)
    '.json',  # Configuración JSON
    '.tsx'  # React/Next.js
}

# Archivos específicos importantes
IMPORTANT_FILES = {
    "requirements.txt", "Dockerfile", "docker-compose.yml", "README.md"
}

# Nombre del archivo de salida
OUTPUT_FILENAME = "CONTEXTO_COMPLETO.md"

# ================= LÓGICA =================

def should_exclude(path: Path, root: Path):
    # Ignorar directorios excluidos
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
            
    # Ignorar archivos por patrón
    if path.name in EXCLUDE_FILES:
        return True
    
    # Ignorar extensiones de imágenes/binarios
    if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', '.ttf'}:
        return True
        
    return False

def is_text_file(path: Path):
    try:
        if path.name in IMPORTANT_FILES:
            return True
        return path.suffix.lower() in ALLOWED_EXTENSIONS
    except:
        return False

def read_file_content(path: Path):
    try:
        # Intentar leer como UTF-8
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            # Fallback a latin-1 si falla utf-8
            with open(path, 'r', encoding='latin-1') as f:
                return f.read()
        except:
            return "[ERROR: Archivo binario o codificación no soportada]"
    except Exception as e:
        return f"[ERROR al leer archivo: {str(e)}]"

def main():
    root = Path('.').resolve()
    output_path = root / OUTPUT_FILENAME
    
    print(f"🚀 Iniciando escaneo del proyecto en: {root}")
    
    content_buffer = []
    
    # 1. Header del archivo
    content_buffer.append(f"# CONTEXTO DEL PROYECTO: {root.name}\n")
    content_buffer.append("Generado automáticamente para revisión de código.\n\n")
    
    # 2. Estructura de directorios (Tree)
    content_buffer.append("## 📁 Estructura del Proyecto\n```\n")
    file_list = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Filtrar directorios in-place
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        
        rel_path = Path(dirpath).relative_to(root)
        if str(rel_path) == '.':
            level = 0
        else:
            level = len(rel_path.parts)
            
        indent = '    ' * level
        if str(rel_path) != '.':
            content_buffer.append(f"{indent}📂 {rel_path.name}/\n")
            
        subindent = '    ' * (level + 1)
        for f in filenames:
            f_path = Path(dirpath) / f
            if not should_exclude(f_path, root):
                content_buffer.append(f"{subindent}📄 {f}\n")
                if is_text_file(f_path):
                    file_list.append(f_path)
    
    content_buffer.append("```\n\n")
    content_buffer.append("---\n\n")
    
    # 3. Contenido de los archivos
    print(f"📄 Procesando {len(file_list)} archivos de código...")
    
    for file_path in sorted(file_list):
        rel_path = file_path.relative_to(root)
        print(f"   Adding: {rel_path}")
        
        file_content = read_file_content(file_path)
        ext = file_path.suffix.lstrip('.') or 'txt'
        
        # Formato Markdown para cada archivo
        content_buffer.append(f"## 📄 Archivo: `{rel_path}`\n")
        content_buffer.append(f"```{ext}\n")
        content_buffer.append(file_content)
        content_buffer.append("\n```\n\n")
        content_buffer.append("---\n\n")

    # 4. Guardar archivo único
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("".join(content_buffer))
        print(f"\n✅ ÉXITO: Archivo generado en: {output_path}")
        print(f"📊 Tamaño total: {output_path.stat().st_size / 1024:.2f} KB")
        print("👉 Por favor, sube este archivo al chat.")
    except Exception as e:
        print(f"\n❌ ERROR al guardar el archivo: {e}")

if __name__ == "__main__":
    main()
