"""
app.py
------
Streamlit frontend for the Life Expectancy Prediction project.

This file is intentionally split into clear sections — path setup, page
config, styling, sidebar, hero, form, prediction, footer — so each part can
be edited independently without hunting through a wall of code. It imports
predict_life_expectancy directly from src/predict.py. The model is not
retrained or reloaded here; this file only collects input and renders output.
"""

import sys
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# PATH SETUP
# So `from src.predict import predict_life_expectancy` works regardless of
# whether you run this with `streamlit run app/app.py` from the project root
# or from inside the app/ folder itself.
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.predict import predict_life_expectancy  # noqa: E402


# ---------------------------------------------------------------------------
# PAGE CONFIG
# Must be the first Streamlit call in the script.
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Life Expectancy Predictor | WDI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# CUSTOM CSS
# This is what pulls the app out of "default Streamlit" territory. Off-white
# paper background, a single terracotta accent, a serif for display type.
# Streamlit's own chrome (the header bar, the hamburger menu) gets dimmed
# down rather than removed outright — some users rely on it, and ripping it
# out entirely tends to break on Streamlit Cloud deployments in ways that
# are annoying to debug.
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --paper: #F6F1E9;
    --paper-warm: #EFE6D8;
    --ink: #2B2420;
    --ink-soft: #5C5248;
    --clay: #B5523B;
    --clay-dark: #963F2C;
    --moss: #6B7A5E;
    --line: #DCD0BC;
    --card: #FFFEFB;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

.stApp {
    background-color: var(--paper);
}

/* Dim Streamlit's default chrome instead of hiding it outright */
header[data-testid="stHeader"] {
    background: transparent;
}
#MainMenu { opacity: 0.35; }

/* Kill the default huge top padding Streamlit adds */
.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1100px;
}

/* ---------- Headings & display type ---------- */
h1, h2, h3, .display-font {
    font-family: 'Fraunces', serif;
    color: var(--ink);
    letter-spacing: -0.01em;
}

.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--clay-dark);
    font-weight: 600;
    margin-bottom: 0.6rem;
}

.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 3rem;
    font-weight: 600;
    line-height: 1.08;
    color: var(--ink);
    margin: 0 0 0.9rem 0;
}

.hero-sub {
    font-size: 1.08rem;
    color: var(--ink-soft);
    max-width: 640px;
    line-height: 1.6;
    margin-bottom: 0;
}

.hero-divider {
    border: none;
    border-top: 1px solid var(--line);
    margin: 2rem 0 2.2rem 0;
}

/* ---------- Section labels ---------- */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--moss);
    font-weight: 600;
    margin-bottom: 0.3rem;
}

/* ---------- Cards ---------- */
.info-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}

.disclaimer-card {
    background: var(--paper-warm);
    border-left: 3px solid var(--clay);
    border-radius: 6px;
    padding: 1rem 1.3rem;
    font-size: 0.92rem;
    color: var(--ink-soft);
    margin: 1.5rem 0 2rem 0;
    line-height: 1.55;
}

/* ---------- Form container ---------- */
div[data-testid="stForm"] {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 2rem 2.2rem 1.4rem 2.2rem;
}

/* ---------- Inputs ---------- */
.stSlider label, .stNumberInput label, .stSelectbox label {
    font-weight: 600 !important;
    color: var(--ink) !important;
    font-size: 0.95rem !important;
}

.stSlider [data-baseweb="slider"] > div > div {
    background: var(--clay) !important;
}

div[data-testid="stNumberInput"] input, div[data-baseweb="select"] {
    border-radius: 8px !important;
}

/* ---------- Buttons ---------- */
.stFormSubmitButton button, .stButton button {
    background: var(--clay) !important;
    color: #FFFEFB !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.6rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.01em;
    transition: background 0.15s ease, transform 0.1s ease;
    width: 100%;
}

.stFormSubmitButton button:hover, .stButton button:hover {
    background: var(--clay-dark) !important;
    transform: translateY(-1px);
}

/* ---------- Result card ---------- */
.result-wrap {
    background: linear-gradient(135deg, #2B2420 0%, #423832 100%);
    border-radius: 18px;
    padding: 2.4rem 2.6rem;
    margin-top: 1.6rem;
    color: #F6F1E9;
}

.result-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #C9A88A;
    margin-bottom: 0.4rem;
}

.result-number {
    font-family: 'Fraunces', serif;
    font-size: 4.2rem;
    font-weight: 600;
    line-height: 1;
    margin: 0.2rem 0;
}

.result-unit {
    font-size: 1.4rem;
    font-weight: 400;
    color: #D9CBB8;
}

