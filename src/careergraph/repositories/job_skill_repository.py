from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from careergraph.db.db_models import JobSkillModel

class JobSkillRepository:
    """
    负责 JobSkillModel 的数据库访问。

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

    def replace_for_job(
           self,
           job_id: int,
           *,
           skills: list[dict[str, object]],
       ) -> list[JobSkillModel] :
           """
           替换职位的技能。
   
           1. 删除原有技能
           2. 添加新技能
           """
           delete_statement = delete(JobSkillModel).where(JobSkillModel.job_id == job_id)
           self.session.execute(delete_statement)
           models = [
               JobSkillModel(
                   job_id=job_id,
                   name=skill["name"],
                   level=skill.get("level"),
                   description=skill.get("description"),
               )
               for skill in skills
           ]
           self.session.add_all(models)
           self.session.commit()
   
           for model in models:
               self.session.refresh(model)
   
           return models
   
    def list_by_job_id(
           self,
           job_id: int,
       ) -> list[JobSkillModel]:
           """
           根据职位 ID 查询技能列表。
   
           查询不到时返回空列表。
           """
           statement = (select(JobSkillModel).where(JobSkillModel.job_id == job_id).order_by(JobSkillModel.id))
           return list(self.session.scalars(statement).all())