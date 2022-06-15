# prefect-openmetadata

## Welcome!

Using [Prefect](https://prefect.io/) and [OpenMetadata](https://open-metadata.org/) together will help you build and maintain a **data platform you can trust**. 

Prefect allows you to orchestrate your data workflows and provides visibility into the health of your **workflow execution** and **workflow lineage**. With OpenMetadata integration, you can enrich your orchestration system with metadata about data lineage, data catalog, data quality and governance, giving you a single pane of glass about the health of your system. 


## Getting Started


### Python setup

Requires an installation of Python 3.8+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

This ``prefect-openmetadata`` package is designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [documentation](https://orion-docs.prefect.io/).

### Installation

Install `prefect-openmetadata` with `pip`:

```bash
pip install prefect-openmetadata
```

### Install `OpenMetadata` and ``Prefect 2.0``

Head over to the [install OpenMetadata](install_openmetadata.md) page for detailed instructions on how to install and configure both platforms.

### Write and run metadata ingestion flow

```python
from prefect_openmetadata.flows import ingest_metadata

config = """See an example in the section: Run ingestion flow"""

if __name__ == "__main__":
    ingest_metadata(config)
```

For more details, check the [run ingestion flow](run_ingestion_flow.md) section.

### Schedule a metadata ingestion flow

Simple example:
```python
DeploymentSpec(
    name="openmetadata-dev",
    flow=ingest_metadata,
    schedule=IntervalSchedule(interval=timedelta(minutes=15)),
)
```

For more details, check the [schedule ingestion flow](schedule_ingestion_flow.md) section.


## Resources

If you encounter any bugs while using `prefect-openmetadata`, feel free to open an issue in the [prefect-openmetadata](https://github.com/PrefectHQ/prefect-openmetadata) repository.

If you have any questions or issues while using `prefect-openmetadata`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).


## Development

If you'd like to install a version of `prefect-openmetadata` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/PrefectHQ/prefect-openmetadata.git

cd prefect-openmetadata/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
