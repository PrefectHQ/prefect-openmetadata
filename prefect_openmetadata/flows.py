"""
## Prefect flow for metadata ingestion

Follow the main documentation for guidance on:

- installing and configuring `Prefect` and `OpenMetadata`,
- running metadata ingestion flows locally and on schedule.
"""
import json
from prefect import flow
from prefect_openmetadata.ingestion_workflow import PrefectOpenMetadataIngestion


@flow
def ingest_metadata(config: str) -> None:
    """
    Args:
        config: JSON-formatted configuration

    Examples:
        Flow ingesting metadata using Prefect:
        ```python
        from prefect_openmetadata.flows import ingest_metadata

        json_config = \"""See an example in the section: Run ingestion flow\"""

        if __name__ == "__main__":
            ingest_metadata(json_config)
        ```
    """
    workflow_config = json.loads(config)
    workflow = PrefectOpenMetadataIngestion.create(workflow_config)
    workflow.execute()
    workflow.raise_from_status()
    workflow.log_flow_status()
    workflow.stop()
