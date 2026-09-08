"""Execute queued jobs synchronously."""


def process(store, job_id):
    payload = store.start(job_id)
    result = payload.upper()
    store.finish(job_id, result)
    return result
