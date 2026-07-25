import json
from pathlib import Path
from typing import Any


def load_json(
    file_path: str | Path,
) -> Any:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_skill_catalog(
    file_path: str | Path,
) -> list[dict[str, Any]]:
    catalog = load_json(file_path)

    if not isinstance(catalog, list):
        raise ValueError(
            "Skill catalog must be a JSON array."
        )

    return catalog


def load_skill_aliases(
    file_path: str | Path,
) -> dict[str, str]:
    aliases = load_json(file_path)

    if not isinstance(aliases, dict):
        raise ValueError(
            "Skill aliases must be a JSON object."
        )

    if not all(
        isinstance(alias, str)
        and isinstance(skill_name, str)
        for alias, skill_name in aliases.items()
    ):
        raise ValueError(
            "Skill aliases must map strings to strings."
        )

    return aliases