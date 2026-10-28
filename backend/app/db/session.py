from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_db_engine(url: str) -> Engine:
    return create_engine(url, pool_pre_ping=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    # autobegin=False: any query outside `with session.begin():` raises, so every
    # transaction boundary in the codebase is explicit.
    return sessionmaker(engine, autobegin=False, expire_on_commit=False)
