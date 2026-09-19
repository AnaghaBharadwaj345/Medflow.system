from src.simulation.engine import SimulationConfig, run_simulation


def compare_strategies(duration=720, seed=42):
    results = []
    for strategy in ["fcfs", "urgency", "weighted_aging"]:
        _, summary, _, _ = run_simulation(SimulationConfig(duration_minutes=duration, seed=seed, strategy=strategy))
        results.append({"strategy": strategy, **summary})
    return results
