from datetime import timedelta
from time import sleep

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import current_user
from src.auth.models import User
from src.database import get_async_session
from sqlalchemy import select, insert, delete

from src.tasks.models import Task
from src.tasks.schemas import TaskCreate

from src.background_tasks.tasks import send_task_notification

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@router.get("")
async def get_user_tasks(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Task).filter_by(executor=user.id)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception:
        return {
            "status": "error",
            "msg": None
        }


@router.post("/add_task")
async def add_task(
        new_task: TaskCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    if new_task.owner_id is None:
        new_task.owner_id = user.id
    if new_task.executor is None:
        new_task.executor = user.id
    send_task_notification.apply_async((user.username, user.email, new_task.name),
                                       eta=new_task.finish_date-timedelta(hours=1))
    stmt = insert(Task).values(**new_task.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "msg": None
    }


@router.post("/delete_task")
async def delete_task(
        del_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Task).where(Task.id == del_id)
    res = await session.execute(query)
    result = res.all()
    print(len(result))
    if len(result) == 0:
        return {
            "status": "error",
            "msg": "task doesnt exists"
        }
    else:
        stmt = delete(Task).where(Task.id == del_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "msg": None
        }


@router.get("/test")
@cache(expire=10)
async def test_apicache():
    sleep(2)
    return {"some data"}
