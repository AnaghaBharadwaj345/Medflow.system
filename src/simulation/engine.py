from dataclasses import dataclass
from typing import Dict, List

import simpy

from src.ai.models import TriageModel, LOSModel, train_models
from src.data.arrivals import Patient, generate_patient, arrival_rate
from src.metrics.metrics import MetricsCollector
from src.scheduling.strategies import Scheduler, STRATEGIES


@dataclass
class SimulationConfig:
    duration_minutes: int = 24 * 60
    seed: int = 42
    capacity: Dict[str, int] | None = None
    strategy: str = "weighted_aging"

    def resources(self) -> Dict[str, int]:
        return self.capacity or {"bed": 10, "icu": 3, "doctor": 3, "nurse": 5, "or": 1}


def run_simulation(config: SimulationConfig):
    triage, los = train_models(random_state=config.seed)
    env = simpy.Environment()
    pools = {name: simpy.Resource(env, capacity=count) for name, count in config.resources().items()}
    metrics = MetricsCollector(config.duration_minutes)
    scheduler = Scheduler(config.strategy, triage, los, pools, metrics, env)
    env.process(arrival_process(env, scheduler, metrics, config))
    env.run(until=config.duration_minutes)
    return metrics.to_frame(), metrics.summary(), triage, los


def arrival_process(env, scheduler, metrics, config):
    import numpy as np
    rng = np.random.default_rng(config.seed)
    while env.now < config.duration_minutes:
        rate = arrival_rate(env.now)
        delay = max(0.5, float(rng.exponential(1 / rate)))
        yield env.timeout(delay)
        if env.now >= config.duration_minutes:
            break
        patient = generate_patient(float(env.now), rng)
        metrics.record_arrival(patient)
        env.process(scheduler.process(patient))
