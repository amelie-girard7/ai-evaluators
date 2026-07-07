# Integrating Evals Into the AI App Lifecycle

From development through production: a continuous evaluation strategy

Decodingai.com's framework for integrating evaluations into the AI application lifecycle defines four phases where evaluation plays a distinct role. This is the operational framework that keeps AI systems reliable in production.

## 9.1 Phase 1: Design (Before You Build)
- Define the task taxonomy and success criteria in writing
- Write evaluation criteria before the first prompt
- Identify what a gold set should contain; begin collecting it
- Choose target metrics and acceptable thresholds (e.g., F1 > 0.85 per theme)
- Identify human reviewers and their domain expertise

## 9.2 Phase 2: Development (Build and Iterate)
- Run unit evals on every prompt change
- Use LLM judge for broader coverage on development set
- Conduct error analysis after each major prompt iteration
- Version-control all prompts alongside eval scores
- Block any change that regresses key metrics

## 9.3 Phase 3: Pre-Production (Before Launch)
- Run full eval suite on held-out test set (not seen during development)
- Conduct human review of 10% of test set outputs
- Verify LLM judge kappa is above threshold
- Stress-test with adversarial examples (edge cases, ambiguous complaints)
- Get domain expert sign-off on taxonomy coverage and accuracy

## 9.4 Phase 4: Production (After Launch)
- Sample 1-2% of production traffic for continuous eval
- Alert when eval scores drift below threshold
- Log all model inputs, outputs, and eval scores for analysis
- Collect novel failure cases and add to gold set
- Re-run full eval suite monthly; re-validate LLM judge quarterly

Section 10
