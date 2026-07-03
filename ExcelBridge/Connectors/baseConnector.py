from abc import ABC, abstractmethod
from typing import Any, Dict, Literal
from pandas import DataFrame


class BaseConnector(ABC):
    @abstractmethod
    def connect(self, **kwargs) -> Any:
        pass
    
    def disconnect(self) -> None:
        pass
    
    @abstractmethod
    def execute_query(self, query: str, warehouse_id: str, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def run_job(self,job_id:int, **kwargs) -> Any:
        pass
    
    @abstractmethod
    def run_notebook(self, notebook_path: str, cluster_id: str, **kwargs) -> Any:
        pass
    
    @abstractmethod
    def upload_df(self, df: DataFrame, table_name: str, mode: Literal['fail', 'replace', 'append', 'delete_rows'] = 'append', **kwargs) -> bool:
        pass
    
    @abstractmethod
    def download_df(self, query: str, **kwargs) -> DataFrame:
        pass    