TASK = {
    "id": "simple_reach_task_2",
    "task_id": "reach_positive_five",
    "name": "reach-positive-five",
    "difficulty": "hard",
    "description": "Start at 0 and reach target position 5.0 on a 1D line.",
    "max_steps": 32,
    "reset_params": {"task_id": 2},
    "action_schema": {"action": "0 for left, 1 for right", "task_id": "reach_positive_five"},
    "grader": "graders.task_2:grade",
    "graders": ["graders.task_2:grade"],
}
