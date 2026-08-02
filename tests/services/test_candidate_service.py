import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from careergraph.db.db_models import (
    CandidateModel,
    SkillModel,
)
from careergraph.exceptions import (
    CandidateNotFoundError,
    DuplicateCandidateError,
)
from careergraph.repositories.candidate_repository import (
    CandidateRepository,
)
from careergraph.schema import (
    CandidateCreate,
    CandidateUpdate,
    ExperienceCreate,
)
from careergraph.services.candidate_services import (
    CandidateService,
)


@pytest.fixture
def candidate_service(
    session: Session,
) -> CandidateService:
    repository = CandidateRepository(
        session,
    )

    return CandidateService(
        session=session,
        candidate_repository=repository,
    )


def test_create_candidate(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
        )
    )

    assert candidate.id is not None
    assert candidate.name == "Zhuoyu"
    assert candidate.skills == []
    assert candidate.experiences == []


def test_create_candidate_with_skills(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
            skills=[
                "Python",
                "SQL",
            ],
        )
    )

    assert {
        skill.name
        for skill in candidate.skills
    } == {
        "python",
        "sql",
    }


def test_create_candidate_with_experiences(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
            experiences=[
                ExperienceCreate(
                    title="Agent Developer",
                    description=(
                        "Built CareerGraph Agent."
                    ),
                )
            ],
        )
    )

    assert len(candidate.experiences) == 1

    experience = candidate.experiences[0]

    assert experience.title == "Agent Developer"

    assert (
        experience.description
        == "Built CareerGraph Agent."
    )

    assert experience.candidate.name == "Zhuoyu"


def test_create_candidate_normalizes_name(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="  Zhuoyu  ",
        )
    )

    assert candidate.name == "Zhuoyu"


def test_create_candidate_normalizes_and_deduplicates_skills(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
            skills=[
                "Python",
                " python ",
                "PYTHON",
                "SQL",
                " sql ",
                "",
                "   ",
            ],
        )
    )

    skill_names = [
        skill.name
        for skill in candidate.skills
    ]

    assert skill_names == [
        "python",
        "sql",
    ]


def test_create_duplicate_candidate_raises_error(
    candidate_service: CandidateService,
) -> None:
    candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
        )
    )

    with pytest.raises(
        DuplicateCandidateError,
        match="Candidate already exists",
    ):
        candidate_service.create_candidate(
            CandidateCreate(
                name="  Zhuoyu  ",
            )
        )


def test_get_candidate(
    candidate_service: CandidateService,
) -> None:
    created_candidate = (
        candidate_service.create_candidate(
            CandidateCreate(
                name="Zhuoyu",
                skills=[
                    "Python",
                ],
            )
        )
    )

    loaded_candidate = (
        candidate_service.get_candidate(
            created_candidate.id,
        )
    )

    assert loaded_candidate.id == created_candidate.id
    assert loaded_candidate.name == "Zhuoyu"

    assert [
        skill.name
        for skill in loaded_candidate.skills
    ] == [
        "python",
    ]


def test_get_missing_candidate_raises_error(
    candidate_service: CandidateService,
) -> None:
    with pytest.raises(
        CandidateNotFoundError,
        match="Candidate not found: 999",
    ):
        candidate_service.get_candidate(999)


def test_get_all_candidates(
    candidate_service: CandidateService,
) -> None:
    candidate_service.create_candidate(
        CandidateCreate(
            name="Alice",
        )
    )

    candidate_service.create_candidate(
        CandidateCreate(
            name="Bob",
        )
    )

    candidates = (
        candidate_service.get_all_candidates()
    )

    assert len(candidates) == 2

    assert [
        candidate.name
        for candidate in candidates
    ] == [
        "Alice",
        "Bob",
    ]


def test_update_candidate_name(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
        )
    )

    updated_candidate = (
        candidate_service.update_candidate(
            candidate_id=candidate.id,
            candidate_data=CandidateUpdate(
                name="Zhuoyu Hao",
            ),
        )
    )

    assert updated_candidate.name == "Zhuoyu Hao"


def test_update_candidate_skills(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
            skills=[
                "Python",
                "SQL",
            ],
        )
    )

    updated_candidate = (
        candidate_service.update_candidate(
            candidate_id=candidate.id,
            candidate_data=CandidateUpdate(
                skills=[
                    "FastAPI",
                    "SQLAlchemy",
                ],
            ),
        )
    )

    assert {
        skill.name
        for skill in updated_candidate.skills
    } == {
        "fastapi",
        "sqlalchemy",
    }


