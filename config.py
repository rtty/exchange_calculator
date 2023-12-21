from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    """
    The application settings.
    """
    DATABASE_URL: str

    class Config:
        env_file = '.env'


# configuration
config = Settings()

# database dependency
engine = create_engine(config.DATABASE_URL, echo=True, echo_pool='debug')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Injects database session.

    :return: db session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
