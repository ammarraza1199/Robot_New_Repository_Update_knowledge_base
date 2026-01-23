# Hospital Assistant Robot - Knowledge Transfer Document

## 1. Overview

This document provides a comprehensive overview of the Hospital Assistant Robot application. The robot is designed to be deployed in a hospital reception area to assist visitors with navigation, answer questions, and monitor the environment for safety and compliance with health guidelines.

The system is built on a robust, multi-process architecture where each core functionality (vision, interaction, audio, motor control) runs as a separate, independent process. This design ensures stability, as a crash in one process will not bring down the entire system. Communication between these processes is handled safely via message queues.

## 2. Implemented Features

-   **Multilingual Conversational AI:** The robot can understand and respond to user queries in English, Hindi, and Telugu.
-   **Rule-Based Navigation:** For direct queries about hospital departments (e.g., "Where is cardiology?"), the system uses a local, rule-based knowledge base to provide immediate and accurate directions.
-   **LLM-Powered General Q&A:** For more general questions, the system uses the Llama 3.1 language model (via the Groq API) to provide helpful responses.
-   **Crowd & Social Distancing Monitoring:** Using a camera and the YOLOv8 object detection model, the system continuously monitors the number of people and their proximity to each other, triggering audio alerts for overcrowding or social distancing violations.
-   **Queue Formation Detection:** The vision system can detect when a group of people forms a line, triggering an announcement to encourage orderly queuing.
-   **Cough & Sneeze Detection:** The robot's microphone listens in the background for loud, sudden noises (like coughs or sneezes) and plays a health reminder announcement.
-   **Audio Interrupt System:** The audio manager is designed to prioritize spoken responses to users. If the robot is making a general announcement (e.g., for overcrowding), and a user speaks to it, the announcement will be immediately interrupted to provide a responsive user experience.
-   **Simulated Motor Control:** The system includes a motor control process that is ready to be integrated with hardware. It currently simulates turning actions based on user interaction.

## 3. Codebase Structure and Explanation

The application is composed of several key Python scripts, each responsible for a specific domain.

---

### `main.py`

*   **Purpose:** This is the main entry point and orchestrator of the entire application. It is responsible for starting all the other processes and managing a graceful shutdown.
*   **Code Explanation:**
    *   It initializes `multiprocessing.Queue` objects (`audio_queue`, `motor_queue`) that serve as the communication channels between the processes.
    *   It creates a `shutdown_flag` and an `audio_playing_flag` (`multiprocessing.Event`), which are shared with the child processes to signal state changes.
    *   It defines a dictionary of all the core processes (`vision`, `interaction`, `audio`, `motor`) and starts them.
    *   The main process then waits indefinitely. When a `KeyboardInterrupt` (Ctrl+C) is detected, it sets the `shutdown_flag` and sends a "shutdown" message to the queues, signaling all child processes to terminate cleanly.
    *   It includes a robust shutdown sequence with `p.join(timeout=...)` and `p.terminate()` to ensure no zombie processes are left behind.

---

### `interaction_process.py`

