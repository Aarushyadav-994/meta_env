TASK = {
    "id": "simple_reach_task_0",
    "task_id": "reach_positive_ten",
    "name": "reach-positive-ten",
    "difficulty": "easy",
    "description": "Start at 0 and reach target position 10.0 on a 1D line.",
    "max_steps": 32,
    "reset_params": {"task_id": 0},
    "action_schema": {"action": "0 for left, 1 for right", "task_id": "reach_positive_ten"},
    "grader": "graders.task_0:grade",
    "graders": ["graders.task_0:grade"],
}
