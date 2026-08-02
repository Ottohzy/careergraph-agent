from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from careergraph.db.db_models import (
    CandidateModel,
    ExperienceModel,
    SkillModel,
)
from careergraph.exceptions import (
    CandidateNotFoundError,
    DuplicateCandidateError,
)
from careergraph.repositories.candidate_repository import (
    CandidateRepository,
)
from careergraph.schema import (
    CandidateCreate,
    CandidateUpdate,
    Experience,
    ExperienceCreate,
    Skill,
)


class CandidateService:
    """
    负责候选人相关业务逻辑。

    Service 层负责：
    - 业务规则
    - 重复数据检查
    - 技能标准化
    - 技能复用
    - 事务提交和回滚
    - 业务异常
    """

    def __init__(
        self,
        session: Session,
        candidate_repository: CandidateRepository,
    ) -> None:
        self.session = session
        self.candidate_repository = candidate_repository

    def create_candidate(
        self,
        candidate_data: CandidateCreate,
    ) -> CandidateModel:
        """
        创建候选人，并保存技能和经历。

        同名候选人已存在时抛出
        DuplicateCandidateError。
        """
        normalized_name = self._normalize_candidate_name(
            candidate_data.name,
        )

        existing_candidate = (
            self.candidate_repository.get_by_name(
                normalized_name,
            )
        )

        if existing_candidate is not None:
            raise DuplicateCandidateError(
                f"Candidate already exists: "
                f"{normalized_name}"
            )

        try:
            candidate = CandidateModel(
                name=normalized_name,
            )

            candidate.skills = self._get_or_create_skills(
                candidate_data.skills,
            )

            candidate.experiences = (
                self._build_experiences(
                    candidate_data.experiences,
                )
            )

            created_candidate = (
                self.candidate_repository.create(
                    candidate,
                )
            )

            self.session.commit()

            return self._reload_candidate(
                created_candidate.id,
            )

        except IntegrityError as exc:
            self.session.rollback()

            raise DuplicateCandidateError(
                "Candidate or skill data already exists."
            ) from exc

        except Exception:
            self.session.rollback()
            raise

    def get_candidate(
        self,
        candidate_id: int,
    ) -> CandidateModel:
        """
        根据 ID 查询候选人。

        不存在时抛出 CandidateNotFoundError。
        """
        candidate = (
            self.candidate_repository.get_by_id(
                candidate_id,
            )
        )

        if candidate is None:
            raise CandidateNotFoundError(
                f"Candidate not found: {candidate_id}"
            )

        return candidate

    def get_all_candidates(
        self,
    ) -> list[CandidateModel]:
        """
        查询所有候选人。
        """
        return self.candidate_repository.get_all()

    def update_candidate(
        self,
        candidate_id: int,
        candidate_data: CandidateUpdate,
    ) -> CandidateModel:
        """
        更新候选人的姓名、技能和经历。

        CandidateUpdate 中为 None 的字段不会修改。
        空列表表示清空对应关系。
        """
        candidate = self.get_candidate(candidate_id)

        try:
            if candidate_data.name is not None:
                normalized_name = (
                    self._normalize_candidate_name(
                        candidate_data.name,
                    )
                )

                self._check_duplicate_name(
                    candidate_id=candidate_id,
                    name=normalized_name,
                )

                candidate.name = normalized_name

            if candidate_data.skills is not None:
                candidate.skills = (
                    self._get_or_create_skills(
                        candidate_data.skills,
                    )
                )

            if candidate_data.experiences is not None:
                candidate.experiences = (
                    self._build_experiences(
                        candidate_data.experiences,
                    )
                )

            self.candidate_repository.update(
                candidate,
            )

            self.session.commit()

            return self._reload_candidate(
                candidate_id,
            )

        except IntegrityError as exc:
            self.session.rollback()

            raise DuplicateCandidateError(
                "Candidate or skill data already exists."
            ) from exc

        except Exception:
            self.session.rollback()
            raise

    def delete_candidate(
        self,
        candidate_id: int,
    ) -> None:
        """
        删除候选人。

        候选人不存在时抛出
        CandidateNotFoundError。
        """
        candidate = self.get_candidate(candidate_id)

        try:
            self.candidate_repository.delete(
                candidate,
            )

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

    def _normalize_candidate_name(
        self,
        name: str,
    ) -> str:
        """
        去除候选人姓名首尾空格。

        这里暂时保留原始大小写，
        避免把人名全部转换为小写。
        """
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError(
                "Candidate name cannot be empty."
            )

        return normalized_name

    def _normalize_skill_name(
        self,
        name: str,
    ) -> str:
        """
        技能名称统一：
        - 去除首尾空格
        - 转为小写
        """
        return name.strip().lower()

    def _normalize_skill_names(
        self,
        skill_names: list[str],
    ) -> list[str]:
        """
        标准化并去除重复技能。

        保留技能首次出现的顺序。
        """
        normalized_skills: list[str] = []
        seen: set[str] = set()

        for skill_name in skill_names:
            normalized_name = (
                self._normalize_skill_name(
                    skill_name,
                )
            )

            if not normalized_name:
                continue

            if normalized_name in seen:
                continue

            seen.add(normalized_name)
            normalized_skills.append(
                normalized_name,
            )

        return normalized_skills

    def _get_or_create_skills(
        self,
        skill_inputs: list[str | Skill],
    ) -> list[SkillModel]:
        """
        查询或创建技能。

        如果技能已经存在，复用已有 SkillModel；
        如果不存在，创建新的 SkillModel。
        """
        normalized_names = (
            self._normalize_skill_names(
                self._extract_skill_names(
                    skill_inputs,
                ),
            )
        )

        skills: list[SkillModel] = []

        for skill_name in normalized_names:
            existing_skill = (
                self._get_skill_by_name(
                    skill_name,
                )
            )

            if existing_skill is not None:
                skills.append(existing_skill)
            else:
                skill = SkillModel(
                    name=skill_name,
                )

                self.session.add(skill)
                skills.append(skill)

        return skills

    def _get_skill_by_name(
        self,
        skill_name: str,
    ) -> SkillModel | None:
        """
        根据标准化后的技能名称查询 Skill。
        """
        statement = (
            select(SkillModel)
            .where(
                SkillModel.name == skill_name,
            )
        )

        return self.session.scalar(statement)

    def _extract_skill_names(
        self,
        skill_inputs: list[str | Skill],
    ) -> list[str]:
        """
        将技能输入统一为字符串列表。
        """
        skill_names: list[str] = []

        for skill_input in skill_inputs:
            if isinstance(skill_input, Skill):
                skill_names.append(skill_input.name)
            else:
                skill_names.append(skill_input)

        return skill_names

    def _build_experiences(
        self,
        experiences: list[ExperienceCreate | Experience],
    ) -> list[ExperienceModel]:
        """
        把 ExperienceCreate 转为 ORM 对象。
        """
        experience_models: list[
            ExperienceModel
        ] = []

        for experience_data in experiences:
            title = experience_data.title.strip()
            description = (
                experience_data.description.strip()
            )

            if not title:
                raise ValueError(
                    "Experience title cannot be empty."
                )

            if not description:
                raise ValueError(
                    "Experience description "
                    "cannot be empty."
                )

            experience_models.append(
                ExperienceModel(
                    title=title,
                    description=description,
                )
            )

        return experience_models

    def _check_duplicate_name(
        self,
        candidate_id: int,
        name: str,
    ) -> None:
        """
        更新姓名时检查是否被其他候选人使用。
        """
        existing_candidate = (
            self.candidate_repository.get_by_name(
                name,
            )
        )

        if (
            existing_candidate is not None
            and existing_candidate.id
            != candidate_id
        ):
            raise DuplicateCandidateError(
                f"Candidate already exists: {name}"
            )

    def _reload_candidate(
        self,
        candidate_id: int,
    ) -> CandidateModel:
        """
        提交事务后重新加载候选人及其关系。
        """
        candidate = (
            self.candidate_repository.get_by_id(
                candidate_id,
            )
        )

        if candidate is None:
            raise CandidateNotFoundError(
                f"Candidate not found after save: "
                f"{candidate_id}"
            )

        return candidate