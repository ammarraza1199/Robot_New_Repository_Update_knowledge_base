# Implementation Plan - Final Deployment Readiness

## Goal Description
Resolve all NLU failures, specifically the "Neurology" misclassification, and achieve >90% pass rate in stress tests. Ensure the `hospital_knowledge_base.json` is robust and handles all keywords, including intentional misspellings, correctly across all languages.

## User Review Required
> [!IMPORTANT]
> The "Brute Force" test will validate EVERY single keyword in the KB. Any failure here effectively means a keyword defined in the JSON is not working as intended in the code.

## Proposed Changes

### Knowledge Base Optimization
#### [MODIFY] [hospital_knowledge_base.json](file:///c:/Users/DELL/Downloads/ZeroKost/Robot_code/Robot_New_Repository_Update_knowledge_base-4.1.1/Robot_New_Repository_Update_knowledge_base-4.1.1/hospital_knowledge_base.json)
- **Deduplication Strategy**:
    - Identify unique keywords across all departments.
    - Resolve collisions:
        - `fever`, `weakness`, `cough` -> Assign to **General Medicine** (remove from General OPD).
        - Specific heart symptoms -> Ensure unique to **Cardiology**.
    - Remove overlapping "Interaction" keywords that collide with "Departments".

### Code Improvements
#### [MODIFY] [interaction_process.py](file:///c:/Users/DELL/Downloads/ZeroKost/Robot_code/Robot_New_Repository_Update_knowledge_base-4.1.1/Robot_New_Repository_Update_knowledge_base-4.1.1/interaction_process.py)
- Add warning logs during KB loading if duplicate keywords are detected.

## Verification Plan
### Automated Tests
- **Re-run Brute Force Test**: `python tests/run_kb_brute_force.py`
    - **Success Criteria**: >95% Pass Rate (allowing for some intentional aliases).
- **Stress Test**: `python tests/run_brutal_stress_tests.py`

### Manual Verification
- Verify critical flows (General OPD triage vs Specialist access) via mock script.

