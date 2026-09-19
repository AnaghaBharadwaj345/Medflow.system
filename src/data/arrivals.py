import numpy as np

COMPLAINTS = ["cardiac", "trauma", "stroke", "respiratory", "chest_pain", "fracture", "migraine", "routine"]


def arrival_rate(minute: float) -> float:
    hour = (8 + minute / 60) % 24
    if 8 <= hour < 12:
        return 0.18
    if 12 <= hour < 18:
        return 0.12
    if 18 <= hour < 22:
        return 0.16
    return 0.055


def generate_patient(arrival_time: float, rng: np.random.Generator):
    complaint = rng.choice(COMPLAINTS, p=[.04, .10, .08, .10, .16, .22, .15, .15])
    age = int(rng.integers(1, 91))
    hr = int(np.clip(rng.normal(92 if complaint in {"cardiac", "respiratory"} else 78, 22), 40, 190))
    bp = int(np.clip(rng.normal(105 if complaint in {"cardiac", "trauma"} else 125, 20), 50, 210))
    spo2 = int(np.clip(rng.normal(93 if complaint == "respiratory" else 97, 3), 70, 100))
    temp = round(float(np.clip(rng.normal(38.0 if complaint in {"cardiac", "respiratory"} else 37.0, .7), 34, 42)), 1)
    rr = int(np.clip(rng.normal(23 if complaint == "respiratory" else 16, 5), 8, 45))
    resources = {"cardiac": ["icu", "doctor", "nurse"], "trauma": ["or", "doctor", "nurse", "bed"], "stroke": ["icu", "doctor"], "respiratory": ["icu", "nurse"], "chest_pain": ["bed", "doctor"], "fracture": ["bed", "doctor"], "migraine": ["bed", "nurse"], "routine": ["bed", "nurse"]}[complaint]
    return Patient(f"P-{int(arrival_time * 10):06d}", arrival_time, age, hr, bp, spo2, temp, rr, complaint, resources)


class Patient:
    def __init__(self, patient_id, arrival_time, age, heart_rate, blood_pressure, spo2, temperature, respiratory_rate, complaint, resources):
        self.id, self.arrival_time, self.age = patient_id, arrival_time, age
        self.heart_rate, self.blood_pressure, self.spo2 = heart_rate, blood_pressure, spo2
        self.temperature, self.respiratory_rate = temperature, respiratory_rate
        self.complaint, self.resources = complaint, resources
