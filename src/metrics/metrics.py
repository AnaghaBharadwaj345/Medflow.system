import numpy as np
import pandas as pd


class MetricsCollector:
    def __init__(self, duration):
        self.duration = duration
        self.rows, self.resource_busy = [], {}

    def record_arrival(self, patient):
        self.rows.append({"id": patient.id, "arrival": patient.arrival_time, "complaint": patient.complaint})

    def _row(self, patient): return next(row for row in self.rows if row["id"] == patient.id)
    def record_prediction(self, patient, acuity, los):
        row = self._row(patient); row.update(predicted_esi=acuity, predicted_los=los)
    def record_start(self, patient, acuity, wait):
        row = self._row(patient); row.update(wait=wait, esi=acuity)
    def record_completion(self, patient, acuity, los):
        row = self._row(patient); row.update(completed=True, actual_los=los)

    def to_frame(self): return pd.DataFrame(self.rows)
    def summary(self):
        frame = self.to_frame()
        if frame.empty: return {"patients": 0}
        waits = frame.get("wait", pd.Series(dtype=float)).dropna()
        return {"patients": len(frame), "treated": int(frame.get("completed", pd.Series(dtype=bool)).sum()), "mean_wait": round(float(waits.mean()), 2) if len(waits) else 0, "p95_wait": round(float(np.percentile(waits, 95)), 2) if len(waits) else 0, "sla_breaches": int(((frame.get("esi", pd.Series(dtype=float)) == 1) & (frame.get("wait", pd.Series(dtype=float)) > 10)).sum())}
