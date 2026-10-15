from __future__ import annotations

from fastapi import FastAPI

from crisisops_example.resources.router import router as resources_router


app = FastAPI(
    title="CrisisOps - Vertical Slice Example",
    version="0.1.0",
)

app.include_router(resources_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
