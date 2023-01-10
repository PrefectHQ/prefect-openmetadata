# Schedule and deploy metadata ingestion flows

## Schedule your OpenMetadata ingestion flows with Prefect

Ingesting your data via manually executed scripts is great for initial exploration, but in order to build a reliable metadata platform, you need to run those workflows on a regular cadence. That’s where you can leverage Prefect [schedules](https://docs.prefect.io/concepts/schedules/) and [deployments](https://docs.prefect.io/concepts/deployments/).

Here is how you can create a `Deployment` to ensure that your metadata ingestion flow `ingest_metadata` in the script `myflow.py` gets refreshed every 15 minutes:

```bash
prefect deployment build -a -n dev myflow.py:ingest_metadata --interval 900
```

Here is an explanation of the `prefect deployment build` flags:

- `-a` - will automatically register the resulting deployment with the API
- `-n` - specifies the name of the deployment - you could use it to differentiate between a deployment for development and production environment
- `myflow.py:ingest_metadata` - entrypoint to the flow object, i.e. the Python script and the flow function name
- `--interval 900` - schedule interval in seconds, here: triggering a new flow run every 15 minutes. With the asynchronous scheduling service in Prefect 2.0, you can schedule your flow to run even every 10 seconds if you need your metadata to be updated near real-time.


## Deploy your execution layer to run your flows

So far, we’ve looked at how you can **create** and **schedule** your workflow, but where does this code actually run? This is a place where the concepts of [storage](https://docs.prefect.io/concepts/storage/) and [infrastructure]() blocks, as well as [work queues and agents](https://docs.prefect.io/concepts/work-queues/) become important. But don’t worry - all you need to know to get started is running a single CLI command:

```bash
prefect agent start -q default
```

Once you have executed that command, your scheduled deployments (*such as the one we defined using `myflow.py` above*) are now scheduled, and Prefect will ensure that your metadata stays up-to-date.

You can observe the state of your metadata ingestion workflows from the [Prefect Orion UI](https://docs.prefect.io/ui/overview/). The UI will also include detailed logs showing which metadata got updated to ensure your data platform remains healthy and observable.

## Using Prefect in the Cloud

If you want to move beyond this local installation, you can deploy Prefect to run your OpenMetadata ingestion workflows by:

- self-hosting the orchestration layer - see the [list of resources on Prefect Discourse](https://discourse.prefect.io/t/how-to-self-host-prefect-2-0-orchestration-layer-list-of-resources-to-get-started/952),
- or signing up for [Prefect Cloud](https://app.prefect.cloud/) - [the following page](https://docs.prefect.io/ui/cloud-getting-started/) will walk you through the process.

For various deployment options of OpenMetadata, check the [Deployment documentation](https://docs.open-metadata.org/deployment).

## Questions about using OpenMetadata with Prefect

If you have any questions about configuring Prefect, post your question on [Prefect Discourse](https://discourse.prefect.io/) or in the [Prefect Community Slack](https://www.prefect.io/slack/).

And if you need support for OpenMetadata, get in touch on [OpenMetadata Slack](https://slack.open-metadata.org).
