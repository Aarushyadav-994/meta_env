TASKS = [
    {
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
        "reward_range": [0.0, 1.0],
    },
    {
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
        "reward_range": [0.0, 1.0],
    },
    {
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
        "reward_range": [0.0, 1.0],
    },
]

TASK_ID_TO_INDEX = {
    "reach_positive_ten": 0,
    "reach_negative_ten": 1,
    "reach_positive_five": 2,
}

TASK_GRADER_PAIRS = [
    ("simple_reach_task_0", "graders:grade_task_0"),
    ("simple_reach_task_1", "graders:grade_task_1"),
    ("simple_reach_task_2", "graders:grade_task_2"),
]

__all__ = ["TASKS", "TASK_ID_TO_INDEX", "TASK_GRADER_PAIRS"]
