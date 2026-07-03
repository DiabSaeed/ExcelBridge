from typing import Any
from fastapi import Request
from models.RequestModels import DatabricksConfig

class ConnectorController:

    def __init__(self, connector_name: str):
        self.connector_name = connector_name

    async def __call__(
        self,
        request: Request,
        config: DatabricksConfig,
    ):

        key = config.host

        connectors = request.app.state.active_connectors

        connector = connectors.get(key)

        if connector is None:
            connector = request.app.state.factory(self.connector_name)
            connector = connector.connect(config.host, config.token)
            connectors[key] = connector
        connector.token = config.token
        return connector
            