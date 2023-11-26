from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from src.database import Base


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String, default='Unnamed')
    owner_id = Column(Integer, nullable=False)
    tags = Column(JSON)
    creation_date = Column(TIMESTAMP, default=datetime.now)
    finish_date = Column(TIMESTAMP, nullable=False)
    task = Column(String)


