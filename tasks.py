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
        "grader": "graders:grade_task_0",
        "graders": ["graders:grade_task_0"],
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
        "grader": "graders:grade_task_1",
        "graders": ["graders:grade_task_1"],
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
        "grader": "graders:grade_task_2",
        "graders": ["graders:grade_task_2"],
    },
]

TASK_ID_TO_INDEX = {
    "reach_positive_ten": 0,
    "reach_negative_ten": 1,
    "reach_positive_five": 2,
}
