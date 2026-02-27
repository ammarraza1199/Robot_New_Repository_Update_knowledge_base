# Resolution Plan: Addressing API Failures & Hallucinations

**Date:** 2026-02-20
**Target Component:** `interaction_process.py`
**Objective:** Eliminate API rate limit errors and reduce hallucinations by enforcing strict Keyword Matching before LLM fallback.

## 1. Problem Diagnosis

Our recent 2080-question simulation revealed two critical failures:
1.  **API Rate Limits (45% Failure):** The system spammed the LLM API, hitting `429 Too Many Requests`.
2.  **High Hallucination Rate (41%):** The LLM provided incorrect departments (e.g., "Ophthalmology" for "Fever") because it was guessing instead of using the Knowledge Base.

**Root Cause:**
The **Logic-First approach is failing**. The system is supposed to check formatting keywords locally *before* asking the LLM. However, looking at the logs:
-   User Input: "fever"
-   System Action: Calls LLM -> `query_llama`
-   Result: 429 Error or Hallucination.

This proves that `find_department()` in `interaction_process.py` is returning `None` even for known keywords like "fever". This forces the system to rely 100% on the LLM, which triggers the rate limits and errors.

## 2. Technical Solution Plan

### Step 1: Fix Keyword Loading Logic (`interaction_process.py`)
**Problem:** The `load_knowledge_base` function or `find_department` function likely has a normalization issue where inputs aren't matching the JSON keys exactly (e.g., case sensitivity, whitespace, or encoding issues).

**Action:**
1.  Debug `load_knowledge_base`: Print the loaded `keyword_index` to verify keywords are actually in memory.
2.  Update `find_department`:
    -   Implement aggressive unicode normalization (NFC) to handle Hindi/Telugu characters correctly.
    -   Ensure case-insensitive matching is robust using `.casefold()`.
    -   Add debug logs to show *why* a match failed (e.g., "Input: 'fever', Keywords matched: []").

### Step 2: Implement "Strict-Filter" LLM Logic
**Problem:** Even when we resort to the LLM, we are sending the *entire* department list, which confuses the model (Context Leakage), causing it to pick "Ophthalmology" just because it's on the list.

**Action:**
1.  **Prioritize General Medicine:** If the LLM prompt contains vague keywords (pain, weakness, fever), strictly inject a system instruction to favor "General Medicine".
2.  **Filter Department List:** Do not send specialized departments (like "Nuclear Medicine" or "Vascular Surgery") to the LLM for simple queries. Reduce the context window to common departments.

### Step 3: API Rate Limit Protection
**Problem:** A `while` loop test script can fire 10 requests per second, instantly getting banned.

**Action:**
1.  **Backoff Strategy:** Modify `query_llama` to catch `429` errors, wait 2 seconds, and retry *once*.
2.  **Test Script Delay:** Add `time.sleep(1.0)` between injections in `master_acoustic_test.py` to simulated realistic user interaction speed.

## 3. Implementation Checklist

- [ ] **Debug**: Create a tiny script `debug_keywords.py` that imports `interaction_process.py` and tests `find_department("fever")`. This will confirm the bug instantly.
- [ ] **Refactor**: Modify `interaction_process.py` to fix the matching bug found above.
- [ ] **Patch**: Update `query_llama` with a retry mechanism for 429 errors.
- [ ] **Verify**: Re-run a small 50-question simulation. We expect **0 LLM calls** for words like "fever" and 100% match rate.

## 4. Expected Outcome
| Metric | Current | Expected After Fix |
| :--- | :--- | :--- |
| **LLM Calls** | 100% of queries | < 20% (Only for true unknown queries) |
| **API Errors** | 45% | < 1% |
| **Accuracy** | 13.5% | > 85% |
| **Latency** | High (Network Dependent) | Instant (Local Match) |

## 5. Next Steps
1.  Approve this plan.
2.  I will run the `debug_keywords.py` script to isolate the exact line of code causing the failure.
3.  Apply the fix to `interaction_process.py`.
