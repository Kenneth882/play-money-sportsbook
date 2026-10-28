import pytest
from sqlalchemy import text
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session, sessionmaker

pytestmark = pytest.mark.integration


def test_committed_write_persists_and_rolled_back_write_does_not(
    session_factory: sessionmaker[Session],
) -> None:
    with session_factory() as session, session.begin():
        session.execute(text("CREATE TABLE probe (value INT NOT NULL)"))
    try:
        with session_factory() as session, session.begin():
            session.execute(text("INSERT INTO probe VALUES (1)"))

        with pytest.raises(RuntimeError), session_factory() as session, session.begin():
            session.execute(text("INSERT INTO probe VALUES (2)"))
            raise RuntimeError("abort the transaction")

        with session_factory() as session, session.begin():
            values = session.execute(text("SELECT value FROM probe")).scalars().all()
        assert values == [1]
    finally:
        with session_factory() as session, session.begin():
            session.execute(text("DROP TABLE probe"))


def test_session_refuses_work_outside_an_explicit_transaction(
    session_factory: sessionmaker[Session],
) -> None:
    with session_factory() as session, pytest.raises(InvalidRequestError):
        session.execute(text("SELECT 1"))
