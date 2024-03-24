from pathlib import Path

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.celery_config.celery_utils import create_celery
from api.routes import seo_classification


def create_app() -> FastAPI:
    current_app = FastAPI(title="Чего нибудь потом напишу",
                          description="И тут тоже")

    current_app.mount("/static", StaticFiles(directory="./api/static"), name="static")
    current_app.celery_app = create_celery()
    current_app.include_router(seo_classification.router)
    return current_app


app = create_app()
celery = app.celery_app


# if __name__ == "__main__":
#     uvicorn.run("main:app", port=9000, reload=True)