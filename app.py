from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from pathlib import Path

app = FastAPI(title="Titanic Survival Prediction API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo
MODEL_PATH = "titanic_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"No se encontró el modelo en {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

# Esquemas
class Passenger(BaseModel):
    Name: str
    Pclass: int
    Sex: str
    Age: float
    Fare: float
    Weight : float

class PredictionResponse(BaseModel):
    message: str

# Servir frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def home():
    html_path = Path(__file__).parent / "static" / "index.html"
    return FileResponse(str(html_path))

# Endpoint de predicción
@app.post("/predict", response_model=PredictionResponse)
def predict_survival(passenger: Passenger):
    try:
        sex_encoded = 0 if passenger.Sex.lower() == "male" else 1
        data = pd.DataFrame([{
            "Pclass": passenger.Pclass,
            "Sex_encoded": sex_encoded,
            "Age": passenger.Age,
            "Fare": passenger.Fare
        }])
        prediction = model.predict(data)[0]

        msg = f"{passenger.Name} sobreviviría 🛟" if prediction == 1 else f"{passenger.Name} no sobreviviría 💀"

        return PredictionResponse(message=msg)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {e}")