from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from careergraph.db.base import Base
from careergraph.db.db_models import (
    CandidateModel,
    ExperienceModel,
    SkillModel,
)


def test_candidate_relationships() -> None:
    engine = create_engine(
        "sqlite:///candidate_relationships_test.db",
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:
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

        session.add(candidate)
        session.commit()

        candidate_id = candidate.id

    with TestingSessionLocal() as session:
        loaded_candidate = session.get(
            CandidateModel,
            candidate_id,
        )

        assert loaded_candidate is not None
        assert loaded_candidate.name == "Zhuoyu"

        assert {
            skill.name
            for skill in loaded_candidate.skills
        } == {
            "python",
            "sql",
        }

        assert len(
            loaded_candidate.experiences
        ) == 1

        assert (
            loaded_candidate.experiences[0].title
            == "Agent Developer"
        )

        assert (
            loaded_candidate.experiences[0]
            .candidate
            .name
            == "Zhuoyu"
        )