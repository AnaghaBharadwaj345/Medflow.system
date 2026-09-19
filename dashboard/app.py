import pandas as pd
import streamlit as st

from src.experiments import compare_strategies
from src.simulation.engine import SimulationConfig, run_simulation

st.set_page_config(page_title="MedFlow Simulator", layout="wide")
st.title("MedFlow — Hospital Resource Management Simulator")
st.caption("Arrivals → AI triage + LOS → aging priority → SimPy scheduler → metrics")

with st.sidebar:
    duration = st.slider("Simulation duration (minutes)", 120, 1440, 720, 60)
    seed = st.number_input("Random seed", 1, 9999, 42)
    strategy = st.selectbox("Strategy", ["fcfs", "urgency", "weighted_aging"])
    run = st.button("Run simulation", type="primary")

if run:
    with st.spinner("Running discrete-event simulation and AI models..."):
        frame, summary, triage, los = run_simulation(SimulationConfig(duration, seed, strategy))
    st.success("Simulation complete")
    cols = st.columns(5)
    cols[0].metric("Arrivals", summary.get("patients", 0))
    cols[1].metric("Treated", summary.get("treated", 0))
    cols[2].metric("Mean wait", f"{summary.get('mean_wait', 0)} min")
    cols[3].metric("P95 wait", f"{summary.get('p95_wait', 0)} min")
    cols[4].metric("ESI-1 SLA breaches", summary.get("sla_breaches", 0))
    st.subheader("Wait by predicted acuity")
    if not frame.empty and "wait" in frame:
        st.bar_chart(frame.dropna(subset=["wait"]).groupby("predicted_esi")["wait"].mean())
    st.dataframe(frame, use_container_width=True)

if st.button("Compare all scheduling strategies"):
    with st.spinner("Running three experiments..."):
        comparison = pd.DataFrame(compare_strategies(duration, seed))
    st.subheader("Strategy comparison")
    st.dataframe(comparison, use_container_width=True)
    st.bar_chart(comparison.set_index("strategy")[['mean_wait', 'p95_wait']])
