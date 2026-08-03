from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from careergraph.db.session import get_db
from careergraph.exceptions import JobNotFoundError
from careergraph.services.job_services import JobService
from careergraph.repositories.job_repositories import JobRepository
from careergraph.schemas.job import JobConfirmResponse, JobCreate, JobExtractResponse, JobResponse, JobSkillConfirmRequest
from fastapi import HTTPException
from careergraph.repositories.job_skill_repository import JobSkillRepository

router = APIRouter(
    prefix="/api/jobs",
    tags=["jobs"],
)

DataBaseSession = Annotated[Session, Depends(get_db)]

@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)

def create_job(
    job_data: JobCreate,
    session: DataBaseSession,
) -> JobResponse:
    """
    创建职位。

    1. 接收请求数据
    2. 调用 Service 层创建职位
    3. 返回创建的职位数据
    """
    job_repository = JobRepository(session=session)
    job_service = JobService(job_repository=job_repository)

    return job_service.create_job(job_data=job_data)

@router.post(
    "/{job_id}/extract_skills",
    response_model = JobExtractResponse,)
def extract_job_skills(
    job_id: int,
    session: DataBaseSession,
) -> JobExtractResponse:
    """
    提取职位技能。

    1. 接收请求数据
    2. 调用 Service 层提取职位技能
    3. 返回提取的技能数据
    """
    job_repository = JobRepository(session=session)
    job_service = JobService(job_repository=job_repository)

    try:
        skills = job_service.extract_job_skills(job_id=job_id)
        
    except JobNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    return JobExtractResponse(job_id=job_id, skills=skills)

@router.post(
    "/{job_id}/confirm",
    response_model = JobConfirmResponse,)
def confirm_job_skills(
    job_id: int,
    request_data: JobSkillConfirmRequest,
    session: DataBaseSession,
) -> JobConfirmResponse:
    """
    确认职位技能。

    1. 接收请求数据
    2. 调用 Service 层确认职位技能
    3. 返回确认后的技能数据
    """
    job_repository = JobRepository(session=session)
    job_skill_repository = JobSkillRepository(session=session)
    job_service = JobService(job_repository=job_repository, job_skill_repository=job_skill_repository)

    try:
        saved_skills = job_service.confirm_job_skills(
            job_id=job_id,
            skill_items=request_data.skills,
        )
        
    except JobNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    return JobConfirmResponse(job_id=job_id, skills=[JobSkillConfirmRequest(name=skill.name, required=skill.required) for skill in saved_skills])
