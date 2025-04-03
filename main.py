from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO, #niveau minimum des messages affichés
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", #format des messages
    handlers=[logging.StreamHandler()] # envoie des logs dans la console
)
logger = logging.getLogger("FastAPI Loan Predictor")

# Init de fastapi
app = FastAPI()

# Load du model
try:
    model = joblib.load('training/model.pkl')
    scaler = joblib.load('training/scaler.pkl')
    logger.info("Model loaded successfully")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise RuntimeError(status_code=500, detail="Error loading model or scaler")

# Pour utiliser les fichiers dans le dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")

# Input
class LoanInput(BaseModel):
    Gender: int # 0 Male, 1 Female
    Married: int # 0 No, 1 Yes
    Dependents: int 
    Education: int # 0 not graduated, 1 Graduated
    Self_Employed: int # 0 no, 1 yes
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: int
    Credit_History: int # 0 no credit history, 1 yes
    Property_Area: int # 0 Rural, 1 Semi rural, 2 Urban

# Home endpoint
@app.get("/", response_class=HTMLResponse)
# ajouter response_class=HTMLResponse indique a fastapi que la reponse sera du html et non du json (par defaut)
async def home():
    #return {"message": "Welcome to the Loan Prediction API."}

    try:
        # Utilise index.html
        return HTMLResponse(content=open("static/index.html").read(), status_code=200)
        # with open("static/index.html", "r") as file:
        #     logger.info("Home page served")
        #     return file.read()
    except Exception as e:
        logging.error(f"Error serving home page: {e}")
        return HTMLResponse(status_code=500, content="Error loading home page")

loan_mapping = {0: 'Loan not approved', 1: 'Loan approved'}

@app.get("/predict", response_class=HTMLResponse) 
# ajouter response_class=HTMLResponse indique a fastapi que la reponse sera du html et non du json (par defaut)
async def predict():

    try:
        # with open("static/predict.html", "r") as file:
        #     logger.info("Predict page served")
        #     return file.read()
        return HTMLResponse(content=open("static/predict.html").read(), status_code=200)

    except Exception as e:
        logging.error(f"Error serving home page: {e}")
        return HTMLResponse(status_code=500, content="Error loading predict page")


# # Prediction endpoint
# @app.post("/predict")
# async def predict_loan(input: LoanInput):
#     input_dict = {
#         'Gender': input.Gender,
#         'Married': input.Married,
#         'Dependents': input.Dependents,
#         'Education': input.Education,
#         'Self_Employed': input.Self_Employed,
#         'ApplicantIncome': input.ApplicantIncome,
#         'CoapplicantIncome': input.CoapplicantIncome,
#         'LoanAmount': input.LoanAmount,
#         'Loan_Amount_Term': input.Loan_Amount_Term,
#         'Credit_History': input.Credit_History,
#         'Property_Area':input.Property_Area
#     }
#     input_df = pd.DataFrame([input_dict])
#     input_scaled = scaler.transform(input_df)
#     prediction = model.predict(input_scaled)
#     prediction = loan_mapping.get(prediction[0], "Unknown")
#     return {"prediction": prediction}

# Prediction endpoint
@app.post("/predict")
async def predict_loan(request: Request):

    data = await request.json()  # Récupérer les données JSON envoyées

    input_dict = {
        'Gender': data['gender'],
        'Married': data['married'],
        'Dependents': data['dependents'],
        'Education': data['education'],
        'Self_Employed': data['Self_Employed'],
        'ApplicantIncome': data['ApplicantIncome'],
        'CoapplicantIncome': data['CoapplicantIncome'],
        'LoanAmount': data['LoanAmount'],
        'Loan_Amount_Term': data['Loan_Amount_Term'],
        'Credit_History': data['Credit_History'],
        'Property_Area': data['Property_Area']
    }
    
    input_df = pd.DataFrame([input_dict])
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)
    prediction = loan_mapping.get(prediction[0], "Unknown")
    return {"prediction": prediction}


# uvicorn main:app --reload