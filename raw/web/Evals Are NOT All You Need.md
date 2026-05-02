---
title: Evals Are NOT All You Need
source: https://www.oreilly.com/radar/evals-are-not-all-you-need/
author:
- '[[Aishwarya Naresh Reganti]]'
- '[[Kiriti Badam]]'
published: 2026-01-28
created: 2026-04-30
description: Build a continuous improvement flywheel to measure and improve AI product
  quality
tags:
- clippings
processed: true
processed_at: '2026-04-30'
---
Evals are having their moment.

It’s become one of the most talked-about concepts in AI product development. People argue about it for hours, write thread after thread, and treat it as the answer to every quality problem. This is a dramatic shift from 2024 or even early 2025, when the term was barely known. Now everyone knows evaluation matters. Everyone wants to “ **build good evals**.“

But now they’re lost. There’s so much noise coming from all directions, with everyone using the term for completely different things. Some (might we say, most) people think “evals” means prompting AI models to judge other AI models, building a dashboard of them that will magically solve their quality problems. They don’t understand that what they actually need is a process, one that’s far more nuanced and comprehensive than spinning up a few automated graders.

We’ve started to really hate the term. It’s bringing more confusion than clarity. Evals are only important in the context of product quality, and product quality is a process. It’s the ongoing discipline of deciding what “good” means for your product, measuring it in the right ways at the right times, learning where it breaks in the real world, and repeatedly closing the loop with fixes that stick.

