import pandas as pd
import numpy as np
import re

input_path = r"C:\Users\abap0\Documents\Files\programmes\projet-scrap\sneakers.csv"
output_path = r"C:\Users\abap0\Documents\Files\programmes\projet-scrap\index.html"

# Lecture du fichier CSV
df = pd.read_csv(input_path)

# --- Normalisation de la colonne 'indice' ---
df["indice"] = df["indice"].str.strip().str.capitalize()

# --- Filtrage des collaborations (avec un 'x' au milieu des noms) ---
df_filtre = df[~df["nom"].str.contains(" x ", case=False, na=False)]

# --- Filtrage des indices "Bon" et "Excellent" ---
bons_indices = ["Bon", "Excellent"]
df_filtre = df_filtre[df_filtre["indice"].isin(bons_indices)]

# --- Filtrage des prix (en dessous de 300€ ou inconnu) ---
df_filtre["prix"] = df_filtre["prix"].replace('', np.nan)
df_filtre["prix_num"] = pd.to_numeric(df_filtre["prix"].str.replace('€', ''), errors='coerce')
df_filtre = df_filtre[(df_filtre["prix_num"].isna()) | (df_filtre["prix_num"] <= 300)]

# --- Extraction du modèle et nettoyage du nom d'origine ---
def process_name_and_model(name):
    """
    Extrait le modèle en se basant sur la dernière paire de guillemets et nettoie le nom d'origine.
    """
    name_str = str(name)
    # Regex améliorée pour capturer le texte entre la dernière paire de guillemets simples ou doubles
    match = re.search(r'["\']([^"\']+)["\']$', name_str)
    
    if match:
        model = match.group(1)
        # Nettoie le nom d'origine
        clean_name = name_str[:match.start()].strip()
        return clean_name, model
    else:
        return name_str, ""

# Applique la fonction et crée les deux colonnes 'nom_propre' et 'modele'
df_filtre[['nom_propre', 'modele']] = df_filtre['nom'].apply(process_name_and_model).tolist()
df_filtre = df_filtre.drop(columns=['nom'])

# --- Sauvegarde du fichier HTML ---
html_output = df_filtre[['nom_propre', 'modele', 'indice', 'prix', 'url']].to_html(
    index=False,
    escape=False,
    classes='table table-striped'
)

html_header = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; margin: 20px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
    tr:nth-child(even) { background-color: #f9f9f9; }
</style>
</head>
<body>
"""

html_footer = """
</body>
</html>
"""

# Écrit le tout dans un fichier HTML
with open(output_path, 'w', encoding="utf-8-sig") as f:
    f.write(html_header)
    f.write(html_output)
    f.write(html_footer)

print(f"✅ Sneakers filtrées sauvegardées dans : {output_path}")
print(f"Nombre de sneakers gardées : {len(df_filtre)}")