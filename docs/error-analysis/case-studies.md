# Error Analysis Case Studies

Applied to both use cases. Each cluster shows the root cause, a representative example, and the fix.

---

## UC1 — Client Feedback Classifier: Error Clusters

### Cluster A: Single-label output on multi-theme client feedback
**Frequency:** Very high (affects ~35% of multi-theme client feedback)
**Root cause:** Prompt says "identify the primary theme" — model returns one theme even when multiple apply
**Representative failure:**
- Input: Example 2 feedback (rejected offer + guide not updated)
- Gold: 5 themes
- Predicted: `["Billing Discrepancy"]` only

**Fix:** Rewrite prompt: *"A feedback may have multiple applicable themes. Return ALL themes that are supported by the feedback text."* Change output schema from `string` to `list[string]`.
**Outcome:** Fixed 34% of all failures in one prompt change.

---

### Cluster B: Billing Discrepancy vs Advertising at misleading prices confusion
**Frequency:** Medium (~18% of billing-related client feedback)
**Root cause:** Taxonomy definitions overlap; no boundary examples in prompt
**Representative failure:**
- Input: Example 1 feedback (multiple guide increases, sold $750k above original guide)
- Gold: Both "Billing Discrepancy" AND "Advertising at misleading prices"
- Predicted: "Billing Discrepancy" only (missed "Advertising at misleading prices")

**Fix:** Add to prompt: *"Billing Discrepancy relates to the gap between guide and likely/eventual selling price. Advertising at misleading prices applies when the advertised price itself creates a false impression, regardless of the billing discrepancy definition. Both can apply simultaneously."* Add 3 boundary examples.
**Outcome:** Reduced this cluster by 71%.

---

### Cluster C: Agent honesty theme missed when language is indirect
**Frequency:** Medium (~15% of honesty-related client feedback)
**Root cause:** Complainants use polite language; "Agent failed to be transparent" vs "Agent was dishonest"
**Representative failure:**
- Input: Client Feedback where complainant says agent "was not forthcoming" with price information
- Gold: "Agent failure to act honestly / fairly"
- Predicted: Nothing in this theme category

**Fix:** Add few-shot examples of indirect language mapping to this theme:
- *"was not forthcoming" → YES for "Agent failure to act honestly/fairly"*
- *"did not provide clear information" → YES*
- *"appeared to be motivated by" → YES if conduct implies deceptive intent*

---

### Cluster D: Novel feedback type — confidentiality request
**Frequency:** Low but emerging (~3%)
**Root cause:** Complainants include a request for confidentiality in the feedback text; model sometimes flags this as a separate theme
**Fix:** Add to taxonomy exclusion list: "Confidentiality requests are procedural, not a feedback item theme. Do not classify this as a theme."

---

## UC2 — RAG Chatbot: Error Clusters

### Cluster A: Hallucinated theme percentages
**Frequency:** High when user asks "what proportion of client feedback relate to X?"
**Root cause:** Retrieved records contain counts but not percentages; LLM calculates percentages not present in context
**Fix:** System prompt addition: *"If the user asks for proportions or percentages, calculate them from the retrieved counts and explicitly state the calculation. Do not invent percentages. If you cannot calculate from the retrieved data, state that you do not have sufficient information."*
**Outcome:** Eliminated 100% of hallucinated percentage cases.

### Cluster B: Wrong feedback count (off by varying amounts)
**Root cause:** Metadata filter for "Western Sydney" not normalised — some records tagged with suburb names, others with LGA names, others with postcodes
**This is a retrieval (infrastructure) problem, not a prompt problem.**
**Fix:** Engineering change — normalise all geographic metadata to a standard postcode list at ingestion time. Rebuild index.

### Cluster C: Date range misinterpretation — FY vs calendar year
**Frequency:** Medium
**Root cause:** "2025-2026" interpreted as either FY (Jul 2025–Jun 2026) or calendar span (Jan 2025–Dec 2026)
**Fix:** Add to system prompt: *"When a user references a year range like '2025-2026', interpret this as financial year (July 2025 to June 2026) unless the user explicitly specifies otherwise. Confirm the date range in your response."*

### Cluster D: Incomplete multi-part answers
**Root cause:** Prompt has no structure requirement for multi-part questions
**Fix:** Add structured output template to system prompt for queries containing "AND": *"If the question contains multiple components, address each component in a separate paragraph with a clear heading."*

---

## Cross-case insight

**The most important finding from both use cases:** Most failures in both systems traced to issues that a single targeted prompt change could fix. Model selection had negligible effect compared to prompt quality. This validates the Hamel Husain principle: invest in error analysis and criteria before investing in model upgrades.

---

*Back: 5-Step Framework | Return to: [Error Analysis Overview](overview.md)*
