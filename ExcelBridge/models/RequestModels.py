from pydantic import BaseModel, Field
from typing import Optional

class DatabricksConfig(BaseModel):
    host: str = Field(..., description="Databricks workspace URL")
    token: str = Field(..., description="Databricks access token")
    http_path: Optional[str] = Field(None, description="SQL Warehouse HTTP path")
    catalog: Optional[str] = Field("hive_metastore", description="Catalog name")
    schema_name: Optional[str] = Field("default", description="Schema name")

class QueryRequest(BaseModel):
    config: DatabricksConfig
    query: str = Field(..., description="SQL query to execute")
    warehouse_id: str = Field(..., description="SQL Warehouse ID")

class JobRequest(BaseModel):
    config: DatabricksConfig
    job_id: int = Field(..., description="Databricks Job ID")

class NotebookRequest(BaseModel):
    config: DatabricksConfig
    notebook_path: str = Field(..., description="Path to the notebook")
    cluster_id: str = Field(..., description="Cluster ID to run the notebook on")