def test_update_candidate_with_empty_skills_clears_skills(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
            skills=[
                "Python",
                "SQL",
            ],
        )
    )

    updated_candidate = (
        candidate_service.update_candidate(
            candidate_id=candidate.id,
            candidate_data=CandidateUpdate(
                skills=[],
            ),
        )
    )

    assert updated_candidate.skills == []


def test_update_candidate_with_none_keeps_skills(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
            skills=[
                "Python",
            ],
        )
    )

    updated_candidate = (
        candidate_service.update_candidate(
            candidate_id=candidate.id,
            candidate_data=CandidateUpdate(
                name="Zhuoyu Hao",
                skills=None,
            ),
        )
    )

    assert [
        skill.name
        for skill in updated_candidate.skills
    ] == [
        "python",
    ]


def test_update_candidate_experiences(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
            experiences=[
                ExperienceCreate(
                    title="Old Experience",
                    description="Old description.",
                )
            ],
        )
    )

    updated_candidate = (
        candidate_service.update_candidate(
            candidate_id=candidate.id,
            candidate_data=CandidateUpdate(
                experiences=[
                    ExperienceCreate(
                        title="Agent Developer",
                        description=(
                            "Built CareerGraph Agent."
                        ),
                    ),
                    ExperienceCreate(
                        title="Backend Developer",
                        description=(
                            "Built FastAPI services."
                        ),
                    ),
                ],
            ),
        )
    )

    assert len(
        updated_candidate.experiences,
    ) == 2

    assert {
        experience.title
        for experience
        in updated_candidate.experiences
    } == {
        "Agent Developer",
        "Backend Developer",
    }


def test_update_missing_candidate_raises_error(
    candidate_service: CandidateService,
) -> None:
    with pytest.raises(
        CandidateNotFoundError,
        match="Candidate not found: 999",
    ):
        candidate_service.update_candidate(
            candidate_id=999,
            candidate_data=CandidateUpdate(
                name="New Name",
            ),
        )


def test_update_to_duplicate_name_raises_error(
    candidate_service: CandidateService,
) -> None:
    candidate_service.create_candidate(
        CandidateCreate(
            name="Alice",
        )
    )

    bob = candidate_service.create_candidate(
        CandidateCreate(
            name="Bob",
        )
    )

    with pytest.raises(
        DuplicateCandidateError,
        match="Candidate already exists",
    ):
        candidate_service.update_candidate(
            candidate_id=bob.id,
            candidate_data=CandidateUpdate(
                name="Alice",
            ),
        )


def test_two_candidates_share_existing_skill(
    candidate_service: CandidateService,
    session: Session,
) -> None:
    first_candidate = (
        candidate_service.create_candidate(
            CandidateCreate(
                name="Alice",
                skills=[
                    "Python",
                ],
            )
        )
    )

    second_candidate = (
        candidate_service.create_candidate(
            CandidateCreate(
                name="Bob",
                skills=[
                    " python ",
                ],
            )
        )
    )

    skill_count_statement = select(
        func.count(SkillModel.id),
    )

    skill_count = session.scalar(
        skill_count_statement,
    )

    assert skill_count == 1

    assert (
        first_candidate.skills[0].id
        == second_candidate.skills[0].id
    )


def test_delete_candidate(
    candidate_service: CandidateService,
) -> None:
    candidate = candidate_service.create_candidate(
        CandidateCreate(
            name="Zhuoyu",
        )
    )

    candidate_service.delete_candidate(
        candidate.id,
    )

    with pytest.raises(
        CandidateNotFoundError,
    ):
        candidate_service.get_candidate(
            candidate.id,
        )


def test_delete_missing_candidate_raises_error(
    candidate_service: CandidateService,
) -> None:
    with pytest.raises(
        CandidateNotFoundError,
        match="Candidate not found: 999",
    ):
        candidate_service.delete_candidate(999)


def test_failed_transaction_does_not_save_candidate(
    candidate_service: CandidateService,
    session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_error(
        candidate: CandidateModel,
    ) -> CandidateModel:
        raise RuntimeError(
            "Simulated database failure",
        )

    monkeypatch.setattr(
        candidate_service.candidate_repository,
        "create",
        raise_error,
    )

    with pytest.raises(
        RuntimeError,
        match="Simulated database failure",
    ):
        candidate_service.create_candidate(
            CandidateCreate(
                name="Zhuoyu",
                skills=[
                    "Python",
                ],
            )
        )

    candidate_count_statement = select(
        func.count(CandidateModel.id),
    )

    candidate_count = session.scalar(
        candidate_count_statement,
    )

    assert candidate_count == 0