import pandas as pd

# Mapping des noms de colonnes incorrects → noms attendus
rename_map = {
    "Mode": "Type de vol",
    "Année": "Annee",
    "Service": "Nature",
    "Compagnie": "compagnie",
    "Nbre mensuel de vols programmés par la Cie sur la relation": "Nombre de vols prévus",
    "Nbre mensuel de vols assurés par la Cie sur la relation": "Nombre de vols effectués",
    "Part (%) de vols assurés par la Cie sur la relation (mois)": "Taux de réalisation",
    "Nbre mensuel de vols annulés par la Cie sur la relation": "Nombre de vols annulés",
    "Part (%) des vols annulés par la Cie sur la relation (mois)": "Taux d'irrégularité",
    "Part (%) des vols exploités par la Cie en retard à l'arrivée sur la relation (mois)": "Retard moyen",
    "Part (%) de la Cie dans les vols en retard à l'arrivée sur la relation (mois)": "Nombre de vols irréguliers",
    "Code Cie": "Code compagnie",
    "Code Aero Départ": "Code aéroport origine",
    "Code Aero Destination": "Code aéroport destination",
    "retards moyennés sur tous les vols de la liaison - compagnie à l'arrivée": "Rang"
}

# Lecture
df = pd.read_csv("init/avion_par_compagnie.csv")

# Renommage
df = df.rename(columns=rename_map)

# Colonnes attendues dans l'ordre
expected_columns = [
    "Type de vol", "Mois", "Annee", "Nature", "Aéroport d'origine", "Aéroport de destination",
    "compagnie", "Nombre de vols prévus", "Nombre de vols effectués", "Taux de réalisation",
    "Nombre de vols irréguliers", "Nombre de vols annulés", "Taux d'irrégularité", "Retard moyen",
    "Code compagnie", "Code aéroport origine", "Code aéroport destination", "Rang"
]

# Filtrer uniquement ces colonnes
df_clean = df[expected_columns]

# Sauvegarde
df_clean.to_csv("init/avion_par_compagnie_clean.csv", index=False)

print("✅ CSV nettoyé enregistré sous 'init/avion_par_compagnie_clean.csv'")
