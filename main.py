from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib

app = FastAPI()

# Cargar el modelo
model = joblib.load('modelo_expectativa_vida.joblib')

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://34.207.209.193:8000",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    bmi: float
    total_expenditure: float

@app.get("/hi")
def index():
    return {"Hello": "Mundo"}

@app.post("/predict")
def predict(item: Item):
    # Crear un DataFrame con los datos de entrada
    data = {' BMI ': [item.bmi], 'Total expenditure': [item.total_expenditure]}
    df = pd.DataFrame(data)

    # Hacer una predicción utilizando el modelo
    prediction = model.predict(df)

    # Devolver la predicción
    return {"prediction": prediction[0]}