We recently talked about this on [*Lenny’s Podcast*](https://youtu.be/z7T1pCxgvlA?si=wpFGuurnmdNpNUOc&t=2001), and so many people reached out saying they related to the confusion, that they’d been struggling with the same questions. That’s why we’re writing this post.

Here’s what this article is going to do: explain the entire system you need to build for AI product quality, without using the word “evals.” (We’ll try our best.:p)

The status quo for shipping any reliable product requires ensuring three things:

- **Offline quality**: A way to estimate how it behaves while you’re still developing it, before any customer sees it
- **Online quality**: Signals for how it’s actually performing once real customers are using it
- **Continuous improvement**: A reliable feedback loop that lets you find problems, fix them, and get better over time

This article is about how to ensure these three things in the context of AI products: why AI is different from traditional software, and what you need to build instead.

## Why Traditional Testing Breaks

In traditional software, testing handles all three things we just described.

Think about booking a hotel on Booking.com. You select your dates from a calendar. You pick a city from a dropdown. You filter by price range, star rating, and amenities. At every step, you’re clicking on predefined options. The system knows exactly what inputs to expect, and the engineers can anticipate almost every path you might take. If you click the ”search” button with valid dates and a valid city, the system returns hotels. The behavior is predictable.

This predictability means testing covers everything:

- **Offline quality?** You write unit tests and integration tests before launch to verify behavior.
- **Online quality?** You monitor production for errors and exceptions. When something breaks, you get a stack trace that tells you exactly what went wrong.
- **Continuous improvement?** It’s almost automatic. You write a new test, fix the bug, and ship. When you fix something, it stays fixed. Find issue, fix issue, move on.

Now imagine the same task, but through a chat interface: ”I need a pet-friendly hotel in Austin for next weekend, under $200, close to downtown but not too noisy.”

The problem becomes much more complex. And the traditional testing approach falls apart.

The way users interact with the system can’t be anticipated upfront. There’s no dropdown constraining what they type. They can phrase their request however they want, include context you didn’t expect, or ask for things your system was never designed to handle. You can’t write test cases for inputs you can’t predict.

And because there’s an AI model at the center of this, the outputs are nondeterministic. The model is probabilistic. You can’t assert that a specific input will always produce a specific output. There’s no single ”correct answer” to check against.

On top of that, the process itself is a black box. With traditional software, you can trace exactly why an output was produced. You wrote the code; you know the logic. With an LLM, you can’t. You feed in a prompt, something happens inside the model, and you get a response. If it’s wrong, you don’t get a stack trace. You get a confident-sounding answer that might be subtly or completely incorrect.

This is the core challenge: AI products have a much larger surface area of user input that you can’t predict upfront, processed by a nondeterministic system that can produce outputs you never anticipated, through a process you can’t fully inspect***.***

The traditional feedback loop breaks down. You can’t estimate behavior during development because you can’t anticipate all the inputs. You can’t easily catch issues in production because there’s no clear error signal, just a response that might be wrong. And you can’t reliably improve because the thing you fix might not stay fixed when the input changes slightly.

Whatever you tested before launch was based on behavior you anticipated. And that anticipated behavior can’t be guaranteed once real users arrive.

This is why we need a different approach to determining quality for AI products. The testing paradigm that works for clicking through Booking.com doesn’t transfer to chatting with an AI. You need something different.

## Model Versus Product

So we’ve established that AI products are fundamentally harder to test than traditional software. The inputs are unpredictable, the outputs are nondeterministic, and the process is opaque. This is why we need dedicated approaches to measuring quality.

But there’s another layer of complexity that causes confusion: the distinction between assessing the model and assessing the product.

Foundation AI models are judged for quality by the companies that build them. OpenAI, Anthropic, and Google all run their models through extensive testing before release. They measure how well the model performs on coding tasks, reasoning problems, factual questions, and dozens of other capabilities. They give the model a set of inputs, check whether it produces expected outputs or takes expected actions, and use that to assess quality.

This is where benchmarks come from. You’ve probably seen them: LMArena, MMLU scores, HumanEval results. Model providers publish these numbers to show how their model stacks up. “We’re #1 on this benchmark” is a common marketing claim.

These scores represent real testing. The model was given specific tasks and its performance was measured. But here’s the thing: These scores have limited use for people building products. Model companies are racing toward capability parity. The gaps between top models are shrinking. What you actually need to know is whether the model will work for your specific product and produce good quality responses in your context.

There are two distinct layers here:

**The model layer**. This is the foundation model itself: GPT, Claude, Gemini, or whatever you’re building on. It has general capabilities that have been tested by its creators. It can reason, write code, answer questions, follow instructions. The benchmarks measure these general capabilities.

**The product layer**. This is your application, the thing you’re actually shipping to users. A customer support bot. A booking assistant. Your product is built on top of a foundation model, but it’s not the same thing. It has specific requirements, specific users, and specific definitions of success. It integrates with your tools, operates under your constraints, and handles use cases the benchmark creators never anticipated. Your product lives in a custom ecosystem that no model provider could possibly simulate.

Benchmark scores tell you what a model can do in general. They don’t tell you whether it works for your product.

The model layer has already been assessed by someone else. Your job is to assess the product layer: against your specific requirements, your specific users, your specific definition of success.

![Model Evaluation](https://www.oreilly.com/radar/wp-content/uploads/sites/3/2026/01/Evaluation.png)

Model Evaluation

We bring this up because so many people obsess over model performance benchmarks. They spend weeks comparing leaderboards, trying to find the “best” model, and end up in “model selection hell.” The truth is, you need to pick something reasonable and build your own quality assessment framework. You cannot heavily rely on provider benchmarks to tell you what works for your product.

## What You Measure Against

So you need to assess your product’s quality. Against what, exactly?

Three things work together:

**Reference examples**: Real inputs paired with known-good outputs. If a user asks, “What’s your return policy?“ what should the system say? You need concrete examples of questions and acceptable answers. These become your ground truth, the standard you’re measuring against.

Start with 10–50 high-quality examples that cover your most important scenarios. A small set of carefully chosen examples beats a large set of sloppy ones. You can expand later as you learn what actually matters in practice.

This is really just product intuition. You’re thinking: What does my product support? How would users interact with it? What user personas exist? How should my ideal product behave? You’re designing the experience and gathering a reference for what “good“ looks like.

**Metrics**: Once you have reference examples, you need to think about how to measure quality. What dimensions matter? This is also product intuition. These dimensions are your metrics. Usually, if you’ve built out your reference example dataset very well, they should give you an overview of what metrics to look into based on the behavior that you want to see. Metrics essentially are dimensions that you want to focus on to assess quality. An example of a dimension could be, say, helpfulness.

**Rubrics**: What does “good“ actually mean for each metric? This is a step that often gets skipped. It’s common to say “we’re measuring helpfulness“ without defining what helpful means in context. Here’s the thing: Helpfulness for a customer support bot is different from helpfulness for a legal assistant. A helpful support bot should be concise, solve the problem quickly, and escalate at the right time. A helpful legal assistant should be thorough and explain all the nuances. A rubric makes this explicit. It’s the instructions that your metric hinges on. You need this documented so everyone knows what they’re actually measuring. Sometimes if metrics are more objective in nature—for instance, “Was a correct JSON retrieved?“ or “Was a particular tool called done correctly?”—you don’t need rubrics at all. Subjective metrics are the ones that you generally need rubrics for, so keep that in mind.

For example, a customer support bot might define helpfulness like this:

- **Excellent**: Resolves the issue completely in one response, uses clear language, offers next steps if relevant
- **Adequate**: Answers the question but requires follow-up or includes unnecessary information
- **Poor**: Misunderstands the question, gives irrelevant information, or fails to address the core issue

To summarize, you have expected behavior from the user, expected behavior from the system (your reference examples), metrics (the dimensions you’re assessing), and rubrics (how you define those metrics). A metric like “helpfulness“ is just a word and means nothing unless it’s grounded by the rubric. All of this gets documented, which helps you start judging offline quality before you ever go into production.

## How You Measure

You’ve defined what you’re measuring against. Now, how do you actually measure it?

There are three approaches, and all of them have their place.

![Three approaches to measuring](https://www.oreilly.com/radar/wp-content/uploads/sites/3/2026/01/image-7.png)

Three approaches to measuring

**Code-based checks**: Deterministic rules that can be verified programmatically. Did the response include a required disclaimer? Is it under the word limit? Did it return valid JSON? Did it refuse to answer when it should have? These checks are simple, fast, cheap, and reliable. They won’t catch everything, but they catch the straightforward stuff. You should always start here.

**LLM as judge**: Using one model to grade another. You provide a rubric and ask the model to score responses. This scales better than human review and can assess subjective qualities like tone or helpfulness.

But there’s a risk. An LLM judge that hasn’t been calibrated against human judgment can lead you astray. It might consistently rate things wrong. It might have blind spots that match the blind spots of the model you’re grading. If your judge doesn’t agree with humans on what “good“ looks like, you’re optimizing for the wrong thing. Calibration against human judgment is super critical.

**Human review**: The gold standard. Humans assess quality directly, either through expert review or user feedback. It’s slow and expensive and doesn’t scale. But it’s necessary. You need human judgment to calibrate your LLM judges, to catch things automated checks miss, and to make final calls on high-stakes decisions.

The right approach: Start with code-based checks for everything you can automate. Add LLM judges carefully, with extensive calibration. Reserve human review for where it matters most.

One important note: When you’re first building your reference examples, have humans do the grading. Don’t jump straight to LLM judges. LLM judges are notorious for being miscalibrated, and you need a human baseline to calibrate against. Get humans to judge first, understand what “good“ looks like from their perspective, and then use that to calibrate your automated judges. Calibrating LLM judges is a whole other blog post. We won’t dig into it here. But this is a nice [guide](https://arize.com/docs/phoenix/cookbook/prompt-engineering/llm-as-a-judge-prompt-optimization) from Arize to help you get started.

## Production Surprises You (and Humbles You)

Let’s say you’re building a customer support bot. You’ve built your reference dataset with 50 (or 100 or 200—whatever that number is, this still applies) example conversations. You’ve defined metrics for helpfulness, accuracy, and appropriate escalation. You’ve set up code checks for response length and required disclaimers, calibrated an LLM judge against human ratings, and run human review on the tricky cases. Your offline quality looks solid. You ship. Then real users show up. Here are just some examples of emerging behaviors you might see. The real world is a lot more nuanced.

- **Your reference examples don’t cover what users actually ask.** You anticipated questions about return policies, shipping times, and order status. But users ask about things you didn’t include: “Can I return this if my dog chewed on the box?“ or “My package says delivered but I never got it, and also I’m moving next week.“ They combine multiple issues in one message. They reference previous conversations. They phrase things in ways your reference examples never captured.
- **Users find scenarios you missed.** Maybe your bot handles refund requests well but struggles when users ask about partial refunds on bundled items. Maybe it works fine in English but breaks when users mix in Spanish. No matter how thorough your prelaunch testing, real users will find gaps.
- **User behavior shifts over time.** The questions you get in month one don’t look like the questions you get in month six. Users learn what the bot can and can’t do. They develop workarounds. They find new use cases. Your reference examples were a snapshot of expected behavior, but expected behavior changes.

And then there’s scale. If you’re handling 5,000 conversations a day with a 95% success rate, that’s still 250 failures every day. You can’t manually review everything.

This is the gap between offline and online quality. Your offline assessment gave you confidence to ship. It told you the system worked on the examples you anticipated. But online quality is about what happens with real users, real scale, and real unpredictability. The work of figuring out what’s actually breaking and fixing it starts the moment real users arrive.

This is where you realize a few things (a.k.a. lessons):

**Lesson 1: Production will surprise you regardless of your best efforts.** You can build metrics and measure them before deployment, but it’s almost impossible to think of all cases. You’re bound to be surprised in production.

**Lesson 2: Your metrics might need updates. They’re not “once done and throw.“ You might need to update rubrics or add entirely new metrics.** Since your predeployment metrics might not capture all kinds of issues, you need to rely on online implicit and explicit signals too: Did the user show frustration? Did they drop off the call? Did they leave a thumbs down? These signals help you sample bad experiences so you can make fixes. And if needed, you can implement new metrics to track how a dimension is doing. Maybe you didn’t have a metric for handling out-of-scope requests. Maybe escalation accuracy should be a new metric.

Over time, you also realize that some metrics become less useful because user behavior has changed. This is where the flywheel becomes important.

## The Flywheel

This is the part most people miss and pay least attention to but you should be paying the *most* attention to. Measuring quality isn’t a phase you complete before launch. It’s not a gate you pass through once. It’s an engine that runs continuously, for the entire life of your product.

Here’s how it works:

**Monitor production.** You can’t review everything, so you sample intelligently. Flag conversations that look unusual: long exchanges, repeated questions, user frustration signals, low confidence scores. These are the interactions worth examining.

**Discover new failure modes.** When you review flagged interactions, you find problems your prelaunch testing missed. Maybe users are asking about a topic you didn’t anticipate. Maybe the system handles a certain phrasing poorly. These are new failure modes, gaps in your understanding of what can go wrong.

**Update your metrics and reference data.** Every new failure mode becomes a new thing to measure. You can either fix the issue and move on, or if you have a sense that the issue needs to be monitored for future interactions, add a new metric or a set of rubrics to an existing metric. Add examples to your reference dataset. Your quality system gets smarter because production taught you what to look for.

**Ship improvements and repeat.** Fix the issues, push the changes, and start monitoring again. The cycle continues.

This is the flywheel: Production informs quality measurement, quality measurement guides improvement, improvement changes production, and production reveals new gaps. It keeps running... (Until your product reaches a convergence point. How often you need to run it depends on your online signals: Are users satisfied, or are there anomalies?)

![The Flywheel of Continuous Improvement](https://www.oreilly.com/radar/wp-content/uploads/sites/3/2026/01/image-8.png)

The Flywheel of Continuous Improvement

**And your metrics have a lifecycle.**

Not all metrics serve the same purpose:

**Capability metrics** (borrowing the term from [Anthropic’s blog](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) measure things you’re actively trying to improve. They should start at a low pass rate (maybe 40%, maybe 60%). These are the hills you’re climbing. If a capability metric is already at 95%, it’s not telling you where to focus.

**Regression metrics** (again borrowing the term from [Anthropic’s blog](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) protect what you’ve already achieved. These should be near 100%. If a regression metric drops, something broke. You need to investigate immediately. As you improve on capability metrics, the things you’ve mastered become regression metrics.

**Saturated metrics** have stopped giving you signal. They’re always green. They’re no longer informing decisions. When a metric saturates, run it less frequently or retire it entirely. It’s noise, not signal.

Metrics should be born when you discover new failure modes, evolve as you improve, and eventually be retired when they’ve served their purpose. **A static set of metrics that never changes is a sign that your quality system has stagnated.**

## So What Are “Evals“?

As promised, we made it through without using the word “evals.“ Hopefully this gives a glimpse into the lifecycle: assessing quality before deployment, deploying with the right level of confidence, connecting production signals to metrics, and building a flywheel.

Now, the issue with the word “evals“ is that people use it for all sorts of things:

- “We should build evals“ → Usually means “we should write LLM judges“ (useless if not calibrated and not part of the flywheel).
- “Evals are dead; A/B testing is key“ → This is part of the flywheel. Some companies overindex on online signals and fix issues without many offline metrics. Might or might not make sense based on product.
- “How are GPT-5.2 evals looking?“ → These are model benchmarks, often not useful for product builders.
- “How many evals do you have?“ → Might refer to data samples, metrics… We don’t know what.

And more!

Here’s the deal: Everything we walked through (distinguishing model from product, building reference examples and rubrics, measuring with code and LLM judges and humans, monitoring production, running the continuous improvement flywheel, managing the lifecycle of your metrics) is what “evals“ should mean. But we don’t think one term should carry so much weight. We don’t want to use the term anymore. We want to point to different parts in the flywheel and have a fruitful conversation instead.

And that’s why **evals are not all you need**. It’s a larger data science and monitoring problem. Think of quality assessment as an ongoing discipline, not a checklist item.

We could have titled this article “Evals Are All You Need.“ But depending on your definition, that might not get you to read this article, because you think you already know what evals are. And it might be just a piece. If you’ve read this far, you understand why.

**Final note:** Build the flywheel, not the checkbox. Not the dashboard. Whatever you need to build that actionable flywheel of improvement.

Post topics: [AI & ML](https://www.oreilly.com/radar/topics/ai-ml/ "AI & ML")

Post tags: [Commentary](https://www.oreilly.com/radar/tag/commentary/ "Commentary")