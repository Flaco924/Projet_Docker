import streamlit as st
import requests
import pydeck as pdk
import pandas as pd
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("✈️ Flight Delay Prediction")

# 🎯 Load compagnie options
compagnies_response = requests.get(f"{API_URL}/compagnies")
compagnies = compagnies_response.json()["compagnies"]

selected_compagnie = st.selectbox("Select Airline Company", compagnies)

if selected_compagnie:
    airports_response = requests.get(f"{API_URL}/airports", params={"compagnie": selected_compagnie})
    airports_data = airports_response.json()

    depart_options = airports_data["departs"]
    arrivee_options = airports_data["arrivees"]

    selected_depart = st.selectbox("Select Departure Airport", depart_options)
    selected_arrivee = st.selectbox("Select Arrival Airport", arrivee_options)
    selected_month = st.selectbox("Select Departure Month", list(range(1, 13)))

    if st.button("Predict Delay"):
        params = {
            "compagnie": selected_compagnie,
            "depart": selected_depart,
            "arrivee": selected_arrivee,
            "mois": selected_month
        }

        delay_response = requests.get(f"{API_URL}/predict_risk", params=params).json()
        time_response = requests.get(f"{API_URL}/predict_time", params=params).json()

        st.markdown(f"### ⏱️ Predicted Delay Time: `{time_response['time']:.2f} min`")
        st.markdown(f"### ⚠️ Predicted Delay Risk: `{delay_response['risk']:.2f}%`")

        # Optional map (if airports in dict)
        airport_locations = {
            "ABIDJAN": {"lat": 5.256, "lon": -3.926},
            "ABU DHABI": {"lat": 24.456, "lon": 54.375},
            "AGADIR": {"lat": 30.325, "lon": -9.413},
            "AJACCIO": {"lat": 41.923, "lon": 8.802},
            "ALGER": {"lat": 36.697, "lon": 3.215},
            "AMSTERDAM": {"lat": 52.309, "lon": 4.763},
            "ATHÈNES": {"lat": 37.936, "lon": 23.947},
            "ATLANTA": {"lat": 33.640, "lon": -84.427},
            "BÂLE-MULHOUSE": {"lat": 47.599, "lon": 7.529},
            "BANGKOK": {"lat": 13.693, "lon": 100.751},
            "BARCELONE": {"lat": 41.297, "lon": 2.083},
            "BASTIA": {"lat": 42.552, "lon": 9.484},
            "BERLIN-TEGEL": {"lat": 52.559, "lon": 13.287},
            "BEYROUTH": {"lat": 33.820, "lon": 35.488},
            "BIARRITZ": {"lat": 43.468, "lon": -1.523},
            "BIRMINGHAM": {"lat": 52.453, "lon": -1.748},
            "BOLOGNE": {"lat": 44.535, "lon": 11.288},
            "BORDEAUX": {"lat": 44.830, "lon": -0.704},
            "BOSTON": {"lat": 42.365, "lon": -71.009},
            "BREST": {"lat": 48.448, "lon": -4.419},
            "BRUXELLES": {"lat": 50.901, "lon": 4.485},
            "BUCAREST-OTOPENI": {"lat": 44.571, "lon": 26.085},
            "BUDAPEST": {"lat": 47.439, "lon": 19.261},
            "CALVI": {"lat": 42.524, "lon": 8.793},
            "CASABLANCA": {"lat": 33.367, "lon": -7.589},
            "CAYENNE": {"lat": 4.821, "lon": -52.365},
            "CHICAGO-O'HARE": {"lat": 41.974, "lon": -87.907},
            "CLERMONT-FERRAND": {"lat": 45.786, "lon": 3.169},
            "COPENHAGUE": {"lat": 55.618, "lon": 12.656},
            "DAKAR": {"lat": 14.674, "lon": -17.499},
            "DELHI": {"lat": 28.556, "lon": 77.100},
            "DETROIT": {"lat": 42.212, "lon": -83.353},
            "DJERBA": {"lat": 33.875, "lon": 10.775},
            "DOHA": {"lat": 25.273, "lon": 51.608},
            "DUBAI": {"lat": 25.253, "lon": 55.364},
            "DUBLIN": {"lat": 53.427, "lon": -6.243},
            "DÜSSELDORF": {"lat": 51.290, "lon": 6.766},
            "EDIMBOURG": {"lat": 55.950, "lon": -3.372},
            "FIGARI": {"lat": 41.501, "lon": 9.097},
            "FLORENCE": {"lat": 43.810, "lon": 11.204},
            "FORT DE FRANCE": {"lat": 14.591, "lon": -61.003},
            "FRANCFORT": {"lat": 50.033, "lon": 8.570},
            "GENÈVE": {"lat": 46.238, "lon": 6.109},
            "GUANGZHOU": {"lat": 23.392, "lon": 113.299},
            "HAMBOURG": {"lat": 53.630, "lon": 9.991},
            "HELSINKI": {"lat": 60.317, "lon": 24.963},
            "HONG KONG": {"lat": 22.308, "lon": 113.918},
            "ISTANBUL-ATATURK": {"lat": 40.977, "lon": 28.821},
            "ISTANBUL-SABIHA GOKCEN": {"lat": 40.899, "lon": 29.309},
            "JOHANNESBOURG": {"lat": -26.139, "lon": 28.246},
            "KIEV": {"lat": 50.345, "lon": 30.893},
            "LA HAVANE": {"lat": 22.989, "lon": -82.409},
            "LE CAIRE": {"lat": 30.121, "lon": 31.405},
            "LILLE": {"lat": 50.561, "lon": 3.088},
            "LISBONNE": {"lat": 38.774, "lon": -9.135},
            "LONDRES CITY": {"lat": 51.505, "lon": 0.055},
            "LONDRES-GATWICK": {"lat": 51.153, "lon": -0.182},
            "LONDRES-HEATHROW": {"lat": 51.470, "lon": -0.454},
            "LONDRES-LUTON": {"lat": 51.879, "lon": -0.376},
            "LORIENT": {"lat": 47.760, "lon": -3.440},
            "LOS ANGELES": {"lat": 33.941, "lon": -118.408},
            "LUXEMBOURG": {"lat": 49.623, "lon": 6.204},
            "LYON": {"lat": 45.726, "lon": 5.090},
            "MADRID": {"lat": 40.471, "lon": -3.562},
            "MALAGA": {"lat": 36.676, "lon": -4.499},
            "MANCHESTER": {"lat": 53.364, "lon": -2.272},
            "MARRAKECH": {"lat": 31.607, "lon": -8.036},
            "MARSEILLE": {"lat": 43.436, "lon": 5.214},
            "MAURICE": {"lat": -20.430, "lon": 57.683},
            "MEXICO CITY": {"lat": 19.436, "lon": -99.072},
            "MIAMI": {"lat": 25.793, "lon": -80.290},
            "MILAN-BERGAME": {"lat": 45.668, "lon": 9.704},
            "MILAN-LINATE": {"lat": 45.448, "lon": 9.278},
            "MILAN-MALPENSA": {"lat": 45.630, "lon": 8.728},
            "MINNEAPOLIS": {"lat": 44.884, "lon": -93.222},
            "MONTPELLIER": {"lat": 43.576, "lon": 3.963},
            "MONTREAL": {"lat": 45.470, "lon": -73.740},
            "MOSCOU": {"lat": 55.972, "lon": 37.414},
            "MUMBAI/BOMBAY": {"lat": 19.089, "lon": 72.867},
            "MUNICH": {"lat": 48.354, "lon": 11.786},
            "NANTES": {"lat": 47.153, "lon": -1.611},
            "NAPLES": {"lat": 40.884, "lon": 14.291},
            "NEW YORK-KENNEDY": {"lat": 40.641, "lon": -73.778},
            "NEW YORK-NEWARK": {"lat": 40.692, "lon": -74.168},
            "NICE": {"lat": 43.658, "lon": 7.215},
            "ORAN": {"lat": 35.623, "lon": -0.621},
            "OSLO": {"lat": 60.193, "lon": 11.100},
            "OUJDA": {"lat": 34.787, "lon": -1.923},
            "PARIS-CDG": {"lat": 49.009, "lon": 2.547},
            "PARIS-ORLY": {"lat": 48.726, "lon": 2.365},
            "PAU": {"lat": 43.380, "lon": -0.418},
            "PÉKIN": {"lat": 40.080, "lon": 116.584},
            "PERPIGNAN": {"lat": 42.740, "lon": 2.871},
            "POINTE A PITRE": {"lat": 16.265, "lon": -61.528},
            "PORTO": {"lat": 41.248, "lon": -8.681},
            "PRAGUE": {"lat": 50.101, "lon": 14.263},
            "PUNTA CANA": {"lat": 18.567, "lon": -68.363},
            "RENNES": {"lat": 48.069, "lon": -1.734},
            "REYKJAVIK": {"lat": 64.136, "lon": -21.939},
            "RIO DE JANEIRO": {"lat": -22.809, "lon": -43.243},
            "ROME-CIAMPINO": {"lat": 41.799, "lon": 12.595},
            "ROME-FIUMICINO": {"lat": 41.800, "lon": 12.238},
            "SAINT DENIS": {"lat": -20.892, "lon": 55.517}
        }

        if selected_depart in airport_locations and selected_arrivee in airport_locations:
            dep_coords = airport_locations[selected_depart]
            arr_coords = airport_locations[selected_arrivee]

            map_data = pd.DataFrame([
                {"lat": dep_coords["lat"], "lon": dep_coords["lon"], "name": "Departure"},
                {"lat": arr_coords["lat"], "lon": arr_coords["lon"], "name": "Arrival"},
            ])

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=(dep_coords["lat"] + arr_coords["lat"]) / 2,
                    longitude=(dep_coords["lon"] + arr_coords["lon"]) / 2,
                    zoom=4,
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=map_data,
                        get_position='[lon, lat]',
                        get_color='[255, 0, 0]',
                        get_radius=70000,
                    ),
                    pdk.Layer(
                        "ArcLayer",
                        data=pd.DataFrame({
                            'start_lat': [dep_coords["lat"]],
                            'start_lon': [dep_coords["lon"]],
                            'end_lat': [arr_coords["lat"]],
                            'end_lon': [arr_coords["lon"]],
                        }),
                        get_source_position=["start_lon", "start_lat"],
                        get_target_position=["end_lon", "end_lat"],
                        get_width=5,
                        get_color=[255, 0, 0],
                    )
                ]
            ))
