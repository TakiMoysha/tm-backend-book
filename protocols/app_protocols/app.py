from fastapi import FastAPI

from app_protocols import __version__

from .routers.info import router as InfoRouter

app = FastAPI(title="WebProtocols", version=__version__)

app.mount("/info", InfoRouter)
