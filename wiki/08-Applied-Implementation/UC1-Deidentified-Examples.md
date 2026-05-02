---
title: Deidentified Complaint Examples
tags:
- wiki
last_updated: '2026-05-01'
sources:
- raw/notes/complaint-classification-examples.md
---

# Deidentified Complaint Examples

> **Privacy notice:** All identifying information (agency names, agent names, property addresses, individual names) has been replaced with generic placeholders. Dollar amounts and dates are retained as they are not uniquely identifying without the removed fields.

---

## Example 1 — Underquoting, price guide escalation

> *I request that my identity remain confidential and not be disclosed to the agency. I wish to lodge a formal complaint regarding the pricing conduct of **[Agency A]** in relation to the sale campaign for **[Property 1]**, Eastern Suburbs NSW, which I believe constitutes underquoting under the Property and Stock Agents Act 2002.*
>
> *The property was initially advertised with a price guide of approximately $2.1 million. I believe this figure was materially below comparable recent sales in the area and did not reflect a reasonable estimate of the likely selling price based on market evidence available at the time.*
>
> *During the campaign, the price guide was increased twice after inspections had commenced, with the final advertised guide being approximately $2.45 million.*
>
> *Despite these revisions, the property ultimately sold for $2.85 million, which is $400,000 above the final guide and $750,000 above the original advertised guide. Based on my direct interactions and market observations, it was apparent that the vendor's price expectations were significantly higher (around $3 million) from the outset.*
>
> *If this was the case, the original guide could not have been a genuine or reasonable estimate of the likely selling price as required under NSW legislation.*

### Correct theme labels

| Theme | Applies | Reasoning |
|---|---|---|
| Unsatisfactory behaviour by strata manager/agent | YES | Agent's overall pricing conduct constitutes unsatisfactory behaviour |
| Agent failure to act honestly / fairly | YES | Original guide cannot have been a good-faith estimate given vendor expectations |
| Underquoting | YES | Price guide materially below eventual sale price; multiple upward revisions |
| Advertising at misleading prices | YES | Advertised at $2.1m when property sold for $2.85m |
| Misleading advertising | YES | Advertising created a misleading impression of the property's value |

---

## Example 2 — Rejected offer, price guide not updated

> ***[Agent B]** of **[Agency B]**, Eastern Suburbs, engaged in underquoting on a property subsequent to my rejected offer, and failed to update the price guide.*
>
> *I offered $1.4m verbally, and then via email on **[Property 2]**, Beachside Suburb NSW, on 17/02/2026. The agent called and rejected the offer at 1:55pm on 18/02/2026.*
>
> *Before close of business on 18/02/2026, my husband emailed and asked for the guide, to which the agent replied "$1.25m".*
>
> *On 19/02/2026 the guide advertised online was $1.25m — below the offer that had already been rejected the previous day.*

### Correct theme labels

| Theme | Applies | Reasoning |
|---|---|---|
| Unsatisfactory behaviour by strata manager/agent | YES | Agent's failure to update guide after rejection is unsatisfactory conduct |
| Agent failure to act honestly / fairly | YES | Quoting $1.25m guide after rejecting a $1.4m offer is misleading |
| Underquoting | YES | Published guide ($1.25m) is below the rejected offer ($1.4m) |
| Advertising at misleading prices | YES | Advertising $1.25m when agent knew $1.4m was insufficient |
| Misleading advertising | YES | Published guide creates false impression of achievable price |

---

## Key labelling challenges illustrated

### Challenge 1: Multi-label output
Both examples require 5 themes each. The most common classifier failure is returning only the most obvious theme (Underquoting) and missing the others. The prompt must explicitly allow list output and the judge must specifically check for completeness.

### Challenge 2: Theme boundary — Underquoting vs Advertising at misleading prices
These themes often co-occur but are distinct:
- **Underquoting** is about the gap between the guide and the likely/eventual selling price
- **Advertising at misleading prices** is specifically about the advertised price being misleading

Both apply when the guide is both below likely value AND published as advertising.

### Challenge 3: Inference vs explicit statement
Example 2 does not say "this is misleading." The LLM must infer that quoting $1.25m after rejecting a $1.4m offer constitutes misleading behaviour. This requires the classifier to reason about the sequence of events, not just keyword-match on theme terms.

---

## Using these examples in your eval suite

```python
GOLD_SET = [
    {
        "id": "example_1",
        "complaint_summary": "Agency A — price guide $2.1m, sold $2.85m, two guide increases during campaign",
        "themes": [
            "Unsatisfactory behaviour by strata manager/agent",
            "Agent failure to act honestly / fairly",
            "Underquoting",
            "Advertising at misleading prices",
            "Misleading advertising"
        ],
        "challenge_flags": ["multi_label", "theme_boundary"]
    },
    {
        "id": "example_2",
        "complaint_summary": "Agent B — offer $1.4m rejected, guide published at $1.25m next day",
        "themes": [
            "Unsatisfactory behaviour by strata manager/agent",
            "Agent failure to act honestly / fairly",
            "Underquoting",
            "Advertising at misleading prices",
            "Misleading advertising"
        ],
        "challenge_flags": ["multi_label", "inference_required", "sequential_reasoning"]
    }
]
```

---

*Back: [Overview](Overview) | Next: [The Taxonomy](The-Taxonomy)*
