# src/stream.py

import asyncio
import threading
import time

from .context import generate_context
from .simulation import run_simulation


async def run_simulation_streaming(params: dict):
    """
    Async generator that runs the simulation pipeline in a background thread
    and yields SSE event dicts as they are emitted.

    Each yielded item: {"event": str, "data": dict}
    """
    loop = asyncio.get_event_loop()
    queue: asyncio.Queue = asyncio.Queue()
    SENTINEL = object()

    def emit(event_type: str, data: dict):
        # Called from the worker thread — must use thread-safe bridge
        loop.call_soon_threadsafe(queue.put_nowait, {"event": event_type, "data": data})

    def worker():
        start = time.time()
        try:
            industry = params.get("industry", "").strip()
            location = params.get("location", "").strip()

            if industry and location:
                context = {"industry": industry, "location": location}
            else:
                context = generate_context()

            emit("stage_start", {"stage": "context"})
            emit("context_ready", context)
            emit("stage_complete", {"stage": "context"})

            run_simulation(
                context=context,
                founder_profile=params.get("founder_profile", "tecnico"),
                time_months=int(params.get("time_months", 2)),
                capital=params.get("capital", "bootstrapped"),
                solution_type=params.get("solution_type", "sin_preferencia"),
                market_target=params.get("market_target", "sin_preferencia"),
                num_solutions=int(params.get("num_solutions", 3)),
                event_callback=emit,
            )

            elapsed = round(time.time() - start)
            emit("simulation_complete", {"elapsed_seconds": elapsed})

        except Exception as e:
            emit("error", {"stage": "unknown", "message": str(e)})

        finally:
            loop.call_soon_threadsafe(queue.put_nowait, SENTINEL)

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    while True:
        item = await queue.get()
        if item is SENTINEL:
            break
        yield item