.result-context {
    font-size: 0.95rem;
    color: #D9CBB8;
    margin-top: 0.8rem;
    line-height: 1.55;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--paper-warm);
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* ---------- Footer ---------- */
.site-footer {
    text-align: center;
    color: var(--ink-soft);
    font-size: 0.82rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--line);
}

/* ---------- Metric chips for grouped inputs ---------- */
.group-title {
    font-family: 'Fraunces', serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--ink);
    margin-bottom: 0.2rem;
    margin-top: 0.6rem;
}

.group-sub {
    font-size: 0.85rem;
    color: var(--ink-soft);
    margin-bottom: 1rem;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# SIDEBAR
# Instructions live here, kept short on purpose — nobody reads a wall of
# text before they've even seen what the tool does. Model Information
# includes both R² and MAE so the reader gets a sense of typical error
# magnitude, not just variance explained.
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<div class='hero-eyebrow'>How this works</div>",
        unsafe_allow_html=True,
    )
    st.markdown("### Quick guide")
    st.markdown(
        """
        1. **Fill in the nine indicators** below — these describe a country
           in a given year, not an individual person.
        2. **Enter values** for each field, or use the +/- controls to
           adjust them precisely.
        3. **Click Predict** to run the trained Random Forest model.
        4. **Read the result** as a statistical estimate, not a guarantee.
        """
    )
    st.markdown("---")
    st.markdown(
        "<div class='hero-eyebrow'>Data source</div>",
        unsafe_allow_html=True,
    )
    st.caption(
        "World Bank World Development Indicators (WDI). Model: Random "
        "Forest Regressor, trained offline and loaded from models/."
    )
    st.markdown("---")
    st.markdown(
        "<div class='hero-eyebrow'>About the model</div>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Nine country-level features feed the model — access to "
        "electricity, health spend, GDP per capita, internet use, "
        "sanitation access, population growth, primary enrollment, and "
        "urbanization. The target is life expectancy at birth, in years."
    )
    st.markdown("---")
    st.markdown(
        "<div class='hero-eyebrow'>Model information</div>",
        unsafe_allow_html=True,
    )
    st.caption(
        "**Model:** Random Forest Regressor  \n"
        "**Dataset:** World Bank Development Indicators (WDI)  \n"
        "**Region:** 48 Sub-Saharan African Countries  \n"
        "**Training Period:** 2000–2023  \n"
        "**Model Performance:**  \n"
        "&nbsp;&nbsp;• R² Score: 0.80  \n"
        "&nbsp;&nbsp;• MAE: 1.73 years"
    )


