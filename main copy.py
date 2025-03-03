import os
import yaml
import subprocess
import sys
import force_utf8  # Active UTF-8 globalement


# Définition des répertoires pour chaque système
DIRECTORIES = {
    "Sciforma": "sciforma_patches",
    "BC": "bc_patches"
}

def load_config():
    """
    Charge la configuration YAML si elle existe.
    """
    config_file = "config.yaml"
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return yaml.safe_load(file) or {}
    return {}

def save_config(config):
    """
    Sauvegarde la configuration mise à jour dans config.yaml.
    """
    with open("config.yaml", "w") as file:
        yaml.dump(config, file)

def process_html_file(html_file, system):
    """
    Exécute tout le pipeline avec le fichier HTML sélectionné et le système spécifié.
    """
    if not os.path.exists(html_file):
        print(f"❌ Erreur : Le fichier {html_file} n'existe pas.")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(html_file))[0]
    correctifs_file = f"{base_name}_correctifs.xlsx"
    enhancements_file = f"{base_name}_enhancements.xlsx"
    master_file = f"{base_name}_Master.xlsx"

    # 🔄 Exécuter l'extraction
    if system == "Sciforma":
        subprocess.run(["python", "extractors/extract_sciforma.py", html_file, "--type", "correctifs", correctifs_file], check=True)
        subprocess.run(["python", "extractors/extract_sciforma.py", html_file, "--type", "améliorations", enhancements_file], check=True)
    elif system == "BC":
        subprocess.run(["python", "extractors/extract_bc.py", html_file, "--type", "correctifs", correctifs_file], check=True)
        subprocess.run(["python", "extractors/extract_bc.py", html_file, "--type", "améliorations", enhancements_file], check=True)

    # 🔄 Nettoyage et mise en forme
    subprocess.run(["python", "processors/clean_data.py", correctifs_file, enhancements_file], check=True)
    subprocess.run(["python", "analysis/extract_modules_dynamic.py", correctifs_file, enhancements_file], check=True)
    subprocess.run(["python", "analysis/categorize_impacts.py", correctifs_file, enhancements_file], check=True)
    subprocess.run(["python", "mergers/merge_to_master.py", base_name, correctifs_file, enhancements_file, master_file], check=True)
    subprocess.run(["python", "processors/format_data.py", master_file], check=True)

    print(f"\n🎉 Processus terminé ! Fichier Master généré : {master_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Erreur : Arguments manquants. Utilisation : python main.py <chemin_html> <système>")
        sys.exit(1)

    html_file = sys.argv[1]
    system = sys.argv[2]

    if system not in DIRECTORIES:
        print("❌ Erreur : Système invalide. Veuillez choisir 'Sciforma' ou 'BC'.")
        sys.exit(1)

    config = load_config()
    config["html_file"] = html_file
    config["system"] = system
    config["html_dir"] = DIRECTORIES[system]

    save_config(config)
    process_html_file(html_file, system)
