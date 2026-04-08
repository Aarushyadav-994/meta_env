from __future__ import annotations

import os

from fastapi import Body, FastAPI
from openai import OpenAI
from pydantic import BaseModel

from environment import SimpleReachEnv
from models import ReachAction, ReachObservation, ReachState
from tasks import TASKS, TASK_ID_TO_INDEX

app = FastAPI(title="Simple Reach OpenEnv Service", version="0.1.0")
ENV = SimpleReachEnv(task_id=int(os.getenv("TASK_ID", "0")))
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")


class ResetRequest(BaseModel):
    task_id: str | int = "reach_positive_ten"
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


class TaskListResponse(BaseModel):
    tasks: list[dict]


class MetadataResponse(BaseModel):
    name: str
    description: str
    version: str
    tasks: list[dict]


class SchemaResponse(BaseModel):
    action: dict
    observation: dict
    state: dict


class MCPResponse(BaseModel):
    jsonrpc: str
    id: str | int | None
    result: dict


class GradeRequest(BaseModel):
    action: dict
    ground_truth: dict | None = None


class GradeResponse(BaseModel):
    score: float


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: str | None) -> None:
    error_value = error if error else "null"
    done_value = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_value} error={error_value}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: list[float]) -> None:
    rewards_value = ",".join(f"{reward:.2f}" for reward in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_value}",
        flush=True,
    )


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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/metadata", response_model=MetadataResponse)
def metadata() -> MetadataResponse:
    return MetadataResponse(
        name="simple-reach-openenv",
        description="Minimal 1D reach environment with three task variants and graders.",
        version="0.1.0",
        tasks=TASKS,
    )


@app.get("/schema", response_model=SchemaResponse)
def schema() -> SchemaResponse:
    return SchemaResponse(
        action=ReachAction.model_json_schema(),
        observation=ReachObservation.model_json_schema(),
        state=ReachState.model_json_schema(),
    )


@app.post("/reset", response_model=EnvResponse)
def reset_env(request: ResetRequest = Body(default=ResetRequest())) -> EnvResponse:
    task_value = request.task_id
    if isinstance(task_value, str):
        mapped_task_id = TASK_ID_TO_INDEX.get(task_value, 0)
    else:
        mapped_task_id = int(task_value)
    options: dict[str, object] = {"task_id": mapped_task_id}
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


@app.get("/tasks", response_model=list[dict])
def tasks_env() -> list[dict]:
    return TASKS


@app.post("/grader", response_model=GradeResponse)
def grader(req: GradeRequest) -> GradeResponse:
    task_id = req.action.get("task_id", "reach_positive_ten")
    action_value = req.action.get("action")
    if action_value is None:
        action_value = req.action.get("response")

    if isinstance(action_value, str):
        normalized = action_value.strip().lower()
        if normalized in {"left", "0"}:
            action_int = 0
        elif normalized in {"right", "1"}:
            action_int = 1
        else:
            action_int = 1
    else:
        action_int = int(action_value)

    expected = {
        "reach_positive_ten": 1,
        "reach_negative_ten": 0,
        "reach_positive_five": 1,
    }.get(str(task_id), 1)
    score = 1.0 if action_int == expected else 0.0
    return GradeResponse(score=score)


@app.post("/mcp", response_model=MCPResponse)
def mcp(payload: dict = Body(default_factory=dict)) -> MCPResponse:
    request_id = payload.get("id")
    return MCPResponse(
        jsonrpc="2.0",
        id=request_id,
        result={"status": "ok"},
    )


def main() -> None:
    task_id = int(os.getenv("TASK_ID", "0"))
    max_steps = int(os.getenv("MAX_STEPS", "32"))
    use_model = bool(API_BASE_URL and MODEL_NAME and HF_TOKEN)
    task_name = os.getenv("TASK_NAME", f"simple-reach-task-{task_id}")
    benchmark = os.getenv("BENCHMARK", "simple-reach")

    client_kwargs = {"api_key": HF_TOKEN or "unused"}
    if API_BASE_URL:
        client_kwargs["base_url"] = API_BASE_URL
    client = OpenAI(**client_kwargs)

    env = SimpleReachEnv(task_id=task_id, max_steps=max_steps)
    observation, info = env.reset()
    log_start(task=task_name, env=benchmark, model=MODEL_NAME)
    total_reward = 0.0
    terminated = False
    truncated = False
    steps_executed = 0
    rewards: list[float] = []
    success = False

    try:
        for step_index in range(1, max_steps + 1):
            position = float(observation[0])
            target_position = float(observation[1])
            action_error: str | None = None

            try:
                if use_model:
                    action, _ = choose_action(
                        client=client,
                        model_name=MODEL_NAME,
                        position=position,
                        target_position=target_position,
                        step_index=step_index,
                    )
                else:
                    action = fallback_action(
                        position=position, target_position=target_position
                    )
            except Exception as exc:
                action = fallback_action(position=position, target_position=target_position)
                action_error = str(exc)

            action_str = "left" if action == 0 else "right"
            observation, reward, terminated, truncated, info = env.step(action)
            done = bool(terminated or truncated)
            total_reward += reward
            rewards.append(reward)
            steps_executed = step_index

            log_step(
                step=step_index,
                action=action_str,
                reward=reward,
                done=done,
                error=action_error,
            )

            if done:
                break

        score = total_reward / max_steps if max_steps > 0 else 0.0
        score = min(max(score, 0.0), 1.0)
        success = bool(score > 0.0 and (terminated or truncated or steps_executed > 0))
    finally:
        env.close()
        log_end(success=success, steps=steps_executed, score=score if 'score' in locals() else 0.0, rewards=rewards)


if __name__ == "__main__":
    main()
