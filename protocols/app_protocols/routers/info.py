from fastapi import APIRouter

from app_protocols import __version__

router = APIRouter(tags=["info"])


@router.get("/")
async def info():
    return {"version": __version__}
