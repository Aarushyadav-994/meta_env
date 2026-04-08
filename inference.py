from __future__ import annotations

import json
import os

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

from environment import SimpleReachEnv

app = FastAPI(title="Simple Reach OpenEnv Service", version="0.1.0")
ENV = SimpleReachEnv(task_id=int(os.getenv("TASK_ID", "0")))


class ResetRequest(BaseModel):
    task_id: int = 0
    seed: int | None = None
    start_position: float | None = None


class StepRequest(BaseModel):
    action: int


class EnvResponse(BaseModel):
    observation: list[float]
    info: dict


class StepResponse(BaseModel):
    observation: list[float]
    reward: float
    terminated: bool
    truncated: bool
    info: dict


class StateResponse(BaseModel):
    task_id: int
    position: float
    target_position: float
    steps_taken: int
    max_steps: int


class HealthResponse(BaseModel):
    status: str
    endpoints: list[str]


def log_event(prefix: str, payload: dict) -> None:
    print(f"{prefix} {json.dumps(payload, sort_keys=True)}", flush=True)


def parse_action(text: str) -> int:
    cleaned = text.strip()
    if cleaned.startswith("0"):
        return 0
    if cleaned.startswith("1"):
        return 1
    raise ValueError(f"Invalid action response: {text}")


def fallback_action(position: float, target_position: float) -> int:
    return 1 if position < target_position else 0


def choose_action(
    client: OpenAI,
    model_name: str,
    position: float,
    target_position: float,
    step_index: int,
) -> tuple[int, str]:
    prompt = (
        "You control a 1D agent. "
        "Return only 0 to move left or 1 to move right. "
        f"Current position: {position}. "
        f"Target position: {target_position}. "
        f"Step index: {step_index}."
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1,
    )
    content = response.choices[0].message.content or ""
    return parse_action(content), content


@app.get("/", response_model=HealthResponse)
def root() -> HealthResponse:
    return HealthResponse(status="ok", endpoints=["/reset", "/step", "/state"])


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok", endpoints=["/reset", "/step", "/state"])


@app.post("/reset", response_model=EnvResponse)
def reset_env(request: ResetRequest) -> EnvResponse:
    options: dict[str, object] = {"task_id": request.task_id}
    if request.start_position is not None:
        options["start_position"] = request.start_position
    observation, info = ENV.reset(seed=request.seed, options=options)
    return EnvResponse(observation=observation.tolist(), info=info)


@app.post("/step", response_model=StepResponse)
def step_env(request: StepRequest) -> StepResponse:
    observation, reward, terminated, truncated, info = ENV.step(request.action)
    return StepResponse(
        observation=observation.tolist(),
        reward=reward,
        terminated=terminated,
        truncated=truncated,
        info=info,
    )


@app.get("/state", response_model=StateResponse)
def state_env() -> StateResponse:
    return StateResponse(**ENV.state())


def main() -> None:
    api_base_url = os.getenv("API_BASE_URL")
    model_name = os.getenv("MODEL_NAME", "")
    hf_token = os.getenv("HF_TOKEN", "")
    task_id = int(os.getenv("TASK_ID", "0"))
    max_steps = int(os.getenv("MAX_STEPS", "32"))
    use_model = bool(api_base_url and model_name and hf_token)

    client_kwargs = {"api_key": hf_token or "unused"}
    if api_base_url:
        client_kwargs["base_url"] = api_base_url
    client = OpenAI(**client_kwargs)

    env = SimpleReachEnv(task_id=task_id, max_steps=max_steps)
    observation, info = env.reset()

    log_event(
        "[START]",
        {
            "api_base_url": api_base_url,
            "model_name": model_name,
            "task_id": task_id,
            "target_position": info["target_position"],
            "use_model": use_model,
        },
    )

    total_reward = 0.0
    terminated = False
    truncated = False
    steps_executed = 0

    for step_index in range(max_steps):
        position = float(observation[0])
        target_position = float(observation[1])

        try:
            if use_model:
                action, raw_response = choose_action(
                    client=client,
                    model_name=model_name,
                    position=position,
                    target_position=target_position,
                    step_index=step_index,
                )
                policy_source = "model"
            else:
                action = fallback_action(
                    position=position, target_position=target_position
                )
                raw_response = "model configuration missing"
                policy_source = "fallback"
        except Exception as exc:
            action = fallback_action(position=position, target_position=target_position)
            raw_response = str(exc)
            policy_source = "fallback"

        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        steps_executed = step_index + 1

        log_event(
            "[STEP]",
            {
                "action": action,
                "distance_to_target": info["distance_to_target"],
                "observation": observation.tolist(),
                "policy_source": policy_source,
                "raw_response": raw_response,
                "reward": reward,
                "step_index": step_index,
                "terminated": terminated,
                "truncated": truncated,
            },
        )

        if terminated or truncated:
            break

    log_event(
        "[END]",
        {
            "steps_executed": steps_executed,
            "task_id": task_id,
            "terminated": terminated,
            "total_reward": total_reward,
            "truncated": truncated,
        },
    )


if __name__ == "__main__":
    main()
