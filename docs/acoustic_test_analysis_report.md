# Acoustic Test Analysis Report
**Date:** 2026-02-20
**Test Run ID:** `acoustic_test_results_20260220_114146.csv`
**Total Questions:** 2080

## 1. Executive Summary

The full-scale acoustic simulation revealed significant issues with the current system's stability and logic. The overall success rate was **13.5%**, heavily impacted by API rate limits and logic failures where simple keyword matches were missed, forcing unnecessary calls to the LLM.

| Metric | Count | Percentage | Description |
| :--- | :--- | :--- | :--- |
| **Total Questions** | **2080** | 100% | Full dataset simulation |
| **Correct Answers** | **281** | **13.5%** | Correct Department or Safe Fallback |
| **API Failures** | **934** | **44.9%** | "Sorry, I'm having trouble connecting to my brain." |
| **Hallucinations** | **865** | **41.6%** | Incorrect Department or Irrelevant Response |

> [!CRITICAL]
> **Nearly 45% of all queries failed due to API Rate Limits.** This confirms that the system is currently **unusable for high-traffic or continuous testing** without implementing rate limiting or caching.

## 2. Detailed Breakdown

### 2.1 Correctness by Language
The system performed best in English, though still with low accuracy. Telgu had a higher "Correct" count largely due to more "Safe Fallback" responses (e.g., "Cannot provide medical advice") which were counted as valid for general queries.

| Language | Correct | Failed (API) | Total | Success Rate |
| :--- | :--- | :--- | :--- | :--- |
| **English** | 158 | 323 | 825 | 19.1% |
| **Hindi** | 25 | 265 | 560 | 4.5% |
| **Telugu** | 98 | 346 | 695 | 14.1% |

### 2.2 Hallucination Patterns
A "Hallucination" in this context refers to the robot providing a confident but incorrect department, or a response that makes no sense.

**Common Hallucination Types:**
1.  **Critical Misrouting**:
    -   *Symptom:* "Weakness"
    -   *Robot:* "Neurology" (Expected: General Medicine)
    -   *Symptom:* "Fever"
    -   *Robot:* "Pediatrics" (Expected: General Medicine / Emergency)
    -   *Symptom:* "Body Pain"
    -   *Robot:* "Heart Disease Dept" or "Rheumatology" (Expected: General Medicine)
2.  **Context Leakage**:
    -   The LLM seems to select departments that appear later in the context list (e.g., Ophthalmology, Orthopedics) simply because they are available options, ignoring the "General" nature of the query.
    -   *Example:* "Eye" -> "Ophthalmology" (Correct), but "Heart" -> " Orthopedics" (Incorrect - random Hallucination seen in logs).

## 3. Root Cause Analysis

### 3.1 The "Keyword Match" Failure (Critical Finding)
The logs reveal that simple keywords like **"fever"**, **"weakness"**, and **"body pain"**—which exist in the Knowledge Base—are **NOT triggering the local keyword search**.
-   **Evidence:** The logs show `LLM request completed` for queries like "fever".
-   **Impact:** Instead of an instant, offline, 100% accurate match, the system calls the LLM.
-   **Consequence:**
    1.  **Wastes API Quota**: Leading to the 429 Rate Limit errors.
    2.  **Introduces Hallucinations**: The LLM is less deterministic than the keyword search.

**Why is it failing?**
The `interaction_process.py` script likely has a mismatch between the loaded language codes (`en`, `hi`, `te`) or the text normalization process strips necessary characters, causing the lookup `keyword_index[lang]` to miss the match.

### 3.2 API Rate Limiting
The test script ran 2080 queries as fast as possible. The Groq API (or the tier being used) has a rate limit (likely tokens/minute or requests/minute).
-   **Result:** After the first ~100 queries, the API started rejecting requests with `429 Too Many Requests`.
-   **Fix:** Implement a delay (`time.sleep(2)`) in the test script or use a paid/higher-tier API key.

## 4. Recommendations

### Immediate Fixes
1.  **Debug Keyword Loading**: Investigate `interaction_process.py` to ensure `general_medicine` keywords are actually loaded and matched. **This is the single biggest fix for accuracy.**
2.  **Rate Limiting**: Add a 2-second delay between requests in `master_acoustic_test.py` to prevent API bans during testing.

### Logic Improvements
1.  **Restrict LLM Scope**: Modify the System Prompt to explicitly prioritize "General Medicine" for vague symptoms if the keyword match fails.
2.  **Hardcoded Redirects**: Ensure the `REDIRECT_DEPARTMENTS` logic in `interaction_process.py` is actually reachable. Currently, the LLM response (e.g., "Emergency Department") might not exactly match the key needed to trigger the redirect.

## 5. Conclusion
The current system is **not production-ready** due to the bypassing of local keyword logic. Fixing the keyword matcher will likely boost accuracy from **13.5% to >80%** (since most test queries are simple keywords) and eliminate the API rate limit issues by reducing LLM calls.
