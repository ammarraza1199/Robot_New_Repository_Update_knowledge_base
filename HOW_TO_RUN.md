# How to Run the Hospital Assistant Robot

This document provides instructions on how to set up and run the Hospital Assistant Robot application.

## 1. Prerequisites

Before you begin, ensure you have the following:

*   **Hardware:**
    *   A compatible Single Board Computer (SBC) like Raspberry Pi (especially for `Picamera2` support).
    *   Picamera2 camera module connected and configured.
    *   Speakers for audio output.
    *   Microphone for speech input.
    *   An external microcontroller (e.g., Arduino) connected via UART for motor control (if physical movement is required).
*   **Software:**
    *   Python 3.10 or higher installed.
    *   `pip` (Python package installer).
    *   `venv` module (usually comes with Python).

## 2. Setup Instructions

1.  **Navigate to the Project Directory:**
    If you haven't already, navigate to the root directory of the `Robot_New_Repository_Update_knowledge_base-5` project:
    ```bash
    cd /path/to/Robot_New_Repository_Update_knowledge_base-5
    ```

2.  **Create a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv .venv
    ```

3.  **Activate the Virtual Environment:**
    ```bash
    source .venv/bin/activate
    ```
    (On Windows, use `.venv\Scripts\activate`)

4.  **Install Required Python Packages:**
    Install all necessary libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables (e.g., API Keys):**
    The application may require API keys (e.g., for Groq LLM). Create a `.env` file in the project's root directory if it doesn't exist, and add your keys:
    ```
    # .env example
    GROQ_API_KEY="your_groq_api_key_here"
    ```
    (Ensure you replace `"your_groq_api_key_here"` with your actual key.)

6.  **Optional: Systemd Service Setup (for headless or persistent operation)**
    If you intend to run the robot as a background service on a Linux system, you can use the provided systemd service file.
    *   Copy the service file:
        ```bash
        sudo cp config/hospital-robot.service /etc/systemd/system/
        ```
    *   Reload systemd and enable the service:
        ```bash
        sudo systemctl daemon-reload
        sudo systemctl enable hospital-robot.service
        sudo systemctl start hospital-robot.service
        ```
    *   To check the status or logs:
        ```bash
        sudo systemctl status hospital-robot.service
        journalctl -u hospital-robot.service -f
        ```

## 3. Running the Application

After completing the setup, ensure your virtual environment is activated and simply run the main Python script:

```bash
source .venv/bin/activate
python main.py
```

The application will start, and you should see log output in your terminal. If you configured it as a systemd service, it will run in the background.

## 4. Troubleshooting

*   **Camera Initialization Failed**: Ensure `Picamera2` is correctly installed and your camera module is enabled and working on your Raspberry Pi.
*   **Audio Issues**: Check your microphone and speaker configurations. Ensure `pyaudio` has access to your audio devices. You might need to install `portaudio19-dev` for `pyaudio` on some Linux systems (`sudo apt-get install portaudio19-dev`).
*   **YOLO Model Not Found**: Verify that `data/yolov8n.pt` exists and the path is correct.
*   **API Key Errors**: Double-check your `.env` file for correct API key configurations.
*   **Python Version**: Ensure you are using Python 3.10 or higher.
