import sys
import pandas as pd

def clean_excel(file_path):
    """
    Nettoie et valide le fichier Excel après extraction :
    - Supprime les lignes où l'ID est manquant
    - Vérifie la présence des colonnes nécessaires
    """
    print(f"[INFO] Vérification et nettoyage des données dans : {file_path}")

    # Charger les données
    df = pd.read_excel(file_path)

    # Vérifier si le fichier contient les bonnes colonnes
    required_columns = {"Section", "Sous-section", "ID", "Description"}
    if not required_columns.issubset(df.columns):
        print(f"[ERREUR] Le fichier '{file_path}' ne contient pas toutes les colonnes requises.")
        return

    # Supprimer les lignes où l'ID est manquant (évite les erreurs en aval)
    initial_rows = len(df)
    df = df.dropna(subset=["ID"])
    rows_removed = initial_rows - len(df)

    # Sauvegarder le fichier nettoyé uniquement si des modifications ont été faites
    if rows_removed > 0:
        df.to_excel(file_path, index=False)
        print(f"[SUCCÈS] {rows_removed} lignes supprimées. Fichier nettoyé : {file_path}")
    else:
        print(f"[INFO] Aucune correction nécessaire dans {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERREUR] Aucun fichier spécifié. Utilisation : python clean_data.py fichier.xlsx")
        sys.exit(1)

    # Nettoyer chaque fichier passé en argument
    for file in sys.argv[1:]:
        clean_excel(file)
