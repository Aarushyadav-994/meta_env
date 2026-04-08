from pydantic import BaseModel


class ReachAction(BaseModel):
    action: int


class ReachObservation(BaseModel):
    position: float
    target_position: float


class ReachState(BaseModel):
    task_id: int
    position: float
    target_position: float
    steps_taken: int
    max_steps: int
