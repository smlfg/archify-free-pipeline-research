"""Command-line entrypoint for one synchronous job."""

from job_store import JobStore
from service import submit


if __name__ == "__main__":
    result = submit(JobStore(), "parcel")
    assert result["state"] == "done"
    assert result["result"] == "PARCEL"
    print(result)
