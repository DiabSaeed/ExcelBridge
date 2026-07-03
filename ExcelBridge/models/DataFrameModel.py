from pydantic import Field, BaseModel
from pandas import DataFrame
from typing import Literal, List, Dict , Any
from .RequestModels import DatabricksConfig

class UploadDataFrameRequest(BaseModel):
    data : List[Dict[str,Any]] = Field(...,description="The dataframe which will be uploaded")
    table_name: str = Field(..., description="The name which dataframe will take in databricks")
    mode: Literal['fail', 'replace', 'append', 'delete_rows'] = Field("append", description="The mode of apploading")
    config: DatabricksConfig
    
class DownloadDataFrameRequest(BaseModel):
    query: str = Field(..., description="The query which will return with the dataframe")
    config: DatabricksConfig