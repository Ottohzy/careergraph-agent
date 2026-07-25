import json

import pytest

from careergraph.config_loader import (
    load_skill_aliases,
    load_skill_catalog,
)


def test_load_skill_catalog(tmp_path):
    file_path = tmp_path / "skill_catalog.json"

    catalog = [
        {
            "name": "Python",
            "category": "programming_language",
        },
        {
            "name": "Docker",
            "category": "devops",
        },
    ]

    file_path.write_text(
        json.dumps(catalog),
        encoding="utf-8",
    )

    result = load_skill_catalog(file_path)

    assert result == catalog


def test_load_skill_aliases(tmp_path):
    file_path = tmp_path / "skill_aliases.json"

    aliases = {
        "py": "Python",
        "python3": "Python",
        "postgres": "PostgreSQL",
    }

    file_path.write_text(
        json.dumps(aliases),
        encoding="utf-8",
    )

    result = load_skill_aliases(file_path)

    assert result == aliases


def test_load_skill_catalog_raises_error_when_not_list(
    tmp_path,
):
    file_path = tmp_path / "skill_catalog.json"

    invalid_catalog = {
        "name": "Python",
        "category": "programming_language",
    }

    file_path.write_text(
        json.dumps(invalid_catalog),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Skill catalog must be a JSON array",
    ):
        load_skill_catalog(file_path)


def test_load_skill_aliases_raises_error_when_not_dict(
    tmp_path,
):
    file_path = tmp_path / "skill_aliases.json"

    invalid_aliases = [
        {
            "alias": "py",
            "skill": "Python",
        }
    ]

    file_path.write_text(
        json.dumps(invalid_aliases),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Skill aliases must be a JSON object",
    ):
        load_skill_aliases(file_path)


def test_load_skill_catalog_raises_error_when_file_missing(
    tmp_path,
):
    missing_file = tmp_path / "missing_catalog.json"

    with pytest.raises(FileNotFoundError):
        load_skill_catalog(missing_file)


def test_load_skill_catalog_raises_error_for_invalid_json(
    tmp_path,
):
    file_path = tmp_path / "skill_catalog.json"

    file_path.write_text(
        '{"name": "Python",}',
        encoding="utf-8",
    )

    with pytest.raises(json.JSONDecodeError):
        load_skill_catalog(file_path)