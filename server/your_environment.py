from environment import SimpleReachEnv


class SimpleReachEnvironment:
    def __init__(self, task_id: int = 0, max_steps: int = 32) -> None:
        self.env = SimpleReachEnv(task_id=task_id, max_steps=max_steps)

    def reset(self, seed: int | None = None, options: dict | None = None):
        return self.env.reset(seed=seed, options=options)

    def step(self, action: int):
        return self.env.step(action)

    def state(self):
        return self.env.state()

    def close(self) -> None:
        self.env.close()
