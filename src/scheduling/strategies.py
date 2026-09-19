from collections import defaultdict

import simpy


class Scheduler:
    def __init__(self, strategy, triage_model, los_model, pools, metrics, env):
        self.strategy, self.triage, self.los = strategy, triage_model, los_model
        self.pools, self.metrics, self.env = pools, metrics, env
        self.waiting = []

    def score(self, patient, acuity):
        if self.strategy == "fcfs": return -patient.arrival_time
        if self.strategy == "urgency": return -acuity
        age = max(0, self.env.now - patient.arrival_time)
        deterioration = max(0, patient.heart_rate - 100) / 20 + max(0, 92 - patient.spo2) / 5
        return acuity * 100 + 8 * age ** 0.75 + 12 * deterioration

    def process(self, patient):
        acuity = self.triage.predict(patient)
        predicted_los = self.los.predict(patient, acuity)
        self.metrics.record_prediction(patient, acuity, predicted_los)
        entry = (self.score(patient, acuity), patient, acuity, predicted_los)
        self.waiting.append(entry)
        while entry in self.waiting:
            self.waiting.sort(key=lambda item: item[0], reverse=True)
            if self.waiting[0] != entry:
                yield self.env.timeout(1)
                entry = (self.score(patient, acuity), patient, acuity, predicted_los)
                continue
            requests = [self.pools[name].request() for name in patient.resources]
            results = yield simpy.events.AllOf(self.env, requests)
            if not results.ok:
                for request, name in zip(requests, patient.resources): self.pools[name].release(request)
                yield self.env.timeout(1)
                continue
            self.waiting.remove(next(item for item in self.waiting if item[1] is patient))
            wait = self.env.now - patient.arrival_time
            self.metrics.record_start(patient, acuity, wait)
            yield self.env.timeout(predicted_los)
            for request, name in zip(requests, patient.resources): self.pools[name].release(request)
            self.metrics.record_completion(patient, acuity, predicted_los)
