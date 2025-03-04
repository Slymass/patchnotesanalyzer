import subprocess
import sys
import os

DEPENDENCIES_FILE = "dependencies.txt"

def install_dependencies():
    """Installe chaque dépendance une par une depuis dependencies.txt."""
    if not os.path.exists(DEPENDENCIES_FILE):
        print(f"Le fichier {DEPENDENCIES_FILE} n'existe pas. Exécute d'abord generate_dependencies.py.")
        return

    with open(DEPENDENCIES_FILE, "r", encoding="utf-8") as f:
        dependencies = [line.strip() for line in f if line.strip()]

    if not dependencies:
        print("Aucune dépendance à installer.")
        return

    for package in dependencies:
        print(f"Installation de {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
        except subprocess.CalledProcessError:
            print(f"Impossible d'installer {package}. Il est peut-être invalide ou inexistant sur PyPI.")

    print("Installation terminée.")

if __name__ == "__main__":
    install_dependencies()
