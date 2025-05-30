from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import psycopg2
from sklearn.preprocessing import LabelEncoder

# Load models and preprocessing
model_xgb_time = joblib.load("../back_flight_delay/models/xgb_model_time.joblib")
model_delay_risk = joblib.load("../back_flight_delay/models/optimized_lgbm_model.joblib")
scaler = joblib.load("../back_flight_delay/models/scaler_xgb_model_time.joblib")
xgb_columns = joblib.load("../back_flight_delay/models/X_train_columns.joblib")

# Connect to DB
conn = psycopg2.connect(
    host="db",
    database="avions",
    user="user",
    password="password"
)
data = pd.read_sql("SELECT * FROM compagnie", conn)

# Encoders
le_compagnie = LabelEncoder()
data["Compagnie_enc"] = le_compagnie.fit_transform(data["compagnie"])
le_depart = LabelEncoder()
data["Depart_enc"] = le_depart.fit_transform(data["depart"])
le_arrivee = LabelEncoder()
data["Arrivee_enc"] = le_arrivee.fit_transform(data["arrivee"])

# API setup
app = FastAPI()

# Allow CORS from front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/compagnies")
def get_compagnies():
    return {"compagnies": sorted(data["compagnie"].unique())}

@app.get("/airports")
def get_airports(compagnie: str = Query(...)):
    df = data[data["compagnie"] == compagnie]
    return {
        "departs": sorted(df["depart"].unique()),
        "arrivees": sorted(df["arrivee"].unique())
    }

@app.get("/predict_risk")
def predict_risk(compagnie: str, depart: str, arrivee: str, mois: int):
    comp = le_compagnie.transform([compagnie])[0]
    dep = le_depart.transform([depart])[0]
    arr = le_arrivee.transform([arrivee])[0]
    input_data = [[comp, dep, arr, mois]]
    risk = model_delay_risk.predict(input_data)[0]
    return {"risk": float(risk)}

@app.get("/predict_time")
def predict_time(compagnie: str, depart: str, arrivee: str, mois: int):
    comp = le_compagnie.transform([compagnie])[0]
    dep = le_depart.transform([depart])[0]
    arr = le_arrivee.transform([arrivee])[0]
    df = pd.DataFrame([[comp, dep, arr, mois, 50, 48, 2]], columns=[
        'Compagnie', 'Aéroport d\'origine', 'Aéroport de destination', 'Mois', 'Scheduled', 'Operated', 'Canceled'
    ])
    df = pd.get_dummies(df, drop_first=True).reindex(columns=xgb_columns, fill_value=0)
    scaled = scaler.transform(df)
    delay_time = model_xgb_time.predict(scaled)[0]
    return {"time": float(delay_time)}
