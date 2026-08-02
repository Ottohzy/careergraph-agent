from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from careergraph.db.base import Base


@pytest.fixture
def session() -> Generator[Session, None, None]:
    """
    为每个测试创建一个独立的内存数据库。

    测试结束后数据库自动销毁，
    不会影响 candidate.db。
    """
    engine = create_engine(
        "sqlite:///:memory:",
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as test_session:
        yield test_session

    Base.metadata.drop_all(bind=engine)
    engine.dispose()