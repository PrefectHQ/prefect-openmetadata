import json
import yaml
import pytest
from metadata.ingestion.api.parser import parse_workflow_config_gracefully


@pytest.fixture
def json_config():
    return """
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


@pytest.fixture
def yaml_config():
    return """
    source:
      type: sample-data
      serviceName: sample_data
      serviceConnection:
        config:
          type: SampleData
          sampleDataFolder: "../example-data"
      sourceConfig: {}
    sink:
      type: metadata-rest
      config: {}
    workflowConfig:
      openMetadataServerConfig:
        hostPort: http://localhost:8585/api
        authProvider: no-auth
    """


def test_ingest_metadata(yaml_config):
    config_dict = yaml.safe_load(yaml_config)
    assert parse_workflow_config_gracefully(config_dict) is not None


def test_ingest_metadata_from_json(json_config):
    config_dict = json.loads(json_config)
    assert parse_workflow_config_gracefully(config_dict) is not None
