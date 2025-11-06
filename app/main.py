import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import base_router


class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            message = record.getMessage()
        except Exception:
            return True
        lower = message.lower()
        # Filter common access log patterns for healthcheck endpoints
        return not ("/healthcheck" in lower and ("get" in lower or "head" in lower))


uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addFilter(HealthCheckFilter())


app = FastAPI(
    title="Midorisour Playground FastAPI",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    version="1.0.0",
    description="",
    openapi_tags=[
        {"name": "Blog", "description": ""},
        {"name": "Working with Frontend", "description": ""},
        {"name": "Healthcheck", "description": "Service liveness endpoint."},
    ],
    contact={
        "name": "Ji Weon Hyeok",
        "url": "http://x-force.example.com/contact/",
        "email": "ben3329@naver.com",
    },
    license_info={
        "name": "MIT License",
        "identifier": "MIT",
    },
    servers=[
        {"url": "https://api.midorisour.kro.kr"},
    ],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    return {"status": "ok"}


app.include_router(base_router)
