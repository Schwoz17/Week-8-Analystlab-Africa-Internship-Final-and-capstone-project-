# Life Expectancy Prediction using World Bank Development Indicators

## Project Overview

This project predicts **life expectancy at birth** for Sub-Saharan African countries using socioeconomic indicators from the **World Bank Development Indicators (WDI)** dataset.

The project covers the complete machine learning workflow:

- Data collection and preprocessing
- Exploratory Data Analysis (EDA)
- Feature engineering
- Model training and evaluation
- Model comparison
- Model deployment using FastAPI
- Interactive web application using Streamlit

---

## Project Objective

The objective of this project is to predict a country's life expectancy using national development indicators such as:

- Access to electricity
- GDP per capita
- Internet usage
- Health expenditure
- Basic sanitation
- Population growth
- Primary school enrollment
- Urban population

---

## Project Structure

```
Life_Expectancy_Prediction_WDI/
│
├── app/
│   ├── __init__.py
│   └── app.py                  # Streamlit application
│
├── api/
│   ├── __init__.py
│   └── main.py                 # FastAPI application
│
├── assets/                     # Screenshots and images
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── random_forest_model.pkl
│   └── feature_names.pkl
│
├── notebooks/
│   └── Life_Expectancy_Prediction.ipynb
│
├── reports/
│
├── src/
│   ├── __init__.py
│   └── predict.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## Dataset

**Source:** World Bank World Development Indicators (WDI)

**Region:** 48 Sub-Saharan African Countries

**Period:** 2000–2023

**Target Variable:** Life expectancy at birth (years)

Raw WDI exports live in `data/raw/` but are not tracked in this repository, since they're large and can be re-downloaded directly from the World Bank source. The cleaned dataset used for training is tracked in `data/processed/`.

---

## Features Used

- Year
- Access to electricity (% of population)
- Current health expenditure (% of GDP)
- GDP per capita (constant 2015 US$)
- Individuals using the Internet (% of population)
- People using at least basic sanitation services (% of population)
- Population growth (annual %)
- School enrollment, primary (% gross)
- Urban population (% of total population)

---

## Machine Learning Models

The following regression models were trained and evaluated on a held-out test set:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

### Model Performance

| Model | MAE | RMSE | R² Score |
|------|------:|------:|------:|
| Linear Regression | 3.61 | 4.67 | 0.565 |
| Random Forest | **1.73** | **3.17** | **0.799** |
| Gradient Boosting | 2.22 | 3.31 | 0.781 |

The Random Forest Regressor achieved the best performance and was selected for deployment.

---

## Deployment

The project includes two separate, independently runnable services:

- **Streamlit Web Application** — a frontend that loads the trained model and calls `predict_life_expectancy()` directly from `src/predict.py`. It does not go through the FastAPI layer.
- **FastAPI REST API** — a separate HTTP interface to the same prediction function, exposed at `/predict`, intended for programmatic access rather than for the Streamlit app to consume.

Both read from the same `models/` artifacts but operate independently of each other.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Matplotlib
- Seaborn
- Streamlit
- FastAPI
- Uvicorn

---

## Installation

Clone the repository

```bash
git clone https://github.com/Schwoz17/Life_Expectancy_Prediction_WDI.git
```

Navigate into the project

```bash
cd Life_Expectancy_Prediction_WDI
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Streamlit App

```bash
streamlit run app/app.py
```

---

## Run the FastAPI Server

```bash
python -m uvicorn api.main:app --reload
```

API documentation (interactive Swagger UI): http://127.0.0.1:8000/docs

---

## Application Preview

*(Add screenshots here once available — e.g. `assets/homepage.png`, `assets/prediction.png`)*

---

### Deployment Note

The Streamlit application performs predictions directly using the trained Random Forest model.

A FastAPI backend is included in the repository to demonstrate API development. For the deployed version, the Streamlit app does not call the hosted API because free-tier hosting services may introduce cold-start delays, resulting in a slower user experience.

## Future Improvements

- Include additional socioeconomic indicators
- Deploy the application to the cloud
- Support predictions for multiple countries simultaneously
- Automatically retrieve the latest World Bank data

---

## Author

**Adeyemi Muiz**

GitHub: `https://www.github.com/Schwoz17`

LinkedIn: `https://www.linkedin.com/in/adeyemimuiz`

Streamlit app: `https://wdi-life-expectancy-prediction.streamlit.app/`