# ---------------------------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------------------------
st.markdown("<div class='hero-eyebrow'>World Bank Development Indicators · ML Forecast</div>", unsafe_allow_html=True)
st.markdown("<h1 class='hero-title'>Life Expectancy Prediction using World Bank Development Indicators</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <p class='hero-sub'>
    This application uses a Random Forest Regression model trained on World
    Bank Development Indicators (WDI) from 48 Sub-Saharan African countries
    to estimate life expectancy at birth. Adjust the national socioeconomic
    indicators below to explore how changes in development factors may
    influence the predicted life expectancy.
    </p>
    """,
    unsafe_allow_html=True,
)
st.markdown("<hr class='hero-divider'>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# DISCLAIMER
# Required, and frankly should be load-bearing — this is the difference
# between a useful policy tool and something that gets misread as medical
# advice for a specific person. It isn't. Worth saying plainly.
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class='disclaimer-card'>
    <strong>This tool estimates national averages, not individuals.</strong>
    Every input below is a country-level socioeconomic indicator from the
    World Bank's WDI dataset — none of it describes a single person's health,
    habits, or risk factors. The output is a statistical estimate intended
    for educational and analytical exploration, not a clinical, actuarial,
    or policy-grade forecast. Treat it the way you'd treat a back-of-envelope
    calculation: useful for intuition, not for decisions that matter.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# INPUT FORM
# Grouped into three logical clusters — Economy & Time, Access & Services,
# Demographics — rather than nine widgets dumped in a flat list. Grouping
# like this gives the eye somewhere to rest, and honestly nine inputs in a
# row is exhausting to fill out.
#
# All nine fields are now st.number_input rather than a mix of sliders and
# number inputs — same min/max/default/step/help as before, just a typed
# field with +/- steppers instead of a drag handle.
# ---------------------------------------------------------------------------
with st.form("prediction_form"):

    # --- Group 1: Economy & Time ---
    st.markdown("<div class='group-title'>Economy &amp; time</div>", unsafe_allow_html=True)
    st.markdown("<div class='group-sub'>When, and how wealthy.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input(
            "Year",
            min_value=2000,
            max_value=2023,
            value=2023,
            step=1,
            help="The calendar year the indicators were recorded. The "
                 "model was trained on WDI data from 2000 to 2023, so "
                 "predictions outside that range aren't supported.",
        )
    with col2:
        gdp_per_capita = st.number_input(
            "GDP per capita (constant 2015 US$)",
            min_value=0.0,
            max_value=30000.0,
            value=2500.0,
            step=100.0,
            help="Gross domestic product divided by population, in constant "
                 "2015 US dollars. Capped at 30,000 to stay within the range "
                 "the model was actually trained on (max ~19,500 in the "
                 "training data).",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Group 2: Access & Services ---
    st.markdown("<div class='group-title'>Access &amp; services</div>", unsafe_allow_html=True)
    st.markdown("<div class='group-sub'>What share of the population can reach basic infrastructure.</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        electricity_access = st.number_input(
            "Access to electricity (% of population)",
            min_value=0.0,
            max_value=100.0,
            value=65.0,
            step=0.5,
            help="Share of the population with access to electricity, "
                 "from any source — grid or off-grid.",
        )
        sanitation_access = st.number_input(
            "Basic sanitation services (% of population)",
            min_value=0.0,
            max_value=100.0,
            value=55.0,
            step=0.5,
            help="Share of the population using at least basic sanitation "
                 "facilities not shared with other households.",
        )
    with col4:
        internet_use = st.number_input(
            "Individuals using the Internet (% of population)",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=0.5,
            help="Share of the population that used the internet from any "
                 "device in the last three months.",
        )
        health_expenditure = st.number_input(
            "Current health expenditure (% of GDP)",
            min_value=0.0,
            max_value=25.0,
            value=5.0,
            step=0.1,
            help="Total health spending — public and private — as a share "
                 "of GDP. Most countries fall between 3% and 12%.",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Group 3: Demographics ---
    st.markdown("<div class='group-title'>Demographics</div>", unsafe_allow_html=True)
    st.markdown("<div class='group-sub'>How the population is growing, settling, and schooling.</div>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        population_growth = st.number_input(
            "Population growth (annual %)",
            min_value=-5.0,
            max_value=10.0,
            value=2.0,
            step=0.1,
            help="Annual population growth rate. Can be negative for "
                 "countries with declining populations.",
        )
        urban_population = st.number_input(
            "Urban population (% of total population)",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=0.5,
            help="Share of the population living in areas classified as "
                 "urban by the national statistical office.",
        )
    with col6:
        school_enrollment = st.number_input(
            "Primary school enrollment (% gross)",
            min_value=0.0,
            max_value=150.0,
            value=95.0,
            step=0.5,
            help="Gross enrollment ratio for primary school. Can exceed "
                 "100% where over-age or under-age students are enrolled.",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Predict Life Expectancy →")


# ---------------------------------------------------------------------------
# VALIDATION + PREDICTION
# number_input already enforces range bounds, so most validation is free.
# The one thing worth checking explicitly: GDP per capita at exactly zero
# is almost certainly a placeholder value nobody meant to submit, not a
# real economy. Worth a soft nudge rather than a hard block.
#
# The model call is wrapped in st.spinner so a loading indicator appears
# directly under the button while predict_life_expectancy() runs — useful
# now, and more noticeable once this is deployed somewhere slower than a
# local machine.
# ---------------------------------------------------------------------------
if submitted:
    if gdp_per_capita == 0.0:
        st.warning(
            "GDP per capita is set to 0 — double-check this is intentional. "
            "A real economy at exactly zero is unusual."
        )

    input_data = {
        "Year": int(year),
        "Access to electricity (% of population)": electricity_access,
        "Current health expenditure (% of GDP)": health_expenditure,
        "GDP per capita (constant 2015 US$)": gdp_per_capita,
        "Individuals using the Internet (% of population)": internet_use,
        "People using at least basic sanitation services (% of population)": sanitation_access,
        "Population growth (annual %)": population_growth,
        "School enrollment, primary (% gross)": school_enrollment,
        "Urban population (% of total population)": urban_population,
    }

    try:
        with st.spinner("Calculating prediction..."):
            prediction = predict_life_expectancy(input_data)
    except Exception as e:
        st.error(
            f"Something went wrong while running the model: {e}. "
            "Check that models/random_forest_model.pkl and "
            "models/feature_names.pkl are present and match the expected "
            "feature schema."
        )
    else:
        # Plain result, no qualitative bucketing — just the number and
        # where it came from.
        st.markdown(
            f"""
            <div class='result-wrap'>
                <div class='result-label'>Predicted life expectancy</div>
                <div class='result-number'>{prediction:.2f}<span class='result-unit'> years</span></div>
                <div class='result-context'>This prediction was generated using a Random Forest Regression model trained on World Bank Development Indicators.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class='site-footer'>
    Life Expectancy Prediction · World Bank Development Indicators ·
    Built for educational and analytical use only.
    </div>
    """,
    unsafe_allow_html=True,
)