# запуск коду за допомогою hypercorn :)

from fastapi import FastAPI
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve


app = FastAPI(title="Finance API")

config = Config()
config.bind = ["localhost:5050"]

from . import routes


def main() -> None:
    asyncio.run(serve(app, config))