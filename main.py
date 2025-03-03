import sys
import os
import yaml
import subprocess


# Définition des répertoires pour chaque système
DIRECTORIES = {
    "Sciforma": "sciforma_patches",
    "BC": "bc_patches"
}

def load_config():
    """ Charge la configuration YAML si elle existe. """
    config_file = "config.yaml"
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return yaml.safe_load(file) or {}
    return {}

def save_config(config):
    """ Sauvegarde la configuration mise à jour dans config.yaml. """
    with open("config.yaml", "w") as file:
        yaml.dump(config, file)

def process_html_file(html_file, system):
    """ Exécute tout le pipeline avec UTF-8 forcé dans `subprocess.run()`. """
    if not os.path.exists(html_file):
        print(f"[ERREUR] Le fichier {html_file} n'existe pas.")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(html_file))[0]
    correctifs_file = f"{base_name}_correctifs.xlsx"
    enhancements_file = f"{base_name}_enhancements.xlsx"
    master_file = f"{base_name}_Master.xlsx"

    commands = [
        ["python", "extractors/extract_sciforma.py", html_file, "--type", "correctifs", correctifs_file],
        ["python", "extractors/extract_sciforma.py", html_file, "--type", "améliorations", enhancements_file],
        ["python", "processors/clean_data.py", correctifs_file, enhancements_file],
        ["python", "analysis/extract_modules_dynamic.py", correctifs_file, enhancements_file],
        ["python", "analysis/categorize_impacts.py", correctifs_file, enhancements_file],
        ["python", "mergers/merge_to_master.py", base_name, correctifs_file, enhancements_file, master_file],
        ["python", "processors/format_data.py", master_file]
    ]

    for cmd in commands:
        print(f"[INFO] Exécution : {' '.join(cmd)}")
        subprocess.run(cmd, check=True, text=True, encoding="utf-8")

    print(f"\n[SUCCÈS] Processus terminé ! Fichier Master généré : {master_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("[ERREUR] Arguments manquants. Utilisation : python main.py <chemin_html> <système>")
        sys.exit(1)

    html_file = sys.argv[1]
    system = sys.argv[2]

    if system not in DIRECTORIES:
        print("[ERREUR] Système invalide. Veuillez choisir 'Sciforma' ou 'BC'.")
        sys.exit(1)

    config = load_config()
    config["html_file"] = html_file
    config["system"] = system
    config["html_dir"] = DIRECTORIES[system]

    save_config(config)
    process_html_file(html_file, system)
