class CandidateNotFoundError(Exception):
    """候选人不存在。"""


class DuplicateCandidateError(Exception):
    """候选人重复。"""

class JobNotFoundError(Exception):
    def __init__(self, job_id: int):
        self.job_id = job_id
        super().__init__(f"Job with ID {job_id} not found.")
        
