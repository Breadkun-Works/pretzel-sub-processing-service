from fastapi import FastAPI, HTTPException, Request
import pkgutil, importlib, asyncio
from typing import Callable, Awaitable, Dict

from config import settings

PROCESSORS: Dict[str, Callable[[dict], Awaitable[dict]]] = {}


def discover_processors():
    for _, mod, _ in pkgutil.iter_modules(["processors"]):
        m = importlib.import_module(f"processors.{mod}")
        if hasattr(m, "run"):
            PROCESSORS[mod] = m.run


discover_processors()

app = FastAPI(title="Pretzel Sub‑Processing Service")


@app.api_route("/process/{name}", methods=["GET", "POST"])
async def process(name: str, request: Request):
    if name not in PROCESSORS:
        raise HTTPException(404, "processor not found")
    payload = dict(request.query_params) if request.method == "GET" else await request.json()
    try:
        result = await asyncio.wait_for(
            PROCESSORS[name](payload),
            timeout=settings.APP_TIMEOUT
        )
    except asyncio.TimeoutError:
        raise HTTPException(504, "processing timeout")
    except Exception as e:
        raise HTTPException(500, str(e))
    return result


@app.get("/process/available")
def available():
    return {"processors": list(PROCESSORS.keys())}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
