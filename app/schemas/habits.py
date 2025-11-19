# app/schemas/habits.py
from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------------------------
# Nested types: Unit + Schedule (mirror your frontend types)
# ---------------------------------------------------------------------------


class HabitUnit(BaseModel):
    """
    Mirrors frontend HabitUnit:

    export type HabitUnit = {
      unitKey: string;
      isCustom: boolean;
      customLabel?: string;
      allowsDecimal?: boolean;
      category?: UnitCategory;
    };
    """

    unitKey: str
    isCustom: bool
    customLabel: Optional[str] = None
    allowsDecimal: Optional[bool] = None
    category: Optional[str] = None  # you can make this a Literal of categories later


class SpecificDaysSchedule(BaseModel):
    """
    { type: 'specific-days', daysOfWeek: number[] }
    """

    type: Literal["specific-days"]
    daysOfWeek: List[int]


class RollingSchedule(BaseModel):
    """
    {
      type: 'rolling',
      intervalType: 'day' | 'week' | 'month',
      intervalQuantity: number,
      resetOnMiss: boolean
    }
    """

    type: Literal["rolling"]
    intervalType: Literal["day", "week", "month"]
    intervalQuantity: int
    resetOnMiss: bool


class FlexibleWindowSchedule(BaseModel):
    """
    {
      type: 'flexible-window',
      windowLength: number,
      intervalType: 'day' | 'week' | 'month',
      resetOnMiss: boolean
    }
    """

    type: Literal["flexible-window"]
    windowLength: int
    intervalType: Literal["day", "week", "month"]
    resetOnMiss: bool


HabitSchedule = Union[
    SpecificDaysSchedule,
    RollingSchedule,
    FlexibleWindowSchedule,
]


# ---------------------------------------------------------------------------
# Habit base + variants
# ---------------------------------------------------------------------------


class HabitBase(BaseModel):
    """
    Shared fields for create/read (no id/creationDate here).
    Internal names are snake_case; JSON uses camelCase via aliases.
    """

    model_config = ConfigDict(populate_by_name=True)

    user_id: UUID = Field(..., alias="userId")
    name: str
    unit: HabitUnit
    target_value: float = Field(..., alias="targetValue")
    schedule: HabitSchedule
    notes: Optional[str] = None
    color: Optional[str] = None

    is_active: bool = Field(default=True, alias="isActive")
    is_archived: bool = Field(default=False, alias="isArchived")

    end_date: Optional[datetime] = Field(default=None, alias="endDate")
    tags: Optional[List[str]] = None


class HabitCreate(HabitBase):
    """
    Input for creating a habit.

    Same fields as HabitBase. The DB will generate:
      - id
      - creation_date
    """
    pass


class HabitRead(HabitBase):
    """
    Output model for a habit.

    Includes:
      - id
      - creationDate (aliased from creation_date)
    """

    id: UUID
    creation_date: datetime = Field(..., alias="creationDate")

    model_config = ConfigDict(
        from_attributes=True,  # allow .from_orm()
        populate_by_name=True,
    )


class HabitUpdate(BaseModel):
    """
    Partial update for a habit.

    All fields optional. Uses snake_case internally, camelCase in JSON.
    """

    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = None
    unit: Optional[HabitUnit] = None
    schedule: Optional[HabitSchedule] = None
    notes: Optional[str] = None
    color: Optional[str] = None

    target_value: Optional[float] = Field(default=None, alias="targetValue")
    is_active: Optional[bool] = Field(default=None, alias="isActive")
    is_archived: Optional[bool] = Field(default=None, alias="isArchived")
    end_date: Optional[datetime] = Field(default=None, alias="endDate")
    tags: Optional[List[str]] = None


class HabitList(BaseModel):
    """
    Wrapper for list responses so you can add pagination later.
    """

    items: List[HabitRead]

    model_config = ConfigDict(populate_by_name=True)
