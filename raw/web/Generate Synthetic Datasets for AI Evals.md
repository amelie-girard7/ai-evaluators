---
title: Generate Synthetic Datasets for AI Evals
source: https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals
author:
- '[[Paul Iusztin]]'
published: 2026-02-24
created: 2026-04-30
description: Learn 5 strategies to generate diverse test inputs for AI evals, from
  cold-start dimension-based generation to production augmentation, agents and RAG.
tags:
- clippings
processed: true
processed_at: '2026-04-30'
---
### 5 strategies from cold start to 450 diverse inputs in minutes

*Welcome to the **[AI Evals & Observability series](https://www.decodingai.com/t/ai-evals-and-observability)**: A 7-part journey from shipping AI apps to systematically improving them. Made by busy people. For busy people.*

🧐 Everyone says you need AI evals. Few explain how to actually build them and answer questions such as…

How do we avoid creating evals that waste our time and resources? How do we build datasets and design evaluators that matter? How do we adapt them for RAG?...and most importantly, how do we stop “vibe checking” and leverage evals to actually track and optimize our app?

*This 7-article series breaks it all down from first principles:*

1. [Integrating AI Evals Into Your AI App](https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app)
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. **Generate Synthetic Datasets for AI Evals** ← *You are here*
4. [How to Design Evaluators](https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures)
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. [RAG Evaluation: The Only 6 Metrics You Need](https://www.decodingai.com/p/rag-evaluation-6-metrics-framework)
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

By the end, you’ll know how to integrate AI evals that actually track and improve the performance of your AI product. No vibe checking required!

**Let’s get started.**

---

In the [previous article](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis), you learned how to iteratively build an evals dataset using the error analysis framework. You started from production traces, labeled them, fixed errors, and grew your dataset over time. **But what if you lack production traces?**

What if your production data only covers a fraction of the features, personas, and edge cases your app supports? Synthetic data fills the gaps that production data alone cannot cover.

When I was building Nova, the deep research agent for my [Agentic AI Engineering course](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31), I hit this exact wall. I built an evaluation layer with binary metrics across dozens of dimensions. The metrics were solid, and the LLM judge was calibrated.

But then I needed test data. The agent lacked real users, real generated articles, and traces. I started by manually writing test inputs. After a painful week, I had maybe 15 examples.

They all reflected my own biases. I was testing the same happy path over and over. Entire categories of failure modes went completely untested.

The most time-consuming bottleneck wasn’t building the judge. It was generating enough diverse, realistic test inputs. That experience taught me that structured synthetic data generation unlocks your entire evals pipeline.

Most teams fire off a single generic prompt to create test inputs. The result is a homogenous, shallow dataset where most examples look identical. The LLM converges on the most generic patterns, causing mode collapse.

You end up testing the same happy path over and over. You need test data, but you lack sufficient or diverse production traffic. Naively generating synthetic data produces datasets that are repetitive and miss your business use cases.

A structured approach gives you control over the distribution of your test inputs. You achieve this by thinking in terms of dimensions, anchoring it in your business use case, and applying targeted strategies.

**In this article, you will learn:**

- When to rely on synthetic data generation.
- Why you should only generate user inputs.
- How to use dimensions to avoid mode collapse.
- Strategies to expand existing production data.
- Approaches for agents, RAG, and deterministic tasks.

![Synthetic data and production traces both feed into the evals dataset, which drives the error analysis flywheel](https://substackcdn.com/image/fetch/$s_!FVJv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc45b991a-4ed5-4d9e-8116-d6c2d8759698_1200x676.png)

Image 1: Synthetic data is a complementary input to production traces — both feed the same evals dataset that drives the error analysis flywheel.

*Before digging into the article, a quick word from our sponsor, Opik.* ↓

---

## Opik: Automated Agent Optimization Using Your Evals Data (Sponsored)

This AI Evals & Observability series is brought to you by **[Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul)**, the LLMOps open-source platform used by Uber, Netflix, Etsy, and more.

We use Opik daily across our courses and AI products. Not just for observability, but now to **automatically optimize our agents’ prompts** using the same datasets and metrics we already have in the platform.

![](https://www.youtube.com/watch?v=FY4uqXmq3fs)

You are learning how to build diverse synthetic datasets to evaluate your AI app. But once you have those datasets and metrics, why stop at measuring quality? **[Opik’s agent optimizer](https://www.comet.com/docs/opik/agent_optimization/quickstart?utm_source=newsletter&utm_medium=partner&utm_campaign=paul)** closes the loop. It uses your **eval dataset to automatically improve your prompts**. Here is why we love it:

- **Same datasets, zero extra setup** — Opik’s optimizer reuses the exact datasets, metrics, and tracing you already have. [Quick start guide](https://www.comet.com/docs/opik/agent_optimization/quickstart?utm_source=newsletter&utm_medium=partner&utm_campaign=paul).
- **Six optimization algorithms** — Choose from strategies like HRPO (our favorite), which performs root-cause analysis on failures and proposes targeted fixes, or evolutionary optimization to explore diverse prompt structures. [See all algorithms.](https://www.comet.com/docs/opik/agent_optimization/algorithms/overview?utm_source=newsletter&utm_medium=partner&utm_campaign=paul)
- **No-code Optimization Studio** — For quick iterations, run optimization directly from the [Optimization Studio UI](https://www.comet.com/docs/opik/agent_optimization/optimization_studio?utm_source=newsletter&utm_medium=partner&utm_campaign=paul). Start from your prompt, pick your dataset, choose an algorithm, and watch Opik test prompt variations against your metrics in real time.

**[Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul)** is fully open source and integrates with OpenAI, Anthropic, Gemini, and 100+ providers. *Start optimizing your agents:*

---

↓ *Now, let’s move back to the article.*

## When Do We Need Synthetic Data?

Before you have any production data, you face *the cold start problem*. You might be building a new feature or preparing for a launch. You need to simulate months of traffic in hours to ensure a reliable initial release. You cannot wait for real users to find your bugs. Synthetic data lets you test your application before day one.

Sometimes your app is live, but you lack enough production data. You might have 50 traces instead of 5,000. The error analysis framework needs enough examples to surface recurring patterns. Synthetic data supplements your real traces.

Other times, your data lacks diversity. You might have plenty of production traces, but they cluster around a few common use cases. Most users ask the same types of questions. You end up with almost no examples of edge cases, adversarial inputs, or minority user personas. Synthetic data lets you deliberately target the underrepresented regions of your input space.

Now that you know when synthetic data is necessary, let’s understand the core principle behind how it works. Most people get this fundamental concept wrong.

## Understanding the Core Principles

*The single most important principle is that **you generate only the user inputs***. These queries, messages, or requests should be as diverse as possible. They must cover all your business use cases, edge cases, and user profiles.

You do not generate the intermediate steps or the final outputs. The whole point of your evals dataset is to capture how your actual system behaves. Synthetic outputs would test a fiction, not your real app.

Instead, you let your real app produce the traces. First, you generate diverse synthetic inputs. Then, you feed all generated inputs into your AI app as if they were real user requests.

You track every trace using your observability platform, such as [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul). This captures all intermediate tool calls, model reasoning, and final outputs. You then pull these full traces to create your synthetic evals dataset.

Finally, you apply the error analysis framework we learned in [Article 2](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis). You label the data with pass/fail judgments, fix errors, build evaluators, and iterate. Your synthetic dataset contains real system behavior triggered by synthetic inputs.

This makes it a valid proxy for production. Since the app handles processing and tool calls, **the entire challenge reduces to a single thing**:

> *You must create diverse, realistic, business-grounded inputs.*

![The synthetic data pipeline from input generation through your AI app and observability to the evals dataset](https://substackcdn.com/image/fetch/$s_!-5_v!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a406f97-34ad-4c5b-a523-b96cee4b129b_1200x676.png)

Image 2: You only generate the synthetic inputs — your real AI app produces the traces and outputs, which flow through your observability platform into a synthetic evals dataset.

Thus, the entire problem reduces to generating input data. Let’s explore concrete strategies for doing so, starting with the most fundamental approach.

## Seeing Your Inputs as Dimensions

When generating input data, using a generic prompt is a mistake. You have zero control over the distribution of edge cases the LLM generates. The LLM will converge on the most generic, repetitive patterns.

Instead, think about a few key dimensions that matter for your application. Model them as tuples to serve as the seeds for your generation process. *A common dimension tuple includes the persona, feature, scenario, and input modality.*

The persona defines the different user types who interact with your app. You get inputs from an impatient customer, a technical expert, or a confused first-time user.

The feature represents the different capabilities of your app that you want to test. Examples include answering emails, generating a meeting summary, or drafting an article.

The scenario defines the specific failure modes or edge cases you want to stress-test. This includes contradictory instructions, garbled input, or outdated information.

The input modality is the format through which the input arrives. This could be plain text, a forwarded email thread, a voice transcript with filler words, or a pasted spreadsheet snippet.

If you define 3 personas, 5 features, 10 scenarios, and 3 input modalities (text, image, documents), and combine them all, you get a maximum of 450 unique data seeds. Each seed is a specific combination that drives a targeted, diverse input.

For each seed, you craft a generation prompt. This prompt includes the dimension values, context about your app, and the scenario’s built-in failure assumption.

Embedding the failure assumption directly in the scenario is highly effective. You tell the LLM exactly what failure to target and what correct behavior looks like [\[1\]](https://www.confident-ai.com/blog/the-definitive-guide-to-synthetic-data-generation-using-llms). This makes your synthetic inputs far more precise.

Here are six dimension seeds with their generation prompts for an email and messaging assistant:

<iframe src="https://datawrapper.dwcdn.net/t7uEh/1/" width="730" height="1692" frameborder="0"></iframe>

Your dimensions will vary depending on your business use case. You might have entirely different dimensions, such as language or urgency level.

#### How much data do you need?

At a minimum, generate enough data so that you have at least one example for each combination of dimensions. Keep generating more data until you stop seeing new failure modes. A simple chatbot might need 200 examples, while a complex agent might need over a thousand.

#### Does this actually work?

You might wonder if synthetic data actually works. From my experience, if well-guided, LLMs are highly capable of generating excellent, diverse examples of user prompts. Synthetic data is the fastest way to build a meaningful evals dataset early on.

Dimension-based generation works great when you start from scratch. But what if you already have some production data and want to expand it?

## When Having Some Production Data

When you have production data, identify your failed or most difficult interactions to use as seeds. If a user input caused your system to fail, generate many variations of that specific input.

You generate multiple variations of the same input with the same underlying semantics to stress-test your app’s consistency. You can vary the phrasing, the level of aggression, or the ambiguity. This ensures your system never fails the same way twice. This method is known as Metamorphic testing.

Suppose your agent fails when users send multi-part questions in a single message. You take this real failed trace, combine it with our multi-dimensional strategy, and ask an LLM to generate 20 variations. The resulting inputs target the same failure class with enough variation to test your fix reliably.

Another method is evolutionary complexity, also known as Evol-Instruct. Originally introduced by the WizardLM researchers to generate synthetic training data for LLMs [\[7\]](https://arxiv.org/abs/2304.12244), it transfers remarkably well to generating evaluation data.

The core problem is the same: producing diverse, progressively complex instructions from a small set of seeds. It uses an evolutionary paradigm to transform simple seed inputs into more complex, realistic ones [\[1\]](https://www.confident-ai.com/blog/the-definitive-guide-to-synthetic-data-generation-using-llms).

*Evol-Instruct is based on 3 core steps:*

1. **In-depth evolving** takes a simple instruction and increases its complexity. It adds constraints, deepens the subject matter, or increases reasoning requirements. A simple order status query evolves into a complex rerouting request.
2. **In-breadth evolving** generates completely new, diverse instructions. This ensures the evaluation suite covers a broad range of topics. While in-depth evolving makes existing inputs harder, in-breadth evolving widens the dataset.
3. **Elimination evolving** is a filtration step. A critic LLM evaluates evolved instructions and discards those that provide no information gain or are nonsensical. This keeps the quality high as complexity grows.

![Evol-Instruct evolutionary data expansion showing in-depth, in-breadth, and elimination evolving from a seed input](https://substackcdn.com/image/fetch/$s_!sO-t!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5393e2f2-1404-4c34-b485-48eb2f3b29f9_1200x888.png)

Image 3: Evol-Instruct uses three evolutionary strategies — in-depth, in-breadth, and elimination evolving — to expand a seed input into a diverse, high-quality evolved dataset.

These methods work well for single-turn interactions. But what about AI agents that handle multi-step, multi-turn conversations?

## When Building Agents

For complex AI agents that plan and execute multi-step workflows, evaluation moves beyond single-turn queries. You need to generate an entire conversation.

To evaluate these systems, you set up a dual-agent dynamic: a tester agent simulating the user, and your actual app agent. The tester agent dynamically generates synthetic inputs turn by turn, reacting to your app’s responses just like a real user would [\[3\]](https://www.zendesk.com/au/blog/zip1-building-realistic-multi-turn-tests-for-ai-agents/). For example, a tester agent playing a frustrated customer might escalate their tone if the first response is vague or pivot to a different request mid-conversation.

Implementing this tester agent uses the exact same ideas as single-turn generation. You define dimensions like personas and scenarios to impersonate, but you simply run the generation iteratively for each conversation turn.

Some recent research from Nov 2025 shows that agents achieve over 90% accuracy on single-step tasks, but conversation correctness drops to 10-15% on full conversations [\[3\]](https://www.zendesk.com/au/blog/zip1-building-realistic-multi-turn-tests-for-ai-agents/). This makes multi-turn flow evaluation a necessity for production reliability.

![Multi-turn synthetic interaction between a tester agent and your AI app with session-level evaluation](https://substackcdn.com/image/fetch/$s_!iClD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d48fe0d-be1e-4826-b232-1ab98efe9a37_1200x888.png)

Image 4: A tester agent dynamically generates reactive inputs across multiple conversation turns, and the entire session is evaluated for goal completion, tone, and process correctness.

Multi-turn interactions are one specialized case for synthetic data. Another common scenario is information retrieval, where your app searches a knowledge base before responding.

## When Doing RAG

When your AI app retrieves information from a knowledge base before generating a response is known as Retrieval-Augmented Generation (RAG). In this scenario, you can use a reverse workflow to create ground-truth datasets. Instead of the standard retrieval flow, you start with the knowledge base and work backwards [\[4\]](https://www.evidentlyai.com/llm-guide/llm-test-dataset-synthetic-data).

You start by taking your documents, PDFs, or structured data. You use an LLM to extract key facts, procedures, numbers, or policies from a specific document chunk that’s part of your knowledge base.

The LLM then generates a realistic user question that can only be answered using that specific chunk. Because the question is derived directly from the source material, you know exactly which document chunk should be retrieved. Which means you can easily generate the right answer as well.

This guarantees perfect alignment between the input, the expected retrieval context, and the expected output. You get a complete ground-truth triplet containing the question, relevant context, and expected answer.

To create more diversity within the dataset, you can use the same strategy to define multiple dimensions and mix up question styles and complexity levels to avoid a shallow dataset.

![Reverse-workflow RAG synthesis deriving questions and answers from knowledge base chunks to create ground-truth triplets](https://substackcdn.com/image/fetch/$s_!EZyL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51414f2b-d109-4a5d-8086-ab41f2bbf027_1200x752.png)

Image 5: The reverse workflow starts from your knowledge base, extracts key facts, generates questions and expected answers, and produces perfectly aligned ground-truth triplets.

This reverse synthesis works because you can derive questions and answers from documents. But what about purely deterministic tasks where the correct answer can be computed exactly?

## For Deterministic Testing

For tasks with deterministic correct answers, you can use your system’s schema or rules to generate both the input and the ground truth. This applies to structured data extraction or calculations, such as text-to-SQL, JSON, code, or math.

You work from the answer backward to the question, similar to the reverse workflow for RAG. However, instead of text, you use schemas, databases, or rule sets [\[6\]](https://deepeval.com/guides/guides-using-synthesizer).

Suppose you want to generate *(text, SQL)* tuples. You have a database with tables for customers, orders, and products. You use your database schema to programmatically generate valid SQL queries of varying complexity. These SQL queries serve as your ground truth.

You then use an LLM to translate each SQL query back into a natural language question. A query selecting customers with pending orders over a specific amount becomes a plain English question.

Your evals dataset now has a natural language input and the correct SQL mapping. You can test whether your system generates the right query and returns the right data.

## Next Steps

Building an evals dataset from production traces alone has limits. Synthetic data solves the cold start problem and fills coverage gaps.

Synthetic data generation is not about blindly asking an LLM to create test cases. It is about structuring your inputs as dimensions, anchoring them in your business use case, and applying the right strategy. The result is a diverse, controlled dataset that you can feed into your error analysis framework.

Now you know how to build your evals dataset from both production and synthetic data. In the next article, we will show you the right way to build your evalautor(s).

Also, remember that this article is part of a **[7-piece series on AI Evals & Observability](https://www.decodingai.com/t/ai-evals-and-observability)**. **Here is what’s ahead:**

1. [Integrating AI Evals Into Your AI App](https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app)
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. **Generate Synthetic Datasets for AI Evals** ← *You just finished this one*
4. [How to Design Evaluators](https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures)
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. [RAG Evaluation: The Only 6 Metrics You Need](https://www.decodingai.com/p/rag-evaluation-6-metrics-framework)
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

See you next Tuesday.

[Paul Iusztin](https://www.pauliusztin.ai/)

---

*What’s your opinion? Do you agree, disagree, or is there something I missed?*

---

*Enjoyed the article? The most sincere compliment is to share our work.*

---

## Go Deeper

**Go from zero to production-grade AI agents** with the [Agentic AI Engineering self-paced course](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31). Built in partnership with [Towards AI](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31).

Across **34 lessons** (articles, videos, and a lot of code), you’ll design, build, evaluate, and deploy production-grade AI agents end to end. By the final lesson, you’ll have **built a multi-agent system** and a **capstone project** where you apply everything you’ve learned on your own.

*Three portfolio projects and a certificate to showcase in interviews. Plus a Discord community where you have direct access to other industry experts and me.*

Rated 4.9/5 ⭐️ by 290+ early students — *“Every AI Engineer needs a course like this.”*

*Not ready to commit?* We also prepared a free 6-day email course to reveal the ***6 critical mistakes that silently destroy agentic systems.** [Get the free email course.](https://email-course.towardsai.net/?ref=b3ab31)*

---

*Thanks again to [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) for sponsoring the series and keeping it free!*

![Opik Banner](https://substackcdn.com/image/fetch/$s_!oSDm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26c21863-4ee6-4026-91c7-74650eb16dac_3168x792.png)

Try Opik for free here (25k spans/month free)

**If you want to monitor, evaluate and optimize your AI workflows and agents:**

---

## References

1. Confident AI. (n.d.). The Definitive Guide to Synthetic Data Generation Using LLMs. Confident AI. [https://www.confident-ai.com/blog/the-definitive-guide-to-synthetic-data-generation-using-llms](https://www.confident-ai.com/blog/the-definitive-guide-to-synthetic-data-generation-using-llms)
2. Husain, H. (n.d.). Using LLM-as-a-Judge For Evaluation: A Complete Guide. Hamel’s Blog. [https://hamel.dev/blog/posts/llm-judge/#example-llm-prompts-for-generating-user-inputs](https://hamel.dev/blog/posts/llm-judge/#example-llm-prompts-for-generating-user-inputs)
3. Zendesk. (n.d.). Building realistic multi-turn tests for AI agents. Zendesk. [https://www.zendesk.com/au/blog/zip1-building-realistic-multi-turn-tests-for-ai-agents/](https://www.zendesk.com/au/blog/zip1-building-realistic-multi-turn-tests-for-ai-agents/)
4. Evidently AI. (n.d.). How to create LLM test datasets with synthetic data. Evidently AI. [https://www.evidentlyai.com/llm-guide/llm-test-dataset-synthetic-data](https://www.evidentlyai.com/llm-guide/llm-test-dataset-synthetic-data)
5. Langfuse. (n.d.). Synthetic Dataset Generation for LLM Evaluation. Langfuse. [https://langfuse.com/guides/cookbook/example\_synthetic\_datasets](https://langfuse.com/guides/cookbook/example_synthetic_datasets)
6. DeepEval. (n.d.). Generate Synthetic Test Data for LLM Applications. DeepEval. [https://deepeval.com/guides/guides-using-synthesizer](https://deepeval.com/guides/guides-using-synthesizer)
7. Xu, C., Sun, Q., Zheng, K., Geng, X., Zhao, P., Feng, J., Tao, C., & Jiang, D. (2023). WizardLM: Empowering Large Language Models to Follow Complex Instructions. arXiv. [https://arxiv.org/abs/2304.12244](https://arxiv.org/abs/2304.12244)

---

## Images

If not otherwise stated, all images are created by the author.