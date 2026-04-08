from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class SimpleReachClient:
    base_url: str

    def reset(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        response = requests.post(f"{self.base_url.rstrip('/')}/reset", json=payload or {})
        response.raise_for_status()
        return response.json()

    def step(self, action: int) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url.rstrip('/')}/step",
            json={"action": action},
        )
        response.raise_for_status()
        return response.json()

    def state(self) -> dict[str, Any]:
        response = requests.get(f"{self.base_url.rstrip('/')}/state")
        response.raise_for_status()
        return response.json()
