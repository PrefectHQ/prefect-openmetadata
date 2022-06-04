# Run metadata ingestion

## Configure your ingestion spec

In the [Install OpenMetadata](install_openmetadata.md) section, you cloned the `prefect-openmetadata` repository. This repository contains a directory **example-data** which you can use to ingest sample data into your `OpenMetadata` backend using Prefect. 

Here is a JSON configuration you can use in your flow to ingest that sample data:

```json
{
  "source": {
    "type": "sample-data",
    "serviceName": "sample_data",
    "serviceConnection": {
      "config": {
        "type": "SampleData",
        "sampleDataFolder": "example-data"
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
```

## Run ingestion workflow locally

Now you can paste the JSON-config from above as a string into your flow and run it:

```python
from prefect_openmetadata.flows import ingest_metadata

config = """
{
  "source": {
    "type": "sample-data",
    "serviceName": "sample_data",
    "serviceConnection": {
      "config": {
        "type": "SampleData",
        "sampleDataFolder": "example-data"
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

if __name__ == "__main__":
    ingest_metadata(config)
```

After running your flow, you should see **new users**, **datasets**, **dashboards,** and other **metadata** in your OpenMetadata UI. Also, **your Prefect UI** will display the workflow run and will show the logs with details on which source system has been scanned and which data has been ingested.

**Congratulations** on building your first metadata ingestion workflow with OpenMetadata and Prefect! Head over to the next section to see how you can run this flow on schedule. 
