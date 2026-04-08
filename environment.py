from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class SimpleReachEnv(gym.Env):
    metadata = {"render_modes": [], "render_fps": 4}

    def __init__(self, target_position: float = 10.0, max_steps: int = 32) -> None:
        super().__init__()
        self.target_position = float(target_position)
        self.max_steps = int(max_steps)

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low=np.array([-np.inf], dtype=np.float32),
            high=np.array([np.inf], dtype=np.float32),
            shape=(1,),
            dtype=np.float32,
        )

        self.position = 0.0
        self.steps_taken = 0

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[np.ndarray, dict[str, Any]]:
        super().reset(seed=seed)
        self.position = 0.0
        self.steps_taken = 0

        if options and "start_position" in options:
            self.position = float(options["start_position"])

        observation = np.array([self.position], dtype=np.float32)
        info = {"target_position": self.target_position}
        return observation, info

    def step(
        self, action: int
    ) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        if not self.action_space.contains(action):
            raise ValueError(f"Invalid action: {action}")

        movement = -1.0 if action == 0 else 1.0
        self.position += movement
        self.steps_taken += 1

        reached_target = bool(self.position >= self.target_position)
        terminated = reached_target
        truncated = self.steps_taken >= self.max_steps and not terminated
        reward = 1.0 if reached_target else -0.01

        observation = np.array([self.position], dtype=np.float32)
        info = {
            "target_position": self.target_position,
            "distance_to_target": float(self.target_position - self.position),
        }
        return observation, reward, terminated, truncated, info


if __name__ == "__main__":
    env = SimpleReachEnv()
    observation, info = env.reset()
    print("reset:", observation, info)

    for step_idx in range(10):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        print(
            f"step={step_idx} action={action} obs={observation} "
            f"reward={reward} terminated={terminated} truncated={truncated} info={info}"
        )
        if terminated or truncated:
            observation, info = env.reset()
            print("reset:", observation, info)
