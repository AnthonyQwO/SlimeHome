# src/models/slime_state.py
from typing import List
from pydantic import BaseModel, Field

class Position(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

class SlimeState(BaseModel):
    current_state: str = "idle"
    duration: int = 10
    position: Position = Field(default_factory=Position)
    hunger: int = 5
    happiness: int = 10
    food_present: bool = False
    food_position: Position = Field(default_factory=Position)
    recent_actions: List[str] = Field(default_factory=list)
    current_input: str = ""

class NavigationParams(BaseModel):
    targetX: float
    targetZ: float

class AIResponse(BaseModel):
    params: NavigationParams
    narration: str