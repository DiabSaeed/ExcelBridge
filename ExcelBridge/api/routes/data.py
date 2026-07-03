from fastapi import Request, APIRouter, Depends
from helper import ResponseEnums
from ..main import app


base_router = APIRouter(
    prefix="/api/v1/",
    tags=["api/v1"]
)

@app.get("/status")
async def get_status():
    return {
        "status": ResponseEnums.CONNECTION_SUCCEEDED.value,
        "connection_type": type(app.state.connector.__name__)
    }