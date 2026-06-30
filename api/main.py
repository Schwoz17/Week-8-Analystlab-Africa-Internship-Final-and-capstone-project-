import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# PATH SETUP
# Same fix as app/app.py: add the project root to sys.path based on this
# file's own location, not on whatever directory the server happens to be
# launched from. Without this, `uvicorn api.main:app` only works if you're
# standing in the project root when you run it — `cd api && uvicorn main:app`
# would break with ModuleNotFoundError: No module named 'src'.
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.predict import predict_life_expectancy  # noqa: E402

# Create the FastAPI application
app = FastAPI(
    title="Life Expectancy Prediction API",
    description="Predict life expectancy using socioeconomic indicators.",
    version="1.0.0"
)


# Define the input data structure.
# Bounds here mirror the Streamlit form exactly, so the same request that
# the UI would never let a user submit can't sneak in through curl/Postman
# either. The model was trained on 2000–2023 data with GDP per capita
# topping out around 19,500 — values outside these ranges are technically
# accepted by the regressor (it'll just extrapolate), so the validation
# below is about keeping inputs honest, not about what the model can
# mathematically swallow.
class PredictionInput(BaseModel):
    Year: int = Field(..., ge=2000, le=2023, description="Year the indicators were recorded (2000–2023).")
    Access_to_electricity: float = Field(..., ge=0, le=100, description="Access to electricity (% of population).")
    Current_health_expenditure: float = Field(..., ge=0, le=25, description="Current health expenditure (% of GDP).")
    GDP_per_capita: float = Field(..., ge=0, le=30000, description="GDP per capita, constant 2015 US$.")
    Internet_users: float = Field(..., ge=0, le=100, description="Individuals using the internet (% of population).")
    Basic_sanitation: float = Field(..., ge=0, le=100, description="People using at least basic sanitation services (% of population).")
    Population_growth: float = Field(..., ge=-5, le=10, description="Population growth, annual %.")
    Primary_school_enrollment: float = Field(..., ge=0, le=150, description="Primary school enrollment (% gross).")
    Urban_population: float = Field(..., ge=0, le=100, description="Urban population (% of total population).")


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to the Life Expectancy Prediction API!"
    }


# Health check endpoint — useful for uptime monitoring or a load balancer,
# separate from "/" so the welcome message can change without breaking
# whatever's polling for liveness.
@app.get("/health")
def health():
    return {"status": "ok"}


# Prediction endpoint
@app.post("/predict")
def predict(data: PredictionInput):

    # Convert API input to the format expected by the model
    input_data = {
        "Year": data.Year,
        "Access to electricity (% of population)": data.Access_to_electricity,
        "Current health expenditure (% of GDP)": data.Current_health_expenditure,
        "GDP per capita (constant 2015 US$)": data.GDP_per_capita,
        "Individuals using the Internet (% of population)": data.Internet_users,
        "People using at least basic sanitation services (% of population)": data.Basic_sanitation,
        "Population growth (annual %)": data.Population_growth,
        "School enrollment, primary (% gross)": data.Primary_school_enrollment,
        "Urban population (% of total population)": data.Urban_population
    }

    # Pydantic already validated types and ranges by the time we get here —
    # what's left to fail is the model layer itself: a missing pickle, a
    # feature name mismatch, anything sklearn-internal. Catching that here
    # means a broken model file returns a clean 500 with a real message
    # instead of FastAPI's raw traceback leaking implementation details.
    try:
        prediction = predict_life_expectancy(input_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {e}. Check that the model artifacts in models/ are present and match the expected feature schema."
        )

    return {
        "Predicted Life Expectancy (years)": round(prediction, 2)
    }