# Hospital Assistant Robot

The Hospital Assistant Robot is an intelligent system designed to operate in a hospital environment, providing assistance through a combination of computer vision, natural language understanding, and automated responses. It is built with a modular, multi-process architecture to ensure real-time responsiveness and efficient resource management.

## Key Features:

*   **Environmental Monitoring (Vision)**: Utilizes YOLOv8 for real-time person detection, crowd analysis, social distancing monitoring, and queue formation detection.
*   **Natural Language Interaction**: Employs Speech-to-Text (STT) and a tiered Natural Language Understanding (NLU) system with a Groq LLM (Llama 3.1) fallback for intelligent conversational capabilities.
*   **Audio Management**: Provides non-blocking audio playback for announcements and interactive speech.
*   **Motor Control**: Interfaces with external hardware for physical movement based on commands.
*   **Comprehensive Logging**: Detailed logging for all processes to aid in debugging and monitoring.

## Performance Metrics

*   **Natural Language Understanding (NLU) Pass Rate**: The comprehensive test suite (`scripts/run_comprehensive_tests.py`) indicates a **96.68%** pass rate for understanding and responding to various user queries across multiple languages, leveraging the knowledge base and LLM fallback.

    *Note: Performance metrics for the YOLOv8 object detection model (e.g., mAP) are not included in the existing test suite and would require a dedicated evaluation dataset and script.*

## Getting Started:

To set up and run the robot application, please refer to the `HOW_TO_RUN.md` guide:

*   [**HOW_TO_RUN.md**](HOW_TO_RUN.md) - Detailed instructions for environment setup, dependency installation, and launching the application.

## System Architecture:

For a deep dive into the robot's design, including its folder structure, inter-process communication, overall workflow, and NLU logic, consult the `ARCHITECTURE.md` document:

*   [**ARCHITECTURE.md**](ARCHITECTURE.md) - Explains the high-level architecture, process breakdown, and communication patterns.

## Project Knowledge Base:

For in-depth technical details about the system's components, data structures, and implementation specifics, refer to the `PROJECT_KNOWLEDGE_BASE.md`:

*   [**PROJECT_KNOWLEDGE_BASE.md**](docs/PROJECT_KNOWLEDGE_BASE.md) - A comprehensive technical reference for AI and developers.

## Core Technologies:

*   **Language**: Python 3.10+
*   **AI Models**: YOLOv8 (Vision), Llama 3.1 via Groq (LLM)
*   **Key Libraries**: `multiprocessing`, `ultralytics`, `SpeechRecognition`, `pyaudio`, `pygame`, `numpy`, `pyserial`.
*   **Hardware Integration**: Picamera2, UART for motor control.
