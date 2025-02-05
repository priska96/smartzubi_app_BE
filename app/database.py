from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .envConfig import Config

SQLALCHEMY_DATABASE_URL = "postgresql://"+ Config.DB_HOSTNAME+":"+Config.DB_PASSWORD+"@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
