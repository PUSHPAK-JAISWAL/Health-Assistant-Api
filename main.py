import os
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Health Assistant API")

# Setup CORS middleware to allow any frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determine the working directory similar to how you did in your Streamlit app
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load the saved models
try:
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
    parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
except Exception as e:
    raise RuntimeError("Error loading model files: " + str(e))

# Pydantic models for request payloads
class DiabetesInput(BaseModel):
    Pregnancies: float
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float

class HeartDiseaseInput(BaseModel):
    age: float
    sex: float
    cp: float
    trestbps: float
    chol: float
    fbs: float
    restecg: float
    thalach: float
    exang: float
    oldpeak: float
    slope: float
    ca: float
    thal: float

class ParkinsonsInput(BaseModel):
    fo: float
    fhi: float
    flo: float
    Jitter_percent: float
    Jitter_Abs: float
    RAP: float
    PPQ: float
    DDP: float
    Shimmer: float
    Shimmer_dB: float
    APQ3: float
    APQ5: float
    APQ: float
    DDA: float
    NHR: float
    HNR: float
    RPDE: float
    DFA: float
    spread1: float
    spread2: float
    D2: float
    PPE: float

# Endpoints

@app.post("/predict/diabetes")
def predict_diabetes(data: DiabetesInput):
    """Predicts whether a person is diabetic."""
    try:
        # Prepare the input list (model expects a 2D list)
        user_input = [[
            data.Pregnancies, data.Glucose, data.BloodPressure, data.SkinThickness,
            data.Insulin, data.BMI, data.DiabetesPedigreeFunction, data.Age
        ]]
        prediction = diabetes_model.predict(user_input)
        diagnosis = 'The person is diabetic' if prediction[0] == 1 else 'The person is not diabetic'
        return {"prediction": diagnosis}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction failed: " + str(e))


@app.post("/predict/heart")
def predict_heart(data: HeartDiseaseInput):
    """Predicts whether a person has heart disease."""
    try:
        user_input = [[
            data.age, data.sex, data.cp, data.trestbps, data.chol, data.fbs,
            data.restecg, data.thalach, data.exang, data.oldpeak, data.slope,
            data.ca, data.thal
        ]]
        prediction = heart_disease_model.predict(user_input)
        diagnosis = "The person is having heart disease" if prediction[0] == 1 else "The person does not have any heart disease"
        return {"prediction": diagnosis}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction failed: " + str(e))


@app.post("/predict/parkinsons")
def predict_parkinsons(data: ParkinsonsInput):
    """Predicts whether a person has Parkinson's disease."""
    try:
        user_input = [[
            data.fo, data.fhi, data.flo, data.Jitter_percent, data.Jitter_Abs,
            data.RAP, data.PPQ, data.DDP, data.Shimmer, data.Shimmer_dB, data.APQ3,
            data.APQ5, data.APQ, data.DDA, data.NHR, data.HNR, data.RPDE, data.DFA,
            data.spread1, data.spread2, data.D2, data.PPE
        ]]
        prediction = parkinsons_model.predict(user_input)
        diagnosis = "The person has Parkinson's disease" if prediction[0] == 1 else "The person does not have Parkinson's disease"
        return {"prediction": diagnosis}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction failed: " + str(e))


# This block allows the API to be started by clicking Run in most IDEs.
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
