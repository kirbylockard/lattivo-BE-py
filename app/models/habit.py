# app/models/habit.py
from __future__ import annotations

import uuid
from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from app.core.database import Base


class Habit(Base):
    """
    Mirrors the frontend Habit type:

    export type Habit = {
      id: string;
      userId: string;
      name: string;
      creationDate: Date;
      endDate?: Date | null;
      isActive: boolean;
      unit: HabitUnit;        // stored as JSONB
      targetValue: number;
      schedule: HabitSchedule; // stored as JSONB
      notes?: string;
      color?: string;
      isArchived: boolean;
      tags?: string[];
    };
    """

    __tablename__ = "habits"

    id = Column(
      UUID(as_uuid=True),
      primary_key=True,
      default=uuid.uuid4,
    )

    user_id = Column(
      UUID(as_uuid=True),
      nullable=False,
      index=True,
    )

    name = Column(String, nullable=False)

    creation_date = Column(
      DateTime(timezone=True),
      nullable=False,
      # pylint: disable=not-callable
      server_default=func.now(),
    )

    end_date = Column(DateTime(timezone=True), nullable=True)

    is_active = Column(Boolean, nullable=False, server_default="true")

    # JSONB blobs that mirror your TS shapes for HabitUnit and HabitSchedule
    unit = Column(JSONB, nullable=False)
    schedule = Column(JSONB, nullable=False)

    target_value = Column(Numeric(18, 4), nullable=False)

    notes = Column(Text, nullable=True)
    color = Column(String, nullable=True)

    is_archived = Column(Boolean, nullable=False, server_default="false")

    tags = Column(ARRAY(String), nullable=True)


class HabitLog(Base):
    """
    Mirrors the frontend HabitLog type:

    export type HabitLog = {
      id: string;
      habitId: string;
      userId: string;
      date: Date;
      status: HabitLogStatus;
      value?: number;
      note?: string;
      createdAt: Date;
    };
    """

    __tablename__ = "habit_logs"

    id = Column(
      UUID(as_uuid=True),
      primary_key=True,
      default=uuid.uuid4,
    )

    habit_id = Column(
      UUID(as_uuid=True),
      ForeignKey("habits.id", ondelete="CASCADE"),
      nullable=False,
      index=True,
    )

    user_id = Column(
      UUID(as_uuid=True),
      nullable=False,
      index=True,
    )

    # “logical” date the log counts for (not necessarily created_at)
    date = Column(Date, nullable=False)

    status = Column(String, nullable=False)  # 'in-progress' | 'completed' | ...

    value = Column(Numeric(18, 4), nullable=True)
    note = Column(Text, nullable=True)

    created_at = Column(
      DateTime(timezone=True),
      nullable=False,
      # pylint: disable=not-callable
      server_default=func.now(),
    )
