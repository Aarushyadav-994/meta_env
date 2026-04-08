from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class SimpleReachEnv(gym.Env):
    metadata = {"render_modes": [], "render_fps": 4}
    TASK_TARGETS = {
        0: 10.0,
        1: -10.0,
        2: 5.0,
    }

    def __init__(self, task_id: int = 0, max_steps: int = 32) -> None:
        super().__init__()
        if task_id not in self.TASK_TARGETS:
            raise ValueError(f"Unsupported task_id: {task_id}")

        self.task_id = int(task_id)
        self.target_position = float(self.TASK_TARGETS[self.task_id])
        self.max_steps = int(max_steps)

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low=np.array([-np.inf, -np.inf], dtype=np.float32),
            high=np.array([np.inf, np.inf], dtype=np.float32),
            shape=(2,),
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

        if options and "task_id" in options:
            new_task_id = int(options["task_id"])
            if new_task_id not in self.TASK_TARGETS:
                raise ValueError(f"Unsupported task_id: {new_task_id}")
            self.task_id = new_task_id
            self.target_position = float(self.TASK_TARGETS[self.task_id])

        if options and "start_position" in options:
            self.position = float(options["start_position"])

        observation = np.array(
            [self.position, self.target_position], dtype=np.float32
        )
        info = {"task_id": self.task_id, "target_position": self.target_position}
        return observation, info

    def step(
        self, action: int
    ) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        if not self.action_space.contains(action):
            raise ValueError(f"Invalid action: {action}")

        movement = -1.0 if action == 0 else 1.0
        self.position += movement
        self.steps_taken += 1

        distance_to_target = abs(self.target_position - self.position)
        reached_target = bool(distance_to_target <= 0.0)
        terminated = reached_target
        truncated = self.steps_taken >= self.max_steps and not terminated
        reward = float(1.0 / (distance_to_target + 2.0))

        observation = np.array(
            [self.position, self.target_position], dtype=np.float32
        )
        info = {
            "task_id": self.task_id,
            "target_position": self.target_position,
            "distance_to_target": float(distance_to_target),
        }
        return observation, reward, terminated, truncated, info


if __name__ == "__main__":
    env = SimpleReachEnv(task_id=0)
    observation, info = env.reset()
    print("reset:", observation.tolist(), info)

    for step_idx in range(10):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        print(
            "step:",
            step_idx,
            "action:",
            action,
            "obs:",
            observation.tolist(),
            "reward:",
            reward,
            "terminated:",
            terminated,
            "truncated:",
            truncated,
            "info:",
            info,
        )
        if terminated or truncated:
            observation, info = env.reset()
            print("reset:", observation.tolist(), info)
