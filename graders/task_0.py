def _normalize_reward(reward: float) -> float:
    return min(max(float(reward), 0.0), 1.0)


def grade(state: dict, reward: float) -> float:
    return _normalize_reward(reward if int(state.get("task_id", -1)) == 0 else 0.0)
