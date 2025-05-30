CREATE TABLE compagnie (
    "Type de vol" TEXT,
    Mois INTEGER,
    Annee INTEGER,
    Nature TEXT,
    "Aéroport d'origine" TEXT,
    "Aéroport de destination" TEXT,
    compagnie TEXT,
    "Nombre de vols prévus" INTEGER,
    "Nombre de vols effectués" INTEGER,
    "Taux de réalisation" FLOAT,
    "Nombre de vols irréguliers" FLOAT,  -- <- ici
    "Nombre de vols annulés" INTEGER,
    "Taux d'irrégularité" FLOAT,
    "Retard moyen" FLOAT,
    "Code compagnie" TEXT,
    "Code aéroport origine" TEXT,
    "Code aéroport destination" TEXT,
    Rang INTEGER
);

COPY compagnie (
    "Type de vol",
    Mois,
    Annee,
    Nature,
    "Aéroport d'origine",
    "Aéroport de destination",
    compagnie,
    "Nombre de vols prévus",
    "Nombre de vols effectués",
    "Taux de réalisation",
    "Nombre de vols irréguliers",
    "Nombre de vols annulés",
    "Taux d'irrégularité",
    "Retard moyen",
    "Code compagnie",
    "Code aéroport origine",
    "Code aéroport destination",
    Rang
)
FROM '/docker-entrypoint-initdb.d/avion_par_compagnie_clean.csv'
DELIMITER ','
CSV HEADER;
