from .baseConnector import BaseConnector
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import SubmitTask, NotebookTask
from sqlalchemy import create_engine #type: ignore
from databricks import sql
import pandas as pd
from typing import Any, Dict, Literal
import logging
import time

class DatabricksConnector(BaseConnector):
    def __init__(self, host: str, token: str):
        self.host = host
        self.token = token
        self.client = None
        self._engines = {}
        self.logger = logging.getLogger(__name__)
        
    def connect(self, **kwargs) -> Any:
        self.host = kwargs.get("host", self.host)
        self.token = kwargs.get("token", self.token)
        
        print(f"====== Connecting to Databricks... Host: {self.host} ======") 
        
        if not self.host or not self.token:
            raise ValueError("Host and Token are required to connect to Databricks.")
            
        try:
            self.client = WorkspaceClient(host=self.host, token=self.token)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Databricks client: {e}")
            
        return self

    def disconnect(self) -> None:
        self.client = None
        for engine in self._engines.values():
            engine.dispose()
        self._engines.clear()

    def _get_engine(self, http_path: str, catalog: str, schema: str):
        connection_key = f"{http_path}_{catalog}_{schema}"
        
        clean_host = self.host.replace("https://", "").replace("http://", "")
        
        connection_string = f"databricks://token:{self.token}@{clean_host}?http_path={http_path}&catalog={catalog}&schema={schema}"
        
        if connection_key not in self._engines:
            self.logger.info("Creating new connection engine")
            self._engines[connection_key] = create_engine(connection_string)
        return self._engines[connection_key]
        
    def execute_query(self, query: str, warehouse_id: str, **kwargs) -> Dict[str, Any]:
        if not self.client:
            raise RuntimeError("Databricks client is not connected. Please connect first.")
            
        response = self.client.statement_execution.execute_statement( #type: ignore
            warehouse_id=warehouse_id,
            statement=query,
            wait_timeout="10s" 
        )
        statment_id = response.statement_id
        if response.status in ["PENDING", "RUNING"]:
            time.sleep(3)
            if statment_id:
                response = self.client.statement_execution.get_statement(statement_id= statment_id)
        return response.as_dict() 

    def run_job(self, job_id: int, **kwargs) -> Any:
        response = self.client.jobs.run_now(job_id=job_id) #type: ignore
        return response.as_dict()

    def run_notebook(self, notebook_path: str, cluster_id: str, **kwargs) -> Any:
        nb_task = NotebookTask(notebook_path=notebook_path)
        
        task = SubmitTask(
            task_key="run_notebook_task",
            existing_cluster_id=cluster_id,
            notebook_task=nb_task
        )
        
        response = self.client.jobs.submit( #type: ignore
            run_name="ExcelBridge_Notebook_Run",
            tasks=[task]
        )
        return response.as_dict()

    def upload_df(self, df: pd.DataFrame, table_name: str, mode: Literal['fail', 'replace', 'append', 'delete_rows'] = 'append', **kwargs) -> bool:
        http_path = kwargs.get("http_path")
        if not http_path:
            raise ValueError("http_path is a must")
        
        catalog = kwargs.get("catalog", "hive_metastore")
        schema = kwargs.get("schema", "default")
        try:
            engine = self._get_engine(
                http_path=http_path,
                catalog=catalog,
                schema=schema
            )
            with engine.begin() as conn:
                df.to_sql(name=table_name, con=conn, if_exists=mode, index=False)
                return True
        except Exception as e:
            self.logger.error(e)
            raise RuntimeError(f"Upload failed: {e}") 

    def download_df(self, query: str, **kwargs) -> pd.DataFrame:
        http_path = kwargs.get("http_path")
        if not http_path:
            raise ValueError("http_path is a must")
        
        catalog = kwargs.get("catalog", "hive_metastore")
        schema = kwargs.get("schema", "default")
        try:
            engine = self._get_engine(
                http_path=http_path,
                catalog=catalog,
                schema=schema
            )
            resulted_df = pd.read_sql(
                sql=query,
                con=engine
            )
            return resulted_df
        except Exception as e:
            self.logger.error(e)
            raise RuntimeError(f"Download failed: {e}")