---
title: How to Design Evaluators That Catch What Actually Breaks
source: https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures
author:
- '[[Paolo Perrone]]'
published: 2026-03-03
created: 2026-04-30
description: Learn how to design AI evaluators using code-based checks, LLM judges,
  and rubrics. Covers grading strategies, common mistakes, and agentic workflow evals.
tags:
- clippings
processed: true
processed_at: '2026-04-30'
---
### The practical guide to code-based checks, LLM judges, and rubrics for real-world AI apps

*Welcome to the **[AI Evals & Observability series](https://www.decodingai.com/t/ai-evals-and-observability)**: A 7-part journey from shipping AI apps to systematically improving them. Made by busy people. For busy people.*

🧐 Everyone says you need AI evals. Few explain how to actually build them and answer questions such as…

How do we avoid creating evals that waste our time and resources? How do we build datasets and design evaluators that matter? How do we adapt them for RAG?...and most importantly, how do we stop “vibe checking” and leverage evals to actually track and optimize our app?

*This 7-article series breaks it all down from first principles:*

1. [Integrating AI Evals Into Your AI App](https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app)
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. [Generate Synthetic Datasets for AI Evals](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals)
4. **How to Design Evaluators** ← *You are here*
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. [RAG Evaluation: The Only 6 Metrics You Need](https://www.decodingai.com/p/rag-evaluation-6-metrics-framework)
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

By the end, you’ll know how to integrate AI evals that actually track and improve the performance of your AI product. No vibe checking required!

**Let’s get started.**

---

## How to Design Evaluators

You have a dataset. You’ve manually labeled examples. You’ve fixed the obvious bugs. Now you need evaluators that can run automatically and catch problems before users do.

But here’s what trips up most teams: they build evaluators that check for things nobody cares about, or they use off-the-shelf metrics that sound impressive but don’t match their actual use case.

Three months ago, I spent a weekend building what I thought was a comprehensive evaluation suite for an AI agent that drafted replies to customer support tickets. I had ROUGE scores, BLEU scores, semantic similarity metrics, the works. Everything from the NLP textbook.

Then I ran it on production traces. The evaluators gave perfect scores to replies that were factually wrong, missed the customer’s actual question, and used the wrong tone for frustrated users. Meanwhile, they penalized perfectly good replies for using “different words than the reference answer.”

That’s when I realized: generic metrics optimize for academic benchmarks, not business outcomes. (And no, I’m not saying academic metrics are useless. They’re just solving a different problem than “did this agent do what my users needed?”)

The solution is to design evaluators that match your specific success criteria. Not what worked for someone else’s summarization task. Not what scored well on SQuAD. What actually matters for your users in your use case.

**In this article, we will cover:**

- The evaluation harness: infrastructure that runs evals end-to-end
- Dataset and metric types: direct scoring vs. pairwise vs. reference-based
- Model evaluation vs. app evaluation (and why benchmarks lie)
- Components of an evaluator: reference examples, metrics, rubrics
- When to use code-based checks vs. LLM judges
- Common mistakes (and how to avoid them)
- Advanced metric designs for multi-turn conversations and agentic workflows

![Designing evaluators for AI applications: from code-based checks to LLM judges.](https://substackcdn.com/image/fetch/$s_!a1uV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ad91d7a-490d-4b4e-ac91-0f48e10bccc7_1456x1048.png)

Image 1: Designing evaluators for AI applications: from code-based checks to LLM judges.

*Before digging into the article, a quick word from our sponsor, Opik.* ↓

---

## Opik: Open-Source LLMOps Platform (Sponsored)

This **AI Evals & Observability** series is brought to you by [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul), the LLMOps open-source platform used by Uber, Etsy, Netflix, and more.

We use Opik daily across our courses and AI products. Not just for observability, but to design and run the exact evaluators this article teaches: custom LLM judges, code-based checks, and experiments. All from the same platform.

![Opik Banner](https://substackcdn.com/image/fetch/$s_!oSDm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26c21863-4ee6-4026-91c7-74650eb16dac_3168x792.png)

Try Opik for free here (25k spans/month free)

This article shows you how to design evaluators. Opik gives you the harness to run them at scale. Here is how we use it:

- **Custom LLM judges with rubrics** — Build the evaluators this article describes: define your criteria, add few-shot examples, and run them across hundreds of traces automatically.
- **Run experiments, compare results** — Test different prompts, models, or configurations side by side. Opik scores each variant with your evaluators and shows you which one wins.
- **Plug evaluators into production** — The same LLM judges you design for testing run on live traces too. Set up alarms when scores drop below your threshold so you catch regressions before users do.

**[Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul)** is fully **open-source** and works with custom code or most AI frameworks. You can also use the managed version for free (with 25K spans/month on their generous free tier):

---

*↓* *Now, let’s move back to the article.*

## Understanding the Evaluation Harness

You can’t manually run 500 test cases. You need automation.

The infrastructure that runs evals end-to-end is called an **evaluation harness (1)**. It loads your dataset, executes your agent on each test case, captures all the outputs and traces, runs your graders, and aggregates the scores into something you can actually use.

Think of it like pytest for AI apps. Except instead of checking if a function returns the right type, you’re checking if an LLM generated text that accomplishes a business goal.

Here’s what a harness does:

1. **Loads tasks** from your evaluation dataset
2. **Provides instructions and tools** to the agent (system prompts, available functions, etc.)
3. **Runs tasks** (often in parallel across multiple trials because LLM outputs vary)
4. **Records everything**: inputs, outputs, tool calls, reasoning traces, intermediate states
5. **Runs graders** on the results (your evaluators)
6. **Aggregates scores** across trials and tasks

![The evaluation harness pipeline: loading tasks, running agents, scoring results, and aggregating metrics.](https://substackcdn.com/image/fetch/$s_!tu0r!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ce14a1c-8162-406e-a728-fd596c93af89_1200x630.png)

Image 2: The evaluation harness pipeline: loading tasks, running agents, scoring results, and aggregating metrics.

Without a harness, you’re manually running your agent on test cases and eyeballing the output. With a harness, you run 500 test cases overnight and wake up to a report showing exactly which failure categories spiked \[1\].

The harness is separate from your evaluators. The evaluators decide what “good” means. The harness handles the boring work of running everything at scale and collecting results.

Popular harness options include [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) (what we use), Braintrust, LangSmith, and open-source frameworks like Promptfoo. But honestly, you can build a minimal harness in ~100 lines of Python if you need custom logic \[1\]. The hard part isn’t the infrastructure - it’s assembling the right context (system prompts, conversation history, retrieved docs, tools) for each task. The key is having one. Don’t manually run evals.

Now let’s talk about what those evaluators actually check.

## Dataset and Metric Types: Three Ways to Grade

When designing an evaluator, you need to pick a grading strategy. There are three main approaches, each suited for different situations.

![Three grading strategies: direct scoring, pairwise comparison, and reference-based evaluation.](https://substackcdn.com/image/fetch/$s_!2d8b!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F748f635b-6849-48a1-88fe-e67c64a46b50_1200x630.png)

Image 3: Three grading strategies: direct scoring, pairwise comparison, and reference-based evaluation.

### 1\. Direct Scoring (Pointwise Evaluation)

The evaluator looks at a single output and scores it in isolation. No comparison to anything else.

**Example:**

- Input: “Refund my order #12345”
- Output: “I’ve processed your refund for order #12345. You’ll see the credit in 3-5 business days.”
- Score: Pass (correctly identified the task, provided timeline, professional tone)

**When to use:**

- You have clear, absolute quality criteria (was it helpful? was it safe? did it call the right tool?)
- You want to track performance over time on the same dataset
- Your baseline is “good enough” not “better than X”

**Metrics:**

- Binary pass/fail
- 0-1 scores (where 1 = perfect)
- Classification labels (Helpful/Neutral/Harmful)

### 2\. Pairwise Comparison

The evaluator compares two outputs and picks which one is better.

**Example:**

- Input: “Refund my order #12345”
- Output A: “Refund processed.”
- Output B: “I’ve processed your refund for order #12345. You’ll see the credit in 3-5 business days.”
- Winner: Output B (more informative, sets expectations)

**When to use:**

- Comparing two model versions (baseline vs. candidate)
- A/B testing different prompts
- LLMs are better at ranking than absolute scoring

**Watch out for biases (2):**

- **Position bias**: LLMs favor the first or last response shown
- **Verbosity bias**: LLMs prefer longer answers even when they’re not better
- **Self-enhancement bias**: LLMs favor outputs from themselves over other models

You can mitigate these by randomizing response order and using multiple trials.

### 3\. Reference-Based Evaluation

The evaluator compares the output to a known “gold standard” answer.

**Example:**

- Input: “What’s the capital of France?”
- Output: “Paris”
- Reference: “Paris”
- Score: Exact match (Pass)

**Example 2 (Semantic equivalence):**

- Input: “Summarize the refund policy”
- Output: “Customers can return items within 30 days for a full refund if unused.”
- Reference: “Full refunds are available for unused products returned within 30 days of purchase.”
- Score: Pass (different wording, same meaning)

**When to use:**

- You have ground truth answers (FAQs, knowledge bases, structured tasks)
- Task has a single correct answer or small set of acceptable answers
- You’re testing retrieval accuracy or factual correctness

**How to measure:**

- **Exact match**: For structured outputs (dates, product IDs, categorical values)
- **Semantic similarity / LLM judges:** For natural language, where multiple phrasings are valid (summaries, explanations, instructions)

**Common metrics (3):**

- Exact match
- ROUGE (recall-oriented, good for summarization)
- BLEU (precision-oriented, originally for translation)
- BERTScore (semantic similarity using embeddings)
- LLM judges (for nuanced semantic equivalence)

**The trap:** Exact match metrics penalize valid variations. If your reference says “The meeting is on Friday” and your agent says “The meeting is scheduled for this Friday,” exact match fails. This is where semantic similarity metrics (BERTScore) or LLM judges become powerful - they can recognize that different phrasings convey the same outcome.

## Model Evaluation vs. App Evaluation (Why Benchmarks Lie)

Here’s a distinction that matters more than people realize:

**Model evaluation** measures the LLM itself, in isolation, on generic tasks. This is what benchmarks like MMLU, HumanEval, and Chatbot Arena do.

**App evaluation** measures your entire application (LLM + prompts + tools + retrieval + business logic) on your specific use case.

High MMLU score doesn’t mean it handles your refund policy correctly. Benchmarks test general capability. You need to test your specific use case.

### Model Evaluation (Benchmarks)

Tests: “Can this LLM answer random trivia, write code snippets, or score high on standardized tests?”

**Useful for:**

- Comparing foundation models across the board
- Understanding general capabilities
- Academic research

**Useless for:**

- Predicting whether it will handle your refund policy correctly
- Knowing if it will escalate frustrated customers at the right time
- Determining if it respects your company’s tone of voice

### App Evaluation (What You Actually Need)

Tests: “Does my customer support agent correctly process refunds, handle escalations, and follow our policies?”

**This is what matters** because your users don’t care if GPT-5 scored 95% on MMLU. They care if it solved their problem.

Your evaluators must be grounded in your business use case, not generic academic benchmarks. This means:

- Testing against your actual policies, not Wikipedia facts
- Using your real user queries, not synthetic textbook questions
- Measuring outcomes that impact revenue, retention, or safety

Benchmarks tell you which LLM is “generally smarter.” App evals tell you which version of your system works better for your users.

Don’t mistake one for the other.

## Components of an Evaluator

Now that you know the types, let’s build one. Every evaluator has three components:

![The three components of every evaluator: reference examples, metrics, and rubrics.](https://substackcdn.com/image/fetch/$s_!b_Ph!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabad08fa-fbdb-45b7-9f1d-00ef87d12897_1200x630.png)

Image 4: The three components of every evaluator: reference examples, metrics, and rubrics.

### 1\. Reference Examples (Few-Shot Prompts)

These are the labeled examples from your dataset. They show the evaluator what “good” and “bad” look like for your specific task.

Remember from Article 2: the real power isn’t in the system prompt, it’s in these few-shot examples. They encode your domain expert’s judgment.

**Example:**

**Example 1 - PASS**

```markup
Input: “I need a refund for order #12345”
Output: “I’ve processed your refund. You’ll see the credit in 3-5 business days.”
Reason: Confirms action, sets timeline, professional tone.
```

**Example 2 - FAIL**

```markup
Input: “Can you waive the late fee on my account?”
Output: “I can help with that!”
Reason: Didn’t actually take action or explain next steps. Empty promise.
```

### 2\. Metrics

The quantifiable measurement of quality. This can be:

- **Objective**: Did it call the right tool? Is the JSON valid? Is the response under 200 words?
- **Subjective**: Was it helpful? Was the tone appropriate? Did it follow the conversation flow?

For objective metrics, use code-based checks (fast, cheap, deterministic).

For subjective metrics, use LLM judges or human evaluation.

### 3\. Rubrics

For subjective metrics, you need a rubric: explicit criteria that define what you’re measuring.

**Bad rubric:**  
*“Was the response helpful?”*

(Too vague. Helpful how? To whom? Compared to what?)

**Good rubric:**  
*“Did the response: (1) correctly identify the user’s request, (2) provide a specific action or next step, (3) include a timeline or expectation, and (4) maintain professional tone?”*

Rubrics force precision. They make subjective judgments repeatable. These criteria become part of your LLM judge’s system prompt.

## Code-Based Evaluators: Fast, Cheap, Objective

Some checks are deterministic. Did the agent call `refund_order()`? Is the output valid JSON? Does it include a required disclaimer?

Use code for these. It’s faster, cheaper, and never gives you a different answer on the same input.

![Code-based evaluators check deterministic criteria: tool calls, format, required elements, and prohibited content.](https://substackcdn.com/image/fetch/$s_!-byG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31a1e6f1-d168-44f4-928c-1a7969ac85f3_1200x630.png)

Image 5: Code-based evaluators check deterministic criteria: tool calls, format, required elements, and prohibited content.

**Use code-based evaluators for:**

- **Tool calls**: Did it call `refund_order()` with the right parameters?
- **Format checks**: Is the output valid JSON? Is it under the character limit?
- **Required elements**: Does it include a disclaimer? Does it have a timestamp?
- **Prohibited content**: Does it contain banned phrases or leaked data?

**Example (pseudocode):**

```markup
def evaluate_refund_agent(trace):
  # Check if right tool was called
  if “refund_order” not in trace.tool_calls:
  return {”pass”: False, “reason”: “Didn’t call refund_order”}

  # Check if order_id parameter was provided
  params = trace.tool_calls["refund_order"].parameters
  if "order_id" not in params:
    return {"pass": False, "reason": "Missing order_id parameter"}

  # Check if response includes timeline
  if not any(word in trace.output.lower() for word in ["days", "week", "timeline"]):
    return {"pass": False, "reason": "No timeline provided to customer"}

  return {"pass": True, "reason": "All checks passed"}\`
```

Code-based evaluators are:

- **Fast**: Milliseconds per check
- **Cheap**: No API costs
- **Reproducible**: Same input always gives same result
- **Easy to debug**: When they fail, you know exactly what broke

But they can’t handle nuance. They can’t judge tone, helpfulness, or conversational flow. For that, you need LLM judges.

These code-based evaluators work exactly like classic unit tests you’re already familiar with. They’re deterministic, fast, and easy to debug. That’s why you should always try to implement code-based checks first before reaching for LLM judges. If you can check it with code, do that. Only use LLM judges when code can’t capture what you need to measure.

## LLM Judges: Flexible, Scalable, Nuanced

An **LLM judge** is an LLM that grades another LLM’s output. You give it the task, the output, and the evaluation criteria, and it returns a score with reasoning

![LLM judge flow: input context and criteria produce a score with reasoning.](https://substackcdn.com/image/fetch/$s_!L6EX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0c0a5b9-99aa-427e-899f-a2e463267ec7_1200x630.png)

Image 6: LLM judge flow: input context and criteria produce a score with reasoning.

LLM judges work in two modes: evaluating outputs against absolute criteria (is it helpful? professional? accurate?) or comparing outputs to reference answers when you have ground truth but need semantic understanding rather than exact string matching.

**Use LLM judges for:**

- **Tone**: Was it empathetic? Professional? Not condescending?
- **Helpfulness**: Did it actually answer the question or deflect?
- **Conversation flow**: Did it maintain context across turns?
- **Reasoning quality**: Did the agent’s plan make sense?

**How it works:**

1. You provide:
	- The input (user query)
		- The output (agent’s response)
		- The context (system prompt, retrieved docs, conversation history)
		- Evaluation criteria (what you’re checking for)
		- Few-shot examples (labeled passes and fails)
2. The LLM judge outputs:
	- A score (pass/fail or 0-1 scale)
		- A critique explaining why

**Example prompt (simplified):**

```markup
You are evaluating customer support responses. For each trace, output Pass or Fail 
with reasoning.

Evaluation criteria:
1. Did the response correctly identify the customer’s request?
2. Did it provide a specific action or next step?
3. Did it include a timeline or expectation?
4. Did it maintain a professional tone?

Here are examples of how a domain expert judged similar cases:

[Few-shot examples from your labeled dataset]

Now evaluate this trace:
Input: [customer query]
Output: [agent response]
Context: [system prompt, policies]
```

The judge generates:

```markup
FAIL

The response correctly identified the refund request (criterion 1: pass) and 
maintained professional tone (criterion 4: pass). However, it didn’t specify a next 
step beyond “we’ll look into this” (criterion 2: fail) and provided no timeline 
(criterion 3: fail). Customer is left waiting with no expectations set.
```

### Strengths of LLM Judges

- **Flexible**: Handle open-ended tasks where code can’t
- **Scalable**: Grade thousands of traces automatically
- **Explainable**: Critiques show reasoning, helping debug failures

### Weaknesses of LLM Judges

- **Non-deterministic**: Same input might get different scores across runs
- **Expensive**: Every evaluation is an API call
- **Needs calibration**: Must align with human judgment (we cover this in Article 5)

### Making LLM Judges More Stable

1. **Use the most capable model** (e.g., Claude Opus, GPT-4o) + footnotes (4)
2. **Add chain-of-thought reasoning** before scoring (”Let’s think step-by-step...”)
3. **Control for verbosity bias** (normalize response lengths)
4. **Run multiple trials** and average scores for critical evals
5. **Increase dataset size** to at least 50-100 samples (reduces noise)

## Common Mistakes (And How to Avoid Them)

### Mistake 1: Not Providing Critiques

**Wrong:**  
Score: 1

**Right:**  
Score: 1

Critique: *“Response correctly identified the refund request but didn’t provide a timeline. Customer left without expectations.”*

Critiques are not optional. They’re how you debug failures and train better evaluators.

### Mistake 2: Overly Terse Critiques

**Wrong:**  
“Bad tone”

**Right:**  
*“Response used dismissive language (’just wait’) when customer expressed frustration about a delayed order. Should have acknowledged frustration and provided specific next steps.”*

The critique should be detailed enough to serve as a few-shot example later.

### Mistake 3: Missing Context

Don’t evaluate the output in isolation. Give the evaluator everything a human would see:

- The full conversation history (for multi-turn tasks)
- Retrieved documents (for RAG)
- System prompts (for understanding constraints)
- Tool call results (for agentic workflows)

If a human needs it to judge quality, the evaluator needs it too.

### Mistake 4: Not Providing Diverse Examples

If all your few-shot examples are “customer angry, agent apologizes,” the judge won’t know how to handle “customer confused, needs technical explanation.”

Cover the failure modes you actually see in production.

### Mistake 5: Using Ready-Made Metrics Without Validation

ROUGE, BLEU, BERTScore, etc. sound professional, but they might not correlate with your actual goal.

Before using any metric, validate it against human judgment on your specific task. If high ROUGE doesn’t mean “users are happy,” don’t optimize for ROUGE.

### Mistake 6: Using 1-5 Scales Instead of Binary Pass/Fail

Wrong:  
Score: 3.2 out of 5

Right:  
Score: 0 (Fail)  
Critique: *“Response didn’t provide a timeline or next steps.”*

Why it matters: A score of 3.2 is ambiguous. Is that good enough to ship? Should you fix it? Binary forces clarity. Either it passes your quality bar or it doesn’t. Scoring on a float scale (0.0-1.0) has the same problem - it leaves room for interpretation instead of forcing a clear decision.

## When Should I Use Similarity Metrics (BERTScore, ROUGE, etc.)?

Short answer: **Only for specific, narrow tasks where semantic overlap actually matters.**

### When They Work

**Summarization:** ROUGE measures how much of the source content appears in the summary. If your task is “don’t miss key facts,” ROUGE helps.

**Translation:** BLEU checks n-gram overlap with reference translations. Works when there’s a narrow acceptable output space.

**Retrieval accuracy:** BERTScore compares semantic similarity between retrieved chunks and expected documents.

### When They Fail

**Open-ended generation:** Your AI agent says “I’ve refunded order #12345. You’ll see the credit in 3-5 days.” Reference says “Refund processed for order #12345, expect 3-5 business days.” Different words, same meaning. ROUGE fails.

**Tone and helpfulness:** Similarity metrics don’t measure if the tone was appropriate or if it actually helped the user.

**Business outcomes:** High similarity doesn’t mean the customer is satisfied, the sale closed, or the task completed.

### The Rule

If your success criterion is “output should be semantically similar to the reference answer,” use similarity metrics.

If your success criteria are *“user achieved their goal,”* use app-level evaluators grounded in outcomes.

![Decision tree for choosing the right evaluator type.](https://substackcdn.com/image/fetch/$s_!Ovy3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbd045ca-c3dc-46b7-a942-0ceec8fe523c_1200x630.png)

Image 7: Decision tree for choosing the right evaluator type.

## Advanced Metric Designs

Now let’s handle the hard cases: multi-turn conversations, complex workflows, and agentic systems.

### Evaluating Multi-Turn Conversation Traces

A single-turn eval checks one input and one output. Multi-turn evals check entire conversations.

**Challenges:**

- Context must carry across turns
- Errors compound (one bad response derails the rest)
- You need to catch the **first upstream failure**, not downstream symptoms

**Strategy:**

1. **End-to-end task success**: Did the agent accomplish the user’s goal by the end?
2. **Turn-by-turn checks**: Evaluate each exchange individually
	- Did turn 3 maintain context from turn 1?
		- Did turn 5 escalate when the user got frustrated?
3. **Failure attribution**: When something breaks, find the first turn where it went wrong

**Example (customer support conversation):**

**Turn 1:**

User: *“I need to return order #12345”*

Agent: *“Sure, I can help with that. What’s the reason for the return?”*

Eval: Pass (acknowledged request, asked clarifying question)

**Turn 2:**

User: *“It arrived damaged”*

Agent: *“I’ll process a refund. Expect 3-5 business days.”*

Eval: FAIL (Skipped required step: didn’t offer replacement or ask for photos of damage)

**Turn 3:**

User: *“Do I need to ship it back?”*

Agent: *“No, keep it.”*

**Eval:** Pass (but only because Turn 2 already failed the workflow)

The **first upstream failure** is Turn 2. Everything after is a consequence.

**Important**: When evaluating any turn, provide all previous turns as context. Evaluating Turn 2? Include Turn 1. Evaluating Turn 3? Include Turns 1 and 2. The evaluator needs the full conversation history to judge whether context was properly maintained.

![Multi-turn conversation evaluation with first upstream failure attribution.](https://substackcdn.com/image/fetch/$s_!F9xg!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec05adaa-5103-4052-aadb-2df1e3cc201e_1200x630.png)

Image 8: Multi-turn conversation evaluation with first upstream failure attribution.

### Evaluating Complex Multi-Step Workflows

Workflows have dependencies. Step 3 can’t succeed if Step 1 failed. Your evaluator needs to know this.

![Evaluating complex multi-step workflows with dependency-aware sequencing.](https://substackcdn.com/image/fetch/$s_!xiHl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bd8fc68-b010-4c85-bdef-89708a22c188_1200x630.png)

Image 9: Evaluating complex multi-step workflows with dependency-aware sequencing.

**Example (flight booking agent):**

Required sequence:

1. Search flights
2. Validate availability
3. Confirm payment
4. Book reservation

**Bad eval:** Check if all steps ran (yes/no)

**Good eval:** Check if steps ran in the right order, with correct dependencies

![code](https://substackcdn.com/image/fetch/$s_!2pwF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc968b3ad-0e3f-4b47-928b-4578eb3a155b_2969x1587.png)

### Evaluating Agentic Workflows

Agents don’t follow fixed scripts. They plan, reason, and adapt. This makes evaluation harder.

![Two-phase agentic workflow evaluation: end-to-end success followed by step-level diagnostics.](https://substackcdn.com/image/fetch/$s_!TV0w!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92400711-7db8-4161-b306-6fad56d41a5a_1200x630.png)

Image 10: Two-phase agentic workflow evaluation: end-to-end success followed by step-level diagnostics.

**Two-phase approach** (from Hamel Husain) (5):

### Phase 1: End-to-End Task Success

Treat the agent as a black box. Did it meet the user’s goal?

**Define precise success rules per task:**

- Exact answer match (for factual tasks)
- Correct side-effect (database updated, email sent, file created)
- User satisfaction (thumbs up, complaint rate, retry rate)

Use human judges or well-aligned LLM judges. **Focus on first upstream failures** during error analysis.

### Phase 2: Step-Level Diagnostics

Once you know which workflows fail, diagnose why.

Assuming you’ve instrumented your system to log tool calls and responses, score:

1. **Tool choice**: Was the selected tool appropriate?
2. **Parameter extraction**: Were inputs complete and well-formed?
3. **Error handling**: Did it recover from empty results or API failures?
4. **Context retention**: Did it preserve earlier constraints?
5. **Plan quality**: Does the agent’s plan match the task requirements?

**Transition matrix analysis** (Bryan Bischof’s approach):

Track which state transitions cause failures.

Example (text-to-SQL agent):

- GenSQL → ExecSQL: 12 failures
- DecideTool → PlanCal: 2 failures

This data-driven view shows where to focus debugging.

**Session-level metrics:**

- Task completion rate
- Step completion (did it finish the required steps?)
- Trajectory quality (did it avoid loops?)
- Self-aware failures (did it acknowledge limitations?)

**Node-level metrics (per tool call):**

- Tool correctness (right tool with right parameters?)
- Tool call accuracy (did the tool run without errors?)
- Output correctness (did the tool return valid results?)

**System efficiency metrics:**

- Latency (time to complete task)
- Token usage (cost per task)
- Tool calls per task (efficiency of plan)

These metrics layer on top of each other\[6\]. System efficiency ensures scalability. Session-level metrics validate goal achievement. Node-level metrics pinpoint root causes.

## Bringing It All Together

Pick evaluators based on what you’re actually trying to measure, not what sounds impressive. Here’s how to decide which evaluator to use:

**Can you check it with code?**

Yes → Use code-based evaluators (tool calls, format checks, required elements)

No → Move to next question

**Is there a single correct answer or narrow acceptable range?**

Yes → Use reference-based evaluation (exact match, ROUGE, BLEU)

No → Move to next question

**Are you comparing two versions?**

Yes → Use pairwise comparison

No → Use direct scoring

**Is the task subjective (tone, helpfulness, flow)?**

Yes → Use LLM judges with rubrics and few-shot examples

No → Rethink your criteria (you might have missed a code-based check)

**Is it a multi-turn or agentic workflow?**

Yes → Use two-phase approach (end-to-end task success + step-level diagnostics)

No → Single-turn direct scoring

And remember: **your evaluators are only as good as your dataset and few-shot examples**. The system prompt matters less than you think. The examples matter more than you think.

## Next Steps

You now know how to design evaluators that match your use case. You know when to use code, when to use LLMs, and when to combine both.

But here’s the critical question we haven’t answered: **How do you know if your evaluator is actually working?**

An evaluator who says everything is great when it’s not is worse than no evaluator at all. You need to validate that your automated judges align with human judgment before you trust them.

That’s what we’ll cover in [Article 5: How to Evaluate the Effectiveness of the Evaluator](https://www.decodingai.com/how-to-evaluate-the-evaluator-validate-llm-judge).

Also, remember that this article is part of a **[7-piece series on AI Evals & Observability](https://www.decodingai.com/t/ai-evals-and-observability)**. **Here’s what’s ahead:**

1. [Integrating AI Evals Into Your AI App](https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app)
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. [Generate Synthetic Datasets for AI Evals](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals)
4. **How to Design Evaluators** ← *You just finished this one*
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. [RAG Evaluation: The Only 6 Metrics You Need](https://www.decodingai.com/p/rag-evaluation-6-metrics-framework)
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

See you next Tuesday.

[Paolo Perrone](https://substack.com/@paoloap)

---

*What’s your opinion? Do you agree, disagree, or is there something I missed?*

---

### Most AI newsletters give you news. The AI Engineer gives you understanding.

One concept per week, explained from first principles: when to fine-tune vs. prompt vs. RAG, which vector database fits your workload, and how companies like DoorDash ship AI at scale.

*Written for senior engineers and tech leads who build with AI, not just read about it.*

---

## Go Deeper

**Go from zero to production-grade AI agents** with the [Agentic AI Engineering self-paced course](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31). Built in partnership with [Towards AI](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31).

Across **34 lessons** (articles, videos, and a lot of code), you’ll design, build, evaluate, and deploy production-grade AI agents end to end. By the final lesson, you’ll have **built a multi-agent system** and a **capstone project** where you apply everything you've learned on your own.

*Three portfolio projects and a certificate to showcase in interviews. Plus a Discord community where you have direct access to other industry experts and me.*

Rated 4.9/5 ⭐️ by 290+ early students — *“Every AI Engineer needs a course like this.”*

*Not ready to commit?* We also prepared a free 6-day email course to reveal the ***6 critical mistakes that silently destroy agentic systems.** [Get the free email course.](https://email-course.towardsai.net/?ref=b3ab31)*

---

*Thanks again to [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) for sponsoring the series and keeping it free!*

![Opik Banner](https://substackcdn.com/image/fetch/$s_!yeD8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdeaa636a-b1a6-429b-83d8-080bc218e596_1200x400.png)

Try Opik for free here (25k spans/month free)

**If you want to monitor, evaluate and optimize your AI workflows and agents:**

---

## References

1. Anthropic. (n.d.). Demystifying evals for AI agents. [https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents](http://not%20ready%20to%20commit/?%20We%20also%20prepared%20a%20free%206-day%20email%20course%20to%20reveal%20the%206%20critical%20mistakes%20that%20silently%20destroy%20agentic%20%20%20systems.%20Get%20the%20free%20email%20course.)
2. Evidentlyai. (n.d.). LLM-as-a-judge: a complete guide. [https://www.evidentlyai.com/llm-guide/llm-as-a-judge](http://not%20ready%20to%20commit/?%20We%20also%20prepared%20a%20free%206-day%20email%20course%20to%20reveal%20the%206%20critical%20mistakes%20that%20silently%20destroy%20agentic%20%20%20systems.%20Get%20the%20free%20email%20course.)
3. Evidentlyai. (n.d.). LLM evaluation metrics and methods. [https://www.evidentlyai.com/llm-guide/llm-evaluation-metrics](http://not%20ready%20to%20commit/?%20We%20also%20prepared%20a%20free%206-day%20email%20course%20to%20reveal%20the%206%20critical%20mistakes%20that%20silently%20destroy%20agentic%20%20%20systems.%20Get%20the%20free%20email%20course.)
4. OpenAI. (n.d.). Evaluation best practices. [https://developers.openai.com/api/docs/guides/evaluation-best-practices](http://not%20ready%20to%20commit/?%20We%20also%20prepared%20a%20free%206-day%20email%20course%20to%20reveal%20the%206%20critical%20mistakes%20that%20silently%20destroy%20agentic%20%20%20systems.%20Get%20the%20free%20email%20course.)
5. Husain, H. (n.d.). How do I evaluate agentic workflows? [https://hamelhusain.substack.com/p/how-do-i-evaluate-agentic-workflows](http://not%20ready%20to%20commit/?%20We%20also%20prepared%20a%20free%206-day%20email%20course%20to%20reveal%20the%206%20critical%20mistakes%20that%20silently%20destroy%20agentic%20%20%20systems.%20Get%20the%20free%20email%20course.)
6. Maxim. (n.d.). Evaluating agentic workflows: The essential metrics that matter. [https://www.getmaxim.ai/articles/evaluating-agentic-workflows-the-essential-metrics-that-matter](https://www.getmaxim.ai/articles/evaluating-agentic-workflows-the-essential-metrics-that-matter)
7. Confident AI. (n.d.). LLM evaluation metrics: Everything you need for LLM evaluation. [https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation](https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation)

---

## Images

If not otherwise stated, all images are created by the author.