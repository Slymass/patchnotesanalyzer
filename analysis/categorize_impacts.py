import sys
import os
import pandas as pd


# Importer le fichier module_mapping.py
try:
    import module_mapping as module_mapping
    MODULE_MAPPING = module_mapping.MODULE_MAPPING  # Assurez-vous que module_mapping.py contient bien un dictionnaire nommé MODULE_MAPPING
except ImportError:
    print("[ERREUR] Impossible d'importer module_mapping.py. Vérifiez que le fichier est bien à la racine du projet.")
    sys.exit(1)

def categorize_impact(file_path):
    """
    Ajoute une colonne 'Module impacté' en fonction de la description du correctif.
    """
    print(f"[INFO] Catégorisation des impacts dans : {file_path}")

    # Charger le fichier Excel
    df = pd.read_excel(file_path)

    # Vérifier que la colonne attendue existe
    if "Description" not in df.columns:
        print(f"[ERREUR] La colonne 'Description' est absente dans {file_path}.")
        return

    # Fonction pour attribuer un module en fonction des mots-clés
    def detect_module(description):
        description = str(description).lower()
        for module, keywords in MODULE_MAPPING.items():
            if any(keyword in description for keyword in keywords):
                return module
        return "Non catégorisé"  # Si aucun mot-clé ne correspond

    # Ajouter la colonne "Module impacté"
    df["Module impacté"] = df["Description"].apply(detect_module)

    # Sauvegarder le fichier modifié
    df.to_excel(file_path, index=False)
    print(f"[SUCCÈS] Catégorisation terminée et sauvegardée dans {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERREUR] Aucun fichier spécifié. Utilisation : python categorize_impacts.py fichier.xlsx")
        sys.exit(1)

    # Appliquer la catégorisation sur chaque fichier donné en argument
    for file in sys.argv[1:]:
        categorize_impact(file)
