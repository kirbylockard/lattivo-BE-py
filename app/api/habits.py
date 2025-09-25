from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

# In-memory store (or later, DB)
class HabitStore:
    def __init__(self):
        self.habits = []
        self.counter = 1

    def reset(self):
        self.habits.clear()
        self.counter = 1

    def list(self):
        return self.habits

    def create(self, name: str, description: str):
        habit = {"id": self.counter, "name": name, "description": description}
        self.habits.append(habit)
        self.counter += 1
        return habit


store = HabitStore()

# Pydantic models
class Habit(BaseModel):
    id: int
    name: str
    description: str

class HabitCreate(BaseModel):
    name: str
    description: str

# Routes
@router.get("/", response_model=List[Habit])
async def list_habits():
    return store.list()

@router.post("/", response_model=Habit, status_code=201)
async def create_habit(habit: HabitCreate):
    return store.create(habit.name, habit.description)
