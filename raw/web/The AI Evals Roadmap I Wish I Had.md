---
title: The AI Evals Roadmap I Wish I Had
source: https://www.decodingai.com/p/the-ai-evals-roadmap-i-wish-i-had
author:
- '[[Paul Iusztin]]'
published: 2026-03-24
created: 2026-04-30
description: Learn how to integrate AI evals into your app. 7 lessons on datasets,
  LLM judges, RAG metrics, and production monitoring. Stop vibe-checking your agents.
tags:
- clippings
processed: true
processed_at: '2026-04-30'
---
### From vibe checking to trusted agents in production

![](https://substackcdn.com/image/fetch/$s_!RTZT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9caacf1c-71bf-48f1-8b03-ff89346e15f8_1200x1200.png)

Welcome to the **[AI Evals & Observability series](https://www.decodingai.com/t/ai-evals-and-observability)**: A 7-part journey from shipping AI apps to systematically improving them. Made by busy people. For busy people.

AI Evals is the topic most AI engineers know they should invest in, but do not know where to start. I remember struggling with this myself.

I did not know how to properly integrate evals into my app until I understood there are three core layers: optimization during development, regression testing before merging, and production monitoring on live traffic. Once that clicked, everything else fell into place.

I did not know how to build LLM judges and evaluators that I could actually trust and use. Every guide I found either hand-waved the details or dumped a generic “helpfulness” metric and moved on. Instead, I needed evaluators grounded in my actual business requirements.

I did not know how to gather custom datasets without wasting too much time. I tried generating hundreds of synthetic test cases up front, but the real unlock came from learning how to organically grow a high-quality dataset from production data, starting small and letting the error-analysis flywheel do the heavy lifting.

The information was scattered across blog posts, talks, and vendor docs. Most of it focused on isolated techniques without showing how everything connects. I built this series as the structured, end-to-end guide I wish I had.

This 7-lesson series breaks it all down from first principles. By the end, you will know how to integrate AI evaluations that actually track and improve your product's performance. No vibe checking required.

The series follows a natural progression. You start by understanding where evals fit. Then, you build the dataset.

Next, you design and validate the evaluators. Finally, you handle specialized domains like RAG and see how it all works in production.

You can read front-to-back for the full journey. Alternatively, jump to the lesson that matches your current pain point. Each lesson stands on its own but references the others.

Without more yada, yada, here are the 7 lessons of the series:  
*(Scroll down to find more about each lesson individually.)*

1. [Integrating AI Evals Into Your AI App](https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app)
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. [Generate Synthetic Datasets for AI Evals](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals)
4. [How to Design Evaluators](https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures)
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. [RAG Evaluation: The Only 6 Metrics You Need](https://www.decodingai.com/p/rag-evaluation-6-metrics-framework)
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

*Everything is completely free, without any hidden costs, thanks to our sponsor, Opik* ↓

---

## Opik: Open-Source LLMOps Platform (Sponsored)

This **AI Evals & Observability** series is brought to you by [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul), the LLMOps open-source platform used by Uber, Etsy, Netflix, and more.

We use Opik daily across our courses and AI products. Not just for observability, but as our **end-to-end evaluation harness**, all from the same platform.

![](https://substackcdn.com/image/fetch/$s_!yCWf!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe3381bc-dda5-4624-8bb9-a961bb331c6d_1764x694.png)

Try Opik for free here (25k spans/month free)

This series teaches you how to build evals from scratch (custom datasets, LLM judges, optimization loops, and production monitoring), while Opik gives you the platform to run everything at scale.

*Here is how we use it:*

- **Custom LLM judges**: Build evaluators by defining your criteria, adding a few-shot examples, and running them across hundreds of traces automatically.
- **Run experiments, compare results**: Test different prompts, models, or parameters from your AI app side by side. Opik scores each variant with your evaluators and shows you which one wins.
- **Plug evaluators into production**: The same LLM judges you design for offline testing run on live traces too. Set up alarms when scores drop below your threshold so you catch regressions before users do.

**[Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul)** is fully **open-source** and works with custom code and with every popular AI framework or tool (*including OpenClaw*). You can also use the managed version for free (with 25K spans/month on their generous free tier):

---

*↓* *Now, let’s move back to the article.*

## Lesson 1: Integrating AI Evals Into Your AI App

To build a reliable system, you first need to know where evaluation fits into the development lifecycle.

Most teams start by *“vibe checking”* their AI app. They manually test a few inputs and eyeball whether the outputs look right. That works for the first version.

But the moment you start adding features, onboarding real users, or trying to improve existing capabilities, vibe checking collapses. This first article gives you the holistic map of where AI Evals fit, so you never feel lost again.

![](https://substackcdn.com/image/fetch/$s_!Y_0d!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e3e3f14-390a-4fcf-b449-d41b3e050fd8_1200x1075.png)

Here is what you will learn:

- The three core scenarios where evals matter: optimization during development, regression testing before merging, and production monitoring on live traffic.
- The difference between guardrails and evaluators. Confusing them leads to gaps in your system.
- The minimum viable tech stack required to start: a custom annotation tool and an LLMOps platform.

## Lesson 2: Build an AI Evals Dataset from Scratch

Once you understand where evals fit, the next step is gathering the data required to measure performance.

You cannot evaluate what you cannot measure. You cannot measure without data. Most teams either skip this step entirely or fire off a generic prompt to create 100 test cases and call it done.

This article teaches the error analysis framework. It is a practical flywheel that turns 20-50 real production traces into a growing, high-quality evals dataset.

![](https://substackcdn.com/image/fetch/$s_!HoRg!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50162cce-1890-424b-ab13-e3fa910dc94b_1200x1200.png)

Here is what you will learn:

- The error analysis flywheel: sample traces, label manually, build evaluators iteratively, perform error analysis, and create specialized evaluators.
- Why one “ *benevolent dictator”* should own labeling consistency across your team.
- How to graduate from generic to specialized evaluators as your understanding deepens.

## Lesson 3: Generate Synthetic Datasets for AI Evals

Production traces alone have limits. You need traffic to get data, and that traffic rarely covers every scenario. What about before you have users?

What about rare failure modes you have never seen in production? Yet! Synthetic data solves the cold start problem and fills coverage gaps.

![Synthetic data and production traces both feed into the evals dataset, which drives the error analysis flywheel](https://substackcdn.com/image/fetch/$s_!FVJv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc45b991a-4ed5-4d9e-8116-d6c2d8759698_1200x676.png)

Synthetic data and production traces both feed into the evals dataset, which drives the error analysis flywheel

Here is what you will learn:

- Why you should generate only inputs, not outputs, and let your real app produce the outputs.
- How to think in dimensions like persona, feature, scenario, and input modality to avoid mode collapse.
- Tester agents for simulating multi-turn conversations.
- The reverse workflow for RAG: generate questions from your knowledge base, not the other way around.

## Lesson 4: How to Design Evaluators

You have the dataset. Now you need evaluators who can actually tell you whether your app is working. This is where most teams make their biggest mistake.

They grab a generic helpfulness metric off the shelf and call it done. This article teaches you how to design evaluators grounded in your actual business requirements.

![Designing evaluators for AI applications: from code-based checks to LLM judges.](https://substackcdn.com/image/fetch/$s_!a1uV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ad91d7a-490d-4b4e-ac91-0f48e10bccc7_1456x1048.png)

Designing evaluators for AI applications: from code-based checks to LLM judges.

Here is what you will learn:

- The evaluation harness: the infrastructure that automates running evaluators across your dataset.
- When to use fast, deterministic code-based evaluators versus flexible, nuanced LLM judges.
- Common design mistakes
- Advanced designs for multi-turn conversations and agentic workflows.

## Lesson 5: How to Evaluate the Evaluator

You built an evaluator. It says everything is great. But is it?

An evaluator that validates every output is worse than no evaluator at all. It gives you false confidence. This article teaches you how to validate your evaluator against human judgment and close the gap when they disagree.

![The evaluator validation workflow](https://substackcdn.com/image/fetch/$s_!1am-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F556c0406-06a3-4c94-8bd7-8755d756cf38_1456x1048.png)

The evaluator validation workflow

Here is what you will learn:

- The iterative refinement loop: measure alignment, diagnose disagreements, adjust few-shot examples, and re-measure.
- Dealing with non-determinism: why LLM judges give different answers on the same input, and how to stabilize them.

## Lesson 6: RAG Evaluation: The Only 6 Metrics You Need

After mastering general evaluators, you can apply these principles to specific architectures like RAG.

RAG evaluation feels overwhelming because everyone proposes different metrics. But it does not have to be complicated. This article proves that there are exactly three variables in any RAG system: Question, Context, and Answer.

There are exactly six possible relationships between them. That is it. Every RAG metric maps to one of these six relationships.

![The six exhaustive relationships between the three RAG variables — Question, Context, and Answer.](https://substackcdn.com/image/fetch/$s_!gtpu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2378513-3c4f-4119-92d0-1cd651bb2be3_1456x1048.png)

The six exhaustive relationships between the three RAG variables — Question, Context, and Answer.

Here is what you will learn:

- The three RAG variables and six exhaustive relationships.
- Tier 1: Retrieval metrics. If retrieval is broken, nothing else matters.
- Tier 2: The three core RAG metrics you always need.
- Tier 3: When core metrics cannot explain the failure.

## Lesson 7: Lessons from 6 Months of Evals on a Production AI Companion

Theory and isolated metrics are useful. But the ultimate test is running this entire system on live user traffic.

The first six articles teach you how to build the system. This final article shows you what it looks like after six months of running it in production.

Written as a guest post by [Alejandro Aboy](https://open.substack.com/users/22949723-alejandro-aboy?utm_source=mentions), Senior Data Engineer at Workpath, it shares the real lessons. We cover what worked, what failed, and what they wish they had known from the start.

![](https://substackcdn.com/image/fetch/$s_!0pKO!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6ea9e7d-8f97-45ec-b767-391bab951a08_3680x4016.png)

Here is what you will learn:

- The three observability problems most teams hit: falling for generic metrics, skipping manual annotation, and not treating AI agents as data products.
- How to use Opik’s architecture, including traces, spans, threads, and prompt versioning, for production monitoring and evals.
- How to reverse-engineer evaluation criteria from real traces instead of guessing upfront.

## How to Take the Course?

After completing these seven articles, you will have the complete mental model for AI Evals. You will understand everything from strategy to production.

As the course is 100% free, with no hidden costs or registration required, taking it is a no-brainer.

Each lesson is a free article hosted on the [Decoding AI Magazine](https://www.decodingai.com/t/ai-evals-and-observability).

Just open each lesson in the order provided by us, and you are good to go:

1. [Integrating AI Evals Into Your AI App](https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app)
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. [Generate Synthetic Datasets for AI Evals](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals)
4. [How to Design Evaluators](https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures)
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. [RAG Evaluation: The Only 6 Metrics You Need](https://www.decodingai.com/p/rag-evaluation-6-metrics-framework)
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

Each lesson will guide you through the required steps.

Enjoy!

## Now What?

After completing these lessons, if you want the information to stick, you have to put everything into practice by building a cool project!

I am sorry to say there is no other way to make learning worthwhile. Pick one problem and get your hands dirty with a project.

**💡** ***Want to share your work on my socials with my 140k+ audience?** If you build a project you are excited about, I will be too. Trust me! I love seeing people build cool stuff. To share it, you can contact me [here](https://www.pauliusztin.ai/contact).*

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

*Thanks again to [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) for sponsoring the series and keeping it free!*

![Opik Banner](https://substackcdn.com/image/fetch/$s_!oSDm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26c21863-4ee6-4026-91c7-74650eb16dac_3168x792.png)

Try Opik for free here (25k spans/month free)

**If you want to monitor, evaluate and optimize your AI workflows and agents:**

---

## Images

If not otherwise stated, all images are created by the author.