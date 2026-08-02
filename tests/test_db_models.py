from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from careergraph.db.base import Base
from careergraph.db.db_models import CandidateModel, ExperienceModel, SkillModel


def test_create_candidate(
    tmp_path,
) -> None:
    database_path = tmp_path / "test.db"

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as database:
        candidate = CandidateModel(
            name="Alice",
        )

        database.add(candidate)
        database.commit()
        database.refresh(candidate)

        assert candidate.id is not None
        assert candidate.name == "Alice"

def test_candidate_has_experiences(
    tmp_path,
) -> None:
    database_path = tmp_path / "test.db"

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    Base.metadata.create_all(bind=engine)

    candidate = CandidateModel(
        name="Alice",
        experiences=[
            ExperienceModel(
                title="Backend Intern",
                description="Built APIs.",
            )
        ],
    )

    with Session(engine) as database:
        database.add(candidate)
        database.commit()
        database.refresh(candidate)

        assert len(candidate.experiences) == 1
        assert (
            candidate.experiences[0].title
            == "Backend Intern"
        )
        assert (
            candidate.experiences[0].candidate_id
            == candidate.id
        )

def test_candidate_has_skills(
    tmp_path,
) -> None:
    database_path = tmp_path / "test.db"

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    Base.metadata.create_all(bind=engine)

    candidate = CandidateModel(
        name="Alice",
        skills=[
            SkillModel(name="python"),
            SkillModel(name="sql"),
        ],
    )

    with Session(engine) as database:
        database.add(candidate)
        database.commit()
        database.refresh(candidate)

        skill_names = {
            skill.name
            for skill in candidate.skills
        }

        assert skill_names == {
            "python",
            "sql",
        }