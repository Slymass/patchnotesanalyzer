import os
import re
import sys
import stdlib_list

# Liste des modules standards de Python
STD_LIB_MODULES = set(stdlib_list.stdlib_list())

def extract_imports_from_file(file_path):
    """Extrait les modules importés d'un fichier Python en filtrant les modules standards."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Recherche des importations : import X et from X import Y
    imports = re.findall(r'^\s*(?:import|from)\s+([\w\d_\.]+)', content, re.MULTILINE)

    # Filtrer pour ne garder que les bibliothèques tierces
    third_party_modules = set()
    for module in imports:
        module_name = module.split(".")[0]  # Garder uniquement le module principal
        if module_name not in STD_LIB_MODULES and not module_name.startswith((".", "..")):
            third_party_modules.add(module_name)

    return third_party_modules

def get_all_python_files(root_dir):
    """Récupère tous les fichiers .py du projet, en ignorant le dossier venv/."""
    python_files = []
    for root, _, files in os.walk(root_dir):
        if "venv" in root or ".venv" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def save_dependencies_to_file(dependencies, filename="dependencies.txt"):
    """Écrit les dépendances dans un fichier texte, en écrasant l'ancien fichier."""
    with open(filename, "w", encoding="utf-8") as f:
        for dep in sorted(dependencies):
            f.write(dep + "\n")
    print(f"Fichier {filename} mis à jour avec {len(dependencies)} dépendances.")

def main():
    """Génère une liste des bibliothèques nécessaires et l'enregistre dans un fichier."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    print("Analyse des fichiers Python dans : " + project_root)

    # Extraire les modules importés
    python_files = get_all_python_files(project_root)
    imported_modules = set()
    
    for file in python_files:
        imported_modules.update(extract_imports_from_file(file))

    # Sauvegarder dans un fichier
    save_dependencies_to_file(imported_modules)

if __name__ == "__main__":
    main()
