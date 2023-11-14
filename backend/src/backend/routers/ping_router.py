from fastapi import APIRouter

router = APIRouter()


@router.post("/ping", tags=["alive"])
async def ping():
    return {"status": "ok", "message": "pong"}