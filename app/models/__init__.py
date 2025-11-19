# app/models/__init__.py
from app.core.database import Base  # re-export Base so Alembic etc. can find models

from .habit import Habit, HabitLog  # noqa: F401
