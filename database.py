from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.types import DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///database.db")
session = sessionmaker(bind=engine)()

class Countdown(Base):
    __tablename__ = "countdowns"

    id = Column(Integer, primary_key = True)
    user_id = Column(String)
    issued_date = Column(DateTime)
    expires_at = Column(DateTime)
    hours = Column(Integer)
    minutes = Column(Integer)
    text = Column(String)
    repeat = Column(Boolean)

Base.metadata.create_all(engine)