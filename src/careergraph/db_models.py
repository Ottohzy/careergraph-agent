from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from careergraph.database import Base


candidate_skills = Table(
    "candidate_skills",
    Base.metadata,
    Column(
        "candidate_id",
        ForeignKey("candidates.id"),
        primary_key=True,
    ),
    Column(
        "skill_id",
        ForeignKey("skills.id"),
        primary_key=True,
    ),
)

class CandidateModel(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    skills: Mapped[list["SkillModel"]] = relationship(
        secondary=candidate_skills,
        back_populates="candidates",
    )

    experiences: Mapped[list["ExperienceModel"]] = relationship(
        back_populates="candidate",
        cascade="all, delete-orphan",
    )

class SkillModel(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    candidates: Mapped[list["CandidateModel"]] = relationship(
        secondary=candidate_skills,
        back_populates="skills",
    )

class ExperienceModel(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id"),
        nullable=False,
    )

    candidate: Mapped["CandidateModel"] = relationship(
        back_populates="experiences",
    )