# Run metadata ingestion, usage workflow and data profiler for Snowflake

This demo will walk you through the process of creating ingestion, usage and profiling workflows.

## Configure your profiling spec
OpenMetadata heavily relies on schemas. You need to understand which arguments are required and which are optional, and which are important for your use case. The easiest way to identify the required and optional arguments of any ingestion or profiling workflow is to import the ``OpenMetadataWorkflowConfig``. 

From this pydantic model, you can drill down into other components using your favorite IDE e.g. Pycharm or VSCode. From there, you can again drill down into ``Source``, ``SourceConfig``, `Sink`, etc.

```python
from metadata.generated.schema.metadataIngestion.workflow import (
    OpenMetadataWorkflowConfig, Source, SourceConfig, Sink
)
```

## Sample ingestion and profiling for Snowflake 
Let's demonstrate how you can profile your data and add data quality tests for a Snowflake data warehouse using Prefect. 

### Install SQLAlchemy package for your connector
First, make sure that you have the ``prefect-openmetadata`` and the ``snowflake-sqlalchemy`` packages installed in your environment.  

### Test the connection
You can test the connection to your end destination using the following Prefect flow:

```python
from prefect_openmetadata.flows import validate_connection

config = """
connection:
  config:
    type: Snowflake
    username: DEMO
    password: xxx
    account: xxx.us-east-2.aws
    database: YOUR_DB
    warehouse: COMPUTE_WH
connectionType: Database
"""


if __name__ == "__main__":
    validate_connection(config)
```

### Ingest your metadata
You can use the configuration below as a template - make sure to adjust it to match your username, password, your database name, and further details about the tables and schemas you want to include. You may optionally ingest your dbt manifest and dbt catalog to display dbt models and dbt docs along with your tables and views.

```python
from prefect_openmetadata.flows import ingest_metadata

config = """
source:
  type: snowflake
  serviceName: snowflake
  serviceConnection:
    config:
      type: Snowflake
      username: "xxx"
      password: "xxx"
      database: "YOURDB"
      warehouse: "COMPUTE_WH"
      account: "YOUR_ACCOUNT.us-east-2.aws"
  sourceConfig:
    config:
      type: DatabaseMetadata
      schemaFilterPattern:
        includes: 
            - YOUR_SCHEMA
      dbtConfigSource:
        dbtCatalogFilePath: /Users/you/catalog.json
        dbtManifestFilePath: /Users/you/manifest.json
sink:
  type: metadata-rest
  config: {}
workflowConfig:
  loggerLevel: DEBUG
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: no-auth
"""

if __name__ == "__main__":
    ingest_metadata(config)
```

### Profile your data and add data quality tests

Here is a flow to profile the previously ingested data:

```python
from prefect_openmetadata.flows import profile_metadata

config = """
source:
  type: snowflake
  serviceName: snowflake
  serviceConnection:
    config:
      type: Snowflake
      username: "xxx"
      password: "xxx"
      database: "YOURDB"
      warehouse: "COMPUTE_WH"
      account: "YOUR_ACCOUNT.us-east-2.aws"
  sourceConfig:
    config:
      type: Profiler
      fqnFilterPattern:
        includes:
        - snowflake.ANNA.ANNA_DEMO.*
      generateSampleData: true
processor:
  type: orm-profiler
  config:
    test_suite:
      name: demo_data
      tests:
        - table: snowflake.ANNA.ANNA_DEMO.RAW_CUSTOMERS
          table_tests:
            - testCase:
                config:
                  value: 100
                tableTestType: tableRowCountToEqual
          column_tests:
            - columnName: ID
              testCase:
                config:
                  minValue: 1
                  maxValue: 100
                columnTestType: columnValuesToBeBetween
sink:
  type: metadata-rest
  config: {}
workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: no-auth
"""

if __name__ == "__main__":
    profile_metadata(config)
```

### Add usage query patterns 

Finally, to ensure that you can see sample data and queries performed over given assets, run the following usage workflow (_as always, adjust to your needs_):

```python
from prefect_openmetadata.flows import ingest_metadata

config = """
source:
  type: type: snowflake-usage
  serviceName: snowflake
  serviceConnection:
    config:
      type: Snowflake
      username: "xxx"
      password: "xxx"
      database: "YOURDB"
      warehouse: "COMPUTE_WH"
      account: "YOUR_ACCOUNT.us-east-2.aws"
  sourceConfig:
    config:
      type: DatabaseUsage
processor:
  type: query-parser
  config:
    filter: ''
workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: no-auth
"""

if __name__ == "__main__":
    ingest_metadata(config)
```

**Congratulations** on building your first metadata ingestion workflows with OpenMetadata and Prefect! Head over to the next section to see how you can run this flow on schedule. 
