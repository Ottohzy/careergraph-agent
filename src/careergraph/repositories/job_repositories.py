from sqlalchemy.orm import Session
from careergraph.db.db_models import JobModel, JobSkillModel
from sqlalchemy import delete, select

class JobRepository:
    """
    负责 JobModel 的数据库访问。

    Repository 只处理数据库操作：
    - 创建
    - 查询
    - 更新
    - 删除

    commit 和 rollback 由 Service 层负责。
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def create(
        self,
        *,
        title: str,
        company: str,
        raw_text: str,
    ) -> JobModel:
        """
        创建职位。

        flush 会把数据发送到数据库，
        但不会结束当前事务。
        """
        job = JobModel(
            title=title,
            company=company,
            raw_text=raw_text,
        )
        self.session.add(job)
        self.session.commit()

        # flush 后数据库已经为 job 生成 id
        self.session.refresh(job)

        return job

    def get_by_id(
        self,
        job_id: int,
    ) -> JobModel | None:
        """
        根据职位 ID 查询。

        查询不到时返回 None。
        """
        return self.session.get(JobModel, job_id)

