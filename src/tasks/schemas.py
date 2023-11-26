from datetime import datetime, timezone

from pydantic import BaseModel, json


class TaskCreate(BaseModel):
    name: str
    owner_id: int
    tags: list
    creation_date: datetime
    finish_date: datetime
    task: str


class TaskRead(BaseModel):
    name: str
    tags: list
    creation_date: datetime
    finish_date: datetime
    task: str
