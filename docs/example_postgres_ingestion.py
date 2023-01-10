"""
pip install SQLAlchemy psycopg2

Login to the UI with user admin, password admin
and use the link below to see how to generate jwtToken:
https://docs.open-metadata.org/how-to-guides/cli-ingestion-with-basic-auth
"""
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
      jwtToken: 'eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJpbmdlc3Rpb24tYm90IiwiaXNCb3QiOnRydWUsImlzcyI6Im9wZW4tbWV0YWRhdGEub3JnIiwiaWF0IjoxNjczMjI4MjEwLCJlbWFpbCI6ImluZ2VzdGlvbi1ib3RAb3Blbm1ldGFkYXRhLm9yZyJ9.fkEZAWUbQEWLC19tOMTMlTxZhkY4YUdOAzDucQVtTtvrgAn8Q3Oi8Ogxc12lCUZh7VI8ykxXFhYqjQbTjp00ZFrSt4hoDn5j7dQ9Ewz4bv35I9m931JkoX-aHclzFeqhSlI6kqkS5KL7sDKhT9eVFEGVmNoBVpcSnz2_6PUD8h0LeUQOxYG4_frqungSWunVScshpqEG-mCyAeXnIFbbt0Wu6x8w-zuNfyEiI3K5VWf2NejEG1hWGYBQjVJNTu7ZQyPdxTYBxkK7kFuj-sN3ASPzdX0DchnUpGpRXpzN8QB73pE9xeLJhD_NB7jPOu1b59XCpdg47UGooRjpumNbuQ'
"""  # noqa

if __name__ == "__main__":
    ingest_metadata(postgres)
