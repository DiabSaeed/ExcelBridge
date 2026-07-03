from fastapi import FastAPI
from Connectors import Factory
from contextlib import asynccontextmanager
from helper import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings() 
    connector_factory = Factory("databricks")
    connector = connector_factory.connect(settings.HOST, settings.TOKEN)
    app.state.connector = connector
    app.state.connector_factory = connector_factory
    yield {
        "connector" : connector
    }
    
    app.state.connection_fatory.disconnect()

app = FastAPI(lifespan=lifespan)

app = FastAPI(lifespan= lifespan)