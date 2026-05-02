---
title: "Evaluating Agentic AI Systems"
tags: [eval, metrics, lifecycle, agent-evals]
last_updated: 2026-04-29
sources:
  - raw/notes/evaluating-agentic-ai-systems.md
---

# Evaluating Agentic AI Systems

How evaluation changes when your AI takes multi-step actions

Anthropic's 'Demystifying Evals for AI Agents' identifies a fundamental challenge: agentic systems make sequences of decisions, and a single failed step can cascade into a failed task even if most steps were correct. Traditional single-turn evals are insufficient.

## 10.1 The Three Levels of Agent Evaluation

## 10.2 Applying Agent Evals to the Complaints Chatbot
The complaints chatbot is a simple two-step agent: retrieve then generate. But even this simple pipeline requires trajectory evaluation:

- Step 1 eval: Did the retrieval query include the correct region filter and date range?
- Step 2 eval: Did the generation use only information from the retrieved context?
- Trajectory eval: Was the overall reasoning chain coherent? Did the agent correctly handle ambiguous date ranges?
- Final state eval: Does the answer match the ground-truth database query result?

A more complex agent - one that decides whether to query by region, by theme, or by date first, or that calls multiple tools - requires full trajectory evaluation. Anthropic recommends building a 'trajectory dataset' of expert-demonstrated correct action sequences, then comparing agent trajectories against these examples.

Section 11
