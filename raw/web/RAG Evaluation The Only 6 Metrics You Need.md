---
title: 'RAG Evaluation: The Only 6 Metrics You Need'
source: https://www.decodingai.com/p/rag-evaluation-6-metrics-framework
author:
- '[[Paul Iusztin]]'
published: 2026-03-17
created: 2026-04-30
description: Learn the 6 exhaustive RAG evaluation metrics derived from 3 variables.
  A tiered framework for diagnosing retrieval and generation failures in production
  AI.
tags:
- clippings
processed: true
processed_at: '2026-05-01'
---
### A complete guide for evaluating your retrieval-augmented generation systems.

*Welcome to the **[AI Evals & Observability series](https://www.decodingai.com/t/ai-evals-and-observability)**: A 7-part journey from shipping AI apps to systematically improving them. Made by busy people. For busy people.*

🧐 Everyone says you need AI evals. Few explain how to actually build them and answer questions such as…

How do we avoid creating evals that waste our time and resources? How do we build datasets and design evaluators that matter? How do we adapt them for RAG?...and most importantly, how do we stop “vibe checking” and leverage evals to actually track and optimize our app?

*This 7-article series breaks it all down from first principles:*

1. [Integrating AI Evals Into Your AI App](https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app)
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. [Generate Synthetic Datasets for AI Evals](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals)
4. [How to Design Evaluators](https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures)
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. ***RAG Evaluation: The Only 6 Metrics You Need** ← You are here*
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

By the end, you’ll know how to integrate AI evals that actually track and improve the performance of your AI product. No vibe checking required!

*Let’s get started.*

---

In our previous article, we covered how to validate your AI judges. We measured agreement with human judgment and iterated until alignment was high. Thus, you can now deploy with confidence.

However, a specialized challenge exists that general-purpose grading tools do not fully address. Evaluating RAG systems introduces a third variable, specifically the retrieved context. With this new element comes a distinct set of failure modes requiring their own metrics.

I am currently building a financial personal assistant at the stealth AI startup I work for. The application runs heavily on RAG. It pulls financial data from Postgres and integrates with external services such as email, Customer Relationship Management (CRM) tools, and cloud drives.

When it came time to evaluate the system, building the dataset proved harder than choosing metrics. Fortunately, we had a domain expert on the team who manually tested the application from the start. Therefore, we translated all of that Quality Assurance (QA) work into our AI evals collection using the error analysis workflow from [Article 2](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis).

Evaluating RAG systems introduces a unique difficulty. Each data sample required the correct context to be loaded into the database. We solved this by coupling every test case with a Postgres SQL export.

This file contained documents, chunks, embeddings, and metadata. We injected it directly into the storage system. This effectively created a cache that bypassed the ingestion pipeline during evals.

Once the data was in place, implementing the core RAG metrics became straightforward. We used tools like [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) and foundational models like Gemini Pro as the LLM judge. We had the context, the query, and the answer, which is everything you need.

What surprised me was that not every capability needed this level of dissection. For our report generation feature, we expect an exact format with specific values pulled from the storage. Checking the final document against a ground truth served as a better proxy than tracing every retrieval step.

*Sometimes assessing the destination matters more than checking the route.*

RAG evaluation feels needlessly complex. Vendors have an incentive to make it difficult. Every framework ships with many metrics and a dashboard, making you feel like you need a PhD to know if your system works.

Underneath all the complexity, **RAG systems possess exactly three core components**. These are the Question (Q), the retrieved Context (C), and the generated Answer (A). Furthermore, with these elements, there are **exactly six possible relationships** between them. When your RAG system fails, it breaks along one of these six relationships every single time.

The beauty of this framework is its exhaustive nature. There are no hidden variables.

You do not always need to evaluate all six individually. For core conversational features, you need the primary metrics because there are many silent failure modes. However, for structured output tasks, an end-to-end check against expected results can be sufficient.

![The six exhaustive relationships between the three RAG variables — Question, Context, and Answer.](https://substackcdn.com/image/fetch/$s_!gtpu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2378513-3c4f-4119-92d0-1cd651bb2be3_1456x1048.png)

Image 1: The six exhaustive relationships between the three RAG variables — Question, Context, and Answer.

**Here is what you will learn in this article:**

- The only six relationships that exist in a RAG system.
- How to evaluate your retrieval step before looking at generation.
- The three core metrics every RAG application needs.
- Advanced metrics for diagnosing subtle hallucinations.
- How to match evaluation frequency and strictness to your domain.
- How to collect and prepare the data your evaluators need.


---


---

*↓* *Now, let’s move back to the article.*

## The Only 6 RAG Evaluation Metrics That Can Exist

Jason Liu properly articulated the framework I am about to walk you through [\[1\]](https://jxnl.co/writing/2025/05/19/there-are-only-6-rag-evals/). Since I wrote the [LLM Engineer’s Handbook](https://www.amazon.com/LLM-Engineers-Handbook-engineering-production/dp/1836200072/) two years ago, I have watched many RAG evaluation tools emerge. They overcomplicate everything with proprietary metric suites.

Through all of that, I already internalized that only three variables matter in any RAG system. Testing the combinations between them is the only thing you should actually do. Jason Liu gave a clean, formal articulation to what I had in mind.

He nailed the structure and deserves the recognition for that.

Every RAG system has three variables. We define `Q` as the user’s question, `C` as the retrieved context, and `A` representing the generated answer. Thus, we use the notation `X|Y` to mean the quality of `X` given `Y`.

There are **exactly six relationships** between these variables:

1. `C|Q` (Context Relevance) asks if the retrieved context addresses the question. This measures your retriever, because if it pulls irrelevant passages, the generator cannot fix the issue.
2. `A|C` (Faithfulness) checks if the answer sticks to what is in the context. This measures your generator to see if the model hallucinated or stayed grounded in the documents.
3. `A|Q` (Answer Relevance) verifies if the response actually addresses the prompt. This is the end-to-end user experience metric. Even if the context is good and the reply is faithful, it must help the person asking.
4. `C|A` (Context Support) ensures the retrieved text contains everything needed to support every claim in the answer. This checks if the provided information was sufficient.
5. `Q|C` (Question Answerability) evaluates if the prompt can even be resolved with this context. This determines whether the system should attempt to reply at all.
6. `Q|A` (Self-Containment) asks if someone can infer the original question from reading the answer alone. This measures whether the output provides enough background to stand on its own.

This framework is exhaustive. Three components produce exactly six conditional relationships. There are no hidden factors.

Therefore, when your RAG system fails, one of these six metrics is broken.

![The complete grid of six RAG relationships — each mapped to the component it diagnoses.](https://substackcdn.com/image/fetch/$s_!j-9F!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8214a72c-1511-4a4d-9806-7914a70aba3d_1200x630.png)

Image 2: The complete grid of six RAG relationships — each mapped to the component it diagnoses (Retriever, Generator, or End-to-End).

Not all six relationships matter equally in every context. We organize them into three tiers. Let us start with retrieval metrics as the prerequisite foundation.

## Tier 1: If Retrieval Is Broken, Nothing Else Matters

RAG is first and foremost a retrieval problem. If the search mechanism does not retrieve the right documents, nothing downstream can save you. The generator will either hallucinate or produce irrelevant answers based on whatever junk it received.

Before evaluating any of the six RAG relationships, you need to know if your retriever even works. You can use classic information retrieval metrics that measure how well you find relevant documents before generation starts. They are fast to compute and do not require LLM judges.

Hence, these measurements give quick feedback for tuning your retriever.

You must establish ground-truth labels to compute these metrics. For each query, you must know which text blocks are actually relevant. You can build this dataset using the reverse workflow presented in depth in [Article 3](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals).

As a quick recap, you start from your knowledge base of document chunks. Then, based on a set of closely related chunks, you generate realistic questions that can only be answered using that unique set of chunks.

Because the prompt derives from the source material, you know exactly which segment should be retrieved. This gives you a perfectly aligned ground-truth triplet: (question, answer, context). Thus, it becomes straightforward to check whether your search tool actually surfaces the right information.

There are four main metrics. `Precision@K` measures the fraction of the top K retrieved chunks that are actually relevant. If your retriever returns 5 chunks but only 2 are useful, your precision is 40%. `Recall@K` asks: of all the relevant chunks that exist in your entire corpus, how many did your retriever actually find in the top K? If the database has 4 chunks that could answer the question but you only retrieved 2 of them, your recall is 50%.

In addition, Mean Average Precision (`MAP@K`) averages precision across multiple queries, rewarding retrievers that consistently rank relevant chunks early. It works by computing precision at every position where a relevant item appears, then averaging those values. Here is a step-by-step example where the truly relevant items are A and C:

![table](https://substackcdn.com/image/fetch/$s_!aVBN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d2e729b-b697-4ddb-b112-d86baa24b08e_1920x415.png)

Average Precision for this query = (1.0 + 0.66) / 2 = 0.83. We only average the precision values at positions where a relevant item appeared (ranks 1 and 3). `MAP@K` then takes this score and averages it across all your queries.

Finally, Mean Reciprocal Rank (`MRR@K`) focuses on the position of the first relevant match. If the first relevant chunk appears at position 3, the reciprocal rank is 1/3; if it appears at position 1, it is 1/1. Higher is better.

Use these for daily development. These indicators are great for tuning embeddings and chunk sizes, while also being perfect for A/B testing retrieval strategies. No LLM is needed, making the process cheap and fast.

These numbers tell you if the search phase works, as illustrated in Image 3. The six RAG relationships tell you if the whole system functions properly, meaning you need both.

![Retrieval metrics applied to a financial assistant query.](https://substackcdn.com/image/fetch/$s_!EMDz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F32e356fc-efd5-420e-a2d4-5025295e9996_1200x630.png)

Image 3: Retrieval metrics applied to a financial assistant query — checking whether the retriever surfaces the right chunks.

With the retrieval confirmed working, you can evaluate the generation step. Let us look at the three core RAG relationships that every system needs.

## Tier 2: The Three RAG Metrics You Always Need

These three metrics directly assess how well your RAG system functions. Most evaluation frameworks prioritize these specific measurements. They map to the three most critical of the six relationships.

First, we have **Context Relevance** (`C|Q`). This checks if the retrieved text actually addresses the prompt’s information needs. Therefore, it measures your search component similar to the metrics from Tier 1, but only looking at the dynamics between the context and question, without any ground truth.

Suppose we have a query about recent payouts from Q4. A good example is when the retrieved data contains the user’s dividend payment records from Q4, which passes. On the other side, a bad scenario occurs when the system returns general information about how these distributions work and their tax implications.

This represents the most common RAG failure mode. In our financial assistant, this often happened when the search tool pulled educational content instead of actual account data.

Second, we have **Faithfulness** (`A|C`). This asks if the reply restricts itself to claims that can be verified from the provided text. Hence, it measures whether your generator hallucinates or not.

In our use case, a good example is when the source contains a CRM record showing a client meeting scheduled for portfolio rebalancing. If the response states exactly that, it passes. A bad example happens when the model adds hallucinated agenda items like tax-loss harvesting strategies, resulting in a failure.

Third, we have **Answer Relevance** (`A|Q`). This checks if the output directly addresses the specific query from the prompt. This serves as the end-to-end user experience metric.

A good example is when a person asks how much their investments grew last month. The reply provides the specific percentage change and absolute dollar amount. A bad scenario is when the text discusses general market performance without mentioning the actual account.

We measure all three metrics using LLM judges as designed in [Article 4](https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures) and validated in [Article 5](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge).

![The three core RAG metrics illustrated with financial assistant examples.](https://substackcdn.com/image/fetch/$s_!gNmS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13d9fabd-661e-47ec-a8fc-1afbdcead725_1200x630.png)

Image 4: The three core RAG metrics illustrated with financial assistant examples — each measures a critical relationship between Question, Context, and Answer.

These three metrics cover the most common failure modes. For specific domains and failure cases, we have to dig deeper into the next 3 metrics.

## Tier 3: When the Core Metrics Can’t Explain the Failure

The last three metrics provide deeper diagnostic insights usually required in sensitive domains or use cases.

First, we have **Context Support** (`C|A`). This checks if the retrieved context contains all the information needed to fully back every claim in the response. While this sounds similar to Faithfulness (`A|C`), the direction is different. Faithfulness asks: *“did the answer deviate from the context?”*, where you look at the answer and check if it introduced claims that aren’t there. Context Support asks: *“was the context sufficient to support the answer?”*, where you look at the context and check if it actually contains everything the answer needs.

Here is a concrete example. Suppose the answer says your total Q4 dividend income was 2,340 *across* 5 *holdings*, *with* *the* *largest* *payout* *from* *MSFT* *at* 890. Now look at the context: it only contains the total dividend amount of $2,340. The per-holding breakdown is nowhere in the retrieved documents. The context was insufficient. It had the total but not the details. The LLM produced a plausible breakdown, but the context could not support it. This is low-context support.

Second, we have **Question Answerability** (`Q|C`). This asks if the user's question can even be resolved with the given information.

Suppose the user asks about crypto portfolio performance, but the retrieved documents only contain equity data. This makes the request unanswerable. The system should refuse rather than guess. This metric is important when you want to validate that your agent answers with “I don’t know” instead of confidently hallucinating an answer due to insufficient context.

In our financial assistant, this was important because some queries can only be resolved if the agent has permissions to access the right external tool first.

Third, we have **Self-Containment** (`Q|A`). This checks if someone can infer the original prompt from the reply alone.

A response stating your portfolio’s return is 12.4% stands alone. A reply stating just 12.4% does not. Prioritize this metric when outputs are forwarded via email, logged in CRM notes, or read without the original conversation.

![Faithfulness vs Context Support — two types of hallucination detection.](https://substackcdn.com/image/fetch/$s_!TV-5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef6c62c8-1af1-4dce-b455-48ed7fea0797_1200x630.png)

Image 5: Faithfulness catches obvious hallucinations where the answer deviates from context. Context Support catches the subtler case where the context was insufficient, and the LLM silently filled the gaps.

You now know what to measure at each tier. Two questions remain. How often should you run each one? Which metrics deserve the most attention for your specific domain?

## Matching Frequency and Strictness to Your Domain

Each tier maps to a different running frequency depending on how fast and cheap you can run the evaluations. It also depends on their overall impact on the system.

**Start with Tier 1** on a daily basis. Implement fast retrieval metrics for everyday development and to tune your retrieval component. These are the cheapest to execute as they do not require LLM judges.

Furthermore, they provide quick feedback cycles. Use them for the improvement flywheel with synthetic data from day zero, focusing on these basic indicators before moving to more complex approaches.

**Move to Tier 2** on a weekly basis. Implement the three primary RAG connections. These core metrics directly assess how well your system functions.

Use LLM-based grading for a more nuanced assessment of these interactions.

**Incorporate Tier 3** on a monthly basis. Introduce advanced metrics when you need deeper insights. Run a full evaluation to identify prompts that the application should not be answering.

![The tiered evaluation cadence.](https://substackcdn.com/image/fetch/$s_!P9iE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7db8998-edea-4843-96e6-f2767bb2d9a9_1200x630.png)

Image 6: The tiered evaluation cadence — cheapest and fastest at the top, deepest and most expensive at the bottom.

Here, we focused only on RAG-related measurements. However, this actually applies to any type of AI evals layer. You could implement Tier 1 checks in your CI/CD pipeline to execute on each commit.

You can trigger Tier 2 evaluations manually before merging your code from your feature branch. Finally, manually run Tier 3 metrics before major releases and strategic decisions.

There is another dimension to consider when choosing metrics for your use case, which is the good old domain.

**Different domains require emphasis on distinct indicators**. What matters most depends on the severity of the use case.

**High-severity domains** include finance, medical, and legal applications. In these fields, Faithfulness (`A|C`) and Context Support (`C|A`) are non-negotiable because every claim must be traceable. Answerability (`Q|C`) is also critical, meaning the application must refuse rather than guess.

Thus, you want precision over recall, which is the exact profile we use for our financial assistant.

**Medium severity domains** include customer support and technical documents. Answer Relevance (`A|Q`) leads here, as the output must be helpful and correct. Answerability (`Q|C`) helps you know when to hand off to a human, and you generally want recall over precision in retrieval.

**Low-severity domains** include research, writing, and content generation, where synthesis and creative reframing are expected. Context Relevance (`C|Q`) and Answer Relevance (`A|Q`) is primary, while Faithfulness (`A|C`) thresholds remain lower. The generator is supposed to add value beyond the raw text.

Therefore, you want high recall in the search phase to cast a wide net across sources.

You know what to measure, when, and what to prioritize. None of this works without the right data and infrastructure. Let us explore how to build the evaluation harness.

## Building the RAG Evaluation Harness

RAG evaluation requires inputs, outputs, and the retrieved context. You need the full triplet.

The most common blind spot involves treating RAG testing like any other LLM assessment. Teams measure the final reply’s quality, but never capture what background data the generator actually worked with. Without that information, half the metrics in this article are impossible to compute.

Next, you should ground your RAG dataset in real human judgment. In our financial assistant, we had a domain specialist on the team who manually QA’d the application from the start. They ran queries, checked whether the right data was retrieved, and verified that the replies made sense.

We translated all of that manual work into our AI evals collection using the error analysis workflow from [Article 2](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis).

Also, building RAG datasets introduces a unique difficulty. Each test case needs the right documents, chunks, and embeddings available in the database. Otherwise, the search tool has nothing to work with.

Running the full ingestion pipeline for every evaluation run is slow and introduces variability.

We solved this by coupling each data point with a Postgres SQL export containing the relevant documents, chunks, embeddings, and metadata. We loaded this file directly into the storage system for each test, effectively creating a context cache. This made the process fast and reproducible.

We inject the records, run the query, evaluate the trace, reset the environment, and move to the next item. Image 7 illustrates these data preparation paths.

![Two paths for building your RAG evaluation dataset.](https://substackcdn.com/image/fetch/$s_!1KvQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f9c048e-214e-481e-b46b-4ca2c6d9a397_1200x630.png)

Image 7: Two paths for building your RAG evaluation dataset — manual expert QA (Article 2) and synthetic reverse workflow (Article 3) — both requiring proper context preparation.

If you do not have enough production data or expert QA samples, you can create synthetic RAG evaluation sets. Use the reverse workflow from [Article 3](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals) by starting from your knowledge base. Use an LLM to extract key facts from specific passages.

Then, formulate realistic user questions that can only be answered using that exact text block.

Because the prompt derives directly from the source material, the input, expected retrieval context, and expected reply are perfectly aligned by construction. This gives you a complete ground-truth triplet. Furthermore, this technique is especially powerful for bootstrapping coverage across your entire document corpus.

Include unanswerable queries in your collection. Do not only formulate prompts that the application should resolve correctly. Instead, create scenarios where the context deliberately lacks the information needed, forcing the agent to refuse or say it does not know.

Without these negative examples, your testing suite is one-sided. Your evals will optimize for always attempting a reply, whereas adding them directly exercises the Answerability metric from Tier 3.

Next, if your RAG architecture integrates with external services, the retrieval path is not just a vector database search. Your agent needs to decide which tool to call first. Should it query Postgres, search the CRM, or check the user’s email?

The best retrieval metrics will not help if your model invoked the wrong data source entirely.

In our financial assistant, this was critical. A query about a client meeting should hit the CRM, not the transaction database. Therefore, we added code-based checks for tool selection alongside our RAG metrics.

Another important trick is to run separate graders per RAG dimension. Do not ask one LLM to evaluate context relevance, faithfulness, and answer relevance in a single prompt. Isolated checks with dimension-specific rubrics produce more consistent results than a unified evaluation.

Ultimately, you need to log specific data for every trace using tools such as [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul). Record retrieved chunks to see what the generator had access to. If faithfulness fails, check whether the reply used information that was not provided. Track metadata such as document IDs and scores, because when context relevance fails, you need to know which items ranked highest. This represents the same observability infrastructure from [Article 1](https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app).

## Next Steps

RAG evaluation is not complex. It is just three variables and six relationships. When your RAG system fails, one of these specific links is broken.

Fix that exact issue and ignore the complexity theater.

Start with Tier 1 retrieval checks as daily prerequisites. Add Tier 2 primary indicators weekly. Extend to Tier 3 when specific failure modes demand it.

Ultimately, match your evaluation priorities to your domain’s risk profile.

Next time you see a vendor dashboard with dozens of RAG metrics, map each one back to the six relationships. If an indicator does not clearly measure one of the core links, it is noise. Drop it and focus on what actually diagnoses failures.

Next up is the [final piece in the series](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability). We will explore real-world lessons from months of running evals on a production AI companion. We will discuss what worked, what failed, and what the team would do differently.

Also, remember that this article is part of a **[7-piece series on AI Evals & Observability](https://www.decodingai.com/t/ai-evals-and-observability)**. **Here’s what’s ahead:**

1. [Integrating AI Evals Into Your AI App](https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app)
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. [Generate Synthetic Datasets for AI Evals](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals)
4. [How to Design Evaluators](https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures)
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. ***RAG Evaluation: The Only 6 Metrics You Need** ← You just finished this one*
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

See you next Tuesday.

[Paul Iusztin](https://www.pauliusztin.ai/)

---

*What’s your opinion? Do you agree, disagree, or is there something I missed?*

---

*Enjoyed the article? The most sincere compliment is to share our work.*

---

## Go Deeper

**Go from zero to production-grade AI agents** with the [Agentic AI Engineering self-paced course](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering). Built in partnership with [Towards AI](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering).

Across **34 lessons** (articles, videos, and a lot of code), you’ll design, build, evaluate, and deploy production-grade AI agents end to end. By the final lesson, you’ll have **built a multi-agent system** and a **capstone project** where you apply everything you've learned on your own.

*Three portfolio projects and a certificate to showcase in interviews. Plus a Discord community where you have direct access to other industry experts and me.*

Rated 4.9/5 ⭐️ by 300+ students — *“Every AI Engineer needs a course like this.”*

*Not ready to commit?* We also prepared a free 6-day email course to reveal the ***6 critical mistakes that silently destroy agentic systems.** [Get the free email course.](https://email-course.towardsai.net/?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering)*

---

![Opik Banner](https://substackcdn.com/image/fetch/$s_!yeD8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdeaa636a-b1a6-429b-83d8-080bc218e596_1200x400.png)

Try Opik for free here (25k spans/month free)

**If you want to monitor, evaluate and optimize your AI workflows and agents:**

---

## References

1. Liu, J. (2025, May 19). There Are Only 6 RAG Evals. jxnl.co. [https://jxnl.co/writing/2025/05/19/there-are-only-6-rag-evals/](https://jxnl.co/writing/2025/05/19/there-are-only-6-rag-evals/)
2. Grace, M., Hadfield, J., Olivares, R., & De Jonghe, J. (2026, January 09). Demystifying Evals for AI Agents. Anthropic Engineering Blog. [https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

---

## Images

If not otherwise stated, all images are created by the author.