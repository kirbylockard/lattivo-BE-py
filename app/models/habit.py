# app/models/habit.py
from __future__ import annotations

import uuid
from datetime import date, datetime

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
    Mirrors the Supabase `public.habits` table and your frontend Habit type.
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

    # Optional fields
    notes = Column(Text, nullable=True)
    color = Column(String, nullable=True)

    # JSONB blobs that mirror HabitUnit & HabitSchedule from the frontend
    unit = Column(JSONB, nullable=False)
    target_value = Column(Numeric(18, 4), nullable=False)
    schedule = Column(JSONB, nullable=False)

    is_active = Column(Boolean, nullable=False, server_default="true")

    # Supabase uses DATE, not timestamptz, for end_date
    end_date = Column(Date, nullable=True)

    is_archived = Column(Boolean, nullable=False, server_default="false")

    # text[] in Supabase
    tags = Column(ARRAY(String), nullable=True)

    # Supabase timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        # pylint: disable=not-callable
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        # pylint: disable=not-callable
        server_default=func.now(),
    )


class HabitLog(Base):
    """
    Habit logs table (local dev only for now).
    Not yet created in Supabase – you can add it later if you want.
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

    # logical date the log counts for (e.g. the day it applies to)
    date = Column(Date, nullable=False)

    # 'in-progress' | 'completed' | 'partial' | ...
    status = Column(String, nullable=False)

    value = Column(Numeric(18, 4), nullable=True)
    note = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        # pylint: disable=not-callable
        server_default=func.now(),
    )
