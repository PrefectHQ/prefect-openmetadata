# Sample profiler configurations

```yaml
source:
  type: snowflake
  serviceName: "<service name>"
  serviceConnection:
    config:
      type: Snowflake
      username: "<username>"
      password: "<password>"
      database: "<database>"
      warehouse: "<warehouse>"
      hostPort: account.region.service.snowflakecomputing.com
      account: "<acount>"
      privateKey: "<privateKey>"
      snowflakePrivatekeyPassphrase: "<passphrase>"
      scheme: "<scheme>"
      role: "<role>"
  sourceConfig:
    config:
      type: Profiler
      fqnFilterPattern: "<table FQN filtering regex>"
processor:
  type: orm-profiler
  config: {}
sink:
  type: metadata-rest
  config: {}
workflowConfig:
  openMetadataServerConfig:
    hostPort: "<OpenMetadata host and port>"
    authProvider: "<OpenMetadata auth provider>"
```

Adding dbt to ingestion spec:

```yaml
sourceConfig:
  config:
    dbtConfigSource:
      dbtSecurityConfig:
        awsAccessKeyId: <AWS Access Key Id>
        awsSecretAccessKey: <AWS Secret Access Key>
        awsRegion: AWS Region
      dbtPrefixConfig:
        dbtBucketName: prefectdata
        dbtObjectPrefix: "dbt/" # s3://prefectdata/dbt/
```

the processor is of type orm-profiler and can include column and table tests:

```yaml
processor:
  type: orm-profiler
  config:
    test_suite:
      name: <Test Suite name>
      tests:
        - table: <Table FQN>
          table_tests:
            - testCase:
                config:
                  value: 100
                tableTestType: tableRowCountToEqual
          column_tests:
            - columnName: <Column Name>
              testCase:
                config:
                  minValue: 0
                  maxValue: 99
                columnTestType: columnValuesToBeBetween
```

# Usage workflow config example

Can be passed to the `ingest_data` flow

```yaml
source:
  type: query-log-usage
  serviceName: local_mysql
  serviceConnection:
    config:
      type: Mysql
      username: openmetadata_user
      password: openmetadata_password
      hostPort: localhost:3306
      connectionOptions: {}
      connectionArguments: {}
  sourceConfig:
    config:
      queryLogFilePath: <path to query log file>
processor:
  type: query-parser
  config:
    filter: ''
stage:
  type: table-usage
  config:
    filename: /tmp/query_log_usage
bulkSink:
  type: metadata-usage
  config:
    filename: /tmp/query_log_usage
workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: no-auth
```
