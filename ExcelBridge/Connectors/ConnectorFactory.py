import logging
from DatabricksConnector import DatabricksConnector

class Factory:
    
    def __init__(self, connector_name: str):
        self.connector_name = connector_name
        self.logger = logging.getLogger(__name__)
        self.connection = None
    def connect(self, host:str,token:str ):
        if self.connector_name.lower() == "databricks":
            self.connection = DatabricksConnector(host= host, token= token)
    def disconnect(self):
        if self.connection:
            self.connection.disconnect()