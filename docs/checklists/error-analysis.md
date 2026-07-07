# Checklist: Error Analysis Session

Run this before starting any error analysis session. The structure prevents the two most common mistakes: jumping to automated clustering before reading data, and fixing the easiest cluster instead of the highest-impact one.

---

## Before the session

- [ ] Minimum **50 failure cases** collected (below eval threshold)
- [ ] Cases stratified — not all from the same complaint type or date range
- [ ] Ground truth available for each case (gold label or verified answer)
- [ ] Session blocked in calendar — allow **2–4 hours minimum**

## During the session

### Step 1: Read before you cluster
- [ ] Manually read **at least 20 cases** before opening any clustering tool
- [ ] Write down 3–5 hypotheses about root causes after reading
- [ ] Note any cases that seem "different" — edge cases often reveal taxonomy gaps

### Step 2: Cluster by root cause
- [ ] Group cases by **why** they failed, not by **how** they failed
- [ ] Label each cluster with a root cause category:
  - Prompt ambiguity
  - Taxonomy gap
  - Multi-label blind spot
  - Retrieval failure (UC2)
  - Training data gap
  - Model overconfidence on edge case

### Step 3: Prioritise
- [ ] Score each cluster: **Frequency × Severity × Fixability**
- [ ] Identify the **highest-impact cluster** (not the easiest one)
- [ ] Document the prioritisation rationale

### Step 4: Hypothesise and test
- [ ] Propose **one targeted fix** for the top cluster
- [ ] Test fix on the **failing cluster only** first
- [ ] Run full eval suite to check for **regressions in other clusters**
- [ ] Only deploy if: cluster improves AND no regressions

## After the session

- [ ] Fixed cases **added to gold set** to prevent future regression
- [ ] Root cause and fix **documented** in this wiki
- [ ] Session findings shared with team
- [ ] **Next error analysis session** scheduled (recommended: monthly)
