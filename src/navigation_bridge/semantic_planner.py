from __future__ import annotations

import json
import os
import urllib.request


class PlannerUnavailable(RuntimeError):
    pass


def mission_to_goal(mission: str) -> dict[str, float]:
    """Ask vLLM for a waypoint; never invent one when the service is unavailable."""
    model = os.environ.get("VLLM_MODEL")
    if not model:
        raise PlannerUnavailable("VLLM_MODEL is not configured")
    payload = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [{
            "role": "user",
            "content": "Return JSON only with numeric x_m and y_m for this robot mission: " + mission,
        }],
    }).encode()
    request = urllib.request.Request(
        os.environ.get("VLLM_BASE_URL", "http://localhost:8000/v1").rstrip("/") + "/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            message = json.loads(response.read().decode())["choices"][0]["message"]["content"]
        value = json.loads(message)
        if not all(isinstance(value[key], (float, int)) for key in ("x_m", "y_m")):
            raise ValueError("planner returned non-numeric coordinates")
        return {"x_m": float(value["x_m"]), "y_m": float(value["y_m"])}
    except (OSError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise PlannerUnavailable(str(error)) from error
