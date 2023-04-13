from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from {{project_name}}.www.precheck import *
# import nothing, just for check something
from {{project_name}}.www.api.api_v1.api import api_router
from {{project_name}}.www.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
