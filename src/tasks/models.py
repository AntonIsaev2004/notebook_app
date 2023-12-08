from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from src.database import Base


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, nullable=False)
    finish_date = Column(TIMESTAMP, nullable=False)
    owner_id = Column(Integer)
    executor = Column(Integer)
    name = Column(String)
    importance = Column(Integer)
    creation_date = Column(TIMESTAMP)
    tags = Column(JSON)
    task = Column(String)
