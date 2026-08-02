from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator

class Skill(BaseModel):
    name: str = Field(min_length = 1, max_length = 100, description="The name of the skill")

    @field_validator('name', mode='before')
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Skill name cannot be empty')
        return value

class Experience(BaseModel):
    title: str = Field(min_length = 1, max_length = 200, description="The title of the experience")
    description: str = Field(min_length = 1, description="The description of the experience")
    skills: list[Skill] = Field(default_factory=list, description="List of skills associated with the experience")

    @field_validator('title', mode='before')
    @classmethod
    def title_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Experience title cannot be empty')
        return value

    @field_validator('description', mode='before')
    @classmethod
    def description_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Experience description cannot be empty')
        return value

class Candidate(BaseModel):
    candidate_id: str = Field(min_length = 1, max_length = 50, description="The unique identifier of the candidate")
    name: str = Field(min_length = 1, max_length = 100, description="The name of the candidate")
    experiences: list[Experience] = Field(default_factory=list, description="List of experiences of the candidate")
    skills: list[Skill] = Field(default_factory=list, description="List of skills of the candidate")

    @field_validator('candidate_id', mode='before')
    @classmethod
    def candidate_id_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Candidate ID cannot be empty')
        return value

    @field_validator('name', mode='before')
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Candidate name cannot be empty')
        return value

class JobSkill(BaseModel):
    name: str = Field(min_length = 1, max_length = 100, description="The name of the job skill")
    required: bool = Field(default=True, description="Indicates if the skill is required for the job")

    @field_validator('name', mode='before')
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Job skill name cannot be empty')
        return value

class Job(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    job_id: str = Field(min_length=1, max_length=50, description="The unique identifier of the job")
    title: str = Field(min_length=1, max_length= 100, description="The title of the job")
    company: str = Field(default="Unknown", min_length=1, max_length= 100, description="The company offering the job")
    description: str = Field(
        min_length=1,
        validation_alias=AliasChoices("description", "raw_text"),
        description="The job description text",
    )
    skills: list[JobSkill] = Field(default_factory=list, description="List of skills required for the job")

    @property
    def raw_text(self) -> str:
        return self.description

    @raw_text.setter
    def raw_text(self, value: str) -> None:
        self.description = value

    @field_validator('job_id', mode='before')
    @classmethod
    def job_id_must_not_be_empty(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Job ID cannot be empty')
        return value

    @field_validator('title', mode='before')
    @classmethod
    def title_must_not_be_empty(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Job title cannot be empty')
        return value

    @field_validator('company', mode='before')
    @classmethod
    def company_must_not_be_empty(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Company name cannot be empty')
        return value

    @field_validator('description', mode='before')
    @classmethod
    def description_must_not_be_empty(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Job description cannot be empty')
        return value

class Analysis(BaseModel):
    analysis_id: str = Field(min_length=1, max_length=50, description="The unique identifier of the analysis")
    job_id: str = Field(min_length=1, max_length=50, description="The related job identifier")
    candidate_id: str = Field(min_length=1, max_length=50, description="The related candidate identifier")
    matched_skills: list[str] = Field(default_factory=list, description="List of skills matched between candidate and job")
    missing_skills: list[str] = Field(default_factory=list, description="List of skills missing in the candidate for the job")
    required_skills: list[str] = Field(default_factory=list, description="List of required skills for the job")
    match_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="The match rate between candidate and job, ranging from 0.0 to 1.0")

    @field_validator('analysis_id', 'job_id', 'candidate_id', mode='before')
    @classmethod
    def identifiers_must_not_be_empty(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Identifier cannot be empty')
        return value

    @field_validator('match_rate', mode='before')
    @classmethod
    def match_rate_must_be_between_0_and_1(cls, value: float) -> float:
        if not (0.0 <= value <= 1.0):
            raise ValueError('Match rate must be between 0.0 and 1.0')
        return value

class LearningTask(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    task_id: str = Field(min_length=1, max_length=50, description="The unique identifier of the learning task")
    skill_name: str = Field(
        min_length=1,
        validation_alias=AliasChoices("skill_name", "skill"),
        description="The skill to be learned",
    )
    description: str = Field(
        min_length=1,
        validation_alias=AliasChoices("description", "reason"),
        description="The reason or summary of the learning task",
    )
    priority: int = Field(default=3, ge=1, le=5,description="The priority of the learning task, with 1 being the highest priority")
    completed: bool = Field(default=False, description="Indicates if the learning task has been completed")

    @property
    def skill(self) -> str:
        return self.skill_name

    @skill.setter
    def skill(self, value: str) -> None:
        self.skill_name = value

    @property
    def reason(self) -> str:
        return self.description

    @reason.setter
    def reason(self, value: str) -> None:
        self.description = value

    @field_validator('task_id', mode='before')
    @classmethod
    def task_id_must_not_be_empty(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Learning task ID cannot be empty')
        return value

    @field_validator('skill_name', mode='before')
    @classmethod
    def skill_must_not_be_empty(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Learning task skill cannot be empty')
        return value

    @field_validator('description', mode='before')
    @classmethod
    def reason_must_not_be_empty(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Learning task reason cannot be empty')
        return value

    @field_validator('priority', mode='before')
    @classmethod
    def priority_must_be_between_1_and_5(cls, value: int) -> int:
        if not (1 <= value <= 5):
            raise ValueError('Learning task priority must be between 1 and 5')
        return value

    @field_validator('completed', mode='before')
    @classmethod
    def completed_must_be_boolean(cls, value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValueError('Learning task completed must be a boolean value')
        return value

class ExperienceCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
    )
    description: str = Field(
        min_length=1,
    )


class CandidateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="The name of the candidate")
    skills: list[str | Skill] = Field(default_factory=list, description="List of skills of the candidate")
    experiences: list[ExperienceCreate | Experience] = Field(default_factory=list, description="List of experiences of the candidate")


class CandidateResponse(CandidateCreate):
    candidate_id: int = Field(ge=1, description="The unique identifier of the candidate")


class CandidateUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    skills: list[str] | None = None
    experiences: list[ExperienceCreate] | None = None
