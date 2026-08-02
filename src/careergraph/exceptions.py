class CandidateNotFoundError(Exception):
    """候选人不存在。"""


class DuplicateCandidateError(Exception):
    """候选人重复。"""