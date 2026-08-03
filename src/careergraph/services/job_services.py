from careergraph.db.db_models import JobModel
from careergraph.repositories.job_repositories import JobRepository
from careergraph.schemas.job import JobCreate, JobSkillConfirmItem
from careergraph.db.db_models import JobSkillModel
from careergraph.exceptions import JobNotFoundError
from careergraph.jd_extractor import extract_skills

class JobService:
    """
    负责 JobModel 的业务逻辑。

    Service 处理：
    - 事务管理
    - 业务逻辑
    """

    def __init__(
        self,
        job_repository: JobRepository,
    ) -> None:
        self.job_repository = job_repository

    def create_job(
        self,
        job_data: JobCreate,
    ) -> JobModel:
        """
        创建职位。
        """
        return self.job_repository.create(
            title=job_data.title.strip(),
            company=job_data.company.strip(),
            raw_text=job_data.raw_text.strip(),
        )

    def extract_job_skills(self, job_id: int) -> list[dict[str,object]]:
        """
        提取职位技能。
        """
        job = self.job_repository.get_by_id(job_id)
        if job is None:
            raise JobNotFoundError(job_id)

        skills = extract_skills(job.raw_text)
        return skills

    def normalize_confirmed_skills(
        self,
        skills: list[JobSkillConfirmItem],
    ) -> list[dict[str, object]]:
        """
        规范化确认的技能列表。

        将技能列表中的每个技能转换为字典形式，
        并确保每个技能都包含 'name' 和 'confidence' 字段。
        """
        normalized: dict[str, bool] = {}
        for skill in skills:
            name = skill.name.strip().lower()
            if not name:
                continue
            normalized[name] = skill.required

        return [
            {"name": name, "required": required}
            for name, required in normalized.items()
        ]  

    def confirm_job_skills(
        self,
        job_id: int,
        skill_items: list[JobSkillConfirmItem],
    ) -> list[JobSkillModel]:
        """
        确认职位技能。

        1. 查询职位是否存在
        2. 规范化技能列表
        3. 替换职位的技能列表
        """
        job = self.job_repository.get_by_id(job_id)
        if job is None:
            raise JobNotFoundError(job_id)

        normalized_skills = self.normalize_confirmed_skills(skill_items)
        return self.job_repository.replace_for_job(
            job_id=job_id,
            skills=normalized_skills,
        ) 