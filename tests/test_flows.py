import json
import pytest
from metadata.ingestion.api.parser import parse_workflow_config_gracefully


@pytest.fixture
def example_config():
    json_config = """
    {
      "source": {
        "type": "sample-data",
        "serviceName": "sample_data",
        "serviceConnection": {
          "config": {
            "type": "SampleData",
            "sampleDataFolder": "../example-data"
          }
        },
        "sourceConfig": {}
      },
      "sink": {
        "type": "metadata-rest",
        "config": {}
      },
      "workflowConfig": {
        "openMetadataServerConfig": {
          "hostPort": "http://localhost:8585/api",
          "authProvider": "no-auth"
        }
      }
    }
    """
    return json_config


def test_ingest_metadata(example_config):
    config_dict = json.loads(example_config)
    assert parse_workflow_config_gracefully(config_dict) is not None
