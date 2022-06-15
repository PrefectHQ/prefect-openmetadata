"""
Extension to the OpenMetadata ProfilerWorkflow class
"""
from metadata.orm_profiler.api.workflow import ProfilerWorkflow
from metadata.generated.schema.metadataIngestion.workflow import (
    OpenMetadataWorkflowConfig,
)
from prefect import get_run_logger


class PrefectOpenMetadataProfiler(ProfilerWorkflow):
    """
    OpenMetadata profiler workflow that adds a method
    allowing to log the workflow status to the Prefect backend.

    Args:
         config: string with a YAML or JSON configuration file
    """

    def __int__(self, config: OpenMetadataWorkflowConfig):
        """
        Args:
            config: string with a YAML or JSON configuration file
        """
        super().__init__(config=config)

    def log_flow_status(self) -> None:
        """
        Log workflow status to the Prefect API backend
        """
        logger = get_run_logger()
        logger.info("Source Status: %s", self.source_status.as_string())
        logger.info("Processir Status: %s", self.processor.get_status().as_string())
        if hasattr(self, "sink"):
            logger.info("Sink Status: %s", self.sink.get_status().as_string())
