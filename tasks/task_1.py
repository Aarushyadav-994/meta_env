TASK = {
    "id": "simple_reach_task_1",
    "task_id": "reach_negative_ten",
    "name": "reach-negative-ten",
    "difficulty": "medium",
    "description": "Start at 0 and reach target position -10.0 on a 1D line.",
    "max_steps": 32,
    "reset_params": {"task_id": 1},
    "action_schema": {"action": "0 for left, 1 for right", "task_id": "reach_negative_ten"},
    "grader": "graders.task_1:grade",
    "graders": ["graders.task_1:grade"],
}
