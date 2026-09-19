from src.simulation.engine import SimulationConfig, run_simulation


def test_simulation_runs():
    frame, summary, _, _ = run_simulation(SimulationConfig(duration_minutes=60, seed=1))
    assert summary["patients"] >= 0
    assert len(frame) == summary["patients"]


def test_all_strategies_run():
    for strategy in ["fcfs", "urgency", "weighted_aging"]:
        _, summary, _, _ = run_simulation(SimulationConfig(duration_minutes=60, seed=2, strategy=strategy))
        assert "treated" in summary
