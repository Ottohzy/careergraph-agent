from fastapi import (
    FastAPI,
    HTTPException,
    status,
)

from careergraph.schema import (
    CandidateCreate,
    CandidateResponse,
)


app = FastAPI(
    title="CareerGraph API",
    description="Career skill matching API",
    version="0.1.0",
)


candidate_store: dict[int, CandidateResponse] = {}
next_candidate_id = 1


@app.get(
    "/health",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/api/candidates",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate(
    candidate: CandidateCreate,
) -> CandidateResponse:
    global next_candidate_id

    created_candidate = CandidateResponse(
        candidate_id=next_candidate_id,
        **candidate.model_dump(),
    )

    candidate_store[next_candidate_id] = (
        created_candidate
    )

    next_candidate_id += 1

    return created_candidate


@app.get(
    "/api/candidates/{candidate_id}",
    response_model=CandidateResponse,
    status_code=status.HTTP_200_OK,
)
def get_candidate(
    candidate_id: int,
) -> CandidateResponse:
    candidate = candidate_store.get(candidate_id)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found.",
        )

    return candidate