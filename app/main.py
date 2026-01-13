import logging
import os
import sys
from copy import deepcopy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        summary=app.summary,
        description=app.description,
        terms_of_service=app.terms_of_service,
        contact=app.contact,
        license_info=app.license_info,
        routes=app.routes,
        webhooks=app.webhooks.routes,
        tags=app.openapi_tags,
        servers=app.servers,
        separate_input_output_schemas=app.separate_input_output_schemas,
    )

    def is_target(path: dict) -> bool:
        tags = path.get("post", {}).get("tags", [])
        if "modify-swagger" in tags:
            return True

    # 스키마 오버라이딩
    # swagger dart code generator를 위해 ref 제거
    for path in openapi_schema["paths"].values():
        if is_target(path):
            for method in path.values():
                if request_body := method.get("requestBody"):
                    if content := request_body.get("content"):
                        if multipart_form_data := content.get("multipart/form-data"):
                            if schema := multipart_form_data.get("schema"):
                                if ref := schema.get("$ref"):
                                    component = deepcopy(
                                        openapi_schema["components"]["schemas"][
                                            ref.split("/")[-1]
                                        ]
                                    )
                                    component.pop("title")
                                    multipart_form_data["schema"] = component
                                    schema.pop("$ref")
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
