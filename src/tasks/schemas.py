from datetime import datetime
from typing import Optional
from pydantic import BaseModel, json


class TaskCreate(BaseModel):
    id: int
    finish_date: datetime
    owner_id: Optional[int] = None
    executor: Optional[int] = None
    name: Optional[str] = 'Unnamed'
    importance: Optional[int] = 1
    creation_date: Optional[datetime] = datetime.now()
    tags: Optional[list] = None
    task: Optional[str] = None



class TaskRead(BaseModel):
    name: str
    tags: list
    creation_date: datetime
    finish_date: datetime
    task: str
