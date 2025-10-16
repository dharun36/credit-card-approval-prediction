import pickle
import numpy as np
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic
from pydantic import BaseModel, Field, validator
import uvicorn
import os

class CreditApplication(BaseModel):
    PriorDefault: int
    CreditScore: float
    YearsEmployed: float
    Income: float
    Employed: int
    Debt: float
    Age: int

    class Config:
        schema_extra = {
            "example": {
                "PriorDefault": 1,
                "CreditScore": 700,
                "YearsEmployed": 5.0,
                "Income": 50000.0,
                "Employed": 1,
                "Debt": 15000.0,
                "Age": 35
            }
        }

    @validator('PriorDefault')
    def validate_prior_default(cls, v):
        if v not in [0, 1]:
            raise ValueError('Prior default must be 0 or 1')
        return v

    @validator('CreditScore')
    def validate_credit_score(cls, v):
        if not 300 <= v <= 850:
            raise ValueError('Credit score must be between 300 and 850')
        return v

    @validator('YearsEmployed')
    def validate_years_employed(cls, v):
        if v < 0:
            raise ValueError('Years employed cannot be negative')
        return v

    @validator('Income')
    def validate_income(cls, v):
        if v < 0:
            raise ValueError('Income cannot be negative')
        return v

    @validator('Employed')
    def validate_employed(cls, v):
        if v not in [0, 1]:
            raise ValueError('Employed must be 0 or 1')
        return v

    @validator('Debt')
    def validate_debt(cls, v):
        if v < 0:
            raise ValueError('Debt cannot be negative')
        return v

    @validator('Age')
    def validate_age(cls, v):
        if not 18 <= v <= 120:
            raise ValueError('Age must be between 18 and 120')
        return v

app = FastAPI(
    title="Credit Card Approval Predictor",
    description="API for predicting credit card application approval",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the model with warning suppression
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# Load the scaler
try:
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
except Exception as e:
    print(f"Error loading scaler: {e}")
    # If scaler is not found, create a new StandardScaler
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()

# Function to scale the features
def scale_features(features):
    features_array = np.array(features).reshape(1, -1)
    return scaler.transform(features_array) if hasattr(scaler, 'mean_') else features_array

try:
    with open('best_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
except Exception as e:
    print(f"Error loading model: {e}")
    raise HTTPException(status_code=500, detail="Model initialization failed")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "prediction": None,
        "error": None
    })

@app.post("/predict")
async def predict(request: Request):
    try:
        # Get JSON data from request
        data = await request.json()
        
        # Create features list from JSON data
        features = [
            int(data['PriorDefault']),
            float(data['CreditScore']),
            float(data['YearsEmployed']),
            float(data['Income']),
            int(data['Employed']),
            float(data['Debt']),
            int(data['Age'])
        ]
        
        # Validate input using pydantic model
        application = CreditApplication(
            PriorDefault=features[0],
            CreditScore=features[1],
            YearsEmployed=features[2],
            Income=features[3],
            Employed=features[4],
            Debt=features[5],
            Age=features[6]
        )
        
        # Scale the features
        scaled_features = scale_features(features)
        prediction = model.predict(scaled_features)
        
        # Get prediction probability if model supports it
        probability = None
        try:
            probability = model.predict_proba(scaled_features)[0][1]
        except:
            pass
        
        # Return JSON response
        response = {
            "approval": bool(prediction[0] == 1),
            "message": "Approved" if prediction[0] == 1 else "Not Approved",
        }
        
        # Add probability if available
        if probability is not None:
            response["probability"] = float(probability)
            response["confidence"] = f"{probability * 100:.1f}%"
            
        return response
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    