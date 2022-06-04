"""
Extention to the OpenMetadata Workflow class
"""
from metadata.ingestion.api.workflow import Workflow
from metadata.generated.schema.metadataIngestion.workflow import (
    OpenMetadataWorkflowConfig,
)
from prefect import get_run_logger


class PrefectOpenMetadataIngestion(Workflow):
    """
    OpenMetadata ingestion workflow that adds a method
    allowing to log the workflow status to the Prefect backend.

    Args:
         config: string with a JSON configuration file
    """

    def __int__(self, config: OpenMetadataWorkflowConfig):
        """
        Args:
            config: string with a JSON configuration file
        """
        super().__init__(config=config)

    def log_flow_status(self) -> None:
        """
        Log workflow status to the Prefect API backend
        """
        logger = get_run_logger()
        logger.info("Source Status: %s", self.source.get_status().as_string())
        if hasattr(self, "stage"):
            logger.info("Stage Status: %s", self.stage.get_status().as_string())
        if hasattr(self, "sink"):
            logger.info("Sink Status: %s", self.sink.get_status().as_string())
        if hasattr(self, "bulk_sink"):
            logger.info("Bulk Sink Status: %s", self.bulk_sink.get_status().as_string())