*   **Purpose:** This is the "brain" of the robot. It handles all user interaction, processing spoken language, understanding intent, and deciding on the appropriate response. It also manages the background audio monitoring for coughs/sneezes.
*   **Code Explanation:**
    *   **`InteractionProcess` Class:**
        *   `__init__`: Initializes the speech recognition library (`sr`), loads the multilingual knowledge base (department keywords, doctors, room numbers), and sets up parameters for cough detection.
        *   `_background_callback`: This is the core of the interaction logic. It runs in a background thread managed by the `speech_recognition` library.
            1.  It first attempts to recognize any captured audio as speech.
            2.  If speech is recognized, it calls `process_command` to handle the user's query.
            3.  If speech is *not* recognized (i.e., it's a non-speech sound), it calculates the audio's volume (dB level). If the volume exceeds a dynamic threshold, it's classified as a "sudden sound," and the cough/sneeze announcement is queued.
        *   `process_command`: Takes the recognized text, determines if it's a navigation query, a medical query (which it deflects), or a general question for the LLM. It then queues the appropriate audio response and motor commands.
        *   `query_llama`: Formats a prompt and sends the user's query to the Groq API to get a response from the Llama 3.1 model.
        *   `start`: The main entry point for the process. It calibrates the microphone for ambient noise and then starts the `listen_in_background` method, which runs the `_background_callback` continuously.

---

### `vision_process.py`

*   **Purpose:** This process is the "eyes" of the robot. It uses the camera to see the environment, detect people, and analyze crowd behavior.
*   **Code Explanation:**
    *   **`VisionProcess` Class:**
        *   `__init__`: Initializes the PiCamera and loads the `yolov8n.pt` model. This initialization is wrapped in a `try...except` block to prevent the process from crashing if the camera or model file is not found.
        *   `detect_people`: Captures a frame from the camera and passes it to the YOLO model to get the coordinates of all detected people.
        *   `analyze_crowd`: This is the main analysis function. It takes the list of detected people and:
            1.  Checks for overcrowding by counting the number of people.
            2.  Checks for social distancing violations by calculating the distance between all pairs of people.
            3.  Calls `detect_queue_formation` to check for queues.
            4.  Queues the appropriate audio announcements based on the results, using a cooldown system to avoid spamming.
        *   `detect_queue_formation`: A new function that analyzes the positions of people to see if they are clustered in a line-like shape.
        *   `run`: The main loop for the process. It runs continuously, capturing frames, calling the analysis functions, and handling graceful shutdown. It includes error handling for camera frame capture to prevent crashes during runtime.

---

### `audio_manager.py`

*   **Purpose:** This process acts as a dedicated, non-blocking server for playing audio. It ensures that only one audio file plays at a time and handles the interrupt logic.
*   **Code Explanation:**
    *   **`AudioManager` Class:**
        *   `__init__`: Initializes the audio queue and a `currently_playing` state variable.
        *   `start`: The main loop. It's designed to be non-blocking. In each iteration, it first checks for new messages on the queue (e.g., `'play'` or `'stop'`) and then checks the status of the music player.
        *   `handle_request`: Processes incoming commands. A `'play'` command loads and plays a file, and a `'stop'` command immediately halts any playing audio.
        *   The main loop (`start`) is responsible for detecting when a sound has *finished* playing (`pygame.mixer.music.get_busy()` is false), at which point it clears the `audio_playing_flag` to signal to other processes that the robot is no longer speaking.

---

### `motor_control_process.py`

*   **Purpose:** This file is a template for controlling the robot's physical movements. It listens for commands and is designed to be easily extended with hardware-specific code.
*   **Code Explanation:**
    *   **`MotorControl` Class:**
        *   The code is structured with clear, commented-out sections (e.g., `Step 1: Uncomment...`, `Step 2: Define your GPIO pins...`).
        *   `_setup_hardware` and `cleanup` are placeholder methods where hardware initialization and cleanup code (e.g., `GPIO.setmode`, `GPIO.cleanup`) should go.
        *   `_turn_degrees`: A placeholder function that simulates turning, showing where the actual stepper motor logic would be implemented.
        *   `handle_command`: Parses commands from the `motor_queue` (e.g., `turn_to:90`) and calls the appropriate placeholder functions.

## 4. How to Run the Application

### Prerequisites

1.  A Raspberry Pi or similar Linux-based system.
2.  Python 3.10+ installed.
3.  A connected camera (e.g., PiCamera) and microphone.
4.  An internet connection (for API access).

### Setup and Run (Development Mode)

1.  **Create Virtual Environment:**
    ```bash
    python3 -m venv .venv
    ```

2.  **Activate Virtual Environment:**
    ```bash
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create Environment File:**
    Create a file named `.env` in the project root and add your Groq API key:
    ```
    GROQ_API_KEY="YOUR_API_KEY_HERE"
    ```

5.  **Run the Application:**
    ```bash
    python main.py
    ```
    Press `Ctrl+C` to stop the application gracefully.

### Run as a Service (Deployment Mode)

For deployment, the included `hospital-robot.service` file should be used to manage the application.

1.  **Install the Service:**
    ```bash
    sudo cp hospital-robot.service /etc/systemd/system/
    ```

2.  **Reload the systemd Daemon:**
    ```bash
    sudo systemctl daemon-reload
    ```

3.  **Enable the Service to Start on Boot:**
    ```bash
    sudo systemctl enable hospital-robot.service
    ```

4.  **Start the Service Immediately:**
    ```bash
    sudo systemctl start hospital-robot.service
    ```

## 5. Service Management Commands

Once the application is running as a service, use these commands to manage it:

*   **Check Status:**
    ```bash
    sudo systemctl status hospital-robot.service
    ```

*   **View Live Logs (Very Important for Debugging):**
    ```bash
    sudo journalctl -u hospital-robot.service -f
    ```

*   **Stop the Service:**
    ```bash
    sudo systemctl stop hospital-robot.service
    ```

*   **Restart the Service:**
    ```bash
    sudo systemctl restart hospital-robot.service
    ```
