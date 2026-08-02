# src/careergraph/repositories/candidate_repository.py

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from careergraph.db.db_models import CandidateModel


class CandidateRepository:
    """
    负责 CandidateModel 的数据库访问。

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
        candidate: CandidateModel,
    ) -> CandidateModel:
        """
        创建候选人。

        flush 会把数据发送到数据库，
        但不会结束当前事务。
        """
        self.session.add(candidate)
        self.session.flush()

        # flush 后数据库已经为 candidate 生成 id
        self.session.refresh(candidate)

        return candidate

    def get_by_id(
        self,
        candidate_id: int,
    ) -> CandidateModel | None:
        """
        根据候选人 ID 查询。

        同时加载候选人的：
        - skills
        - experiences

        查询不到时返回 None。
        """
        statement = (
            select(CandidateModel)
            .options(
                selectinload(
                    CandidateModel.skills,
                ),
                selectinload(
                    CandidateModel.experiences,
                ),
            )
            .where(
                CandidateModel.id == candidate_id,
            )
        )

        return self.session.scalar(statement)

    def get_by_name(
        self,
        name: str,
    ) -> CandidateModel | None:
        """
        根据候选人姓名查询。

        这里只进行精确查询，不负责 strip、
        lower 等标准化操作。
        """
        statement = (
            select(CandidateModel)
            .options(
                selectinload(
                    CandidateModel.skills,
                ),
                selectinload(
                    CandidateModel.experiences,
                ),
            )
            .where(
                CandidateModel.name == name,
            )
        )

        return self.session.scalar(statement)

    def get_all(
        self,
    ) -> list[CandidateModel]:
        """
        查询所有候选人。

        按照 ID 从小到大排列，
        同时加载技能和经历。
        """
        statement = (
            select(CandidateModel)
            .options(
                selectinload(
                    CandidateModel.skills,
                ),
                selectinload(
                    CandidateModel.experiences,
                ),
            )
            .order_by(
                CandidateModel.id,
            )
        )

        result = self.session.scalars(statement)

        return list(result.all())

    def update(
        self,
        candidate: CandidateModel,
    ) -> CandidateModel:
        """
        保存候选人的更新。

        candidate 必须是当前 Session 管理的对象。
        """
        self.session.add(candidate)
        self.session.flush()

        return candidate

    def delete(
        self,
        candidate: CandidateModel,
    ) -> None:
        """
        删除候选人。

        是否允许删除不存在的候选人，
        应由 Service 层判断。
        """
        self.session.delete(candidate)
        self.session.flush()

    def exists_by_id(
        self,
        candidate_id: int,
    ) -> bool:
        """
        判断候选人 ID 是否存在。
        """
        statement = (
            select(CandidateModel.id)
            .where(
                CandidateModel.id == candidate_id,
            )
        )

        candidate_id_result = self.session.scalar(
            statement,
        )

        return candidate_id_result is not None

    def exists_by_name(
        self,
        name: str,
    ) -> bool:
        """
        判断候选人姓名是否存在。
        """
        statement = (
            select(CandidateModel.id)
            .where(
                CandidateModel.name == name,
            )
        )

        candidate_id = self.session.scalar(statement)

        return candidate_id is not None