from dataclasses import dataclass
from typing import Dict

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error

FEATURES = ["age", "heart_rate", "blood_pressure", "spo2", "temperature", "respiratory_rate", "complaint_code"]
COMPLAINT_CODE = {name: i for i, name in enumerate(["cardiac", "trauma", "stroke", "respiratory", "chest_pain", "fracture", "migraine", "routine"])}


def vector(patient):
    return [patient.age, patient.heart_rate, patient.blood_pressure, patient.spo2, patient.temperature, patient.respiratory_rate, COMPLAINT_CODE[patient.complaint]]


def synthetic_training_data(n=8000, seed=7):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 7))
    X[:, 0] = rng.integers(1, 91, n)
    X[:, 1] = np.clip(rng.normal(82, 25, n), 40, 190)
    X[:, 2] = np.clip(rng.normal(120, 25, n), 50, 210)
    X[:, 3] = np.clip(rng.normal(96, 5, n), 70, 100)
    X[:, 4] = np.clip(rng.normal(37, 1, n), 34, 42)
    X[:, 5] = np.clip(rng.normal(17, 6, n), 8, 45)
    X[:, 6] = rng.integers(0, 8, n)
    risk = (X[:, 1] > 125) + (X[:, 2] < 85) * 2 + (X[:, 3] < 90) * 2 + (X[:, 5] > 30) + (X[:, 6] < 4) + (X[:, 0] > 70)
    acuity = np.select([risk >= 5, risk >= 3, risk >= 1], [1, 2, 3], default=4)
    los = np.clip(20 + acuity * 18 + X[:, 6] * 3 + rng.normal(0, 8, n), 10, 180)
    return X, acuity, los


@dataclass
class ModelReport:
    accuracy: float
    f1: float
    los_mae: float


class TriageModel:
    def __init__(self, model): self.model = model
    def predict(self, patient): return int(self.model.predict([vector(patient)])[0])


class LOSModel:
    def __init__(self, model): self.model = model
    def predict(self, patient, acuity): return max(5.0, float(self.model.predict([vector(patient)])[0]))


def train_models(random_state=42):
    X, y_triage, y_los = synthetic_training_data(seed=random_state)
    split = int(len(X) * .8)
    triage = GradientBoostingClassifier(random_state=random_state).fit(X[:split], y_triage[:split])
    los = RandomForestRegressor(n_estimators=80, random_state=random_state, n_jobs=-1).fit(X[:split], y_los[:split])
    return TriageModel(triage), LOSModel(los)
