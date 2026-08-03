from pydantic import BaseModel, Field, ConfigDict

class JobCreate(BaseModel):
    
    title: str = Field(min_length=1, max_length=200, description="The title of the job")
    company: str = Field(min_length=1, max_length=200, description="The company offering the job")
    raw_text: str = Field(min_length=1, description="The raw text description of the job")


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(gt=0, description="The unique identifier of the job")
    title: str = Field(min_length=1, max_length=200, description="The title of the job")
    company: str = Field(min_length=1, max_length=200, description="The company offering the job")
    raw_text: str = Field(min_length=1, description="The raw text description of the job")

class ExtractedJobSkill(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="The name of the extracted job skill")
    required: bool = Field(default=True, description="Indicates if the skill is required for the job")

class JobExtractResponse(BaseModel):
    job_id: int = Field(gt=0, description="The unique identifier of the job")
    skills: list[ExtractedJobSkill] = Field(default_factory=list, description="List of extracted skills for the job")

class JobSkillConfirmItem(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="The name of the job skill")
    required: bool = Field(default=True, description="Indicates if the skill is required for the job")

class JobSkillConfirmRequest(BaseModel):
    skills: list[JobSkillConfirmItem] = Field(default_factory=list, description="List of skills to confirm for the job")

class JobConfirmResponse(BaseModel):
    job_id: int = Field(gt=0, description="The unique identifier of the job")
    skills: list[JobSkillConfirmItem] = Field(default_factory=list, description="List of confirmed skills for the job")