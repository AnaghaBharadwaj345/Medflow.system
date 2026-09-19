# MedFlow — Hospital Resource Management Simulator

MedFlow is a browser-based prototype for simulating hospital operations. It models patient arrivals, urgency-aware queues, resource capacity, allocation decisions, waiting time, and competing scheduling strategies in an operations dashboard.

## Run locally

No build step is required. Open `index.html` in a browser, or serve the folder with:

```bash
python -m http.server 8000
```

Then visit http://localhost:8000.

## Included prototype features

- Priority patient queue with Critical, Urgent, Moderate, and Low urgency levels.
- Live simulation clock and patient waiting-time updates.
- Capacity tracking for beds, ICU beds, operating rooms, doctors, nurses, and emergency vehicles.
- Resource utilization progress bars and patient-flow visualization.
- Strategy comparison: urgency first, balanced scheduling, and utilization first.
- Patient surge simulation through the **Add patient** action.
- Reset and pause/run controls, activity log, and responsive mobile layout.

## Suggested next step for a full simulator

Move the simulation engine into Python (for example, a Streamlit app or FastAPI service). Represent each patient as an event with `arrival_time`, `urgency`, `required_resources`, and `service_duration`; use a priority queue to select the next patient. At each time step, reserve resources atomically, record wait time and utilization, then release resources on discharge. Add scenario controls for staff shortages, ambulance patterns, department constraints, and unexpected resource failures. The dashboard can then consume the engine's metrics to compare strategies over repeated runs.
