from sqlalchemy.orm import Session

from careergraph.db.db_models import (
    CandidateModel,
    ExperienceModel,
    SkillModel,
)
from careergraph.repositories.candidate_repository import (
    CandidateRepository,
)


def test_create_candidate(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    candidate = CandidateModel(
        name="Zhuoyu",
    )

    created_candidate = repository.create(
        candidate,
    )

    session.commit()

    assert created_candidate.id is not None
    assert created_candidate.name == "Zhuoyu"


def test_get_candidate_by_id(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    candidate = CandidateModel(
        name="Zhuoyu",
    )

    repository.create(candidate)
    session.commit()

    loaded_candidate = repository.get_by_id(
        candidate.id,
    )

    assert loaded_candidate is not None
    assert loaded_candidate.id == candidate.id
    assert loaded_candidate.name == "Zhuoyu"


def test_get_candidate_by_id_returns_none(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    loaded_candidate = repository.get_by_id(
        999,
    )

    assert loaded_candidate is None


def test_get_candidate_by_name(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    candidate = CandidateModel(
        name="Zhuoyu",
    )

    repository.create(candidate)
    session.commit()

    loaded_candidate = repository.get_by_name(
        "Zhuoyu",
    )

    assert loaded_candidate is not None
    assert loaded_candidate.name == "Zhuoyu"


def test_get_candidate_with_skills_and_experiences(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    candidate = CandidateModel(
        name="Zhuoyu",
    )

    candidate.skills.extend(
        [
            SkillModel(name="python"),
            SkillModel(name="sql"),
        ]
    )

    candidate.experiences.append(
        ExperienceModel(
            title="Agent Developer",
            description="Built CareerGraph Agent.",
        )
    )

    repository.create(candidate)
    session.commit()

    loaded_candidate = repository.get_by_id(
        candidate.id,
    )

    assert loaded_candidate is not None

    assert {
        skill.name
        for skill in loaded_candidate.skills
    } == {
        "python",
        "sql",
    }

    assert len(
        loaded_candidate.experiences,
    ) == 1

    assert (
        loaded_candidate.experiences[0].title
        == "Agent Developer"
    )


def test_get_all_candidates(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    repository.create(
        CandidateModel(name="Alice"),
    )

    repository.create(
        CandidateModel(name="Bob"),
    )

    session.commit()

    candidates = repository.get_all()

    assert len(candidates) == 2

    assert [
        candidate.name
        for candidate in candidates
    ] == [
        "Alice",
        "Bob",
    ]


def test_update_candidate(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    candidate = CandidateModel(
        name="Zhuoyu",
    )

    repository.create(candidate)
    session.commit()

    candidate.name = "Zhuoyu Hao"

    updated_candidate = repository.update(
        candidate,
    )

    session.commit()

    loaded_candidate = repository.get_by_id(
        candidate.id,
    )

    assert updated_candidate.name == "Zhuoyu Hao"
    assert loaded_candidate is not None
    assert loaded_candidate.name == "Zhuoyu Hao"


def test_delete_candidate(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    candidate = CandidateModel(
        name="Zhuoyu",
    )

    repository.create(candidate)
    session.commit()

    candidate_id = candidate.id

    repository.delete(candidate)
    session.commit()

    loaded_candidate = repository.get_by_id(
        candidate_id,
    )

    assert loaded_candidate is None


def test_exists_by_id(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    candidate = CandidateModel(
        name="Zhuoyu",
    )

    repository.create(candidate)
    session.commit()

    assert repository.exists_by_id(
        candidate.id,
    ) is True

    assert repository.exists_by_id(
        999,
    ) is False


def test_exists_by_name(
    session: Session,
) -> None:
    repository = CandidateRepository(session)

    candidate = CandidateModel(
        name="Zhuoyu",
    )

    repository.create(candidate)
    session.commit()

    assert repository.exists_by_name(
        "Zhuoyu",
    ) is True

    assert repository.exists_by_name(
        "Unknown",
    ) is False