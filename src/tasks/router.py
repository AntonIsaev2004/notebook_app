from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import fastapi_users
from src.auth.models import User
from src.database import get_async_session
from sqlalchemy import select, insert

from src.tasks.models import Task
from src.tasks.schemas import TaskCreate

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)

current_user = fastapi_users.current_user()


@router.get("")
async def get_user_tasks(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Task).filter_by(owner_id=user.id - 1)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception:
        return {
            "status": "error"
        }


@router.post("")
async def add_task(
        new_task: TaskCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    new_task.owner_id = user.id
    stmt = insert(Task).values(**new_task.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success"
    }
