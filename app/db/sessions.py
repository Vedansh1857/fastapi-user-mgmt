from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.ext.declarative import declarative_base

# MySQL connection string
engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()