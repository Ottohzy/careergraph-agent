from sqlalchemy import select

from careergraph.db.database import (
    SessionLocal,
    init_database,
)
from careergraph.db.db_models import (
    CandidateModel,
    ExperienceModel,
    SkillModel,
)


def main() -> None:
    init_database()

    with SessionLocal() as database:
        python_skill = SkillModel(name="python")
        fastapi_skill = SkillModel(name="fastapi")

        candidate = CandidateModel(
            name="Alice",
            skills=[
                python_skill,
                fastapi_skill,
            ],
            experiences=[
                ExperienceModel(
                    title="Backend Intern",
                    description=(
                        "Built REST APIs with FastAPI."
                    ),
                ),
            ],
        )

        database.add(candidate)
        database.commit()
        database.refresh(candidate)

        statement = select(CandidateModel).where(
            CandidateModel.id == candidate.id
        )

        saved_candidate = database.scalar(statement)

        if saved_candidate is None:
            raise RuntimeError(
                "Candidate was not saved."
            )

        print(saved_candidate.id)
        print(saved_candidate.name)
        print(
            [
                skill.name
                for skill in saved_candidate.skills
            ]
        )
        print(
            [
                experience.title
                for experience
                in saved_candidate.experiences
            ]
        )


if __name__ == "__main__":
    main()