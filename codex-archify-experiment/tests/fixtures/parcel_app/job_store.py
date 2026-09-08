"""In-memory job states for the project-reader smoke example."""


class JobStore:
    def __init__(self):
        self.jobs = {}

    def enqueue(self, payload):
        job_id = len(self.jobs) + 1
        self.jobs[job_id] = {"state": "queued", "payload": payload, "result": None}
        return job_id

    def start(self, job_id):
        job = self.jobs[job_id]
        if job["state"] != "queued":
            raise ValueError("Only queued jobs can start")
        job["state"] = "running"
        return job["payload"]

    def finish(self, job_id, result):
        job = self.jobs[job_id]
        if job["state"] != "running":
            raise ValueError("Only running jobs can finish")
        job.update(state="done", result=result)
