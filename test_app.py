import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

# Test home route
def test_home():
    response = client.get("/")
    assert response.status_code == 200, 'Failed to load the home page'
    assert "Welcome to Loan Prediction" in response.text

# Test predict page route
def test_predict_page():
    response = client.get("/predict")
    assert response.status_code == 200, 'Failed to load the predict page'

def test_prediction():
    payload = {
        'Gender': 1,
        'Married': 1,
        'Dependents': 4,
        'Education': 1,
        'Self_Employed': 0,
        'ApplicantIncome': 35000,
        'CoapplicantIncome': 35000,
        'LoanAmount': 200000,
        'Loan_Amount_Term': 360,
        'Credit_History': 0,
        'Property_Area': 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200, 'Failed to predict'
    assert "prediction" in response.json(), 'Response missing prediction field'

# pour tester :
# pytest test_app.py