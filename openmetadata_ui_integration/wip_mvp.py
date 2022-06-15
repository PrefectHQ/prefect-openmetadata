"""
API service for metadata ingestion directly from the OpenMetadata UI (no-code workflows)
"""
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from prefect.client import get_client
from metadata.generated.schema.api.services.ingestionPipelines.testServiceConnection import (
    TestServiceConnectionRequest,
)
from metadata.generated.schema.entity.services.ingestionPipelines.ingestionPipeline import (
    IngestionPipeline,
)
from metadata.utils.connections import (
    SourceConnectionException,
    get_connection,
    test_connection,
)
from uuid import UUID
from prefect_openmetadata.ingestion_workflow import PrefectOpenMetadataIngestion


app = FastAPI(title="Prefect OpenMetadata Ingestion & Profiling")


@app.get("/")
def read_root():
    return {"message": "hello from Prefect OpenMetadata UI Integration Service!"}


@app.get("/api/rest_status")
async def get_api_healthcheck_status():
    async with get_client() as client:
        url = client.api_url
        response = await client.api_healthcheck()
    if response is None:
        return {"message": f"Prefect Ingestion service is healthy and running at {url}"}
    else:
        return {"message": response}


@app.post("/api/test_connection")
async def test_connction(conn: TestServiceConnectionRequest):
    connection = get_connection(conn.connection.config)
    try:
        test_connection(connection)
    except SourceConnectionException as err:
        return JSONResponse(
            content=f"Connection error from {connection} - {err}",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )


@app.post("/api/flow_runs/")
async def run_ingestion_flow_ad_hoc(ingestion_spec: IngestionPipeline):
    workflow = PrefectOpenMetadataIngestion.create(ingestion_spec.dict())
    workflow.execute()
    workflow.raise_from_status()
    workflow.log_flow_status()
    workflow.stop()


@app.post("/api/deployments/")
async def create_deployment(ingestion_spec: IngestionPipeline):
    async with get_client() as client:
        # todo find out how to translate the OM config into a Prefect deployment spec
        response = await client.create_deployment(ingestion_spec)
        return response


@app.delete("/api/deployments/{deployment_id}")
async def delete_deployment(deployment_id: UUID):
    async with get_client() as client:
        response = await client.delete_deployment(deployment_id)
        return response


@app.post("/api/flow_runs/{deployment_id}")
async def create_flow_run_from_deployment(deployment_id: UUID):
    async with get_client() as client:
        response = await client.create_flow_run_from_deployment(deployment_id)
        return response


@app.get("/api/flow_runs/{flow_run_id}")
async def get_flow_run_status(flow_run_id: UUID):
    async with get_client() as client:
        response = await client.read_flow_run(flow_run_id)
        return response


@app.delete("/api/flow_runs/{flow_run_id}")
async def delete_flow_run(flow_run_id: UUID):
    async with get_client() as client:
        response = await client.delete_flow_run(flow_run_id)
        return response
