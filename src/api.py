# src/api.py

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse

from .stream import run_simulation_streaming

app = FastAPI(title="Meta-Problems")

FRONTEND_PATH = Path(__file__).parent / "frontend" / "index.html"


@app.get("/")
async def index():
    return FileResponse(FRONTEND_PATH)


@app.get("/api/simulate")
async def simulate(
    industry: str = "",
    location: str = "",
    founder_profile: str = "tecnico",
    time_months: int = 2,
    capital: str = "bootstrapped",
    solution_type: str = "sin_preferencia",
    market_target: str = "sin_preferencia",
    num_solutions: int = 3,
):
    params = {
        "industry": industry,
        "location": location,
        "founder_profile": founder_profile,
        "time_months": time_months,
        "capital": capital,
        "solution_type": solution_type,
        "market_target": market_target,
        "num_solutions": num_solutions,
    }

    async def event_generator():
        async for item in run_simulation_streaming(params):
            yield {
                "event": item["event"],
                "data": json.dumps(item["data"], ensure_ascii=False),
            }

    return EventSourceResponse(event_generator())
