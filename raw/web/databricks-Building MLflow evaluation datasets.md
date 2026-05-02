---
title: Building MLflow evaluation datasets
source: https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/build-eval-dataset
author:
- '[[mssaperla]]'
published: null
created: 2026-05-01
description: Build MLflow evaluation datasets for your GenAI apps using various methods,
  including from traces, from scratch, from existing data, or synthetic generation.
tags:
- clippings
processed: true
processed_at: '2026-05-01'
---
To systematically test and improve a GenAI application, you use an evaluation dataset. An evaluation dataset is a selected set of example inputs — either labeled (with known expected outputs) or unlabeled (without ground-truth answers). Evaluation datasets help you improve your app's performance in the following ways:

- Improve quality by testing fixes against known problematic examples from production.
- Prevent regressions. Create a "golden set" of examples that must always work correctly.
- Compare app versions. Test different prompts, models, or app logic against the same data.
- Target specific features. Build specialized datasets for safety, domain knowledge, or edge cases.
- Validate the app across different environments as part of LLMOps.

MLflow evaluation datasets are stored in Unity Catalog, which provides built-in versioning, lineage, sharing, and governance.

## Requirements

- To create an evaluation dataset, you must have `CREATE TABLE` permissions on a Unity Catalog schema.
- An evaluation dataset is attached to an MLflow experiment. If you do not already have an experiment, see [Create an MLflow Experiment](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/getting-started/connect-environment#create-expt) to create one.

## Data sources for evaluation datasets

You can use any of the following to create an evaluation dataset:

- Existing traces. If you have already captured traces from a GenAI application, you can use them to create an evaluation dataset based on real-world scenarios.
- An existing dataset, or directly entered examples. This option is useful for quick prototyping or for targeted testing of specific features.
- Synthetic data. Databricks can automatically generate a representative evaluation set from your documents, allowing you to quickly evaluate your agent with good coverage of test cases.

This page describes how to create an MLflow evaluation dataset. You can also use other types of datasets, such as Pandas DataFrames or a list of dictionaries. See [MLflow evaluation examples for GenAI](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/eval-examples) for examples.

## Create a dataset using the UI

Follow these steps to use the UI to create a dataset from existing traces. For reference information, see [MLflow evaluation dataset UI](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/concepts/eval-datasets#ui).

1. Click **Experiments** in the sidebar to display the Experiments page.
2. Click on the name of your experiment to open it.
	![Open experiment](https://learn.microsoft.com/en-us/azure/databricks/_static/images/mlflow3-genai/eval-monitor/experiments-page.png)
3. In the left sidebar, click **Traces**.
4. Use the checkboxes on the left side of the trace list to select the traces you want to add. To select all traces on the current page, click the checkbox next to **Trace ID** in the column header.
	![Select traces](https://learn.microsoft.com/en-us/azure/databricks/_static/images/mlflow3-genai/eval-monitor/select-traces.gif)
5. Click **Actions**. The button label shows the number of selected traces, for example **Actions (3)**.
	![Actions menu](https://learn.microsoft.com/en-us/azure/databricks/_static/images/mlflow3-genai/eval-monitor/actions-menu-eval-dataset.png)
6. Under **Use for evaluation**, select **Add to evaluation dataset**. The **Add traces to evaluation dataset** dialog opens.
7. If no evaluation datasets exist for this experiment, or if you want to add traces to a new dataset, follow these steps to create a new evaluation dataset:
	1. Click **Create new dataset**.
		2. Select the Unity Catalog schema to hold the new dataset.
		3. Enter a name for the dataset and click **Create Dataset**.
		4. Click **Export** and then click **Done**.
	![Add traces dialog if no evaluation datasets exist](https://learn.microsoft.com/en-us/azure/databricks/_static/images/mlflow3-genai/eval-monitor/add-traces-dialog-none-existing.png)
	If evaluation datasets already exist for the experiment, click **Export** to the right of the dataset you want to add the traces to. You can export to more than one dataset. When you've finished exporting, click **Done**.
	![Add traces dialog if with existing evaluation datasets](https://learn.microsoft.com/en-us/azure/databricks/_static/images/mlflow3-genai/eval-monitor/add-traces-eval-set-dialog.png)

## Create a dataset using the SDK

Follow these steps to use the SDK to create a dataset. For reference information, see [Evaluation dataset reference](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/concepts/eval-datasets).

### Step 1. Create the dataset

Python

```python
import mlflow
import mlflow.genai.datasets
import time
from databricks.connect import DatabricksSession

# 0. If you are using a local development environment, connect to Serverless Spark which powers MLflow's evaluation dataset service
spark = DatabricksSession.builder.remote(serverless=True).getOrCreate()

# 1. Create an evaluation dataset

# Replace with a Unity Catalog schema where you have CREATE TABLE permission
uc_schema = "workspace.default"
# This table will be created in the above UC schema
evaluation_dataset_table_name = "email_generation_eval"

eval_dataset = mlflow.genai.datasets.create_dataset(
    name=f"{uc_schema}.{evaluation_dataset_table_name}",
)
print(f"Created evaluation dataset: {uc_schema}.{evaluation_dataset_table_name}")
```

### Step 2: Add records to your dataset

This section describes several options for adding records to the evaluation dataset.

#### From existing traces

One of the most effective ways to build a relevant evaluation dataset is by curating examples directly from your application's historical interactions captured by MLflow Tracing. You can create datasets from traces using either the MLflow Monitoring UI or the SDK.

Programmatically search for traces and then add them to the dataset using `search_traces()`. Use filters to identify traces by success, failure, use in production, or other properties. See [Search traces programmatically](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/tracing/observe-with-traces/query-via-sdk).

Python

```python
import mlflow

# 2. Search for traces
traces = mlflow.search_traces(
    filter_string="attributes.status = 'OK'",
    order_by=["attributes.timestamp_ms DESC"],
    tags.environment = 'production',
    max_results=10
)

print(f"Found {len(traces)} successful traces")

# 3. Add the traces to the evaluation dataset
eval_dataset = eval_dataset.merge_records(traces)
print(f"Added {len(traces)} records to evaluation dataset")

# Preview the dataset
df = eval_dataset.to_df()
print(f"\nDataset preview:")
print(f"Total records: {len(df)}")
print("\nSample record:")
sample = df.iloc[0]
print(f"Inputs: {sample['inputs']}")
```

#### Select traces for evaluation datasets

Before adding traces to your dataset, identify which traces represent important test cases for your evaluation needs. You can use both quantitative and qualitative analysis to select representative traces.

**Quantitative trace selection**

Use the MLflow UI or SDK to filter and analyze traces based on measurable characteristics:

- **In the MLflow UI**: Filter by tags (e.g., `tag.quality_score < 0.7`), search for specific inputs/outputs, sort by latency or token usage
- **Programmatically**: Query traces to perform advanced analysis

Python

```python
import mlflow
import pandas as pd

# Search for traces with potential quality issues
traces_df = mlflow.search_traces(
    filter_string="tag.quality_score < 0.7",
    max_results=100
)

# Analyze patterns
# For example, check if quality issues correlate with token usage
correlation = traces_df["span.attributes.usage.total_tokens"].corr(traces_df["tag.quality_score"])
print(f"Correlation between token usage and quality: {correlation}")
```

For complete trace query syntax and examples, see [Search traces programmatically](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/tracing/observe-with-traces/query-via-sdk).

**Qualitative trace selection**

Review individual traces to identify patterns requiring human judgment:

- Examine inputs that led to low-quality outputs
- Look for patterns in how your application handled edge cases
- Identify missing context or faulty reasoning
- Compare high-quality vs. low-quality traces to understand differentiating factors

Once you've identified representative traces, add them to your dataset using the search and merge methods described above.

#### From domain expert labels

Leverage feedback from domain experts captured in MLflow labeling sessions to enrich your evaluation datasets with ground truth labels. Before doing these steps, follow the [collect domain expert feedback](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/human-feedback/expert-feedback/label-existing-traces) guide to create a labeling session.

Python

```python
import mlflow.genai.labeling as labeling

# Get a labeling sessions
all_sessions = labeling.get_labeling_sessions()
print(f"Found {len(all_sessions)} sessions")

for session in all_sessions:
    print(f"- {session.name} (ID: {session.labeling_session_id})")
    print(f"  Assigned users: {session.assigned_users}")

# Sync from the labeling session to the dataset

all_sessions[0].sync(dataset_name=f"{uc_schema}.{evaluation_dataset_table_name}")
```

#### Build from scratch or import existing

You can import an existing dataset or curate examples from scratch. Your data must match (or be transformed to match) the [evaluation dataset schema](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/concepts/eval-datasets).

Python

```python
# Define comprehensive test cases
evaluation_examples = [
    {
        "inputs": {"question": "What is MLflow?"},
        "expected": {
            "expected_response": "MLflow is the largest open source AI engineering platform for agents, LLMs, and ML models.",
            "expected_facts": [
                "open source AI engineering platform",
                "agents, LLMs, and ML models",
                "experiment tracking",
                "model deployment"
            ]
        },
    },
]

eval_dataset = eval_dataset.merge_records(evaluation_examples)
```

#### Seed using synthetic data

Generating synthetic data can expand your testing efforts by quickly creating diverse inputs and covering edge cases. See [Synthesize evaluation sets](https://learn.microsoft.com/en-us/azure/databricks/generative-ai/agent-evaluation/synthesize-evaluation-set).

#### For conversation simulation

To enable reproducible multi-turn testing, use code similar to the following to store test cases for conversation simulation. For complete documentation on simulating multi-turn conversations, see [Conversation simulation](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/conversation-simulation).

Python

```python
from mlflow.genai.datasets import create_dataset, get_dataset
from mlflow.genai.simulators import ConversationSimulator

# Create a dataset for simulation test cases
dataset = create_dataset(
    name="conversation_scenarios",
    tags={"type": "simulation", "agent": "support-bot"},
)

# Define test cases with goals and personas
simulation_test_cases = [
    {
        "inputs": {
            "goal": "Get help setting up experiment tracking",
            "persona": "You are a data scientist new to MLflow",
        },
    },
    {
        "inputs": {
            "goal": "Debug a model deployment error",
            "persona": "You are a senior engineer who expects precise answers",
        },
    },
    {
        "inputs": {
            "goal": "Understand model versioning best practices",
            "persona": "You are building an ML platform for your team",
            "context": {"team_size": "large", "compliance": "strict"},
        },
    },
]

dataset.merge_records(simulation_test_cases)

# Later, use the dataset with ConversationSimulator
dataset = get_dataset(name="conversation_scenarios")
simulator = ConversationSimulator(test_cases=dataset)
```

## Update existing datasets

You can use the UI or the SDK to update an evaluation dataset.

### Databricks UI

Use the UI to add records to an existing evaluation dataset.

1. Open the dataset page in the Databricks workspace:
	1. In the Databricks workspace, navigate to your experiment.
		2. In the sidebar at left, click **Datasets**.
		3. Click on the name of the dataset in the list.
	![Datasets tab in sidebar](https://learn.microsoft.com/en-us/azure/databricks/_static/images/mlflow3-genai/eval-monitor/datasets-tab.png)
2. Click **Add record**. A new row appears with generic content.
3. Edit the new row directly to enter the input and expectations for the new record. Optionally, set any tags for the new record.
4. Click **Save changes**.

### MLflow SDK

Use the MLflow SDK to update and existing evaluation dataset:

Python

```python
import mlflow.genai.datasets
import pandas as pd

# Load existing dataset
dataset = mlflow.genai.datasets.get_dataset(name="catalog.schema.eval_dataset")

# Add new test cases
new_cases = [
    {
        "inputs": {"question": "What are MLflow models?"},
        "expectations": {
            "expected_facts": ["model packaging", "deployment", "registry"],
            "min_response_length": 100
        }
    }
]

# Merge new cases
dataset = dataset.merge_records(new_cases)
```

## Limitations

- [Customer Managed Keys (CMK)](https://learn.microsoft.com/en-us/azure/databricks/security/keys/customer-managed-keys) are not supported.
- Maximum of 2000 rows per evaluation dataset.
- Maximum of 20 expectations per dataset record.

If you need any of these limitations relaxed for your use case, contact your Databricks representative.

## Next steps

- [Evaluate your app](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/evaluate-app) - Use your newly created dataset for evaluation
- [Create custom judges](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/custom-judge/create-custom-judge) - Build custom LLM judges to evaluate your application outputs
- [Align judges with feedback](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/align-judges) - Continuously improve your evaluations by aligning judges with expert feedback
- [Query traces via SDK](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/tracing/observe-with-traces/query-via-sdk) - Advanced programmatic trace analysis for dataset selection

---

## Additional resources

Training

Module

[Run evaluations and generate synthetic datasets - Training](https://learn.microsoft.com/en-us/training/modules/run-evaluations-generate-synthetic-datasets/?source=recommendations)

Learn how to run evaluations and generate synthetic datasets with the Azure AI Evaluation SDK.

Certification

[Microsoft Certified: Azure Data Scientist Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-scientist/?source=recommendations)

Manage data ingestion and preparation, model training and deployment, and machine learning solution monitoring with Python, Azure Machine Learning and MLflow.