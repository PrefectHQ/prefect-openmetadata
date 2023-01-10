# Run metadata ingestion

## Configure your ingestion spec

Here is a simple flow example demonstratig how you can ingest data from a Postgres database into your `OpenMetadata` backend using Prefect: [example_postgres_ingestion.py](./example_postgres_ingestion.py).

```python
from prefect_openmetadata.flows import ingest_metadata

postgres = """
source:
  type: postgres
  serviceName: local_postgres
  serviceConnection:
    config:
      type: Postgres
      username: postgres
      password: postgres
      hostPort: localhost:5432
  sourceConfig:
    config:
      markDeletedTables: true
      includeTables: true
      includeViews: false
sink:
  type: metadata-rest
  config: {}
workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: openmetadata
    securityConfig:
      jwtToken: 'your_token'
"""

if __name__ == "__main__":
    ingest_metadata(postgres)

```

Each flow is based on a configuration YAML or JSON spec that follows similar structure to the following:

```yaml
source:
  type: sample-data
  serviceName: sample_data
  serviceConnection:
    config:
      type: SampleData
      sampleDataFolder: "example-data"
  sourceConfig: {}
sink:
  type: metadata-rest
  config: {}
workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: no-auth
```

## Run ingestion workflow locally

Now you can paste the config from above as a string into your flow and run it:

```python
from prefect_openmetadata.flows import ingest_metadata

config = """
YOUR_CONFIG
"""

if __name__ == "__main__":
    ingest_metadata(config)
```

After running your flow, you should see **new users**, **datasets**, **dashboards,** or similar **metadata** objects in your OpenMetadata UI. Also, **your Prefect UI** will display the workflow run and will show the logs with details on which source system has been scanned and which data has been ingested.

**Congratulations** on building your first metadata ingestion workflow with OpenMetadata and Prefect! Head over to the next section to see how you can run this flow on schedule. 
