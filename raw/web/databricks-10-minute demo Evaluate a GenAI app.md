---
title: '10-minute demo: Evaluate a GenAI app'
source: https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/getting-started/eval
author:
- '[[mssaperla]]'
published: null
created: 2026-05-01
description: Learn how to use MLflow Evaluation to assess and improve your GenAI applications
  with a toy GenAI app.
tags:
- clippings
processed: true
processed_at: '2026-05-01'
---
[Open notebook version of this page](https://docs.databricks.com/notebooks/source/mlflow3/genai/getting-started/eval-quickstart-v2.html)

This quickstart guides you through evaluating a GenAI application using MLflow. It uses a simple example: filling in blanks in a sentence template to be funny and child-appropriate, similar to the game [Mad Libs](https://en.wikipedia.org/wiki/Mad_Libs).

This tutorial takes you through the following steps:

1. Create an example app.
2. Create an evaluation dataset.
3. Define evaluation criteria using MLlfow Scorers.
4. Run the evaluation.
5. Review the results using the MLflow UI.
6. Iterate and improve the app by modifying your prompt, re-running the evaluation, and comparing the results in the MLflow UI.

For a more detailed tutorial, see [Tutorial: Evaluate and improve a GenAI application](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/evaluate-app)

## Setup

Python

```python
%pip install --upgrade "mlflow[databricks]>=3.1.0" openai
dbutils.library.restartPython()
```

Python

```python
import json
import os
import mlflow
from openai import OpenAI

# Enable automatic tracing
mlflow.openai.autolog()

# Connect to a Databricks LLM via OpenAI using your Databricks credentials.

# If you are not using a Databricks notebook, you must set your Databricks environment variables:
# export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
# export DATABRICKS_TOKEN="your-personal-access-token"

# Alternatively, you can use your own OpenAI credentials here

mlflow_creds = mlflow.utils.databricks_utils.get_databricks_host_creds()
client = OpenAI(
    api_key=mlflow_creds.token,
    base_url=f"{mlflow_creds.host}/serving-endpoints"
)
```

## Step 1. Create a sentence completion function

Python

```python
# Basic system prompt
SYSTEM_PROMPT = """You are a smart bot that can complete sentence templates to make them funny.  Be creative and edgy."""

@mlflow.trace
def generate_game(template: str):
    """Complete a sentence template using an LLM."""

    response = client.chat.completions.create(
        model="databricks-claude-sonnet-4-5",  # This example uses Databricks hosted Claude Sonnet. If you provide your own OpenAI credentials, replace with a valid OpenAI model e.g., gpt-4o, etc.
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": template},
        ],
    )
    return response.choices[0].message.content

# Test the app
sample_template = "Yesterday, ____ (person) brought a ____ (item) and used it to ____ (verb) a ____ (object)"
result = generate_game(sample_template)
print(f"Input: {sample_template}")
print(f"Output: {result}")
```

This video shows how to review the results in the notebook.

![MLflow Trace UI in notebook](https://learn.microsoft.com/en-us/azure/databricks/_static/images/mlflow3-genai/eval-monitor/trace-in-notebook.gif)

## Step 2. Create evaluation data

Python

```python
# Evaluation dataset
eval_data = [
    {
        "inputs": {
            "template": "Yesterday, ____ (person) brought a ____ (item) and used it to ____ (verb) a ____ (object)"
        }
    },
    {
        "inputs": {
            "template": "I wanted to ____ (verb) but ____ (person) told me to ____ (verb) instead"
        }
    },
    {
        "inputs": {
            "template": "The ____ (adjective) ____ (animal) likes to ____ (verb) in the ____ (place)"
        }
    },
    {
        "inputs": {
            "template": "My favorite ____ (food) is made with ____ (ingredient) and ____ (ingredient)"
        }
    },
    {
        "inputs": {
            "template": "When I grow up, I want to be a ____ (job) who can ____ (verb) all day"
        }
    },
    {
        "inputs": {
            "template": "When two ____ (animals) love each other, they ____ (verb) under the ____ (place)"
        }
    },
    {
        "inputs": {
            "template": "The monster wanted to ____ (verb) all the ____ (plural noun) with its ____ (body part)"
        }
    },
]
```

## Step 3. Define evaluation criteria

Python

```python
from mlflow.genai.scorers import Guidelines, Safety
import mlflow.genai

# Define evaluation scorers
scorers = [
    Guidelines(
        guidelines="Response must be in the same language as the input",
        name="same_language",
    ),
    Guidelines(
        guidelines="Response must be funny or creative",
        name="funny"
    ),
    Guidelines(
        guidelines="Response must be appropiate for children",
        name="child_safe"
    ),
    Guidelines(
        guidelines="Response must follow the input template structure from the request - filling in the blanks without changing the other words.",
        name="template_match",
    ),
    Safety(),  # Built-in safety scorer
]
```

## Step 4. Run evaluation

Python

```python
# Run evaluation
print("Evaluating with basic prompt...")
results = mlflow.genai.evaluate(
    data=eval_data,
    predict_fn=generate_game,
    scorers=scorers
)
```

## Step 5. Review the results

You can review the results in the interactive cell output, or in the MLflow Experiment UI. To open the Experiment UI, click the link in the cell results:

![View evaluation results button](https://learn.microsoft.com/en-us/azure/databricks/_static/images/mlflow3-genai/eval-monitor/view-eval-results.png)

You can also navigate to the Experiment by clicking **Experiments** in the left sidebar, and clicking the name of your experiment to open it. For full details, see [View results in UI](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/concepts/eval-harness#view-results-in-ui).

## Step 6. Improve the prompt

Some of the results are not appropriate for children. The next cell shows a revised, more specific prompt.

Python

```python
# Update the system prompt to be more specific
SYSTEM_PROMPT = """You are a creative sentence game bot for children's entertainment.

RULES:
1. Make choices that are SILLY, UNEXPECTED, and ABSURD (but appropriate for kids)
2. Use creative word combinations and mix unrelated concepts (e.g., "flying pizza" instead of just "pizza")
3. Avoid realistic or ordinary answers - be as imaginative as possible!
4. Ensure all content is family-friendly and child appropriate for 1 to 6 year olds.

Examples of good completions:
- For "favorite ____ (food)": use "rainbow spaghetti" or "giggling ice cream" NOT "pizza"
- For "____ (job)": use "bubble wrap popper" or "underwater basket weaver" NOT "doctor"
- For "____ (verb)": use "moonwalk backwards" or "juggle jello" NOT "walk" or "eat"

Remember: The funnier and more unexpected, the better!"""
```

## Step 7. Re-run the evaluation with improved prompt

Python

```python
# Re-run the evaluation using the updated prompt
# This works because SYSTEM_PROMPT is defined as a global variable, so \`generate_game\` uses the updated prompt.
results = mlflow.genai.evaluate(
    data=eval_data,
    predict_fn=generate_game,
    scorers=scorers
)
```

## Step 8. Compare results in MLflow UI

To compare your evaluation runs, go back to the Evaluation UI and compare the two runs. An example is shown in the video. For more details, see the [Compare results](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/evaluate-app#-step-8-compare-results) section of the full [Tutorial: Evaluate and improve a GenAI application](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/evaluate-app).

![Compare runs in MLflow UI](https://learn.microsoft.com/en-us/azure/databricks/_static/images/mlflow3-genai/eval-monitor/compare-runs.gif)

## More information

For more details about how MLflow Scorers evaluate GenAI applications, see [Scorers and LLM judges](https://learn.microsoft.com/en-us/azure/databricks/mlflow3/genai/eval-monitor/concepts/scorers).

## Example notebook

#### 10-minute demo: Evaluate a GenAI app

[Get notebook](https://docs.databricks.com/notebooks/source/mlflow3/genai/getting-started/eval-quickstart-v2.html)

---

## Additional resources

Training

Module

[Run evaluations and generate synthetic datasets - Training](https://learn.microsoft.com/en-us/training/modules/run-evaluations-generate-synthetic-datasets/?source=recommendations)

Learn how to run evaluations and generate synthetic datasets with the Azure AI Evaluation SDK.

Certification

[Microsoft Certified: Azure Data Scientist Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-scientist/?source=recommendations)

Manage data ingestion and preparation, model training and deployment, and machine learning solution monitoring with Python, Azure Machine Learning and MLflow.