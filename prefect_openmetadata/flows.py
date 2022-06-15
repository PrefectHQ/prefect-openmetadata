"""
## Prefect flows and tasks for OpenMetadata workflows include:
- metadata ingestion workflow: information about your tables, view, schemas, etc
- usage ingestion workflow: query and audit logs showing usage patterns
- profiler workflow: profile data and run data validation tests

Follow the main documentation for guidance on:

- installing and configuring `Prefect` and `OpenMetadata`,
- running metadata ingestion flows locally and on schedule.
"""
import json
import yaml
from metadata.generated.schema.metadataIngestion.workflow import (
    OpenMetadataWorkflowConfig,
)
from metadata.generated.schema.api.services.ingestionPipelines.testServiceConnection import (
    TestServiceConnectionRequest,
)
from metadata.utils.connections import (
    get_connection,
    test_connection,
)
from prefect import flow, task, get_run_logger
from prefect_openmetadata.ingestion_workflow import PrefectOpenMetadataIngestion
from prefect_openmetadata.profiler_workflow import PrefectOpenMetadataProfiler


class OpenMetadataFailedConnection(Exception):
    """Exception for failed connection attempts"""


@task
async def run_ingestion_task(om_workflow_model: OpenMetadataWorkflowConfig) -> None:
    """
    Task ingesting metadata into OpenMetadata backend

    Args:
        om_workflow_model: ingestion spec as a pydantic model
    """
    workflow = PrefectOpenMetadataIngestion(om_workflow_model)
    workflow.execute()
    workflow.log_flow_status()
    workflow.raise_from_status()
    workflow.stop()


@flow
def ingest_metadata(config: str, is_json: bool = False) -> None:
    """
    Ingests raw metadata about tables, dashboards, users, topics, pipelines, etc.
    The same flow is used for usage ingestion.

    Args:
        config: configuration spec, by default in YAML, optionally in JSON
        is_json: flag whether `config` is a JSON spec rather than YAML

    Examples:
        Flow ingesting metadata using Prefect:
        ```python
        from prefect_openmetadata.flows import ingest_metadata

        config = \"""See an example in the section: Run ingestion flow\"""

        if __name__ == "__main__":
            ingest_metadata(config)
        ```
    """
    om_workflow_config = json.loads(config) if is_json else yaml.safe_load(config)
    om_workflow_model = OpenMetadataWorkflowConfig.parse_obj(om_workflow_config)
    run_ingestion_task(om_workflow_model)


@task
async def run_profiling_task(om_workflow_model: OpenMetadataWorkflowConfig) -> None:
    """
    Task profiling a given OpenMetadata source

    Args:
        om_workflow_model: profiling spec as a pydantic model
    """
    workflow = PrefectOpenMetadataProfiler(om_workflow_model)
    workflow.execute()
    workflow.log_flow_status()
    workflow.raise_from_status()
    workflow.stop()


@flow
def profile_metadata(config: str, is_json: bool = False) -> None:
    """
    Profiles metadata about tables, dashboards, users, topics, pipelines, etc.

    Args:
        config: configuration spec, by default in YAML, optionally in JSON
        is_json: flag whether `config` is a JSON spec rather than YAML

    Examples:
        Flow profiling metadata using Prefect:
        ```python
        from prefect_openmetadata.flows import profile_metadata

        config = \"""See an example in the section: Run profiling flow\"""

        if __name__ == "__main__":
            profile_metadata(config)
        ```
    """
    om_workflow_config = json.loads(config) if is_json else yaml.safe_load(config)
    om_workflow_model = OpenMetadataWorkflowConfig.parse_obj(om_workflow_config)
    run_profiling_task(om_workflow_model)


@task
async def make_test_connection(conn_config: TestServiceConnectionRequest) -> None:
    """
    Task maging a test connection to the specified OpenMetadata connection

    Args:
        conn_config: connection spec as a pydantic model
    """
    logger = get_run_logger()
    connection = get_connection(conn_config.connection.config)
    try:
        test_connection(connection)
        logger.info("Connection successful!")
    except OpenMetadataFailedConnection as exc:
        logger.error("Test connection failed")
        raise exc


@flow
def validate_connection(conn_config: str, is_json: bool = False):
    """
    Makes a SQLAlchemy connection based on a given JSON or YAML config for testing.
    Go to the [OpenMetadata schema definitions](https://github.com/open-metadata/OpenMetadata/tree/main/catalog-rest-service/src/main/resources/json/schema/entity/services/connections),
    to inspect required fields to connect with your desired system and crawl its metadata.

    Requires installing the required sqlalchemy subpackage for the relevant connector
    e.g. Snowflake connection requires `pip install snowflake-sqlalchemy`

    Args:
        conn_config: connection spec as a string from a JSON spec
        is_json:  flag whether `conn_config` is a JSON spec rather than YAML

    Examples:
        Flow testing connection using Prefect:
        ```python
        from prefect_openmetadata.flows import validate_connection

        config = \"""
        connection:
          config:
            type: Snowflake
            username: DEMO
            password: xxx
            account: xxx.us-east-2.aws
            database: YOUR_DB
            warehouse: COMPUTE_WH
        connectionType: Database
        \"""

        if __name__ == "__main__":
            validate_connection(config)
        ```
    """
    conn_spec_dict = json.loads(conn_config) if is_json else yaml.safe_load(conn_config)
    conn_model = TestServiceConnectionRequest.parse_obj(conn_spec_dict)
    make_test_connection(conn_model)
