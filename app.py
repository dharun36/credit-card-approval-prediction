import pickle
import numpy as np
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic
from pydantic import BaseModel, Field, field_validator, ConfigDict
import uvicorn
import os
import logging

class CreditApplication(BaseModel):
    PriorDefault: int
    CreditScore: float
    YearsEmployed: float
    Income: float
    Employed: int
    Debt: float
    Age: int

    # Pydantic v2 configuration and example
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "PriorDefault": 1,
                "CreditScore": 700,
                "YearsEmployed": 5.0,
                "Income": 50000.0,
                "Employed": 1,
                "Debt": 15000.0,
                "Age": 35,
            }
        }
    )

    @field_validator('PriorDefault')
    def validate_prior_default(cls, v):
        if v not in [0, 1]:
            raise ValueError('Prior default must be 0 or 1')
        return v

    @field_validator('CreditScore')
    def validate_credit_score(cls, v):
        if not 300 <= v <= 850:
            raise ValueError('Credit score must be between 300 and 850')
        return v

    @field_validator('YearsEmployed')
    def validate_years_employed(cls, v):
        if v < 0:
            raise ValueError('Years employed cannot be negative')
        return v

    @field_validator('Income')
    def validate_income(cls, v):
        if v < 0:
            raise ValueError('Income cannot be negative')
        return v

    @field_validator('Employed')
    def validate_employed(cls, v):
        if v not in [0, 1]:
            raise ValueError('Employed must be 0 or 1')
        return v

    @field_validator('Debt')
    def validate_debt(cls, v):
        if v < 0:
            raise ValueError('Debt cannot be negative')
        return v

    @field_validator('Age')
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
# Logging level via LOG_LEVEL env (default INFO)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())

# Allow overriding CORS origins with env var ALLOWED_ORIGINS (comma-separated)
_allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
_default_origins = ["http://localhost:8000", "http://127.0.0.1:8000"]
_allowed_origins = (
    [o.strip() for o in _allowed_origins_env.split(",") if o.strip()]
    if _allowed_origins_env else _default_origins
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
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

# Load the scaler (path configurable via SCALER_PATH)
scaler_path = os.getenv("SCALER_PATH", "scaler.pkl")
try:
    with open(scaler_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
except Exception as e:
    # If scaler is not found, create a new StandardScaler (will be pass-through)
    from sklearn.preprocessing import StandardScaler
    logging.warning(f"Scaler not found at '{scaler_path}': {e}. Using pass-through scaling.")
    scaler = StandardScaler()

# Function to scale the features
def scale_features(features):
    features_array = np.array(features).reshape(1, -1)
    return scaler.transform(features_array) if hasattr(scaler, 'mean_') else features_array

# Load the model (path configurable via MODEL_PATH)
model_path = os.getenv("MODEL_PATH", "best_model.pkl")
try:
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
except Exception as e:
    logging.error(f"Error loading model from '{model_path}': {e}")
    raise RuntimeError(f"Model initialization failed: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": hasattr(scaler, 'mean_')
    }

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
        logging.info(f"Prediction: {prediction}")


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
    