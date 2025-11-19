# app/api/habits.py
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.params import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.habit import Habit
from app.schemas.habits import HabitCreate, HabitRead, HabitUpdate, HabitList

router = APIRouter()


# ---------------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------------


@router.post(
    "/",
    response_model=HabitRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_habit(
    habit_in: HabitCreate,
    session: AsyncSession = Depends(get_session),
) -> HabitRead:
    """
    Create a new habit.

    - Accepts camelCase JSON (userId, targetValue, etc.).
    - Internally uses snake_case (user_id, target_value, etc.) to match the DB.
    """

    # Convert Pydantic model → plain dict with snake_case keys
    data = habit_in.model_dump(by_alias=False)

    db_habit = Habit(**data)
    session.add(db_habit)
    await session.commit()
    await session.refresh(db_habit)

    # Return as HabitRead, using from_attributes/from_orm
    return HabitRead.model_validate(db_habit, from_attributes=True)


# ---------------------------------------------------------------------------
# LIST
# ---------------------------------------------------------------------------


@router.get(
    "/",
    response_model=HabitList,
)
async def list_habits(
    userId: UUID = Query(..., description="The user's UUID"),
    session: AsyncSession = Depends(get_session),
) -> HabitList:
    """
    List all habits belonging to a specific user.
    Requires a userId query parameter.
    """

    # Query habits filtered by this user
    result = await session.execute(select(Habit).where(Habit.user_id == userId))
    habits: List[Habit] = result.scalars().all()

    items = [HabitRead.model_validate(h, from_attributes=True) for h in habits]

    return HabitList(items=items)


# ---------------------------------------------------------------------------
# READ ONE
# ---------------------------------------------------------------------------


@router.get(
    "/{habit_id}",
    response_model=HabitRead,
)
async def get_habit(
    habit_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> HabitRead:
    """
    Get a single habit by its id.
    """

    db_habit = await session.get(Habit, habit_id)
    if not db_habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return HabitRead.model_validate(db_habit, from_attributes=True)


# ---------------------------------------------------------------------------
# UPDATE (PARTIAL)
# ---------------------------------------------------------------------------


@router.patch(
    "/{habit_id}",
    response_model=HabitRead,
)
async def update_habit(
    habit_id: UUID,
    habit_update: HabitUpdate,
    session: AsyncSession = Depends(get_session),
) -> HabitRead:
    """
    Partially update a habit.

    Only fields present in the body are updated.
    """

    db_habit = await session.get(Habit, habit_id)
    if not db_habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    update_data = habit_update.model_dump(
        exclude_unset=True,
        by_alias=False,  # use snake_case keys
    )

    for field, value in update_data.items():
        setattr(db_habit, field, value)

    session.add(db_habit)
    await session.commit()
    await session.refresh(db_habit)

    return HabitRead.model_validate(db_habit, from_attributes=True)


# ---------------------------------------------------------------------------
# DELETE (NO CONTENT)
# ---------------------------------------------------------------------------


@router.delete(
    "/{habit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_habit(
    habit_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> Response:
    """
    Delete a habit.

    204 No Content MUST NOT have a response body, so we:
    - don't declare a response_model
    - explicitly return an empty Response with status 204
    """

    db_habit = await session.get(Habit, habit_id)
    if not db_habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    await session.delete(db_habit)
    await session.commit()

    # 204 with no body
    return Response(status_code=status.HTTP_204_NO_CONTENT)
