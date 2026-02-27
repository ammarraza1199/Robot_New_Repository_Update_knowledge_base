# Hospital Robot: System Feature Report

**Platform**: Raspberry Pi 5 / miniDSP / Audio Card / Arduino  
**Software Version**: Hospital Assistant v6.1  
**Core Technologies**: Python 3.10+, YOLOv8, Llama 3.1 LLM, Picamera2

---

## 1. Hardware-Integrated Feature Set

### A. Intelligent Audio System (miniDSP + Audio Card)
*   **Self-Healing Device Detection**: Automatically scans and identifies the "miniDSP" microphone array upon startup. If disconnected, it attempts to fall back to the first available input, ensuring robust operation in fluctuating hardware setups.
*   **High-Fidelity Output**: Leverages the 8ohm speaker via a dedicated Audio Card for clear announcements in noisy hospital environments.
*   **Interrupt Capability**: Prioritizes user interaction over background events. If a user says "Hello" while a vision alert is playing, the system instantly halts the alert to listen.
*   **Sudden Noise Alert**: Uses dB threshold analysis to detect coughing or sneezing and politely offers health advice (e.g., "Please wear a mask if you are unwell").

### B. Advanced Vision Intelligence (Raspberry Pi 5 + Picamera2)
*   **Crowd Density Monitoring**: Real-time analysis of population count using YOLOv8. If the count exceeds a threshold (Default: 25), it triggers "Overcrowding" alerts to manage patient flow.
*   **Social Distancing Enforcement**: Calculates distances between individuals and gently reminds them to maintain safe separation.
*   **Queue Discipline**: Detects linear formations of people and encourages orderly queuing behavior.

### C. Motor Control & Movement (Arduino Interface)
*   **Directional Orientation**: Receives high-level commands (e.g., `turn_to:45`) and translates them into serial signals (`L`, `R`) for the Arduino motor controller, allowing the robot to physically face the user or area of interest.

---

## 2. Natural Language Understanding (NLU) Features

### A. Tiered Intelligence Architecture
The robot uses a sophisticated 3-tier system to answer questions:
1.  **Tier 1: Instant Answers**: Immediate responses for greetings, identity queries (e.g., "Who are you?"), and basic FAQ items stored locally in `hospital_knowledge_base.json`.
2.  **Tier 2: Department Routing**: Matches keywords (e.g., "Heart", "Cardiology", "Chest Pain") to specific locations and doctors, even guiding users across multiple languages (English, Hindi, Telugu).
3.  **Tier 3: Generative AI (Llama 3.1)**: Handles complex, unstructured queries by sending them to the Groq API, providing human-like explanations when simple keywords fail.

### B. Safety & Ethics
*   **Medical Advice Guardrails**: A strict filter prevents the robot from diagnosing illnesses or prescribing medication. Queries like "What pill should I take?" are met with a safe refusal and a recommendation to see a doctor.

### C. Multilingual Support
*   **Language Detection**: Automatically detects the language spoken (English, Hindi, Telugu) based on grammar anchors and specific keywords.
*   **Cross-Lingual Fallback**: If a term isn't found in the spoken language, it searches the knowledge base across all supported languages to find a match.

---

## 3. Reliability & Maintenance Features

*   **Log Rotation**: Automatically archives old logs and rotates daily to prevent disk space exhaustion.
*   **Crash Recovery**: The Multi-Process Architecture ensures that if one component (e.g., Vision) fails, the main Interaction loop can continue functioning or restart the failed process.
*   **Diagnostic Tools**: Includes `check_system.py` to validate hardware health (Mic, Cam, Internet) before full deployment.
