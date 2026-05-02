---
title: "Checklist: LLM Judge Quality"
tags: [seed]
last_updated: 2026-04-29
sources: [seed]
unsourced: true
---

# Checklist: LLM Judge Quality

Before deploying an LLM judge for automated scoring, verify all items below. An unvalidated judge is not a judge — it is a guess at scale.

---

## Design checklist

- [ ] All criteria are **binary (YES/NO)** — not Likert, not open-ended
- [ ] Each criterion addresses **one dimension only** — no bundling
- [ ] Each criterion has **at least 2 positive examples** (correct → YES)
- [ ] Each criterion has **at least 2 negative examples** (wrong → NO)
- [ ] Known edge case clusters have **boundary examples** in the prompt
- [ ] Judge uses a **different model family** from the evaluated model
- [ ] Judge prompt includes a **chain-of-thought scratchpad** instruction
- [ ] Judge output is **structured JSON** with one key per criterion

## Validation checklist

- [ ] Judge has been run on the **full gold set** (200–500 items)
- [ ] **Cohen kappa computed per criterion** vs human labels
- [ ] Kappa is **> 0.6 on all criteria** before production deployment
- [ ] **False positive and false negative rates** computed per criterion
- [ ] Failure analysis conducted on disagreement cases
- [ ] Re-validation **scheduled quarterly** or after any model update

## Deployment checklist

- [ ] Judge is **version-controlled** alongside the system prompt it evaluates
- [ ] Judge **alerts on kappa drop** > 0.1 vs baseline
- [ ] Judge results are **logged** with input, output, and verdict for audit
- [ ] A **human review fallback** exists for cases where judge confidence is low

---

## Quick kappa reference

| Kappa | Status | Action |
|---|---|---|
| < 0.4 | Poor | Do not deploy — rewrite criteria |
| 0.4–0.6 | Moderate | Analyse disagreements; add examples |
| 0.6–0.8 | Good | Deploy — monitor quarterly |
| > 0.8 | Excellent | Deploy — monitor bi-annually |
