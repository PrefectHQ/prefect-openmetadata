# Schedule and deploy metadata ingestion flows


## Schedule your OpenMetadata ingestion flows with Prefect

Ingesting your data via manually executed scripts is great for initial exploration, but in order to build a reliable metadata platform, you need to run those workflows on a regular cadence. That’s where you can leverage Prefect [schedules](https://www.notion.so/OM-Docs-01b7a7fbf2ec44f7ab9fa08085b51d14) and [deployments](https://orion-docs.prefect.io/concepts/deployments/).

Here is how you can add a `DeploymentSpec` to your flow to ensure that your metadata gets refreshed every 15 minutes:

```python
# ingestion_flow.py
from datetime import timedelta
from prefect.deployments import DeploymentSpec
from prefect.flow_runners import SubprocessFlowRunner
from prefect.orion.schemas.schedules import IntervalSchedule
from prefect_openmetadata.flows import ingest_metadata

json_config = """See an example in tests/test_flows.py"""

DeploymentSpec(
    name="openmetadata-dev",
    flow=ingest_metadata,
    parameters=dict(config=json_config),
    flow_runner=SubprocessFlowRunner(),
    schedule=IntervalSchedule(interval=timedelta(minutes=15)),
)
```

Here is an explanation of the `DeploymentSpec` arguments:

- `name` - specifies the name of the deployment - you could use it to differentiate between a deployment for development and production environment
- `flow` - points to the flow object, i.e. the flow function name
- `flow_runner` - specifies how the flow run should be deployed; this allows you to deploy the flow run as a docker container, a Kubernetes job, or as a local subprocess - for example, you can deploy it as a subprocess running in a Conda virtual environment named "openmetadata" using the syntax: 
      
      ```python
      SubprocessFlowRunner(condaenv="openmetadata")
      ```

- `schedule` - allows you to choose and customize your desired schedule class; in this example, we are using a simple `IntervalSchedule` triggering a new flow run every 15 minutes. With the asynchronous scheduling service in Prefect 2.0, you could even schedule your flow to run every 10 seconds if you need your metadata to be always up-to-date.

To deploy this scheduled workflow to Prefect, run the following command from your CLI:

```python
prefect deployment create ingestion_flow.py
```

## Deploy Prefect OpenMetadata ingestion flows

So far, we’ve looked at how you can **create** and **schedule** your workflow, but where does this code actually run? This is a place where the concepts of [storage](https://orion-docs.prefect.io/concepts/storage/), [work queues, and agents](https://orion-docs.prefect.io/concepts/work-queues/) become important. But don’t worry - all you need to know to get started is running one CLI command for each of those concepts.

**1) Storage**

Storage is used to tell Prefect where your workflow code lives. To configure storage, run:

```python
prefect storage create
```

The CLI will guide you through the process to select the storage of your choice - to get started you can select the Local Storage and choose some path in your file system. You can then directly select it as your default storage.

**2) Work Queue**

Work queues collect scheduled runs and agents pick those up from the queue. To create a default work queue, run:

```python
prefect work-queue create default
```

**3) Agent**

Agents are lightweight processes that poll their work queues for scheduled runs and execute workflows on the infrastructure you specified on the `DeploymentSpec`’s `flow_runner`. To create an agent corresponding to the default work queue, run:

```python
prefect agent start default
```

That’s all you need! Once you have executed those three commands, your scheduled deployments (*such as the one we defined using `ingestion_flow.py` above*) are now scheduled, and Prefect will ensure that your metadata stays up-to-date.

You can observe the state of your metadata ingestion workflows from the [Prefect Orion UI](https://orion-docs.prefect.io/ui/overview/). The UI will also include detailed logs showing which metadata got updated to ensure your data platform remains healthy and observable.

## Using Prefect 2.0 in the Cloud

If you want to move beyond this local installation, you can deploy Prefect 2.0 to run your OpenMetadata ingestion workflows by:

- self-hosting the orchestration layer - see the [list of resources on Prefect Discourse](https://discourse.prefect.io/t/how-to-self-host-prefect-2-0-orchestration-layer-list-of-resources-to-get-started/952),
- or signing up for [Prefect Cloud 2.0](https://beta.prefect.io/) - [the following page](https://discourse.prefect.io/t/how-to-get-started-with-prefect-cloud-2-0/539) will walk you through the process.

For various deployment options of OpenMetadata, check the “Deploy” section of [this documentation](https://docs.open-metadata.org/).

## Questions about using OpenMetadata with Prefect

If you have any questions about configuring Prefect, post your question on [Prefect Discourse](https://discourse.prefect.io/) or in the [Prefect Community Slack](https://www.prefect.io/slack/).

And if you need support for OpenMetadata, get in touch on [OpenMetadata Slack](https://slack.open-metadata.org).
