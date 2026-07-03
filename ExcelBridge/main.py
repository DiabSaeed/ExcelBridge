from fastapi import FastAPI
from Connectors.ConnectorFactory import Factory
from contextlib import asynccontextmanager
from Controllers import ConnectorController
from api.routes.data import base_router, data_router
@asynccontextmanager
async def lifespan(
    app: FastAPI
    ): 
    app.state.factory = Factory
    app.state.active_connectors = {}
    yield 
    for connector in app.state.active_connectors.values():
        connector.disconnect()
    app.state.active_connectors.clear()

app = FastAPI(lifespan=lifespan)
app.include_router(base_router)
app.include_router(data_router)
