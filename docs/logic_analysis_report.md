# Logic Analysis: Unexpected Redirections

**Issue Verified:** User reported unexpected redirections to **Ophthalmology** and **Orthopaedics** (Hallucinations).

## 1. The "Ophthalmology" Hallucination
You are seeing "Ophthalmology" results because of how the LLM Fallback works vs. standard Keyword Matching.

*   **Standard Logic (Reference)**: In `interaction_process.py`, there is a `REDIRECT_DEPARTMENTS` list that explicitly forces "Ophthalmology" queries to go to "General Medicine". This works fine for exact keywords like "eye" or "ophthalmology".
*   **The Problem (LLM Bypass)**: When the user asks a question that *doesn't* exactly match a keyword (e.g., "I have eye irritation"), the system falls back to the LLM (AI Brain).
*   **Why it happens**: The LLM is given the *entire* list of departments from `hospital_knowledge_base.json` as context. Since **"Ophthalmology" exists as a valid department in your JSON file**, the LLM sees it and correctly recommends it. **The LLM is unaware of the hardcoded redirect rule.**

**Solution Options:**
1.  **Remove the Department**: Delete the "Ophthalmology" entry from `data/hospital_knowledge_base.json` if it shouldn't exist at all.
2.  **Update Context**: Update `interaction_process.py` to filter out redirected departments before sending them to the LLM.

## 2. The "Orthopaedics" Redirection
You are being sent to Orthopaedics because of **Duplicate Keywords** in your Knowledge Base.

*   **Conflict Found**: The keyword **"back ache"** is listed in BOTH **General Medicine** AND **Orthopaedics**.
*   **Logic**: The system loads departments in order. Since "Orthopaedics" is loaded *after* "General Medicine" in the JSON file, it overrules the previous entry.
*   **Result**: Any user mentioning "back ache" is automatically routed to **Orthopaedics**.

**Other Duplicates Found:**
*   **"bp" / "blood pressure"**: Exists in both **General OPD** and **General Medicine**.
*   **"dizziness"**: Exists in **General Medicine**, **Cardiology**, and **Neurology**.

## 3. Summary of Findings
| Symptom | Routed To | Why? |
| :--- | :--- | :--- |
| "Eye irritation" | **Ophthalmology** | LLM sees hidden "Ophthalmology" dept in JSON and recommends it (Bypasses redirect). |
| "Back ache" | **Orthopaedics** | Duplicate keyword. Orthopaedics overwrites General Medicine. |
| "Blood Pressure" | **General Medicine** | Duplicate keyword. General Medicine overwrites General OPD. |

I recommend cleaning up `data/hospital_knowledge_base.json` to remove these duplicates and hidden departments to fix this behavior permanently.
