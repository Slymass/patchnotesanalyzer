import os
from bs4 import BeautifulSoup
import re

def extract_modules_dynamic(html_file):
    """
    Analyse le fichier HTML et extrait dynamiquement les modules impactés
    en filtrant les identifiants de correctifs et les termes génériques.
    Génère un dictionnaire propre avec des expressions complètes et leurs variantes.
    """
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    modules_detected = {}

    # Liste des mots ou expressions génériques à ignorer
    generic_terms = {"améliorations", "anomalies", "corrigées", "correctifs", "prérequis", "techniques"}

    for header in soup.find_all(["h2", "h3"]):
        section_title = header.get_text(strip=True)

        # Ignorer les titres contenant des identifiants de correctifs (ex: "#SCI-4554")
        if re.match(r"^#\w+-\d+", section_title):
            continue

        # Nettoyage du titre et extraction des expressions
        words = section_title.lower().split()
        module_candidates = [word for word in words if word not in generic_terms]

        if module_candidates:
            module_name = " ".join(module_candidates).capitalize()  # Capitalisation pour une meilleure lisibilité
            normalized_name = module_name.lower()

            # Ajouter le module avec sa variante complète
            if module_name not in modules_detected:
                modules_detected[module_name] = {module_name}  # On stocke aussi la version complète

            # Ajouter toutes les variantes (extraction de sous-phrases pertinentes)
            for i in range(len(module_candidates)):
                sub_phrase = " ".join(module_candidates[i:])  # Garder des expressions cohérentes
                modules_detected[module_name].add(sub_phrase)

    # Convertir les ensembles en listes triées pour la compatibilité JSON/Python
    return {key: sorted(list(value)) for key, value in modules_detected.items()}

def save_mapping_to_file(mapping, output_folder):
    """
    Sauvegarde le mapping des modules détectés dans un fichier sous forme de dictionnaire Python.
    """
    os.makedirs(output_folder, exist_ok=True)  # S'assurer que le dossier analysis existe
    output_file = os.path.join(output_folder, "module_mapping.py")

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("MODULE_MAPPING = {\n")
        for module, keywords in mapping.items():
            file.write(f'    "{module}": {keywords},\n')
        file.write("}\n")

    print(f"[SUCCÈS] Mapping des modules sauvegardé dans {output_file}")

if __name__ == "__main__":
    html_file = "sciforma_patches/2024-09.html"  # Remplace par ton fichier HTML
    output_folder = "analysis"  # Dossier où stocker le fichier module_mapping.py

    modules_found = extract_modules_dynamic(html_file)
    save_mapping_to_file(modules_found, output_folder)
