class CareerGraphOrchestrator:
    def __init__(self) -> None:
        pass

    def analyze_job(
        self,
        candidate_id: int,
        job_id: int,
    ) -> dict:
        return {
            "candidate_id": candidate_id,
            "job_id": job_id,
            "status": "completed",
        }