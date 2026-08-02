import pytest

from careergraph.jd_extractor import extract_skills
from careergraph.schema import JobSkill


def skills_to_dict(
    skills: list[JobSkill],
) -> dict[str, bool]:
    """
    将 JobSkill 列表转换成字典，方便测试时比较。

    示例：
    [
        JobSkill(name="Python", required=True),
        JobSkill(name="Docker", required=False),
    ]

    转换为：
    {
        "Python": True,
        "Docker": False,
    }
    """
    return {
        skill.name: skill.required
        for skill in skills
    }


def test_extract_standard_skill():
    aliases = {
        "python": "Python",
    }

    jd_text = "Strong Python programming skills required."

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Python",
            required=True,
        )
    ]


def test_extract_skill_alias():
    aliases = {
        "postgres": "PostgreSQL",
    }

    jd_text = "Experience using Postgres is required."

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="PostgreSQL",
            required=True,
        )
    ]


def test_extract_skill_ignores_case():
    aliases = {
        "python": "Python",
    }

    jd_text = "PYTHON experience is required."

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Python",
            required=True,
        )
    ]


def test_extract_removes_duplicate_skills():
    aliases = {
        "python": "Python",
        "python3": "Python",
        "py": "Python",
    }

    jd_text = (
        "Experience with Python, Python3 "
        "and Py is required."
    )

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Python",
            required=True,
        )
    ]


def test_extract_preferred_skill():
    aliases = {
        "docker": "Docker",
    }

    jd_text = "Docker experience is preferred."

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Docker",
            required=False,
        )
    ]


def test_extract_nice_to_have_skill():
    aliases = {
        "kubernetes": "Kubernetes",
    }

    jd_text = "Kubernetes experience is nice to have."

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Kubernetes",
            required=False,
        )
    ]


def test_extract_a_plus_skill():
    aliases = {
        "docker": "Docker",
    }

    jd_text = "Docker knowledge would be a plus."

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Docker",
            required=False,
        )
    ]


def test_extract_bonus_skill():
    aliases = {
        "langchain": "LangChain",
    }

    jd_text = "LangChain experience is a bonus."

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="LangChain",
            required=False,
        )
    ]


def test_extract_chinese_preferred_skill():
    aliases = {
        "docker": "Docker",
    }

    jd_text = "有 Docker 使用经验者优先。"

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Docker",
            required=False,
        )
    ]


def test_extract_chinese_bonus_skill():
    aliases = {
        "langchain": "LangChain",
    }

    jd_text = "掌握 LangChain 属于加分项。"

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="LangChain",
            required=False,
        )
    ]


def test_required_overrides_preferred():
    aliases = {
        "python": "Python",
    }

    jd_text = """
    Python experience is preferred.
    Strong Python skills are required.
    """

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Python",
            required=True,
        )
    ]


def test_required_remains_required_when_preferred_appears_later():
    aliases = {
        "python": "Python",
    }

    jd_text = """
    Strong Python skills are required.
    Additional Python project experience is preferred.
    """

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Python",
            required=True,
        )
    ]


def test_extract_multiple_skills():
    aliases = {
        "python": "Python",
        "sql": "SQL",
        "docker": "Docker",
    }

    jd_text = """
    Strong Python and SQL skills are required.
    Docker experience is preferred.
    """

    result = extract_skills(jd_text, aliases)

    assert skills_to_dict(result) == {
        "Python": True,
        "SQL": True,
        "Docker": False,
    }


def test_extract_multiple_aliases_for_different_skills():
    aliases = {
        "py": "Python",
        "postgres": "PostgreSQL",
        "docker": "Docker",
    }

    jd_text = """
    Experience with Py and Postgres is required.
    Docker experience is nice to have.
    """

    result = extract_skills(jd_text, aliases)

    assert skills_to_dict(result) == {
        "Python": True,
        "PostgreSQL": True,
        "Docker": False,
    }


def test_extract_empty_text():
    aliases = {
        "python": "Python",
    }

    result = extract_skills("", aliases)

    assert result == []


def test_extract_whitespace_only_text():
    aliases = {
        "python": "Python",
    }

    result = extract_skills(
        "   \n\n   ",
        aliases,
    )

    assert result == []


def test_extract_no_matching_skills():
    aliases = {
        "python": "Python",
        "docker": "Docker",
    }

    jd_text = (
        "Excellent communication and "
        "teamwork skills are required."
    )

    result = extract_skills(jd_text, aliases)

    assert result == []


def test_extract_with_empty_aliases():
    jd_text = "Python and Docker are required."

    result = extract_skills(jd_text, {})

    assert result == []


def test_extract_same_skill_on_multiple_lines():
    aliases = {
        "python": "Python",
    }

    jd_text = """
    Python programming experience required.
    Strong Python debugging skills required.
    Python project experience required.
    """

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Python",
            required=True,
        )
    ]


def test_extract_ignores_empty_lines():
    aliases = {
        "python": "Python",
        "docker": "Docker",
    }

    jd_text = """

    Python experience is required.


    Docker experience is preferred.

    """

    result = extract_skills(jd_text, aliases)

    assert skills_to_dict(result) == {
        "Python": True,
        "Docker": False,
    }


@pytest.mark.parametrize(
    (
        "marker",
        "expected_required",
    ),
    [
        ("preferred", False),
        ("nice to have", False),
        ("a plus", False),
        ("bonus", False),
        ("优先", False),
        ("加分项", False),
        ("最好具备", False),
    ],
)
def test_extract_preferred_markers(
    marker: str,
    expected_required: bool,
):
    aliases = {
        "docker": "Docker",
    }

    jd_text = f"Docker experience is {marker}."

    result = extract_skills(jd_text, aliases)

    assert result == [
        JobSkill(
            name="Docker",
            required=expected_required,
        )
    ]