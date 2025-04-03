import pytest
from main import model, loan_mapping
import pandas as pd 

def test_model_prediction():
    input_df = pd.DataFrame([[0,0,0,1,0,5849,0,0,360,1,2]],
                            columns=["Gender", "Married", "Dependents", "Education", "Self_Employed", "ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area"])
    
    print(input_df)
    prediction = model.predict(input_df)[0]
    prediction = loan_mapping.get(prediction, "Unknown")

    assert prediction == "Loan approved", 'The prediction did not return the expected result'

