# PROJECT_KNOWLEDGE_BASE: Hospital Assistant Robot

This document serves as the definitive technical reference for the Hospital Assistant Robot. It is designed to provide an AI or developer with a complete understanding of the system architecture, logic flows, and implementation details.

---

## 1. System Architecture: Multi-Process Orchestration

The system follows a **decentralized multi-process architecture** using Python's `multiprocessing` module. This design ensures that compute-intensive tasks (Vision) do not block real-time responsiveness (Interaction/Audio).

### Inter-Process Communication (IPC)
The processes communicate via two primary mechanisms:
1.  **Shared Queues (`multiprocessing.Queue`)**:
    *   `audio_queue`: Used to send playback requests (file paths or commands) to the `AudioManager`.
    *   `motor_queue`: Used to send movement commands (e.g., `turn_to:90`) to the `MotorControl` process.
2.  **Shared Events (`multiprocessing.Event`)**:
    *   `shutdown_flag`: System-wide signal to terminate all processes gracefully.
    *   `audio_playing_flag`: A binary state indicator. When `True`, background vision/cough announcements are deferred to avoid overlapping with high-priority user interaction audio.

---

## 2. Process Breakdown

### 2.1 The Orchestrator (`main.py`)
*   **Role**: Initializes shared resources (Queues, Events) and spawns child processes.
*   **Logic**:
    *   Uses a dictionary `processes = {}` to track subprocess objects.
    *   Implements a robust `KeyboardInterrupt` handler that sets the `shutdown_flag` and calls `.join(timeout=...)` on all children, followed by `.terminate()` if they hang.

### 2.2 The Brain: Interaction Process (`interaction_process.py`)
*   **Role**: Handles Speech-to-Text (STT), natural language understanding (NLU), and response coordination.
*   **Core Logic**:
    *   **STT**: Uses `speech_recognition` (SR) with a background listener thread.
    *   **NLU Hierarchy (Tiered)**:
        1.  **Tier 1: Keyword-Based Interactions**: Direct lookup in `interactions` section of `hospital_knowledge_base.json`.
        2.  **Tier 2: Navigational Logic**: Matches keywords for hospital departments (e.g., "Cardiology") and provides location/doctor info.
        3.  **Tier 3: LLM Fallback**: If Tiers 1 & 2 yield no match, the query is sent to the **Groq API (Llama 3.1)** for a generative response.
    *   **Medical Safety**: A strict `is_medical_query` check filters out queries asking for diagnosis or medication, providing a predefined refusal message.
    *   **Audio Background Monitoring**: Identifies loud sudden noises (dB threshold) to trigger cough/sneeze health reminders.

### 2.3 The Eyes: Vision Process (`vision_process.py`)
*   **Role**: Environment monitoring using YOLOv8.
*   **Capabilities**:
    *   **Person Detection**: Uses `ultralytics` YOLOv8n model on `Picamera2` frames.
    *   **Crowd Analysis**: Monitors population density; triggers "Overcrowding" alerts if thresholds (default: 25) are exceeded.
    *   **Social Distancing**: Calculates Euclidean distances between centroids; triggers alerts for proximity violations.
    *   **Queue Formation**: Uses hierarchical clustering (`scipy.cluster.hierarchy`) to detect line-like formations and encourages orderly queuing.

### 2.4 The Voice: Audio Manager (`pyaudio_player.py` / `audio_manager.py`)
*   **Role**: Non-blocking audio playback server.
*   **Logic**:
    *   Standardizes playback using `pygame.mixer` or `pyaudio`.
    *   Manages the `audio_playing_flag` to coordinate with other processes.
    *   Implements an "Interrupt" capability: incoming high-priority interaction audio can stop current background alerts.

### 2.5 The Movement: Motor Control (`motor_control_process.py`)
*   **Role**: Hardware abstraction for physical movement.
*   **Logic**:
    *   Listens for string commands on `motor_queue`.
    *   Translates commands (e.g., `turn_to:30`) into serial characters (`L`, `R`, `C`) sent over UART (`/dev/ttyS0`) to an external microcontroller (e.g., Arduino).

---

## 3. Support Infrastructure

### 3.1 Centralized Logging (`logging_config.py`)
*   **Mechanism**: Uses `logging.handlers.TimedRotatingFileHandler`.
*   **Storage**: Logs are stored in `logs/robot_run.log`.
*   **Rotation**: Daily rotation at midnight, keeping a 7-day backup history.
*   **Levels**: Console output is filtered to `INFO`, while the log file captures the full `DEBUG` stream for deep investigation.

### 3.2 State Management (`shared_state.py`)
*   Provides standardized integer constants to represent the robot's current lifecycle state:
    *   `STATE_IDLE` (0): Waiting for user.
    *   `STATE_LISTENING` (1): Audio capture active.
    *   `STATE_SPEAKING` (2): TTS output active.
    *   `STATE_PROCESSING` (3): NLU/LLM compute in progress.
    *   `STATE_ERROR` (-1): System failure state.

---

## 4. Data Structure: Knowledge Base (`hospital_knowledge_base.json`)

The KB is a standard JSON file containing:
*   **`departments`**: List of IDs, canonical names, and multilingual keywords/locations.
*   **`interactions`**: Pre-defined Q&A pairs for common queries (Greetings, Identity, Canteen, etc.).
*   **`services`**: Keywords for specific diagnostics (X-Ray, CT Scan).
*   **`languages`**: Supported codes (`en`, `hi`, `te`).

---

## 4. Maintenance and Validation

### 4.1 Diagnostic Layer
*   `check_system.py`: A comprehensive health check script validating internet, microphone, camera, speaker, and disk space.

### 4.2 Verification Suite
*   `run_comprehensive_tests.py`: A robust test runner that uses **Mocks** to simulate a full interaction cycle without requiring hardware or active LLM credits.
*   `generate_tests.py`: Generates large-scale JSON test data from the Knowledge Base keywords.

---

## 5. Technical Stack
*   **Language**: Python 3.10+
*   **AI Models**: YOLOv8 (Vision), Llama 3.1 via Groq (LLM).
*   **Libraries**: `multiprocessing`, `speech_recognition`, `pygame`, `cv2`, `picamera2`, `scipy`.
*   **Communication**: UART/Serial for motors, HTTPS for Groq, Local IPC for processes.
