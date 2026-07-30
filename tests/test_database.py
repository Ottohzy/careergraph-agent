from sqlalchemy import create_engine
from sqlalchemy import inspect

from careergraph.database import Base
from careergraph import db_models


def test_create_all_creates_expected_tables(
    tmp_path,
) -> None:
    database_path = tmp_path / "test.db"

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)

    table_names = set(
        inspector.get_table_names()
    )

    assert "candidates" in table_names
    assert "skills" in table_names
    assert "experiences" in table_names
    assert "candidate_skills" in table_names