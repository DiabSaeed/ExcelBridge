from fastapi import Request, APIRouter, HTTPException
from helper import ResponseEnums
from models.RequestModels import QueryRequest, JobRequest, NotebookRequest
from models.DataFrameModel import UploadDataFrameRequest, DownloadDataFrameRequest
from Controllers.ConnectorController import ConnectorController
from Controllers.DataController import DataController

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
    
@data_router.post("/job")
async def run_job(
    req: JobRequest,
    request: Request
):
    try:
        connector = await get_connector(request,req.config)
        
        result = connector.run_job(req.job_id)
        
        return {
            "Status": ResponseEnums.CONNECTION_SUCCEEDED.value,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@data_router.post("/notebook")
async def run_notebook(
    req:NotebookRequest,
    request: Request
):
    try:
        connector = await get_connector(request,req.config)
        
        result = connector.run_notebook(req.notebook_path,req.cluster_id)
        
        return {
            "Status": ResponseEnums.CONNECTION_SUCCEEDED.value,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@data_router.post("/uploadDF")
async def upload_df(
    req: UploadDataFrameRequest,
    request: Request
):
    try:
        processed_df = DataController().process_uploaded(response=req.data)
        connector = await get_connector(request,req.config)
        result = connector.upload_df(
            df = processed_df,
            table_name = req.table_name,
            mode = req.mode,
            http_path = req.config.http_path,
            catalog=req.config.catalog,  
            schema=req.config.schema
        )
        return {
            "Status": ResponseEnums.CONNECTION_SUCCEEDED.value,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@data_router.post("/downloadDF")
async def download_df(
    req: DownloadDataFrameRequest,
    request: Request
):
    try:
        connector = await get_connector(request,req.config)
        result = connector.download_df(
            query = req.query,
            http_path = req.config.http_path,
            catalog=req.config.catalog,  
            schema=req.config.schema
        )
        processed_response = DataController().process_downloaded(df=result)
        return {
            "Status": ResponseEnums.CONNECTION_SUCCEEDED.value,
            "result": processed_response
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    