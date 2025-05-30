from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import psycopg2

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement des modèles
model_xgb_time = joblib.load("models/xgb_model_time.joblib")
model_delay_risk = joblib.load("models/optimized_lgbm_model.joblib")
scaler = joblib.load("models/scaler_xgb_model_time.joblib")
columns = joblib.load("models/X_train_columns.joblib")


def load_data_and_encoders():
    conn = psycopg2.connect(
        host="db",
        database="avions",
        user="user",
        password="password"
    )
    data = pd.read_sql("SELECT * FROM compagnie", conn)
    if data.empty:
        return data, None, None, None

    le_compagnie = LabelEncoder()
    le_depart = LabelEncoder()
    le_arrivee = LabelEncoder()

    data["Compagnie_enc"] = le_compagnie.fit_transform(data["compagnie"])
    data["Depart_enc"] = le_depart.fit_transform(data["Aéroport d'origine"])
    data["Arrivee_enc"] = le_arrivee.fit_transform(data["Aéroport de destination"])

    return data, le_compagnie, le_depart, le_arrivee


@app.get("/compagnies")
def get_compagnies():
    data, le_compagnie, _, _ = load_data_and_encoders()
    if le_compagnie is None:
        return {"compagnies": []}
    return {"compagnies": le_compagnie.classes_.tolist()}


@app.get("/airports")
def get_airports(compagnie: str):
    data, le_compagnie, le_depart, le_arrivee = load_data_and_encoders()
    if le_compagnie is None:
        return {"departs": [], "arrivees": []}
    comp_encoded = le_compagnie.transform([compagnie])[0]
    subset = data[data["Compagnie_enc"] == comp_encoded]
    departs = le_depart.inverse_transform(subset["Depart_enc"].unique())
    arrivees = le_arrivee.inverse_transform(subset["Arrivee_enc"].unique())
    return {"departs": sorted(departs), "arrivees": sorted(arrivees)}


@app.get("/predict_risk")
def predict_risk(compagnie: str, depart: str, arrivee: str, mois: int):
    data, le_compagnie, le_depart, le_arrivee = load_data_and_encoders()
    if le_compagnie is None:
        return {"risk": None}
    comp = le_compagnie.transform([compagnie])[0]
    dep = le_depart.transform([depart])[0]
    arr = le_arrivee.transform([arrivee])[0]
    input_data = [[comp, dep, arr, mois]]
    prediction = model_delay_risk.predict(input_data)[0]
    return {"risk": float(prediction)}


@app.get("/predict_time")
def predict_time(compagnie: str, depart: str, arrivee: str, mois: int):
    data, le_compagnie, le_depart, le_arrivee = load_data_and_encoders()
    if le_compagnie is None:
        return {"time": None}
    comp = le_compagnie.transform([compagnie])[0]
    dep = le_depart.transform([depart])[0]
    arr = le_arrivee.transform([arrivee])[0]
    df_input = pd.DataFrame([[comp, dep, arr, mois, 50, 48, 2]], columns=[
        'compagnie', 'Aéroport d\'origine', 'Aéroport de destination', 'Mois',
        'Nombre de vols prévus', 'Nombre de vols effectués', 'Nombre de vols annulés'
    ])
    df_encoded = pd.get_dummies(df_input, drop_first=True)
    df_encoded = df_encoded.reindex(columns=columns, fill_value=0)
    scaled = scaler.transform(df_encoded)
    prediction = model_xgb_time.predict(scaled)[0]
    return {"time": float(prediction)}
