# MedFlow — Hospital Resource Management Simulator

MedFlow models a hospital emergency department as a discrete-event system:

**Arrivals → AI triage and LOS prediction → mathematical priority score → atomic scheduler → SimPy engine → metrics → dashboard**

## What is implemented

### 1. Patient arrival generator
`src/data/arrivals.py` uses a non-homogeneous Poisson process. The arrival rate changes by simulated hour: morning surge, evening demand, and overnight lull. Generated patients have age, HR, BP, SpO2, temperature, respiratory rate, complaint, arrival time, and required resources.

### 2. AI layer
`src/ai/models.py` trains two real scikit-learn models on a reproducible labelled synthetic dataset generated from published-style triage signals:

- GradientBoostingClassifier predicts acuity/ESI-like levels 1–4 from vitals, age, and complaint.
- RandomForestRegressor predicts length of stay, and the predicted duration is used by the simulation to release resources.

This is not a hardcoded lookup: models are fitted at runtime and their predictions flow into `Scheduler.process()`.

### 3. Priority scoring
The weighted strategy uses:

```text
score = 100 * acuity + 8 * waiting_time^0.75 + 12 * deterioration_risk
```

The aging term is sub-linear but unbounded, so lower-acuity patients eventually overtake a patient that has already waited too long. FCFS and urgency-only baselines are also implemented.

### 4. Scheduler and resource manager
SimPy resources enforce hard capacities. A patient requests every required resource before treatment starts, giving atomic multi-resource acquisition for surgery and ICU cases. Resources are released only after predicted LOS elapses.

### 5. Simulation and dashboard
`src/simulation/engine.py` runs the 24-hour discrete-event model. `dashboard/app.py` exposes strategy selection, KPI cards, wait distributions, raw results, and an A/B strategy comparison.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
PYTHONPATH=. streamlit run dashboard/app.py
```

Run tests:

```bash
PYTHONPATH=. pytest
```

## Repository structure

```text
src/
  ai/             # model training and inference
  data/           # non-homogeneous arrivals and patient schema
  scheduling/     # FCFS, urgency, weighted aging, atomic allocation
  simulation/     # SimPy engine
  metrics/        # KPI collection and reporting
dashboard/        # Streamlit UI
tests/            # simulation tests
results/          # generated experiment outputs
models/           # optional saved artifacts
```

## Validation and metrics

The dashboard reports mean wait, 95th-percentile wait, treatment throughput, ESI-1 SLA breaches, and strategy comparisons. The metrics layer is ready for Erlang-C and Little's Law validation; the next experiment notebook should compare `L = λW` and analytical M/M/c wait against simulation output.

## Third-party disclosure

This project uses SimPy for discrete-event simulation, NumPy and pandas for numerical data, scikit-learn for trained models, Streamlit for the dashboard, Plotly-compatible Streamlit charts, pytest for tests, and joblib for optional model persistence. No third-party template is included.

## Important disclaimer

This is an educational operations-research prototype. It is not a clinical triage system and must not be used for real patient-care decisions.
