from graders import grade_task_0, grade_task_1, grade_task_2

GRADERS = {
    "simple_reach_task_0": grade_task_0,
    "simple_reach_task_1": grade_task_1,
    "simple_reach_task_2": grade_task_2,
}

__all__ = ["grade_task_0", "grade_task_1", "grade_task_2", "GRADERS"]
