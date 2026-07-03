from fastapi import Request, APIRouter, HTTPException
from helper import ResponseEnums
from models.RequestModels import QueryRequest
from Controllers.ConnectorController import ConnectorController

get_connector = ConnectorController("databricks")

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api/v1"]
)

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api/v1/data"]
)

@base_router.get("/status")
async def get_status():
    return {
        "status": ResponseEnums.CONNECTION_SUCCEEDED.value,
        "message": "API is running successfully"
    }

@data_router.post("/query")
async def query(
    req: QueryRequest,
    request: Request 
):
    try:
        connector = await get_connector(request, req.config)
        # connector = connector.connect(req.config.host,req.config.token)
        result = connector.execute_query(
            query=req.query,
            warehouse_id=req.warehouse_id
        )
        
        return {
            "Status": ResponseEnums.CONNECTION_SUCCEEDED.value,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))