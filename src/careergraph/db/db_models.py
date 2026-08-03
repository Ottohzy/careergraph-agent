from __future__ import annotations

from sqlalchemy import (
    Boolean,
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

from careergraph.db.base import Base


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

class JobModel(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    company: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    skills: Mapped[list["JobSkillModel"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
    )

class JobSkillModel(Base):
    __tablename__ = "job_skills"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=False,
    )

    job: Mapped["JobModel"] = relationship(
        back_populates="skills",
    )