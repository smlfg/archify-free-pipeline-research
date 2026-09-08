"""Validate incoming jobs and hand accepted work to the worker."""

from worker import process


def submit(store, payload):
    if not isinstance(payload, str) or not payload.strip():
        raise ValueError("A nonempty string is required")
    job_id = store.enqueue(payload)
    process(store, job_id)
    return store.jobs[job_id]
