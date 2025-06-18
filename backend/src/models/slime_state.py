# src/models/slime_state.py
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class Position:
    x: float
    y: float
    z: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Position':
        return cls(
            x=data.get('x', 0.0),
            y=data.get('y', 0.0),
            z=data.get('z', 0.0)
        )
    
    def to_dict(self) -> Dict[str, float]:
        return {'x': self.x, 'y': self.y, 'z': self.z}

@dataclass
class SlimeState:
    current_state: str
    duration: int
    position: Position
    hunger: int
    happiness: int
    food_present: bool
    food_position: Position
    recent_actions: List[str]
    current_input: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SlimeState':
        return cls(
            current_state=data.get('current_state', 'idle'),
            duration=data.get('duration', 10),
            position=Position.from_dict(data.get('position', {})),
            hunger=data.get('hunger', 5),
            happiness=data.get('happiness', 10),
            food_present=data.get('food_present', False),
            food_position=Position.from_dict(data.get('food_position', {})),
            recent_actions=data.get('recent_actions', []),
            current_input=data.get('current_input', '')
        )

@dataclass
class AIResponse:
    params: Dict[str, Any]
    narration: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'params': self.params,
            'narration': self.narration
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIResponse':
        return cls(
            params=data.get('params', {}),
            narration=data.get('narration', '')
        )