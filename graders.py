def _normalize_reward(reward: float) -> float:
    return min(max(float(reward), 0.0), 1.0)


def grade_task_0(state: dict, reward: float) -> float:
    return _normalize_reward(reward if int(state.get("task_id", -1)) == 0 else 0.0)


def grade_task_1(state: dict, reward: float) -> float:
    return _normalize_reward(reward if int(state.get("task_id", -1)) == 1 else 0.0)


def grade_task_2(state: dict, reward: float) -> float:
    return _normalize_reward(reward if int(state.get("task_id", -1)) == 2 else 0.0)


GRADERS = {
    "simple_reach_task_0": grade_task_0,
    "simple_reach_task_1": grade_task_1,
    "simple_reach_task_2": grade_task_2,
}
