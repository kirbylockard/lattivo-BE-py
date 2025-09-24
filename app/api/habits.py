from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_session
from app.models.habit import Habit

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.get("/")
async def list_habits(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Habit))
    habits = result.scalars().all()
    return habits
