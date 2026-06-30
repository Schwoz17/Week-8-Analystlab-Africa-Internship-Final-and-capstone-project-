"""
predict.py
----------
Core inference logic for the Life Expectancy Prediction project.

Loads the pre-trained Random Forest model and the feature ordering used
during training, then exposes a single public function — predict_life_expectancy —
that the Streamlit app (and the FastAPI service, if you wire it up later)
calls directly. No retraining, no dataset loading. Just inference.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

# Resolve paths relative to this file, not the working directory the app
# happens to be launched from. Saves a whole class of "works on my machine"
# bugs when app.py is run from a different folder.
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "random_forest_model.pkl"
FEATURES_PATH = BASE_DIR / "models" / "feature_names.pkl"

_model = None
_feature_names = None


def _load_artifacts():
    """Lazy-load the model and feature list once, then cache in memory.

    Streamlit reruns the whole script on every interaction, so without this
    guard you'd be reloading a Random Forest off disk on every slider drag.
    Not ideal. Both artifacts were saved with joblib, so they're loaded with
    joblib.load() rather than pickle — joblib is the format sklearn itself
    recommends for persisting models, since it's more efficient with the
    numpy arrays that live inside a fitted RandomForestRegressor.
    """
    global _model, _feature_names

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    if _feature_names is None:
        _feature_names = joblib.load(FEATURES_PATH)

    return _model, _feature_names


def predict_life_expectancy(data: dict) -> float:
    """
    Predict life expectancy at birth (years) from country-level indicators.

    Parameters
    ----------
    data : dict
        Dictionary keyed by feature name, e.g.:
        {
            "Year": 2023,
            "Access to electricity (% of population)": 62.4,
            "Current health expenditure (% of GDP)": 3.8,
            "GDP per capita (constant 2015 US$)": 2100.0,
            "Individuals using the Internet (% of population)": 38.0,
            "People using at least basic sanitation services (% of population)": 45.0,
            "Population growth (annual %)": 2.5,
            "School enrollment, primary (% gross)": 95.0,
            "Urban population (% of total population)": 53.0,
        }

    Returns
    -------
    float
        Predicted life expectancy at birth, in years.
    """
    model, feature_names = _load_artifacts()

    # Build a single-row DataFrame, ordered exactly the way the model expects.
    # Order matters more than people think with sklearn — get this wrong and
    # you get a confident, silently wrong prediction. No error, just garbage.
    row = pd.DataFrame([[data[name] for name in feature_names]], columns=feature_names)

    prediction = model.predict(row)
    return float(np.round(prediction[0], 1))