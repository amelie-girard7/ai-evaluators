---
title: Synthesize evaluation sets
source: https://learn.microsoft.com/en-us/azure/databricks/generative-ai/agent-evaluation/synthesize-evaluation-set
author:
- '[[mssaperla]]'
published: null
created: 2026-05-01
description: Learn about how to synthesize evaluation sets from documents.
tags:
- clippings
processed: true
processed_at: '2026-05-01'
---
This page describes how to synthetically generate a high-quality evaluation set for measuring the quality of your agent.

Manually building an evaluation set is often time-consuming, and it is difficult to ensure that it covers all of the functionality of your agent. Agent Evaluation removes this barrier by automatically generating a representative evaluation set from your documents, allowing you to quickly evaluate your agent with good coverage of test cases.

## Generate an evaluation set

To synthesize evaluations for an agent that uses document retrieval, use the `generate_evals_df` method that is part of the `databricks-agents` Python package. For details about the API, see the [Python SDK reference](https://api-docs.databricks.com/python/databricks-agents/latest/databricks_agent_eval.html#databricks.agents.evals.generate_evals_df).

This method requires you to provide your documents as a Pandas DataFrame or a Spark DataFrame.

The input dataframe must have the following columns:

- `content`: The parsed document content as a string.
- `doc_uri`: The document URI.

You can use three additional parameters to help control the generation:

- `num_evals`: The total number of evaluations to generate across all of the documents. The function tries to distribute generated evals over all of your documents, taking into consideration their size. If `num_evals` is less than the number of documents, not all documents will be covered in the evaluation set.
	For details about how `num_evals` is used to distribute evaluations across the documents, see [How `num_evals` is used](#num-evals).
- `agent_description`: A task description of the agent
- `question_guidelines`: A set of guidelines that help guide the synthetic question generation. This is a free-form string that will be used to prompt the generation. See the example below.

The output of `generate_evals_df` is a DataFrame. The columns in the DataFrame depend on whether you are using MLflow 3 or MLflow 2.

### MLflow 3

- `request_id`: A unique request id.
- `inputs`: The synthesized inputs, in [Chat Completion API](https://platform.openai.com/docs/api-reference/chat)
- `expectations`: A dictionary with two fields:
	- `expected_facts`: A list of expected facts in the response. This column has dtype list\[string\].
		- `expected_retrieved_context`: The context this evaluation has been synthesized from, including the document content and the doc\_uri.

### MLflow 2

- `request_id`: A unique request id.
- `request`: The synthesized request.
- `expected_facts`: A list of expected facts in the response. This column has dtype list\[string\].
- `expected_retrieved_context`: The context this evaluation has been synthesized from, including the document content and the doc\_uri.

## Example

The following example uses `generate_evals_df` to generate an evaluation set and then directly calls `mlflow.genai.evaluate()` to measure the performance of Meta Llama 3.1 on this eval set. The Llama 3.1 model has never seen your documents, so it is likely to hallucinate. Even so, this experiment is a good baseline for your custom agent.

Python

```python
%pip install mlflow[databricks] databricks-agents
dbutils.library.restartPython()

import mlflow
from databricks.agents.evals import generate_evals_df
from mlflow.genai.scorers import Correctness
import pandas as pd

# \`docs\` can be a Pandas DataFrame or a Spark DataFrame with two columns: 'content' and 'doc_uri'.
docs = pd.DataFrame.from_records(
    [
      {
        'content': f"""
            Apache Spark is a unified analytics engine for large-scale data processing. It provides high-level APIs in Java,
            Scala, Python and R, and an optimized engine that supports general execution graphs. It also supports a rich set
            of higher-level tools including Spark SQL for SQL and structured data processing, pandas API on Spark for pandas
            workloads, MLlib for machine learning, GraphX for graph processing, and Structured Streaming for incremental
            computation and stream processing.
        """,
        'doc_uri': 'https://spark.apache.org/docs/3.5.2/'
      },
      {
        'content': f"""
            Spark's primary abstraction is a distributed collection of items called a Dataset. Datasets can be created from Hadoop InputFormats (such as HDFS files) or by transforming other Datasets. Due to Python's dynamic nature, we don't need the Dataset to be strongly-typed in Python. As a result, all Datasets in Python are Dataset[Row], and we call it DataFrame to be consistent with the data frame concept in Pandas and R.""",
        'doc_uri': 'https://spark.apache.org/docs/3.5.2/quick-start.html'
      }
    ]
)

agent_description = """
The Agent is a RAG chatbot that answers questions about using Spark on Databricks. The Agent has access to a corpus of Databricks documents, and its task is to answer the user's questions by retrieving the relevant docs from the corpus and synthesizing a helpful, accurate response. The corpus covers a lot of info, but the Agent is specifically designed to interact with Databricks users who have questions about Spark. So questions outside of this scope are considered irrelevant.
"""

question_guidelines = """
# User personas
- A developer who is new to the Databricks platform
- An experienced, highly technical Data Scientist or Data Engineer

# Example questions
- what API lets me parallelize operations over rows of a delta table?
- Which cluster settings will give me the best performance when using Spark?

# Additional Guidelines
- Questions should be succinct, and human-like
"""

num_evals = 10

evals = generate_evals_df(
    docs,
    # The total number of evals to generate. The method attempts to generate evals that have full coverage over the documents
    # provided. If this number is less than the number of documents, is less than the number of documents,
    # some documents will not have any evaluations generated. See "How num_evals is used" below for more details.
    num_evals=num_evals,
    # A set of guidelines that help guide the synthetic generation. These are free-form strings that will be used to prompt the generation.
    agent_description=agent_description,
    question_guidelines=question_guidelines
)

display(evals)

# Evaluate the model using the newly generated evaluation set. After the function call completes, click the UI link to see the results. You can use this as a baseline for your agent.
predict_fn = mlflow.genai.to_predict_fn("endpoints:/databricks-meta-llama-3-1-405b-instruct")

results = mlflow.genai.evaluate(
  predict_fn=predict_fn,
  scorers=[Correctness()],
  data=evals
)
```

Example output is shown below. The output columns depend on whether you are using MLflow 3 or MLflow 2.

### MLflow 3

In the following example output, the columns `request_id` and `expectations.expected_retrieved_context` are not shown.

| inputs.messages\[0\].content | expectations.expected\_facts |
| --- | --- |
| What is Spark SQL used for in Apache Spark? | - Spark SQL is used for SQL processing in Apache Spark. - Spark SQL is used for structured data processing in Apache Spark. |
| What are some high-level tools supported by Apache Spark, and what purposes do they serve? | - Spark SQL for SQL and structured data processing. - pandas API on Spark for handling pandas workloads. - MLlib for machine learning. - GraphX for graph processing. - Structured Streaming for incremental computation and stream processing. |
| What is the primary abstraction in Spark and how are Datasets represented in Python? | - The primary abstraction in Spark is a Dataset. - In Python, Spark's Datasets are referred to as DataFrame. - In Python, Datasets are represented as Dataset\[Row\]. |
| Why are all Datasets in Python called DataFrames in Spark? | - Datasets in Python are called DataFrames in Spark to maintain consistency with the data frame concept. - The data frame concept is standard in Pandas and R. |

### MLflow 2

In the following example output, the columns `request_id` and `expected_retrieved_context` are not shown.

| request | expected\_facts |
| --- | --- |
| What is Spark SQL used for in Apache Spark? | - Spark SQL is used for SQL processing in Apache Spark. - Spark SQL is used for structured data processing in Apache Spark. |
| What are some high-level tools supported by Apache Spark, and what purposes do they serve? | - Spark SQL for SQL and structured data processing. - pandas API on Spark for handling pandas workloads. - MLlib for machine learning. - GraphX for graph processing. - Structured Streaming for incremental computation and stream processing. |
| What is the primary abstraction in Spark and how are Datasets represented in Python? | - The primary abstraction in Spark is a Dataset. - In Python, Spark's Datasets are referred to as DataFrame. - In Python, Datasets are represented as Dataset\[Row\]. |
| Why are all Datasets in Python called DataFrames in Spark? | - Datasets in Python are called DataFrames in Spark to maintain consistency with the data frame concept. - The data frame concept is standard in Pandas and R. |

## How num\_evals is used

`num_evals` is the total number of evaluations generated for the set of documents. The function distributes these evaluations across the documents while trying to account for differences in document size. That is, it tries to maintain approximately the same number of questions per page across the document set.

If `num_evals` is less than the number of documents, some documents will not have any evaluations generated. The DataFrame returned by the function includes a column with the `source_doc_ids` that were used to generate evaluations. You can use this column to join back to your original DataFrame to generate evals for the documents that were skipped.

To help estimate the `num_evals` for a desired coverage, we provide the `estimate_synthetic_num_evals` method:

Python

```python
from databricks.agents.evals import estimate_synthetic_num_evals

num_evals = estimate_synthetic_num_evals(
  docs, # Same docs as before.
  eval_per_x_tokens = 1000 # Generate 1 eval for every x tokens to control the coverage level.
)
```

## Create a synthetic evaluation set — example notebook

See the following notebook for example code to create a synthetic evaluation set.

#### Synthetic evaluations example notebook

[Get notebook](https://docs.databricks.com/notebooks/source/generative-ai/synthetic-evals-notebook.html)

## Information about the models powering synthetic data

- Synthetic data might use third-party services to evaluate your generative AI applications, including Azure OpenAI operated by Microsoft.
- For Azure OpenAI, Databricks has opted out of Abuse Monitoring so no prompts or responses are stored with Azure OpenAI.
- For European Union (EU) workspaces, synthetic data uses models hosted in the EU. All other regions use models hosted in the US.
- Disabling [Partner-powered AI features](https://learn.microsoft.com/en-us/azure/databricks/databricks-ai/partner-powered) prevents the synthetic data service from calling partner-powered models.
- Data sent to the synthetic data service is not used for any model training.
- Synthetic data is intended to help customers evaluate their agent applications, and the outputs should not be used to train, improve, or fine-tune an LLM.

## Limitation

You cannot create synthetic evaluation datasets in a workspace with [serverless egress control](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/network-policies) enabled.

---

## Additional resources

Training

Module

[Run evaluations and generate synthetic datasets - Training](https://learn.microsoft.com/en-us/training/modules/run-evaluations-generate-synthetic-datasets/?source=recommendations)

Learn how to run evaluations and generate synthetic datasets with the Azure AI Evaluation SDK.

Certification

[Microsoft Certified: Azure Data Scientist Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-scientist/?source=recommendations)

Manage data ingestion and preparation, model training and deployment, and machine learning solution monitoring with Python, Azure Machine Learning and MLflow.